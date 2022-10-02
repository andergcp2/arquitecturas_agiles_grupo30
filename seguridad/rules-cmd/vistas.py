from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
from modelos import db, User, UserSchema, Rule, RuleSchema
import requests

user_schema = UserSchema()
rule_schema = RuleSchema()

class VistaRule(Resource):
    def get(self, rule_id):
        return rule_schema.dump(Rule.query.get_or_404(rule_id))

class VistaRules(Resource):

    @jwt_required()
    def get(self):
        # user_id = get_jwt_identity()
        # print("rules-qry headers: ", request.headers)
        security_resp = requests.post('http://localhost:3691/check', headers = request.headers)
        print("rules-qry security resp: ", security_resp)

        return security_resp.json()
        # return [rule_schema.dump(ca) for ca in Rule.query.all()]
