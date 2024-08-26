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

#! Internal imports
from app_config import app, api, db
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
        #! now that we have an id, store the id inside the session
        session["user_id"] = user.id
        #! return the user
        return user.to_dict(), 201
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
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid Credentials"}, 422
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/api/v1/signout", methods=["DELETE"])
def signout():
    try:
        if "user_id" in session:
            del session["user_id"]
        return {}, 204
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/v1/me", methods=["GET"])
def me():
    try:
        if "user_id" in session:
            user = db.session.get(User, session.get("user_id"))
            return user.to_dict(), 200
        else:
            return {"error": "Please Login or Signup"}, 400
    except Exception as e:
        return {"error": str(e)}, 400

api.add_resource(Productions, "/productions")
api.add_resource(ProductionByID, "/productions/<int:id>")
api.add_resource(CrewMembers, "/crew-members")
api.add_resource(CrewMemberByID, "/crew-members/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
