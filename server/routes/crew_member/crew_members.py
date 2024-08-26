from routes.__init__ import Resource, request, db
from models.crew_member import CrewMember

class CrewMembers(Resource):

    def get(self):
        try:
            serialized_crew = [crew.to_dict() for crew in CrewMember.query]
            return serialized_crew, 200
        except Exception as e:
            return str(e), 400

    def post(self):
        try:
            data = (
                request.get_json()
            )  #! you might get a 405 if content type has not been set
            crew = CrewMember(**data)  #! model validations kick in at this point
            db.session.add(crew)
            db.session.commit()  #! database constraints kick in
            return crew.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400
