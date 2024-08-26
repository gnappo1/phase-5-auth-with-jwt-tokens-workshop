from routes.__init__ import Resource, request, g, db, make_response

class ProductionByID(Resource):
    def get(self, id):
        try:
            return g.production.to_dict(rules=("crew_members",)), 200
        except Exception as e:
            return {"error": str(e)}, 400

    def patch(self, id):
        try:
            #! extract request's data
            data = request.get_json()
            #! use the data to patch the object
            for attr, value in data.items():
                setattr(g.production, attr, value)  #! MODEL VALIDATIONS KICK IN HERE
            db.session.commit()
            #! return the serialized patched object
            return g.production.to_dict(rules=("crew_members",)), 202
        except Exception as e:
            return {"error": str(e)}, 422

    def delete(self, id):
        try:
            db.session.delete(g.production)
            db.session.commit()
            return {}, 204
        except Exception as e:
            return {"error": str(e)}, 422
