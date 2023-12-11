# database.py
import os
import sqlite3
from datetime import datetime
from tabulate import tabulate

database_name = None

current_time = datetime.now().strftime("%A   %m/%d/%y  %I:%M:%S %p")


def create():
    """
    This function prompt the variable database_name for the user to put the name for the new database file,
    Then it checks if the data stored in the variable database_name has already existed using the os module to and if
    the output, if the output comes out as TRUE, it raises a value_error which stop the whole program from running ,
    in the case of which the variable  database comes out as FALSE,then it runs the lines of code in the ELSE condition,
    Then ask for the name you would like to store your sql table and checks if the name haven't existed

    """
    global database_name
    # Accept the user's name for the database file
    database_name = input("What would you like to name your database? ") + ".db"
    # Checks if the file has already existed in the working path
    if os.path.exists(database_name):
        print(f"Database file {database_name} already exists. Not creating a new one.")
        return ValueError(f"Database file {database_name} already exists. Not creating a new one.")
    else:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # Accept the user's name for the table
        in_table_name = input("What would you like to name your table: ")
        c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name =?", (in_table_name,))
        table_exists = c.fetchone() is not None
        # CHECKS IF THE NAME OF THE SQL-TABLE HASN'T EXISTED,BY CHECKING THE NAME IN SQLITE-MASTER
        if table_exists:
            return ValueError(f"The table {in_table_name} already exists.")
        else:
            c.execute(f"""
                    CREATE TABLE {in_table_name}(
                    Type TEXT,
                    Item TEXT,
                    QuantityStock INTEGER,
                    Quantitysold
                    Restock INTEGER,
                    sales INTEGER,
                    Price INTEGER,
                    DateTime TEXT)""")
    conn.commit()
    conn.close()


def add_newstock():
    """ This function allows the user to input new stocks , existing_db_files to fetch file with .db to
     be able to connect the function to the sql.
    (stock) get the item which is about to be stored and the if statement checks is the (stock) is a string ,
    the try block has the (quantity) to accept the quantity of the item about to be stored and (price) for the amount of
    the item incase there is a value error the except block returns an error message to the user to input only integers
    the else block interact with the database to insert the dats into the table """
    sold_quantity = 0
    # Fetches file with .db in the working directory
    try:
        existing_db_files = [file for file in os.listdir() if file.endswith(".db")]
        db_filename = existing_db_files[0]
    except IndexError:
        print("You need to create a file first")
    else:
        # Accept the name of item about to be entered into the table
        stock = input("Name of the item: ").upper()
        # The IF statements checks is the (stock) isn't an integer
        if stock.isdigit():
            print("Error: Please enter a valid item name, not an integer.")
        else:
            try:
                quantity = int(input("Quantity of the item: "))
                price = int(input("Price per one: "))
            # returns an error message to the user if price & quantity isn't string
            except ValueError:
                print("Error: Please enter a valid amount of quantity, not a string.")
                # returns an error message to the user if there is an error in the sql table
            except sqlite3.Error:
                print("SQL Error")
            else:
                restock_value = "-"
                add_type = "NEW STOCK"
                conn = sqlite3.connect(db_filename)
                c = conn.cursor()
                c.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
                table_name = c.fetchone()
                tb_name = table_name[0]
                c.execute(f"INSERT INTO {tb_name} VALUES(?, ?, ?, ?, ?, ?, ?)",
                          (add_type, stock, quantity, sold_quantity, restock_value, price, current_time))
                conn.commit()
                conn.close()


def update_stock():
    try:
        existing_db_files = [file for file in os.listdir() if file.endswith(".db")]
        db_filename = existing_db_files[0]
    except IndexError:
        print("You need to create a database file")
    else:
        up_stock = input("Name of the item: ").upper()
        if up_stock.isdigit():
            print("Error: Please enter a valid item name, not an integer.")
        else:
            try:
                # accept the newly added amount of quantity to be added
                up_quantity = int(input("Amount of the quantity to be added: "))
            except ValueError:
                print("Error: Please enter a valid item name, not an integer.")
            except sqlite3.Error:
                print("sqlite error")
            else:
                conn = sqlite3.connect(db_filename)
                c = conn.cursor()
                c.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
                table_name = c.fetchone()
                tb_name = table_name[0]
                c.execute(f"SELECT * FROM {tb_name} WHERE Item =? ", (up_stock,))
                # Fetches the tuples of the name of the item in (up_stock)
                find_existing = c.fetchall()[0]
                # Fetches the index at position in [2] & [5] to fetch the number in the quantity column & price column in the
                # SQL table
                find_quantity = find_existing[2]
                find_price = find_existing[5]
                update_type = "UPDATED  STOCK"
                quantity_sold = "-"
                # adds us the number in the (find_quantity) with the (up_quantity)
                updated_amount = find_quantity + up_quantity
                c.execute(f"INSERT INTO {tb_name} VALUES(?, ?, ?, ?, ?, ?, ?)",
                          (
                              update_type, up_stock, updated_amount, quantity_sold, up_quantity, find_price, current_time,))
                c.execute(f"UPDATE {tb_name} SET QuantityStock =? WHERE Item =?", (updated_amount, up_stock))
                # IT CHECKS THE ITEM COLUMN IN THE SQL TABLE IF THE INPUT OF THE USER HAS ALREADY EXISTED,
                # IF IT HAS ALREADY EXISTED THEN IF FETCH THE QUANTITY OF THE ITEM AND ADD IT UP WITH THE NEWLY UP_QUANTITY
                # INPUT,IT THEN UPDATE THE COLUMN
                conn.commit()
                conn.close()


def sales():
    """
    when this function is called it subtract the amount sold from the amount of quantity in stock of the item
    being sold then it adds the sold numbers of the item being sold to the previous sales

    :return:
    """
    try:
        existing_db_files = [file for file in os.listdir() if file.endswith(".db")]
        db_filename = existing_db_files[0]
    except IndexError:
        print("You need to create a database file")
    else:
        sold_stock = input("Name of the item: ").upper()
        if sold_stock.isdigit():
            print("Error: Please enter a valid item name, not an integer.")
        else:
            try:
                sold_quantity = int(input("Quantity sold: "))
            except ValueError:
                print("Error: Please enter a valid item name, not an integer.~")
            except sqlite3.Error:
                print("Error handling the SQL")

            else:
                conn = sqlite3.connect(db_filename)
                c = conn.cursor()
                c.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
                table_name = c.fetchone()
                tb_name = table_name[0]
                c.execute(f"SELECT * FROM {tb_name} WHERE Item =?", (sold_stock,))
                find_existing = c.fetchall()[0]
                # Fetches the index at position in [2], [5], [3] to fetch the number in the quantity column ,price column &
                # previous sold column in the SQL table

                find_quantity = find_existing[2]
                find_price = find_existing[5]
                prev_sold = find_existing[3]
                sold_type = "SOLD  STOCK"
                restock_value = "-"
                sold_amount = find_quantity - sold_quantity
                total_sold = prev_sold + sold_quantity
                c.execute(f"INSERT INTO {tb_name} VALUES(?, ?, ?, ?, ?, ?, ?)",
                          (sold_type, sold_stock, sold_amount, total_sold, restock_value, find_price, current_time,))
                c.execute(f"UPDATE {tb_name} SET QuantityStock =?, QuantitySold =? WHERE Item =?",
                          (sold_amount, total_sold, sold_stock,))
                conn.commit()
                conn.close()


def all_items():
    """This print the whole table of the database"""
    path_file = [file for file in os.listdir() if file.endswith(".db")]
    db_name = path_file[0]
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
    table_name = c.fetchone()
    tb_name = table_name[0]
    items = c.execute(f"SELECT rowid, * FROM {tb_name}")
    print(tabulate(items, headers=["S/N", "TYPE", "NAME", "QUANTITY In Stock", "Quantity Sold ", "RECENTLY ADDED",
                                   "PRICE", "TIMESTAMP"], tablefmt="fancy_grid"))
    conn.commit()
    conn.close()


def search():
    """This function filters the database according to the user input"""
    path_file = [file for file in os.listdir() if file.endswith(".db")]
    db_name = path_file[0]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
    table_name = c.fetchone()
    tb_name = table_name[0]
    print("Search options:\n"
          "1: Search by the stock name\n"
          "2: Search by the transaction type\n"
          "3: Search by transaction typ and stock name\n")
    search_opt = input("pick")
    if search_opt == "1":
        search_input = input("What would you like to search for....: ").upper()
        c.execute(f"SELECT rowid, * FROM {tb_name} WHERE Item =?", (search_input,))
        search_results = c.fetchall()
        print(tabulate(search_results,
                       headers=["S/N", "TYPE", "NAME", "QUANTITY In Stock", "Quantity Sold ", "RECENTLY ADDED",
                                "PRICE", "TIMESTAMP"], tablefmt="fancy_grid"))
    elif search_opt == "2":
        search_input = input("What would you like to search for....: ").upper()
        c.execute(f"SELECT rowid, * FROM {tb_name} WHERE Type =?", (search_input,))
        search_results = c.fetchall()
        print(tabulate(search_results,
                       headers=["S/N", "TYPE", "NAME", "QUANTITY In Stock", "Quantity Sold ", "RECENTLY ADDED",
                                "PRICE", "TIMESTAMP"], tablefmt="fancy_grid"))
    elif search_opt == "3":
        search_item = input("What stock would you like to search for: ").upper()
        search_type = input("What type would you like to search for: ").upper()
        c.execute(f"SELECT rowid, * FROM {tb_name} WHERE Item =? AND Type =?", (search_item, search_type,))
        search_results = c.fetchall()
        print(tabulate(search_results,
                       headers=["S/N", "TYPE", "NAME", "QUANTITY In Stock", "Quantity Sold ", "RECENTLY ADDED",
                                "PRICE", "TIMESTAMP"], tablefmt="fancy_grid"))
    else:
        print("Invalid option")
    conn.commit()
    conn.close()


print(current_time)
