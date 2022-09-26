from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route('/test1')
def test_dummyjson():
    resp = requests.get('https://dummyjson.com/todos')
    return resp.json()

@app.route('/test2')
def test_signin():
    admin = {'user': 'admin', 'password': 'adminABC', 'name':'Administrator', 'email':'admin@monitor-abc.co', 'role':'ADMIN'}
    client = {'user': 'mango', 'password': 'mangoABC', 'name':'Mr Mango', 'email':'mango@cats.co', 'role':'CLIENT'}
    operator = {'user': 'chispas', 'password': 'chispasABC', 'name':'Chispitas', 'email':'chispas@cats.co','role':'OPERATOR'}

    resp = requests.post('http://localhost:5000/signin', json=admin) 
    print("test-signin " + admin['user'] + str(resp.status_code))

    resp = requests.post('http://localhost:5000/signin', json=client) 
    print("test-signin " + client['user'] + str(resp.status_code))

    resp = requests.post('http://localhost:5000/signin', json=operator) 
    print("test-signin " + operator['user'] + str(resp.status_code))

    return resp.json()


@app.route('/test3')
def test_login():
    print("test-login")
    login = {'user': 'admin', 'password': 'adminABC'}
    login_resp = requests.post('http://localhost:3690/login', json=login) 
    
    print("test-rules")
    token = login_resp.json()['token'] 
    headers = {'Test-City': 'killa', 'Test-IP': '10.20.0.3', 'Content-Type': 'application/json', 'Authorization': "Bearer {}".format(token)}
    rules_qry_resp = requests.get('http://localhost:3692/rules', headers = headers) 
    #endpoint_carreras = "/usuario/{}/carreras".format(str(self.usuario_code))

    print("test-return "+ rules_qry_resp.json())
    return rules_qry_resp.json()


if __name__ == "__main__":
    app.run(debug=True)

