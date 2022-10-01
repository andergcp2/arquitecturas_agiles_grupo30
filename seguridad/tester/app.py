from urllib import request
from flask import Flask
from datetime import datetime, timedelta
import requests
import json
import random


app = Flask(__name__)
usuarios = [{"user":"admin","password":"adminABC"},{"user":"admin1","password":"adminABC1"},{"user":"admin2","password":"adminABC"},{"user":"mango","password":"mangoABC"}] 
ips = ['10.20.0.3','10.20.0.1','10.20.0.2','10.20.0.4','10.20.0.5'] 
ciudades = ['bogota','cali','killa','cartagena','bucaramanga'] 

@app.route('/test1')
def test_dummyjson():
    resp = requests.get('https://dummyjson.com/todos')
    return resp.json()

@app.route('/test2')
def test_signin():
    admin = {'user': 'admin', 'password': 'adminABC', 'name':'Administrator', 'email':'admin@monitor-abc.co', 'role':'ADMIN'} 
    client = {'user': 'mango', 'password': 'mangoABC', 'name':'Mr Mango', 'email':'mango@cats.co', 'role':'CLIENT'}
    operator = {'user': 'chispas', 'password': 'chispasABC', 'name':'Chispitas', 'email':'chispas@cats.co','role':'OPERATOR'}

    resp = requests.post('http://localhost:3690/signin', json=admin) 
    print("test-signin " + admin['user'] + str(resp.status_code))

    resp = requests.post('http://localhost:3690/signin', json=client) 
    print("test-signin " + client['user'] + str(resp.status_code))

    resp = requests.post('http://localhost:3690/signin', json=operator) 
    print("test-signin " + operator['user'] + str(resp.status_code))

    return resp.json()


@app.route('/test3')
def test_ok():
    print(str(datetime.now()) +" test-login")
    login = {'user': 'admin', 'password': 'adminABC'}
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    
    print(str(datetime.now()) +" test-rules")
    token = login_resp.json()['token'] 
    headers = {'Test-IP': '10.20.0.3', 'Test-City': 'cali', 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
    rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers) 

    print(str(datetime.now()) +" test-return")
    return rules_qry_resp.json()


@app.route('/test4')
def test_ip():
    print(str(datetime.now()) +" test-login")
    login = {'user': 'admin', 'password': 'adminABC'}
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    
    print(str(datetime.now()) +" test-rules")
    token = login_resp.json()['token'] 
    headers = {'Test-IP': '10.20.0.9', 'Test-City': 'chia', 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
    rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers) 

    print(str(datetime.now()) +" test-return")
    return rules_qry_resp.json()

@app.route('/test5')
def test_city():
    print(str(datetime.now()) +" test-login")
    login = {'user': 'admin', 'password': 'adminABC'}
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    
    print(str(datetime.now()) +" test-rules")
    token = login_resp.json()['token'] 
    headers = {'Test-IP': '10.20.0.3', 'Test-City': 'chia', 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
    rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers) 

    print(str(datetime.now()) +" test-return")
    return rules_qry_resp.json()

@app.route('/test6')
def test_validar_acceso():
    print(str(datetime.now()) +" test-login")
    login = {'user': 'admin', 'password': 'adminABC'} 
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    print(login_resp.status_code)
    if login_resp.status_code == 200:
        print(str(datetime.now()) +" test-rules")
        token = login_resp.json()['token'] 
        headers = {'Test-IP': ips[0], 'Test-City': 'cali', 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
        rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers)
        print(str(datetime.now()) +" test-return")
        print(rules_qry_resp.json())
        return rules_qry_resp.json()



@app.route('/test7')
def test_validar_acceso_operador():
    print(str(datetime.now()) +" test-login")
    login = {'user': 'chispas', 'password': 'chispasABC'} 
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    if login_resp.status_code == 200:
        print(str(datetime.now()) +" test-rules")
        token = login_resp.json()['token'] 
        headers = {'Test-IP': ips[1], 'Test-City': ciudades[4], 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
        rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers)
        print(str(datetime.now()) +" test-return")
        print(rules_qry_resp.json())
        if rules_qry_resp.status_code=='403':
            print("Enviar mensaje de notificacion")
        elif rules_qry_resp.status_code==400:
            print("Correo")
    
        return rules_qry_resp.json()


    
    


#if __name__ == "__main__":
 #   app.run(debug=True)
