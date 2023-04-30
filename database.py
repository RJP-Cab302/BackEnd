from sqlite3 import *
from os import path
import bcrypt
import constraints

db_file = constraints.DB_FILE

def create_database(db_name):
    """Creates a database with the following tables:
    Users: UserId, UserName, UserPassword, Name, UserType
    BookingData: Year, Day, BaseFare, TotalSpaces, SpacesSold, DaysForSale
    @param db_name(string): name of the database to be created
    """
    """
    used to test booking table database
    sql_instruction1 = f"INSERT INTO BookingTable(UserId, vehicleRego, Year, Day, Price) VALUES ('1', 'reer', '2023', '23', "40.29");"
    db.execute(sql_instruction1)
    connection.commit()
    db.close()
    """
    connection = connect(database=db_name)
    db = connection.cursor()

    db.execute("CREATE TABLE Users(UserId INTEGER UNIQUE primary key AUTOINCREMENT, UserName TEXT UNIQUE, UserPassword TEXT(200), Name TEXT, UserType INTEGER, UserAddress TEXT UNIQUE);")
    db.execute("CREATE TABLE BookingData(Year INTEGER, Day INTEGER, BaseFare FLOAT, TotalSpaces INTEGER, SpacesSold INTEGER, MaxPrice FLOAT, MinPrice FLOAT, DaysForSale INTEGER, CONSTRAINT  PKYearDay Primary Key (Year, Day));")
    db.execute("CREATE TABLE BookingTable(BookingId INTEGER UNIQUE primary key AUTOINCREMENT,UserId INTEGER UNIQUE, vehicleRego TEXT, Year INTEGER, Day INTEGER, Price FLOAT)")
    db.execute("CREATE TABLE VehicleTable(vehicleRego TEXT UNIQUE primary key, vehicleType TEXT, vehicleMake TEXT, vehicleModel TEXT, UserId INTEGER, FOREIGN KEY(UserId) REFERENCES Users(UserId));")

    connection.commit()

    db.close()
    connection.close()

def add_vehicle_to_database(vehicle_rego, user_id, vehicle_type, vehicle_make, vehicle_model):
    """Adds a vehicle to the Vehicle table in the database. Will add only the vehicle_rego, vehicle_type, vehicle_make, vehicle_model, user_id.
    @param vehicle_rego(string): The registration of the vehicle.
    @param vehicle_type(string): The type of the vehicle.
    @param vehicle_make(string): The make of the vehicle.
    @param vehicle_model(string): The model of the vehicle.
    @param user_id(int): The user id of the user who owns the vehicle.
    """
    global db_file

    if not path.exists(db_file):
        create_database(db_file)

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"INSERT INTO VehicleTable(vehicleRego, vehicleType, vehicleMake, vehicleModel, UserId) VALUES ('{vehicle_rego}', '{vehicle_type}', '{vehicle_make}', '{vehicle_model}', '{user_id}');"

    try:
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    except IntegrityError:
        print("Vehicle already in database")
        db.close()
        connection.close()
        return False
    except:
        print("Something else went wrong")
        db.close()
        connection.close()
        return False

def get_vehicles_from_database_by_user_id(user_id):
    """Gets all the vehicles from the Vehicle table in the database. Will get only the vehicle_rego, vehicle_type, vehicle_make, vehicle_model, user_id.
    @param user_id(int): The user id of the user who owns the vehicle.
    @return: list of tuples containing the vehicle_rego, vehicle_type, vehicle_make, vehicle_model, user_id.
    """
    global db_file

    if not path.exists(db_file):
        create_database(db_file)

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"SELECT vehicleRego, vehicleType, vehicleMake, vehicleModel FROM VehicleTable WHERE UserId = '{user_id}';"

    try:
        db.execute(sql_instruction)
        result = db.fetchall()
        db.close()
        connection.close()
        return result
    except:
        print("Something went wrong")
        db.close()
        connection.close()
        return False

def get_vehicle_from_database_by_rego(vehicle_rego):
    """Gets a vehicle from the Vehicle table in the database. Will get only the vehicle_rego, vehicle_type, vehicle_make, vehicle_model, user_id.
    @param vehicle_rego(string): The registration of the vehicle.
    @return: tuple containing the vehicle_rego, vehicle_type, vehicle_make, vehicle_model, user_id.
    """
    global db_file

    if not path.exists(db_file):
        create_database(db_file)

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"SELECT vehicleRego, vehicleType, vehicleMake, vehicleModel, UserId FROM VehicleTable WHERE vehicleRego = '{vehicle_rego}';"

    try:
        db.execute(sql_instruction)
        result = db.fetchone()
        db.close()
        connection.close()
        return result
    except:
        print("Something went wrong")
        db.close()
        connection.close()
        return False

def delete_vehicle_from_database(vehicle_rego, user_id):
    """Deletes a vehicle from the Vehicle table in the database. Will delete only the vehicle_rego, vehicle_type, vehicle_make, vehicle_model, user_id.
    @param vehicle_rego(string): The registration of the vehicle.
    @return: True if successful, False if not.
    """
    global db_file

    if not path.exists(db_file):
        create_database(db_file)

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"DELETE FROM VehicleTable WHERE vehicleRego = '{vehicle_rego}' AND UserId = '{user_id}';"

    try:
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    except:
        print("Something went wrong")
        db.close()
        connection.close()
        return False

def get_user_id_from_database(user_name):
    """Gets the user id from the User table in the database. Will get only the user_id.
    @param user_name(string): The user name of the user, should be an email address.
    @return: int containing the user_id.
    """
    global db_file

    if not path.exists(db_file):
        create_database(db_file)

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"SELECT UserId FROM Users WHERE UserName = '{user_name}';"

    try:
        db.execute(sql_instruction)
        result = db.fetchone()
        db.close()
        connection.close()
        return result[0]
    except:
        print("Something went wrong")
        db.close()
        connection.close()
        return False

def get_name_from_database(user_name):
    """Gets the name from the User table in the database. Will get only the name.
    @param user_name(string): The user name of the user, should be an email address.
    @return: string containing the name.
    """
    global db_file

    if not path.exists(db_file):
        print("No database found")
        return False

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"SELECT Name FROM Users WHERE UserName = '{user_name}';"

    try:
        db.execute(sql_instruction)
        result = db.fetchone()
        db.close()
        connection.close()
        return result[0]
    except:
        print("Something went wrong")
        db.close()
        connection.close()
        return False

def get_address_from_database(user_name):
    """Gets the name from the User table in the database. Will get only the name.
    @param user_name(string): The user name of the user, should be an email address.
    @return: string containing the name.
    """
    global db_file

    if not path.exists(db_file):
        print("No database found")
        return False

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"SELECT UserAddress FROM Users WHERE UserName = '{user_name}';"

    try:
        db.execute(sql_instruction)
        result = db.fetchone()
        db.close()
        connection.close()
        return result[0]
    except:
        print("Something went wrong")
        db.close()
        connection.close()
        return False

def add_user_to_database(user_name, user_password, name):
    """Adds a user to the User table in the database. Will add only the user_name and user_password.
    @param user_name(string): The user name of the user, should be an email address.
    @param user_password(string): The password of the user. (The password will be hashed.)
    """

    user_password_hashed = str(hash_password(user_password))
    global db_file
    
    if not path.exists(db_file):
        create_database(db_file)
    
    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"INSERT INTO Users(UserName, UserPassword, Name) VALUES ('{user_name}', '{user_password_hashed}','{name}');"
    
    try:
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    except IntegrityError:
        print("Username already in database")
        db.close()
        connection.close()
        return False
    except:
        print("Something else went wrong")
        db.close()
        connection.close()
        return False
    
def update_user_address_to_database(user_name, user_address):
    global db_file

    if not path.exists(db_file):
        create_database(db_file)

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"UPDATE Users SET UserAddress = '{user_address}' WHERE UserName = '{user_name}';"

    try:
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    except IntegrityError:
        #TODO: is this error correct? Do we need to just update the address?
        print("User's address already in database")
        db.close()
        connection.close()
        return False
    except:
        print("Something else went wrong")
        db.close()
        connection.close()
        return False

def hash_password(password):
    """Hashes and salts a password using bcrypt.
    @param password: string
    @return: the hashed and salted password
    """
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()
    
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    
    return hash.decode()

def check_hash(entered_password, hashed_password):
    """Checks a plain text password against a hashed and salted password.
    @param entered_password: string of the plain text password.
    @param hashed_password: string of the hashed password
    @returns: bool, true if entered_password is the same as the hashed_password. false if they don't match.
    """
    userBytes = entered_password.encode()
    result = bcrypt.checkpw(userBytes, hashed_password.encode())
    return result

def check_user_password_in_database(entered_user_name, entered_user_password):
    """Checks if the entered_user_password is the same as the password stored in the database
    for the entered_user_name.
    @param entered_user_name: string of the username to be checked
    @param entered_user_password: plain text string of the password to be checked
    @return: bool, true if the entered_user_password matches the password saved in the database.
    """
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False
    
    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"SELECT UserPassword FROM Users WHERE UserName == '{entered_user_name}'"

    db.execute(sql_instruction)

    rows = db.fetchall()

    db.close()
    connection.close()

    for row in rows:
        if check_hash(entered_user_password,row[0]):
            return True
    
    print("Password does not match")
    return False


def update_profile(username, name, userAddress):
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"UPDATE Users SET Name = '{name}', UserAddress ='{userAddress}' WHERE UserName == '{username}'"
    try:
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close() 
        return True
    except:
        return False


def password_reset(userName,new_password, old_password):
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False

    user_password_hashed = str(hash_password(new_password))

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction = f"UPDATE Users SET UserPassword = '{user_password_hashed}' WHERE UserName = '{userName}';"
    if(check_user_password_in_database(userName, old_password)):
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    else:
        print("Old password does not match, please try again")
        return False
        

def delete_user_from_database(user_name):
    """Deletes a user fron the database.
    @param user_name: string of the user to be deleted.
    @return: true if the operation was successful
    """
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False
    
    sql_instruction = f"DELETE from Users WHERE UserName = ('{user_name}');"
    
    connection = connect(database=db_file)
    db = connection.cursor()

    db.execute(sql_instruction)
    connection.commit()
    db.close()
    connection.close()
    return True

def create_booking_data(year, day, base_fare, total_spaces, days_for_sale, max_price, min_price):
    """create_booking_data _summary_ 
    Creates an entry in the BookingData table of the database for a particular year and day.
    To be used if the year and day does not already exist in the table.

    Args:
        year (int): _description_ year of the booking data
        day (int): _description_ day of the booking data
        base_fare (number): _description_ the base fare used for calculating all the fare of the day
        total_spaces (int): _description_ the total number of spaces that can be sold to tourist for the day
        days_for_sale (int): _description_ the total number of days prior to the actual day, that the spaces will be on sale.
        max_price (float): _description_ the maximum price that a fare can be sold on that day
        min_price (float): _description_ the minimum price that a fare can be sold on that day
    """
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        create_database(db_file)
    
    sql_instruction = f"SELECT Year, Day FROM BookingData WHERE Year == ({year}) and Day == ({day})"

    connection = connect(database=db_file, timeout=5)
    db = connection.cursor()

    db.execute(sql_instruction)

    rows = db.fetchall()

    db.close()
    connection.close()
    
    if len(rows) == 0:
        print("adding")
        connection = connect(database=db_file, timeout=5)
        db = connection.cursor()
        sql_instruction = f"INSERT INTO BookingData(Year, Day, BaseFare, TotalSpaces, DaysForSale, MaxPrice, MinPrice) VALUES ({year}, {day},{base_fare}, {total_spaces},{days_for_sale}, {max_price}, {min_price});"

        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    return False

def change_booking_data_sold_spaces(year, day, space_sold):
    """change_booking_data_sold_spaces _summary_
    Changes the sold spaces in the booking data for the given year and day.

    Args:
        year (int): _description_ year of the booking data
        day (int): _description_ day of the booking data
        space_sold (int): _description_ current spaces sold for the year and day

    Returns:
        bool: _description_ True is update was successful
    """    
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False
    
    sql_instruction = f"SELECT Year, Day, TotalSpaces FROM BookingData WHERE Year == ({year}) and Day == ({day})"

    connection = connect(database=db_file, timeout=5)
    db = connection.cursor()

    db.execute(sql_instruction)

    rows = db.fetchall()

    db.close()
    connection.close()

    print(rows[0][2])

    if len(rows) == 1:
        if rows[0][2] < space_sold:
            print("Too many spaces sold")
            return False

        print("updating")
        connection = connect(database=db_file, timeout=5)
        db = connection.cursor()
        sql_instruction = f"UPDATE BookingData SET SpacesSold = {space_sold} WHERE Year == ({year}) and  Day == ({day})"
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True

    print("Booking data does not have a matching day to update")
    return False

def get_booking_data_sold_spaces(year, day):
    """get_booking_data_sold_spaces _summary_ gets all the booking data for a selected year day

    Args:
        year (int): _description_ year selected
        day (int): _description_ day selected

    Returns:
        list: _description_ [Year, Day, BaseFare, TotalSpaces, SpacesSold, DaysForSale, MaxPrice, MinPrice]
    """    
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False
    
    sql_instruction = f"SELECT Year, Day, BaseFare, TotalSpaces, SpacesSold, DaysForSale, MaxPrice, MinPrice FROM BookingData WHERE Year == ({year}) and Day == ({day})"

    connection = connect(database=db_file, timeout=5)
    db = connection.cursor()

    db.execute(sql_instruction)

    rows = db.fetchall()

    db.close()
    connection.close()

    return rows[0]

def adjust_base_fare(year, day, new_base_fare):
    """Adjust the base fare price of a chosen date.
    @param year: number of the year of the chosen date.
    @param day: number of the chosen date.
    @param new_base_fare: number of the new price of the chosen date.
    @return: true if the operation was successful
    """
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False

    connection = connect(database=db_file)
    db = connection.cursor()

    sql_instruction1 = f"SELECT MinPrice, MaxPrice, BaseFare FROM BookingData WHERE Year = '{year}' and Day = '{day}';"
    db.execute(sql_instruction1)
    rows = db.fetchall()

    sql_instruction = f"UPDATE BookingData SET BaseFare = '{new_base_fare}' WHERE Year = '{year}' and Day = '{day}';"

    if rows:
        if(new_base_fare == rows[0][2]):
            db.close()
            connection.close()
            print("You have entered the current price")
            return False
        elif(rows[0][0] <= new_base_fare and new_base_fare <= rows[0][1]):
            db.execute(sql_instruction)
            connection.commit()
            db.close()
            connection.close()
            print("Price have been changed")
            return True
        elif(rows[0][0] > new_base_fare or new_base_fare > rows[0][1]):
            db.close()
            connection.close()
            print(f"The chosen price should be between {rows[0][0]} and {rows[0][1]}")
            return False         
    else:
        print("The chosen date is not valid")
        db.close()
        connection.close()
        return False
    
        
if __name__ == "__main__":
    #print(add_user_to_database("bob@user.com","password", "Bob"))
    #print(get_user_id_from_database("tom@user.com"))
    print(add_vehicle_to_database("CBA-123",1))
    #print(get_vehicle_from_database_by_rego("ABC-123"))
    print(get_vehicles_from_database_by_user_id(1))
    #print(delete_vehicle_from_database("CBA-321",1))
    #print(check_user_password_in_database("jim@user.com","password"))
    #print(delete_user_from_database("tim@user.com"))
    #create_booking_data(2023,120,50,99,30,400,5)
    #adjust_base_fare(2023, 120, 150)
    #print(change_booking_data_sold_spaces(2023,113,50))
    #print(get_booking_data_sold_spaces(2023, 120))
    #print(password_reset("jim@user.com","change","password"))
    #print(update_profile('jim@user.com','Jim','22 brisbane'))
    #print(get_name_from_database("bob@user.com"))

