import datetime
import json
import jwt
from functools import wraps
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from appauth import auth_required 
from constraints import SECRET_KEY
from database import add_user_to_database, check_user_password_in_database, delete_user_from_database, create_booking_data, get_booking_data_sold_spaces
from yield_management import Fare_Calculator

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return json.dumps({'name': 'test message',
                       'message': 'The API is working'})

@app.route('/example', methods=['GET','POST'])
@cross_origin()
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
@cross_origin()
@auth_required
def protected():
    return json.dumps({'message':'This place is only for those with a auth token',
                       'Success':'You have successfully used an auth token'})


@app.route('/login')
@cross_origin()
def login():
    auth = request.authorization
    if not auth:
        return json.dumps({"message" : "Basic authorization required, need username and password"})

    if not check_user_password_in_database(auth.username, auth.password):
        return json.dumps({"message" : "Username or password invalid"})
    
    token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},SECRET_KEY,algorithm="HS256")
    return json.dumps({'token': token})

@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    #TODO: Sign up should only take an email as a username
    users_emails = ['gmail.com', 'yahoo.com','icloud.com', 'outlook.com']
    types = ['tourist', 'local_council','business', 'residen']
    username_email = request.form['username'].split('@')[-1]

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
        if username_email not in users_emails.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't entered a valid email address", "code":401}),
                    status=401,
                    mimetype='application/json')
            return response

        if "username" not in json_message.keys() or "password" not in json_message.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't formatted the request correctly", "code":401}),
                    status=401,
                    mimetype='application/json')
            return response
        
        if "userType" not in types.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't selected a user type", "code":400}),
                    status=400,
                    mimetype='application/json')
            return response

        if "userAddress" not in json_message.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't entered a home address", "code":400}),
                    status=400,
                    mimetype='application/json')
            return response

        if(add_user_to_database(json_message["username"], json_message["password"], json_message["userType"]), json_message["userAddress"]):
            response = app.response_class(json.dumps({"message":"Sign up successful", "code":200}),
                                    status=200,
                                    mimetype='application/json')
        else:
            response = app.response_class(json.dumps({"message":"Sign up failed, user might already exist", "code":401}),
                                    status=401,
                                    mimetype='application/json')

        return response
    else:
        return json.dumps({'ERROR': 'Error',
                    'message': 'Content is not supported'})

@app.route('/delete', methods=['DELETE'])
@cross_origin()
@auth_required
def delete():
    """To delete a user account
    """
    if request.method == 'DELETE':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    
    auth = request.authorization
    if not auth:
        return json.dumps({"message" : "Basic authorization required, need username and password"})

    if not check_user_password_in_database(auth.username, auth.password):
        return json.dumps({"message" : "Username or password invalid"})
    
    if delete_user_from_database(auth.username):
        response = app.response_class(json.dumps({"message":"Delete successful", "code":200}),
                                    status=200,
                                    mimetype='application/json')
    
    return response

#Create booking data.
@app.route('/create_booking_data', methods=['POST'])
#TODO: enable after testing complete @auth_required 
@cross_origin()
def create_booking_data_endpoint():

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    else:
        response = app.response_class(json.dumps({"message":"You did it wrong, needs JSON", "code":401}),
                                    status=401,
                                    mimetype='application/json')

    if "year" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs year field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "day" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs day field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "base_fare" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs base_fare field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "total_spaces" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs total_spaces field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "days_for_sale" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs days_for_sale field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "min_price" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs min_price field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "max_price" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs max_price field", "code":401}),
                            status=401,
                            mimetype='application/json')
    
    if create_booking_data(json_message['year'],json_message['day'],json_message['base_fare'],json_message['total_spaces'],json_message['days_for_sale'],json_message['max_price'],json_message['min_price']):
        response = app.response_class(json.dumps({"message":"Database has been updated", "code":200}),
                                    status=200,
                                    mimetype='application/json')
    else:
        response = app.response_class(json.dumps({"message":"Database did not update", "code":401}),
                            status=401,
                            mimetype='application/json')

    return response

@app.route('/get_day_price', methods=['POST'])
@cross_origin()
def get_day_price_endpoint():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    else:
        response = app.response_class(json.dumps({"message":"You did it wrong, needs JSON", "code":401}),
                                    status=401,
                                    mimetype='application/json')
    
    if "year" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs year field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "day" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs day field", "code":401}),
                            status=401,
                            mimetype='application/json')
    if "current_day" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs current_day field", "code":401}),
                            status=401,
                            mimetype='application/json')

    try:
        datalist = year, day, base_fare, total_spaces, spaces_sold, days_for_sale, max_price, min_price = get_booking_data_sold_spaces(json_message["year"],json_message["day"])
        first_day_on_sale = day - days_for_sale
        print("first_day_on_sale: ", first_day_on_sale)

        #TODO: Account for day running into the next year
        current_day = int(datetime.datetime.now().strftime("%j"))
        current_year = int(datetime.datetime.now().strftime("%Y"))

        print("Current day: ", current_day)
        print("Current year: ", current_year)
        print("Requested day: ", day)
        
        day_of_sale = day - current_day
        print("day_of_sale: ", day_of_sale)

        if(current_day > day):
            response = app.response_class(json.dumps({"message":"Request Unuccessful, day requested is in the past","code":401}),
                status=401,
                mimetype='application/json')
        else:
            cal = Fare_Calculator(base_fare,total_spaces,spaces_sold,day_of_sale,days_for_sale, max_price, min_price)
            fare = cal.calculate_fare()
            print(f"new price ${fare}")
            response = app.response_class(json.dumps({"message":"Request Successful", "Price":fare,"code":200}),
                                status=200,
                                mimetype='application/json')
    except:
        print("big boo boo")
        response = app.response_class(json.dumps({"message":"Sorry something went wrong, most likely no data for that day", "code":401}),
                    status=401,
                    mimetype='application/json')
    
    return response

if __name__ == '__main__':
    app.run(port=8080)