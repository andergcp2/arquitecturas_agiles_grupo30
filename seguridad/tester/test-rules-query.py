import json
from unittest import TestCase
#from faker import Faker
#from faker.generator import random
from datetime import datetime
from app import app


class TestSecurityRulesQuery(TestCase):

    def setUp(self):
        #self.data_factory = Faker()
        self.client = app.test_client()
        self.headers_ope = {'user': 'chispas', 'password': 'chispasABC', 'IP': '10.20.0.3', 'City': 'cali', 'Time': '01.10.2022 23:45:30'}
        self.headers_cli = {'user': 'mango', 'password': 'mangoABC', 'IP': '10.20.0.3', 'City': 'cali', 'Time': '01.10.2022 23:45:30'}
        self.headers_adm  = {'user': 'admin', 'password': 'adminABC', 'IP': '10.20.0.3', 'City': 'cali', 'Time': '01.10.2022 23:45:30'}
        self.headers_ope_error_ip = {'user': 'chispas', 'password': 'chispasABC', 'IP': '10.20.0.8', 'City': 'cali', 'Time': '01.10.2022 23:45:30'}
        self.headers_cli_error_ip = {'user': 'mango', 'password': 'mangoABC', 'IP': '10.20.0.8', 'City': 'cali', 'Time': '01.10.2022 23:45:30'}
        self.headers_adm_error_ip  = {'user': 'admin', 'password': 'adminABC', 'IP': '10.20.0.8', 'City': 'cali', 'Time': '01.10.2022 23:45:30'}
        self.headers_ope_error_city = {'user': 'chispas', 'password': 'chispasABC', 'IP': '10.20.0.2', 'City': 'Armenia', 'Time': '01.10.2022 23:45:30'}
        self.headers_cli_error_city = {'user': 'mango', 'password': 'mangoABC', 'IP': '10.20.0.2', 'City': 'Barranquilla', 'Time': '01.10.2022 23:45:30'}
        self.headers_adm_error_city  = {'user': 'admin', 'password': 'adminABC', 'IP': '10.20.0.2', 'City': 'Cancun', 'Time': '01.10.2022 23:45:30'}
        self.headers_ope_error_time = {'user': 'chispas', 'password': 'chispasABC', 'IP': '10.20.0.2', 'City': 'Armenia', 'Time': '02.10.2022 01:25:30'}
        self.headers_cli_error_time = {'user': 'mango', 'password': 'mangoABC', 'IP': '10.20.0.2', 'City': 'Barranquilla', 'Time': '02.10.2022 01:25:30'}
        self.headers_adm_error_time  = {'user': 'admin', 'password': 'adminABC', 'IP': '10.20.0.2', 'City': 'Cancun', 'Time': '02.10.2022 01:25:30'}
        print("")
        
    def test_client_headers_ok_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_cli)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '200')

    def test_operator_headers_ok_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_ope)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_admin_headers_ok_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_adm)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')

    def test_client_headers_ip_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_cli_error_ip)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '400')
    
    def test_operator_headers_ip_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_ope_error_ip)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') #deberia ser 400
    
    def test_admin_headers_ip_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_adm_error_ip)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') #deberia ser 400

    def test_client_headers_city_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_cli_error_city)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_operator_headers_city_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_ope_error_city)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') 
    
    def test_admin_headers_city_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_adm_error_city)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') 
    
    def test_client_headers_time_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_cli_error_time)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_operator_headers_time_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_ope_error_time)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') 
    
    def test_admin_headers_time_error_security_ok(self):
        req = self.client.get("/test-rules-qry", json = self.headers_adm_error_time)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    

    def test_client_headers_ok_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_cli)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '200')
    
    def test_operator_headers_ok_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_ope)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_admin_headers_ok_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_adm)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_client_headers_ip_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_cli_error_ip)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '400')
    
    def test_operator_headers_ip_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_ope_error_ip)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') #deberia ser 400
    
    def test_admin_headers_ip_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_adm_error_ip)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') #deberia ser 400

    def test_client_headers_city_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_cli_error_city)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_operator_headers_city_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_ope_error_city)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') 
    
    def test_admin_headers_city_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_adm_error_city)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') 
    
    def test_client_headers_time_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_cli_error_time)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
    
    def test_operator_headers_time_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_ope_error_time)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403') 
    
    def test_admin_headers_time_error_security_ok_cmd(self):
        req = self.client.get("/test-rules-cmd", json = self.headers_adm_error_time)
        resp = json.loads(req.get_data())
        print(str(datetime.now()) +" resp: "+ str(resp))
        self.assertEqual(req.status_code, 200)
        self.assertEqual(resp['status'], '403')
""" """ 