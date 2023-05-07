import datetime
import math
from database import *

#days within a year
def days_in_year(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return 366
    else:
        return 365

class Fare_Calculator:
    def __init__(self, base_fare, total_spaces, spaces_sold, day_of_sale, total_days_for_sale, max_price, min_price):
        self.base_fare = base_fare
        self.total_spaces = total_spaces
        self.day_of_sale = day_of_sale
        self.total_days_for_sale = total_days_for_sale
        self.max_price = max_price
        self.min_price = min_price
        if spaces_sold == None:
            spaces_sold = 0
        self.spaces_sold = spaces_sold
        assert day_of_sale <= total_days_for_sale, "Can not have days till permit, greater than days for sale"
        assert spaces_sold <= total_spaces, "Can not have more spaces sold than total spaces"
        print(f'Base fare: ${base_fare}\nTotal spaces: {total_spaces}\nSpaces sold: {spaces_sold}\nSpaces expected to be sold: {self.expected_remaining()}\nDays till permit: {day_of_sale}\nDays for sale: {total_days_for_sale}')

    def expected_remaining(self):
        expected_change_per_day = self.total_spaces / self.total_days_for_sale
        expected = self.day_of_sale * expected_change_per_day
        return expected
    
    def calculate_fare(self):
        
        price = math.floor(self.base_fare * (self.spaces_sold / self.expected_remaining()))
        if price > self.max_price:
            return self.max_price
        
        if price < self.min_price:
            return self.min_price

        return price
    
if __name__ == "__main__":
    day = 120
    year = 2023
    datalist = year, day, base_fare, total_spaces, spaces_sold, days_for_sale, max_price, min_price = get_booking_data_sold_spaces(year,day)
    
    first_day_on_sale = day - days_for_sale
    print("first_day_on_sale: ", first_day_on_sale)
    current_day = datetime.datetime.now().strftime("%j")
    current_year = datetime.datetime.now().strftime("%Y")
    print("Current day: ", int(current_day))
    day_of_sale = day - int(current_day)
    print("day_of_sale: ", day_of_sale)
    
    cal = Fare_Calculator(base_fare,total_spaces,spaces_sold,day_of_sale,days_for_sale, max_price, min_price)
    print(f"new price ${cal.calculate_fare()}")
