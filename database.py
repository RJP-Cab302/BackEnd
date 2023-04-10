from sqlite3 import *
from os import path
import bcrypt

def create_user_database(db_name):

    connection = connect(database=db_name)
    db = connection.cursor()

    db.execute("CREATE TABLE Users(UserId INTEGER UNIQUE primary key AUTOINCREMENT, UserName TEXT UNIQUE, UserPassword TEXT(200), Name TEXT, UserType INTEGER);")

    connection.commit()

    db.close()
    connection.close()

def add_user_to_database(user_name, user_password):

    user_password_hashed = str(hash_password(user_password))
    users_db_file = "./Users.db"
    if not path.exists(users_db_file):
        create_user_database(users_db_file)
    
    connection = connect(database=users_db_file)
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
    users_db_file = "./Users.db"

    if not path.exists(users_db_file):
        print("Database does not exist")
        return False
    
    connection = connect(database=users_db_file)
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
    users_db_file = "./Users.db"

    if not path.exists(users_db_file):
        print("Database does not exist")
        return False
    
    sql_instruction = f"DELETE from Users WHERE UserName = ('{user_name}');"
    
    connection = connect(database=users_db_file)
    db = connection.cursor()

    db.execute(sql_instruction)
    connection.commit()
    db.close()
    connection.close()
    return True

if __name__ == "__main__":
    # print(add_user_to_database("tim@user.com","password"))
    # print(check_user_password_in_database("tim@user.com","password"))
    print(delete_user_from_database("tim@user.com"))

