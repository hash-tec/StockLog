# main.py
from datetime import datetime

import database as db


class Stocks:
    # db.create()
    """This class contains methods that calls the function in the database modules"""
    def __init__(self):
        self.db_details = None
        self.stock = None
        self.quantity = None
        self.price = None
        self.current_time = None

    @staticmethod
    def new_database():
        db.create()

    def user_input(self):
        self.stock = input("Name of the item: ")
        self.quantity = int(input("Quantity of the item: "))
        self.price = int(input("Price per one: "))
        self.current_time = datetime.now().strftime("%A   %m/%d/%y  %I:%M:%S %p  ")
        self.db_details = (self.stock, self.quantity, self.price, self.current_time)

    @staticmethod
    def add_newstock():
        db.add_newstock()

    @staticmethod
    def up_stock():
        db.update_stock()

    @staticmethod
    def sales():
        db.sales()

    @staticmethod
    def user_search():
        db.search()

    @staticmethod
    def all_stocks():
        db.all_items()


stocks = Stocks()

if __name__ == "__main__":

    while True:
        print("Welcome back ")
        user_choice = input("what would you like to do:\nPick a number to perform a function\n"
                            "1: Create new database file\n"
                            "2: Add stocks to your list\n"
                            "3: Update stocks\n"
                            "4: Make a sales\n"
                            "5: Search option\n"
                            "6: Get stock list\n"
                            "7: Exit\n")
        # The IF statements calls the method in the class STOCKS  according to the user input
        if user_choice == '1':
            stocks.new_database()
            break
        elif user_choice == '2':
            stocks.add_newstock()
        elif user_choice == '3':
            stocks.up_stock()
        elif user_choice == '4':
            stocks.sales()
        elif user_choice == '5':
            stocks.user_search()
        elif user_choice == "6":

            stocks.all_stocks()
        elif user_choice == '7':
            print("You've exited the program....")
            break
        else:
            print("Invalid choice")

print(datetime.now().strftime("%A   %m/%d/%y  %I:%M:%S %p  "))
