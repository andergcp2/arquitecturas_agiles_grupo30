from email.policy import default
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.String(50))
    pwd = db.Column(db.String(50))
    name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    role = db.Column(db.Enum("ADMIN", "OPERATOR", "CLIENT", name='RoleUser'))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
