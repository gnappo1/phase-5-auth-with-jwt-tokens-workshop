from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt
# from flask_session import Session
from flask_jwt_extended import JWTManager
from os import environ
from datetime import timedelta

app = Flask(__name__)
# flask-sqlalchemy connection to app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
# app.config["SESSION_TYPE"] = "sqlalchemy"
db = SQLAlchemy(app)
# app.config["SESSION_SQLALCHEMY"] = db
# flask_jwt_extended configuration
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False #! https vs http
app.config["JWT_CSRF_IN_COOKIES"] = True  #! double CSRF protection
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=24)

# app.secret_key = environ.get("SESSION_SECRET")
# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")
# flask-cors configuration
cors = CORS(app)
# flask-bcrypt configuration
flask_bcrypt = Bcrypt(app)
# flask-session configuration
# Session(app)
