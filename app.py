
import json
from flask import Flask, request


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(port=8080)