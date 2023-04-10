import math

class Fare_Calculator:
    def __init__(self, base_fare, total_spaces, spaces_sold, days_till_permit, days_for_sale):
        self.base_fare = base_fare
        self.total_spaces = total_spaces
        self.days_till_perimt = days_till_permit
        self.days_for_sale = days_for_sale
        self.spaces_sold = spaces_sold
        assert days_till_permit <= days_for_sale, "Can not have days till permit, greater than days for sale"
        print(f'Base fare: ${base_fare}\nTotal spaces {total_spaces}\nSpaces sold: {spaces_sold}\nSpaces expected to be sold: {self.expected_remaining()}\nDays to go: {days_till_permit}\nDays for sale: {days_for_sale}')
        

    def expected_remaining(self):
        expected_change_per_day = self.total_spaces / self.days_for_sale
        expected = self.days_till_perimt * expected_change_per_day
        return expected
    
    def calculate_fare(self):
        return math.floor(self.base_fare * self.spaces_sold / self.expected_remaining())
    
if __name__ == "__main__":
    cal = Fare_Calculator(100,45,100,15,30)
    print(cal.expected_remaining())
    print(f"new price ${cal.calculate_fare()}")
