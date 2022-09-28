from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity
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

# @jwt_required()
class VistaRules(Resource):
    def get(self):
        # user_id = get_jwt_identity()
        
        #print("rules-qry headers: ", request.headers)
        #headers = {'Test-City': 'killa', 'Test-IP': '10.20.0.3', 
        rules_qry_resp = requests.post('http://localhost:3691/check', headers = request.headers) 
        print("rules-qry resp: ", rules_qry_resp)        
        #if rules_qry_resp == 200:
        
        return rules_qry_resp.json()
        # return [rule_schema.dump(ca) for ca in Rule.query.all()]
