from routes.__init__ import Resource, g, request, db, login_required

class CrewMemberByID(Resource):
    def get(self, id):
        if g.crew:
            return g.crew.to_dict(rules=("production",)), 200
        return {"message": f"Could not find CrewMember with id #{id}"}, 404
    
    @login_required
    def patch(self, id):
        try:
            #! extract request's data
            data = request.get_json()
            #! use the data to patch the object
            for attr, value in data.items():
                setattr(g.crew, attr, value)  #! MODEL VALIDATIONS KICK IN HERE
            db.session.commit()
            #! return the serialized patched object
            return g.crew.to_dict(rules=("production",)), 202
        except Exception as e:
            return {"error": str(e)}, 422
    
    @login_required
    def delete(self, id):
        try:
            db.session.delete(g.crew)
            db.session.commit()
            return {}, 204
        except Exception as e:
            return {"error": str(e)}, 422
