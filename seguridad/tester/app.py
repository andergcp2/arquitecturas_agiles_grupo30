from flask import request
from flask import Flask
from datetime import datetime, timedelta
import json
import requests

app = Flask(__name__)


@app.route('/test1')
def test_dummyjson():
    resp = requests.get('https://dummyjson.com/todos')
    return resp.json()

@app.route('/test2')
def test_signin():
    admin = {'user': 'admin', 'password': 'adminABC', 'name':'Administrator', 'email':'marlonagon@yahoo.com', 'role':'ADMIN'} 
    operator = {'user': 'chispas', 'password': 'chispasABC', 'name':'Chispitas', 'email':'cesar_2005@hotmail.com','role':'OPERATOR'}
    client = {'user': 'mango', 'password': 'mangoABC', 'name':'Mr Mango', 'email':'m.agonf@uniandes.edu.co', 'role':'CLIENT'}

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
    login = {'user': 'mango', 'password': 'mangoABC'}
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    print(login_resp)
    
    print(str(datetime.now()) +" test-rules")
    token = login_resp.json()['token'] 
    headers = {'Test-IP': '10.20.0.3', 'Test-City': 'cali', 'Test-Time': '02.10.2022 03:55:30', 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
    rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers) 

    print(str(datetime.now()) +" test-return "+ str(rules_qry_resp))
    return rules_qry_resp.json()


@app.route('/test4')
def test_ip():
    print(str(datetime.now()) +" test-login")
    login = {'user': 'chispas', 'password': 'chispasABC'}
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    
    print(str(datetime.now()) +" test-rules")
    token = login_resp.json()['token'] 
    headers = {'Test-IP': '10.20.0.9', 'Test-City': 'cali', 'Test-Time': '01.10.2022 23:55:30','Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
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

@app.route('/test-rules-qry')
def test():
    print(str(datetime.now()) +" test-login")
    login = {'user': "{}".format(request.json['user']), 'password': "{}".format(request.json['password']) }
    login_resp = requests.post('http://localhost:3690/login', json=login) 
   
    print(str(datetime.now()) +" test-rules")
    headers = {'Test-IP': "{}".format(request.json['IP']), 
            'Test-City': "{}".format(request.json['City']),
            'Test-Time': "{}".format(request.json['Time']),
            'Content-Type': 'application/json', 
            'Authorization': "Bearer {}".format(login_resp.json()['token'])}
    rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers) 

    print(str(datetime.now()) +" test-return")
    return rules_qry_resp.json()    

@app.route('/test-rules-cmd')
def testcmd():
    print(str(datetime.now()) +" test-login")
    login = {'user': "{}".format(request.json['user']), 'password': "{}".format(request.json['password']) }
    login_resp = requests.post('http://localhost:3690/login', json=login) 
   
    print(str(datetime.now()) +" test-rules-cmd")
    headers = {'Test-IP': "{}".format(request.json['IP']), 
            'Test-City': "{}".format(request.json['City']),
            'Test-Time': "{}".format(request.json['Time']),
            'Content-Type': 'application/json', 
            'Authorization': "Bearer {}".format(login_resp.json()['token'])}
    rules_cmd_resp = requests.get('http://localhost:3693/rules', headers = headers) 

    print(str(datetime.now()) +" test-return")
    return rules_cmd_resp.json()   
    


#if __name__ == "__main__":
#    app.run(debug=True)
