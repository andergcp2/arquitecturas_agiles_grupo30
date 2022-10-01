from email.policy import default
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

db = SQLAlchemy()

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.String(50))
    pwd = db.Column(db.String(50))
    type = db.Column(db.Enum("IP", "LOCATION", "SCHEDULE", name='policyType'))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        load_instance = True
