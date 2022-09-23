import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app

class TestCreateUser(TestCase):

    def createUser(self, role):
        signed = False
        while(not(signed)):
            new_user = {
                "user": self.data_factory.word(),
                "password": self.data_factory.word(),
                "name": self.data_factory.name(),
                "email": self.data_factory.email(),
                "role": role
            }

            req_new_user = self.client.post("/signin", data=json.dumps(new_user), headers={'Content-Type': 'application/json'})
            resp_new_user = json.loads(req_new_user.get_data())
            if(type(resp_new_user)==dict):
                signed=True
            else:
                print("not signed: ", new_user["user"], resp_new_user)
            
            self.user = new_user
            self.resp_new_user = resp_new_user


    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        self.createUser('ADMIN')
        self.user1 = self.user
        self.resp_user1 = self.resp_new_user

        self.createUser('OPERATOR')
        self.user2 = self.user
        self.resp_user2 = self.resp_new_user

        self.createUser('CLIENT')
        self.user3 = self.user
        self.resp_user3 = self.resp_new_user


    def test_create_users(self):
        #print("..")
        self.assertEqual(self.resp_user1["mensaje"], "usuario creado exitosamente")
        self.assertEqual(self.resp_user2["mensaje"], "usuario creado exitosamente")
        self.assertEqual(self.resp_user3["mensaje"], "usuario creado exitosamente")


    def test_create_user_exist(self):
        user = {
            "user": self.user3["user"],
            "password": self.data_factory.word(),
            "name": self.data_factory.name(),
            "email": self.data_factory.email(),
            "role": self.user3["role"]
        }
        req_user = self.client.post("/signin", data=json.dumps(user), headers={'Content-Type': 'application/json'})
        resp_user = json.loads(req_user.get_data())
        self.assertEqual(req_user.status_code, 400)
        self.assertEqual(resp_user, "Ya existe un usuario registrado con ese identificador")


    def test_crete_email_exist(self):
        user = {
            "user": self.data_factory.word(),
            "password": self.data_factory.word(),
            "name": self.data_factory.name(),
            "email": self.user3["email"],
            "role": self.user3["role"]
        }
        req_user = self.client.post("/signin", data=json.dumps(user), headers={'Content-Type': 'application/json'})
        resp_user = json.loads(req_user.get_data())
        self.assertEqual(req_user.status_code, 400)
        self.assertEqual(resp_user, "Ya existe un usuario registrado con ese correo")
   

    def test_login(self):
        req_login = self.client.post("/login",
                    data=json.dumps({"user":self.user1["user"], "password":self.user1["password"]}),
                    headers={'Content-Type': 'application/json'})
        resp_login = json.loads(req_login.get_data())
        self.assertEqual(req_login.status_code, 200)
        self.assertEqual(resp_login["mensaje"], "Inicio de sesión exitoso")


    def test_login_user_doesnt_exist(self):
        req_login = self.client.post("/login",
                    data=json.dumps({"user":"user-no-existe", "password":self.user1["password"]}),
                    headers={'Content-Type': 'application/json'})
        resp_login = json.loads(req_login.get_data())
        self.assertEqual(req_login.status_code, 404)
        self.assertEqual(resp_login, "El usuario no existe")


    def test_login_wrong_password(self):
        req_login = self.client.post("/login",
                    data=json.dumps({"user":self.user2["user"], "password":self.user3["password"]}),
                    headers={'Content-Type': 'application/json'})
        resp_login = json.loads(req_login.get_data())
        self.assertEqual(req_login.status_code, 404)
        self.assertEqual(resp_login, "El usuario no existe")

"""
"""
