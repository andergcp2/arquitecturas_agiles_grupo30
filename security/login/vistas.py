from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
#import requests

from modelos import db, User, UserSchema

user_schema = UserSchema()

class VistaSignIn(Resource):

    def post(self):
        validate = self.validateUser(request)
        if validate is not None:
            return "already user exists with this " + validate, 400

        # role = db.Column(db.Enum("ADMIN", "OPERATOR", "CLIENT", name='RoleUser'))
        new_user = User(usr=request.json["user"], 
                        pwd=request.json["password"], 
                        name=request.json["name"],
                        email=request.json["email"],
                        role=request.json["role"])
        db.session.add(new_user)
        db.session.query(User).filter(User.usr.like(request.json["user"])).first()
        db.session.commit()
        token = create_access_token(identity=new_user.id, additional_claims={"role": new_user.role, "user": new_user.usr, "username": new_user.name})
        return {"mensaje": "user created ok", "token": token, "id": new_user.id}

    def validateUser(self, request):
        user = db.session.query(User).filter(User.usr.like(request.json["user"])).first()
        if user is not None:
            return "id"
    
        email = db.session.query(User).filter(User.email.like(request.json["email"])).first()
        if email is not None:
            return "email"


class VistaLogIn(Resource):
    
    def post(self):
        user = User.query.filter(User.usr == request.json["user"], User.pwd == request.json["password"]).first()
        # db.session.commit()
        if user is None:
            return "user does not exist", 404
        else:
            token = create_access_token(identity=user.id, additional_claims={"role": user.role, "user": user.usr, "username": user.name})
            return {"mensaje": "login ok", "token": token}
