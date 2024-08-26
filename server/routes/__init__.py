from flask import request, g, make_response, session
from flask_restful import Resource
from app_config import db
from functools import wraps

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return {"error": "Access Denied, please log in!"}, 422
        return func(*args, **kwargs)

    return decorated_function