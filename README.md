# Shop Record and Sales Activity Tracker

## Overview

This project consists of two Python scripts: `database.py` and `main.py`. The `database.py` script provides backend
functionalities for managing shop records and sales activity using SQLite, while `main.py` serves as a user interface
for interacting with these functionalities.

### `main.py`

- **User Interface:**
  - Provides a command-line interface for users to interact with the shop record and sales activity functionalities.

## Usage

1. Ensure you have Python installed.
2. Install required dependencies using `pip install tabulate` (if not already installed).

### Running the Application

```bash
python main.py


## Features

### `database.py`

- **Database Creation:**
  - `create()`: Creates a new SQLite database and table for managing shop records.

- **Stock Management:**
  - `add_newstock()`: Adds new stock items to the database.
  - `update_stock()`: Updates the quantity of existing stock items in the database.

- **Sales Transactions:**
  - `sales()`: Records sales transactions, updating stock quantities and total quantity sold.

- **Data Display:**
  - `all_items()`: Displays the entire table of items in a tabulated format.

- **Search Functionality:**
  - `search()`: Allows users to search for items based on various criteria.


