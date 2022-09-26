from email.policy import default
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    running = db.Column(db.Boolean, default=False)
    type = db.Column(db.Enum("HOME", "OFFICE", name='typeRule'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.String(20))
    pwd = db.Column(db.String(20))
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.Enum("ADMIN", "OPERATOR", "CLIENT", name='RoleUser'))

class RuleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rule
        include_relationships = True
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
