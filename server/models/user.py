from models.__init__ import SerializerMixin, validates, re, db
from sqlalchemy.ext.hybrid import hybrid_property
from app_config import flask_bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    _password_hash = db.Column("password", db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    created_productions = db.relationship(
        "Production",
        back_populates="creator",
        cascade="all, delete-orphan"
    )

    def __init__(self, username, email, password_hash=None, **kwargs):
        super().__init__(username=username, email=email, **kwargs)
        if password_hash:
            self.password_hash = password_hash

    serialize_rules = ("-_password_hash", "-created_productions.creator")

    @hybrid_property
    def password_hash(self):
        # return self._password_hash
        raise AttributeError("you cannot see passwords!")

    @password_hash.setter
    def password_hash(self, new_password):
        hashed_password = flask_bcrypt.generate_password_hash(new_password).decode("utf-8")
        self._password_hash = hashed_password

    def authenticate(self, password_to_check):
        return flask_bcrypt.check_password_hash(self._password_hash, password_to_check)
