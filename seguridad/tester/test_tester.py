import json
from unittest import TestCase
#from app import app
import requests
import responses

class TestTester(TestCase):

    usuarios = [{"user":"admin","password":"adminABC"},{"user":"admin1","password":"adminABC1"},{"user":"admin2","password":"adminABC"}]


    def validarMicros(self):       

        #print("Acceso Administrador con credenciales correctas y acceso a reglas")
        #req_new_user = self.client.post("/test6", headers={'Content-Type': 'application/json'})
        #resp_new_user = json.loads(req_new_user.get_data())
        #print(resp_new_user)
        ##login = {'user': 'admin', 'password': 'adminABC'}
        #login_resp = requests.post('http://localhost:3690/login', json=login) 
        #print(login_resp)
        response = requests.get('https://dummyjson.com/todos')
        self.assertEqual(200,response.status_code)