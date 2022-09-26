from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
#import requests

#from modelos import db, Policy, PolicySchema
#policy_schema = PolicySchema()

class VistaSecurityCheck(Resource):

    def post(self):
        ip = request.headers["Test-IP"]
        ips = ['10.20.0.1', '10.20.0.2', '10.20.0.3']
        if ip not in ips:
            return {"status": "403", "mensaje": "security check black list IP: "+ ip}

        city = request.headers["Test-City"]
        cities = ['bogota', 'cali', 'killa']
        if city not in cities:
            return {"status": "404", "mensaje": "security check wrong location: "+ city}

        return {"status": "200", "mensaje": "security check ok"}
