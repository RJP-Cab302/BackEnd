import json
import jwt
from functools import wraps
from flask import request
from constraints import SECRET_KEY

def auth_required(f):
    '''Protects an API endpoint from general access. Requires the API endpoint to be a POST method
    with receives JSON with a field "token" containing a jwt token, which is obtained from the login endpoint.
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.json["token"]
        except:
            return json.dumps({'message': 'Token is missing, login in to get token'})
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return json.dumps({'message': 'Token has expired, please login again'})
        except:
            return json.dumps({'message': 'Token is invalid!'})
        
        return f(*args, **kwargs)
    
    return decorated