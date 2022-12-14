from datetime import datetime
from flask import request
from flask_jwt_extended import decode_token
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, desc
import json
import redis

#import requests

#from modelos import db, Policy, PolicySchema
#policy_schema = PolicySchema()

class VistaSecurityCheck(Resource):

    def __init__(self) -> None:
        # self.redis_cli = redis.Redis(host="localhost", password="redispw", port=6379, decode_responses=True, encoding="utf-8", )
        # self.admin_email = 'ag.castiblanco1207@uniandes.edu.co'
        self.admin_email = 'c.solanor@uniandes.edu.co'
        self.redis_cli = redis.Redis(host="localhost", port=6379, decode_responses=True, encoding="utf-8", )
        super().__init__()

    def post(self):
        authorized = self.is_authorized(request.headers)
        if authorized == True:    
            return {"status": "200", "mensaje": "security check ok"}
        else:
            return authorized


    def is_authorized(self, headers):
        role_check = self.check_role(headers)
        ip_check = self.check_ip(headers)
        city_check = self.check_city(headers)
        time_check = self.check_time(headers)

        if role_check == True and ip_check == True and city_check == True and time_check == True:
            return True

        checks = [role_check, ip_check, city_check, time_check]
        for ch in checks:
            if not ch == True:
                return ch

    def check_role(self, headers):
        role = decode_token(headers["Authorization"].split()[1])["role"]

        if not role == "CLIENT":
            self.send_sec_alert("sec", {"status": "403", "mensaje": "security check role does not have access to the resource: "+ role, "receptores": "{}".format(self.admin_email)})
            return {"status": "403", "mensaje": "security check role does not have access to the resource: "+ role}
        return True
        
    def check_ip(self, headers):
        ip = headers["Test-IP"]
        ips = ['10.20.0.1', '10.20.0.2', '10.20.0.3']

        if ip not in ips:
            self.send_sec_alert("sec", {"status": "400", "mensaje": "security check black list IP: "+ ip, "receptores": "{}".format(self.admin_email)})
            return {"status": "400", "mensaje": "security check black list IP: "+ ip}
        return True

    def check_city(self, headers):
        city = headers["Test-City"]
        cities = ['bogota', 'cali', 'killa']
        client_email = self.get_client_email(headers)

        if city not in cities:
            self.send_sec_alert("code-sec", {"status": "403", "mensaje": "security check wrong location: "+ city, "receptores": "{}, {}".format(self.admin_email, client_email)})
            return {"status": "403", "mensaje": "security check wrong location: "+ city}
        return True

    def check_time(self, headers):
        time = headers["Test-Time"]

        if time:
            dt = datetime.strptime(time, '%d.%m.%Y %H:%M:%S')
            if dt.hour >= 0 and dt.hour < 5:
                self.send_sec_alert("code-sec", {"status": "403", "mensaje": "security check suspicious time: "+ time, "receptores": "{}".format(self.admin_email)})
                return {"status": "403", "mensaje": "security check suspicious time: "+ time}
        return True

    def send_sec_alert(self, topico, mensaje):
        # respuesta = self.redis_cli.publish(topico, json.dumps(mensaje))
        self.redis_cli.publish(topico, json.dumps(mensaje))
        # print("Mensaje para cola")
        # print(json.dumps(mensaje))
        # print("respuesta redis:")
        # print(respuesta)

    def get_client_email(self, headers):
        return decode_token(headers["Authorization"].split()[1])["email"]