from database import add_user_to_database, add_vehicle_to_database, create_booking_data, get_user_id_from_database
import datetime

fake_password = "password"
random_user_emails_and_names = [["sally@test.com", "sally"],["tom@test.com","tom"], ["fred@flintstones.com", "fred"], ["betty@flintstones.com", "betty"]]

# Add users to database
for email,name in random_user_emails_and_names:
    add_user_to_database(email, fake_password, name)

# Add vehicles to database
for i, item in enumerate(random_user_emails_and_names):
    email, name = item
    add_vehicle_to_database(str(i)+"rego", get_user_id_from_database(email),"Car", "Toyota", "Corolla")

# Add booking data to database
current_day = int(datetime.datetime.now().strftime("%j"))

current_year = int(datetime.datetime.now().strftime("%Y"))

for i in range(current_day, 365):
    create_booking_data(current_year, i, 50, 50, 180, 100, 5)

for i in range(1, current_day):
    create_booking_data(current_year + 1, i, 50, 50, 180, 100, 5)