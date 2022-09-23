from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
from modelos import db, User, UserSchema, Rule, RuleSchema

user_schema = UserSchema()
rule_schema = RuleSchema()

class VistaRule(Resource):
    def get(self, rule_id):
        return rule_schema.dump(Rule.query.get_or_404(rule_id))

class VistaRules(Resource):
    def get(self):
        return [rule_schema.dump(ca) for ca in Rule.query.all()]

class VistaKong(Resource):
    def get(self):
        user = User.query.filter(User.role == 'ADMIN').first()
        if user is None:
            return "user no existe", 404
        else:
            token = create_access_token(identity=user.id, additional_claims={"role": user.role, "user": user.user})
            return {"mensaje": "session init ok", "token": token}
