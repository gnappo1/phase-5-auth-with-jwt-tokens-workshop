from routes.__init__ import Resource, request, db, make_response, login_required
from models.production import Production
# from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError

class Productions(Resource):

    def get(self):
        try:
            serialized_prods = [prod.to_dict() for prod in Production.query]
            return make_response(serialized_prods, 200)
            # return serialized_prods, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @login_required
    def post(self):
        try:
            data = (
                request.get_json()
            )  #! you might get a 405 if content type has not been set
            prod = Production(**data)  #! model validations kick in at this point
            db.session.add(prod)
            db.session.commit()  #! database constraints kick in
            return prod.to_dict(rules=("crew_members",)), 201
        except IntegrityError as e:
            db.session.rollback()
            return {"error": e.args[0]}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400
