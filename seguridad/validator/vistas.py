from datetime import datetime
from flask import request
from flask_jwt_extended import create_access_token
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
        self.redis_cli = redis.Redis(host="localhost", port=6379, decode_responses=True, encoding="utf-8", )
        super().__init__()

    def post(self):
        authorized = self.is_authorized(request.headers)
        if authorized == True:    
            return {"status": "200", "mensaje": "security check ok"}
        else:
            return authorized


    def is_authorized(self, headers):
        ip_check = self.check_ip(headers)
        city_check = self.check_city(headers)
        time_check = self.check_time(headers)

        if ip_check == True and city_check == True and time_check == True:
            return True

        if not ip_check == True:
            return ip_check
        if not city_check == True:
            return city_check
        if not time_check == True: 
            return time_check

    def check_ip(self, headers):
        ip = headers["Test-IP"]
        ips = ['10.20.0.1', '10.20.0.2', '10.20.0.3']
        if ip not in ips:
            self.send_sec_alert("sec", {"status": "400", "mensaje": "security check black list IP: "+ ip, "receptores": "['admin']"})
            return {"status": "400", "mensaje": "security check black list IP: "+ ip}
        return True

    def check_city(self, headers):
        city = headers["Test-City"]
        cities = ['bogota', 'cali', 'killa']
        if city not in cities:
            self.send_sec_alert("code-sec", {"status": "403", "mensaje": "security check wrong location: "+ city, "receptores": "['admin']"})
            return {"status": "403", "mensaje": "security check wrong location: "+ city}
        return True

    def check_time(self, headers):
        time = headers["Test-Time"]
        if time:
            dt = datetime.strptime(time, '%d.%m.%Y %H:%M:%S')
            if dt.hour >= 0 and dt.hour < 5:
                self.send_sec_alert("sec", {"status": "403", "mensaje": "security check suspicious time: "+ time, "receptores": "['admin']"})
                return {"status": "403", "mensaje": "security check suspicious time: "+ time}
        return True

    def send_sec_alert(self, topico, mensaje):
        respuesta = self.redis_cli.publish(topico, json.dumps(mensaje))
        # print("Mensaje para cola")
        # print(json.dumps(mensaje))
        # print("respuesta redis:")
        # print(respuesta)