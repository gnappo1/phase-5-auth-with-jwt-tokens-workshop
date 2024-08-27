#!/usr/bin/env python3

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py

#! External libraries imports
from flask import request, g, render_template, make_response, session
from time import time
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_refresh_cookies,
    get_jwt,
    get_jwt_identity,
    current_user,
    jwt_required,
    verify_jwt_in_request
)
from jwt.exceptions import ExpiredSignatureError

#! Internal imports
from app_config import app, api, db, jwt
from models.production import Production
from models.crew_member import CrewMember
from models.user import User
from routes.crew_member.crew_member_by_id import CrewMemberByID
from routes.crew_member.crew_members import CrewMembers
from routes.production.production_by_id import ProductionByID
from routes.production.productions import Productions

#! ==================
#! GENERAL ROUTE CONCERNS


@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404


@app.before_request
def before_request():
    #! First refactor when inserting crew routes BUT not very DRY right?
    # if request.endpoint == "productionbyid":
    #     id = request.view_args.get("id")
    #     prod = db.session.get(Production, id)
    #     g.prod = prod
    # elif request.endpoint == "crewmemberbyid":
    #     id = request.view_args.get("id")
    #     crew = db.session.get(CrewMember, id)
    #     g.crew = crew
    #! Better Approach
    path_dict = {"productionbyid": Production, "crewmemberbyid": CrewMember}
    if request.endpoint in path_dict:
        id = request.view_args.get("id")
        if record := db.session.get(path_dict.get(request.endpoint), id):
            key_name = "production" if request.endpoint == "productionbyid" else "crew"
            setattr(g, key_name, record)
        else:
            return {
                "error": f"Could not find a {path_dict.get(request.endpoint).__name__} with id #{id}"
            }, 404


#!======================
#! API ROUTES
# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.get(User, identity)


@app.route("/")
def homepage():
    productions = Production.query.order_by("title")
    crew_members = CrewMember.query.order_by("name")
    return render_template(
        "homepage.html", prods=productions, crew_members=crew_members
    )


@app.route("/api/v1/signup", methods=["POST"])
def signup():
    try:
        #! extract the data out of the request
        data = request.get_json()
        #! instantiate a new User object
        user = User(**data)
        #! add the object to the session
        db.session.add(user)
        #! commit the session
        db.session.commit()
        #! now that we have an id, create tokens for the information we want to store
        response = make_response(user.to_dict(), 201)
        access_token = create_access_token(
            identity=user.id, additional_claims={"role_id": 1}, fresh=True
        )
        refresh_token = create_refresh_token(
            identity=user.id
        )
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        # session["user_id"] = user.id
        #! return the response
        return response

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400


@app.route("/api/v1/signin", methods=["POST"])
def signin():
    try:
        #! extract the data out of the request
        data = request.get_json()
        #! check that the credentials are correct
        user = User.query.filter_by(email=data.get("email")).first()
        #! 2.0 Query Interface
        # user = db.session.scalars(
        #     db.select(User).where(User.email == "matteo@gmail.com")
        # ).first()
        if user and user.authenticate(data.get("password_hash")):
            #! log the user in
            response = make_response(user.to_dict(), 200)
            access_token = create_access_token(
                identity=user.id, additional_claims={"role_id": 1}, fresh=True
            )
            refresh_token = create_refresh_token(identity=user.id)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            # session["user_id"] = user.id
            #! return the response
            return response
        return {"error": "Invalid Credentials"}, 401
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/api/v1/signout", methods=["DELETE"])
@jwt_required(refresh=True)
def signout():
    try:
        response = make_response({}, 204)
        unset_access_cookies(response)
        unset_refresh_cookies(response)
        #! token invalidation/revocation strategy here
        return response
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/api/v1/me", methods=["GET"])
@jwt_required(refresh=True)
def me():
    try:
        verify_jwt_in_request()
        return make_response(current_user.to_dict(), 200)
    except ExpiredSignatureError as e:
        access_token = create_access_token(
            identity=current_user.id, additional_claims={"role_id": 1}, fresh=True
        )
        response = make_response(current_user.to_dict(), 200)
        set_access_cookies(response, access_token)
        return response
    except Exception as e:
        return {"error": str(e)}, 400


api.add_resource(Productions, "/productions")
api.add_resource(ProductionByID, "/productions/<int:id>")
api.add_resource(CrewMembers, "/crew-members")
api.add_resource(CrewMemberByID, "/crew-members/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
