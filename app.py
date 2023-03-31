
import datetime
import json
import jwt
from functools import wraps
from flask import Flask, request, make_response
from appauth import auth_required 
from constraints import SECRET_KEY

app = Flask(__name__)


#To be replaced with a database, (<Login> : <Password>)
users = {"james@user.com" : "Password"}
#End To be replaced with a database


@app.route('/')
def index():
    return json.dumps({'name': 'test message',
                       'message': 'The API is working'})

@app.route('/example', methods=['GET','POST'])
def example_end_point():
    '''Example api end point, for both GET and POST methods.
    Incoming JSON via the POST method is in the form of a dictionary.
    '''
    
    if request.method == 'GET':
        print("GET")
        return json.dumps({'name': 'test message',
                       'message': 'The API is working, this is sample JSON'})

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json_message = request.json
            for m in json_message:
                print(m)
            return json_message
        else:
            return json.dumps({'ERROR': 'Error',
                        'message': 'Content is not supported'})

@app.route('/protected', methods=['POST'])
@auth_required
def protected():
    return json.dumps({'message':'This place is only for those with a auth token',
                       'Success':'You have successfully used an auth token'})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth:
        return json.dumps({"message" : "Basic authorization required, need username and password"})
    
    if auth.username not in users.keys():
        return json.dumps({"message" : "Username or password invalid"})

    if users[auth.username] != auth.password:
        return json.dumps({"message" : "Username or password invalid"})
    
    token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},SECRET_KEY,algorithm="HS256")
    return json.dumps({'token': token})


if __name__ == '__main__':
    app.run(port=8080)