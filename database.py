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
    connection = connect(database=db_name)
    db = connection.cursor()

    db.execute("CREATE TABLE Users(UserId INTEGER UNIQUE primary key AUTOINCREMENT, UserName TEXT UNIQUE, UserPassword TEXT(200), Name TEXT, UserType INTEGER);")
    db.execute("CREATE TABLE BookingData(Year INTEGER, Day INTEGER, BaseFare FLOAT, TotalSpaces INTEGER, SpacesSold INTEGER, MaxPrice FLOAT, MinPrice FLOAT, DaysForSale INTEGER, CONSTRAINT  PKYearDay Primary Key (Year, Day));")

    connection.commit()

    db.close()
    connection.close()

def add_user_to_database(user_name, user_password):
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

    sql_instruction = f"INSERT INTO Users(UserName, UserPassword) VALUES ('{user_name}', '{user_password_hashed}');"
    
    try:
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()
        return True
    except IntegrityError:
        print("Username already in database")
        return False
    except:
        print("Something else went wrong")
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


if __name__ == "__main__":
    #print(add_user_to_database("jim@user.com","password"))
    #print(check_user_password_in_database("tom@user.com","password"))
    #print(delete_user_from_database("tim@user.com"))
    #create_booking_data(2023,120,50,99,30,400,5)
    print(change_booking_data_sold_spaces(2023,113,50))
    #print(get_booking_data_sold_spaces(2023, 120))

