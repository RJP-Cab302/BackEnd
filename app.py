
import json
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'name': 'test message',
                       'message': 'The API is working'})

if __name__ == '__main__':
    app.run(port=8080)