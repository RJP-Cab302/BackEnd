import datetime
import json
import jwt
from functools import wraps
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from appauth import auth_required 
from constraints import SECRET_KEY
from database import add_user_to_database, check_user_password_in_database, delete_user_from_database 
from database import create_booking_data, get_booking_data_sold_spaces, update_user_address_to_database 
from database import add_vehicle_to_database, delete_vehicle_from_database, get_user_id_from_database 
from database import update_profile, get_name_from_database, get_vehicles_from_database_by_user_id 
from database import parking_booking, get_booking_number,  get_address_from_database
from yield_management import days_in_year

from yield_management import Fare_Calculator
from email_validator import validate_email, EmailNotValidError
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
    
    token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},SECRET_KEY,algorithm="HS256")
    name = get_name_from_database(auth.username)
    return json.dumps({'token': token, 'name': name})

@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json        

        if "username" not in json_message.keys() or "password" not in json_message.keys() or "name" not in json_message.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't formatted the request correctly", "code":401}),
                    status=401,
                    mimetype='application/json')
            return response
        

        if not check_email(json_message["username"]):
            response = app.response_class(json.dumps({"message":"Umm you haven't entered a valid email address", "code":422}),
                    status=422,
                    mimetype='application/json')
            return response   

        
        if(add_user_to_database(json_message["username"], json_message["password"], json_message["name"])):
                
            response = app.response_class(json.dumps({"message":"Sign up successful", "code":200}),
                                    status=200,
                                    mimetype='application/json')
     
        else:
            response = app.response_class(json.dumps({"message":"Sign up failed, user might already exist", "code":401}),
                                    status=401,
                                    mimetype='application/json')
        
        #TODO: The address works, better if it is here, better if it is its own API endpoint. But we can leave it here for now.
        if("useraddress" in json_message.keys() and json_message["useraddress"] != None): #not sure if that's will work, to be double checked
                update_user_address_to_database(json_message["username"], json_message["useraddress"])

        return response
    else:
        return json.dumps({'ERROR': 'Error',
                    'message': 'Content is not supported'})
    
@app.route('/update_profile', methods=['GET','POST'])
@cross_origin()
@auth_required
def Update_profile():

    if request.method == 'GET':
        json_message = request.json
        user_name1 = jwt.decode(json_message['token'], SECRET_KEY, algorithms="HS256")["user"]
        userName = get_name_from_database(user_name1)
        user_address= get_address_from_database(user_name1)
        return json.dumps({'name': userName,
                       'address': user_address})
     
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if(content_type == 'application/json'):
        json_message = request.json  

        if "name" not in json_message.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't entered your name", "code":401}),
                    status=401,
                    mimetype='application/json')
            return response

        if "useraddress" not in json_message.keys():
            response = app.response_class(json.dumps({"message":"Umm you haven't entered your address", "code":401}),
                    status=401,
                    mimetype='application/json')
            return response
        
        user_name = jwt.decode(json_message['token'], SECRET_KEY, algorithms="HS256")["user"]
        
        if(update_profile(user_name, json_message["name"], json_message["useraddress"],)):
            return  json.dumps({'name': 'test message',
                       'message': 'The user\'s profile has been updated'})
        else: 
            return  json.dumps({'name': 'test message',
                       'message': ' The user\'s profile has not been updated'})
    else:
        return json.dumps({'name': 'test message',
                      'message': 'The provided details are not valid'})



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
    
    if json_message["day"] > days_in_year(json_message["year"]):
        response = app.response_class(json.dumps({"message":f"You did it wrong, there are only {days_in_year(json_message['year'])} in {json_message['year']}", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response
    
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
    
    if json_message["day"] > days_in_year(json_message["year"]):
        response = app.response_class(json.dumps({"message":f"You did it wrong, there are only {days_in_year(json_message['year'])} in {json_message['year']}", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response

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

@app.route('/add_vehicle', methods=['POST'])
@cross_origin()
@auth_required
def add_vehicle_endpoint():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    else:
        response = app.response_class(json.dumps({"message":"You did it wrong, needs JSON", "code":401}),
                                    status=401,
                                    mimetype='application/json')
        return response

    if "vehicle_rego" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs vehicle_rego field", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response
    
    if "vehicle_type" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs vehicle_type field", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response
    
    if "vehicle_make" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs vehicle_make field", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response

    if "vehicle_model" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs vehicle_model field", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response
    

    try:
        user_name = jwt.decode(json_message['token'], SECRET_KEY, algorithms="HS256")["user"]
        user_id = get_user_id_from_database(user_name)
        if add_vehicle_to_database(json_message['vehicle_rego'], user_id, json_message['vehicle_type'], json_message['vehicle_make'], json_message['vehicle_model']):
            response = app.response_class(json.dumps({"message":"Vehicle added", "code":200}),
                                    status=200,
                                    mimetype='application/json')
        else:
            response = app.response_class(json.dumps({"message":"Vehicle not added, might already be in database", "code":401}),
                                    status=401,
                                    mimetype='application/json')
    except:
        print("big boo boo")
        response = app.response_class(json.dumps({"message":"Sorry something went wrong trying to add the vehicle to the database", "code":401}),
                    status=401,
                    mimetype='application/json')

    return response

@app.route('/delete_vehicle', methods=['DELETE'])
@cross_origin()
@auth_required
def delete_vehicle_endpoint():
    if request.method == 'DELETE':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    else:
        response = app.response_class(json.dumps({"message":"You did it wrong, needs JSON", "code":401}),
                                    status=401,
                                    mimetype='application/json')
        return response

    if "vehicle_rego" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs vehicle_rego field", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response

    try:
        user_name = jwt.decode(json_message['token'], SECRET_KEY, algorithms="HS256")["user"]
        user_id = get_user_id_from_database(user_name)
        if delete_vehicle_from_database(json_message['vehicle_rego'], user_id):
            response = app.response_class(json.dumps({"message":"Vehicle deleted", "code":200}),
                                    status=200,
                                    mimetype='application/json')
        else:
            response = app.response_class(json.dumps({"message":"Vehicle not deleted, might not be in database", "code":401}),
                                    status=401,
                                    mimetype='application/json')
    except:
        print("big boo boo")
        response = app.response_class(json.dumps({"message":"Sorry something went wrong trying to delete the vehicle from the database", "code":401}),
                    status=401,
                    mimetype='application/json')

    return response

@app.route('/user_get_vehicles', methods=['POST'])
@cross_origin()
@auth_required
def user_get_vehicle_endpoint():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    else:
        response = app.response_class(json.dumps({"message":"You did it wrong, needs JSON", "code":401}),
                                    status=401,
                                    mimetype='application/json')
        return response

    try:
        user_name = jwt.decode(json_message['token'], SECRET_KEY, algorithms="HS256")["user"]
        user_id = get_user_id_from_database(user_name)
        vehicles = get_vehicles_from_database_by_user_id(user_id)
        response = app.response_class(json.dumps({"message":"Vehicles retrieved", "vehicles":vehicles, "code":200}),
                                status=200,
                                mimetype='application/json')
    except:
        print("big boo boo")
        response = app.response_class(json.dumps({"message":"Sorry something went wrong trying to retrieve the vehicles from the database", "code":401}),
                    status=401,
                    mimetype='application/json')

    return response


@app.route('/booking', methods=['POST'])
@cross_origin()
@auth_required
def booking():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_message = request.json
    else:
        response = app.response_class(json.dumps({"message":"You did it wrong, needs JSON", "code":401}),
                                    status=401,
                                    mimetype='application/json')
        return response
    
    if "vehicle_rego" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs vehicle_rego field", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response
        
    if "year" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs year field", "code":401}),
                            status=401,
                            mimetype='application/json')

    if "day" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs day field", "code":401}),
                            status=401,
                            mimetype='application/json')

    if "base_fare" not in json_message.keys():
        response = app.response_class(json.dumps({"message":"You did it wrong, needs price ", "code":401}),
                            status=401,
                            mimetype='application/json')
    
    if json_message["day"] > days_in_year(json_message["year"]):
        response = app.response_class(json.dumps({"message":f"You did it wrong, there are only {days_in_year(json_message['year'])} in {json_message['year']}", "code":401}),
                            status=401,
                            mimetype='application/json')
        return response

    user_name = jwt.decode(json_message['token'], SECRET_KEY, algorithms="HS256")["user"]
    user_id = get_user_id_from_database(user_name)

    if(parking_booking(user_id, json_message['vehicle_rego'], json_message['year'], json_message['day'], json_message["base_fare"])):
        bookingNumber = get_booking_number(user_id, json_message['vehicle_rego'], json_message['year'], json_message['day'], json_message["base_fare"])
        response = app.response_class(json.dumps({"message":"Booking has been made", "booking_number":bookingNumber, "code":200}),
                                status=200,
                                mimetype='application/json')
        return response
    else:
        response = app.response_class(json.dumps({"message":"Booking already exits in the database", "code":401}),
                    status=401,
                    mimetype='application/json')
        return response

def check_email(email):
    try:    
        emailinfo = validate_email(email, check_deliverability=False)  
        return True
    except EmailNotValidError:
        return False


if __name__ == '__main__':
    
    app.run(port=8080)
    
    