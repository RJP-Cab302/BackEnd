from sqlite3 import *
from os import path
import bcrypt

db_file = "./Storage.db"

def create_database(db_name):

    connection = connect(database=db_name)
    db = connection.cursor()

    db.execute("CREATE TABLE Users(UserId INTEGER UNIQUE primary key AUTOINCREMENT, UserName TEXT UNIQUE, UserPassword TEXT(200), Name TEXT, UserType INTEGER);")
    db.execute("CREATE TABLE BookingData(Year INTEGER, Day INTEGER, BaseFare FLOAT, TotalSpaces INTEGER, SpacesSold INTEGER, DaysForSale INTEGER, CONSTRAINT  PKYearDay Primary Key (Year, Day));")

    connection.commit()

    db.close()
    connection.close()

def add_user_to_database(user_name, user_password):

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
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()
    
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    
    return hash.decode()

def check_hash(entered_password, hashed_password):
    userBytes = entered_password.encode()
    result = bcrypt.checkpw(userBytes, hashed_password.encode())
    return result

def check_user_password_in_database(entered_user_name, entered_user_password):
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

def create_booking_data(year, day, base_fare, total_spaces, days_for_sale):
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
        sql_instruction = f"INSERT INTO BookingData(Year, Day, BaseFare, TotalSpaces, DaysForSale) VALUES ({year}, {day},{base_fare}, {total_spaces},{days_for_sale});"

        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()

def change_booking_data_sold_spaces(year, day, space_sold):
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False
    
    sql_instruction = f"SELECT Year, Day FROM BookingData WHERE Year == ({year}) and Day == ({day})"

    connection = connect(database=db_file, timeout=5)
    db = connection.cursor()

    db.execute(sql_instruction)

    rows = db.fetchall()

    db.close()
    connection.close()

    if len(rows) == 1:
        print("updating")
        connection = connect(database=db_file, timeout=5)
        db = connection.cursor()
        sql_instruction = f"UPDATE BookingData SET SpacesSold = {space_sold} WHERE Year == ({year}) and  Day == ({day})"
        db.execute(sql_instruction)
        connection.commit()
        db.close()
        connection.close()

def get_booking_data_sold_spaces(year, day):
    global db_file

    if not path.exists(db_file):
        print("Database does not exist")
        return False
    
    sql_instruction = f"SELECT Year, Day, BaseFare, TotalSpaces, SpacesSold, DaysForSale FROM BookingData WHERE Year == ({year}) and Day == ({day})"

    connection = connect(database=db_file, timeout=5)
    db = connection.cursor()

    db.execute(sql_instruction)

    rows = db.fetchall()

    db.close()
    connection.close()

    return rows


if __name__ == "__main__":
    # print(add_user_to_database("tim@user.com","password"))
    # print(check_user_password_in_database("tim@user.com","password"))
    #print(delete_user_from_database("tim@user.com"))
    # create_booking_data(2023,300,100,99,30)
    change_booking_data_sold_spaces(2023,300,5)
    #print(get_booking_data_sold_spaces(2023, 300))

