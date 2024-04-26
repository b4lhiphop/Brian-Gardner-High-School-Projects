import string
import random
import sqlite3
import getpass
import bcrypt
conn = sqlite3.connect('expense_tracker')
cursor = conn.cursor()


# Create the employees table (if not already created)
cursor.execute("""CREATE TABLE IF NOT EXISTS user
(username text,password text,first_name text,last_name text,email text,user_id text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS transactions
 (expense_name, expense_price, date, category, expenses,user_id,transaction_id)""")
# cursor.execute("DROP TABLE IF EXISTS transactions")








conn.commit()
#PAGES
def welcome_page(cursor, conn):
    print("Hello User! Welcome To The Expense Tracker Program")
   
    while True:
        try:
            choice = int(input("1: Login \n2: Sign Up\n3: QUIT\n"))
            if choice == 1:
                username, user_id = login_page(cursor, conn)
                break
            elif choice == 2:
                username, user_id = create_account(cursor, conn)
                break
            elif choice == 3:
                print("OK BYE")
                username, user_id = None, None
                break
            else:
                print("Invalid choice. Please try again.")
                retry_choice = int(input("Press 1 to Try Again, Press 2 To QUIT"))
                if retry_choice == 2:
                    username, user_id = None, None
                    break
        except ValueError:
            print("Invalid input. Please enter a valid choice.")


    return username, user_id
def login_page(cursor, conn):
    while True:
        username = input("Please Insert Username: ")
        if username_check(cursor, conn, username):
            break  # Exit the loop if the username is valid
        else:
            print("Username Not Found")
            choice = int(input("1: Try Again\n2: Go Home\n3: QUIT\n"))
            if choice == 1:
                continue  # Restart the loop
            elif choice == 2:
                welcome_page(cursor, conn)
            else:
                return None, None  # Exit the function


    try:
        result = password_page(cursor, conn, username)
        if result is not None:
            username, user_id = result
        else:
            username, user_id = None, None
    except ValueError:
        print("An error occurred. Please try again.")
        username, user_id = None, None


    return username, user_id


def create_account(cursor, conn):
    check = True
    while check:
        username = input("Please Create Username: ")
        if username_check(cursor, conn, username):
            print("Username is already taken, please try again.")
        else:
            check = False  # Use the assignment operator here to exit the loop


    raw_password = getpass.getpass("Please Create Password: ")
    hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
    first_name = input("Please Insert First Name: ")
    last_name = input("Please Insert Last Name: ")
    email = input("Please Insert Email: ")
    user_id = create_id(8)
    cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", (username, hashed_password, first_name, last_name, email, user_id))
    conn.commit()  # Make sure to commit the changes to the database
    res = cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
    user_id = res.fetchone()[0]  # Fetch the first column value
    return username, user_id
def password_page(cursor, conn, username):
    while True:
        try:
            password = getpass.getpass("Please Insert Password: ")
            if not password_check(cursor, conn, username, password):
                print("Your Password is incorrect")
                choice = input("Press 1 to Try again\nPress 2 to go Home\nPress 3 to Quit: ")
                if choice == '3':
                    return None, None
                elif choice == '2':
                    return welcome_page(cursor, conn)  # Return the result of the welcome_page function
                else:
                    print("Invalid choice. Please try again.")
            else:
                res = cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
                user_id_tuple = res.fetchone()
                if user_id_tuple:
                    user_id = user_id_tuple[0]
                else:
                    user_id = None
                return username, user_id
        except:
            print("Input Incorrect")
            choice = input("Press 1 to Try again\nPress 2 to go Home\nPress 3 to Quit: ")
            if choice == '3':
                return None, None
            elif choice == '2':
                return welcome_page(cursor, conn)
            else:
                print("Invalid choice. Please try again.")


   
    return username, user_id
def create_id(lim): # Creates id with optional characters from full alphabet
    characters = string.ascii_letters+string.digits
    id =''
    i = 0
    for i in range(lim):
        id = id + random.choice(characters)
    return id




def username_check(cursor,conn,username): # Checks if the username the user inputted is in the list or not. if it is it returns true. If Not Returns False
    res = cursor.execute("SELECT username FROM user")
    username_tuples = res.fetchall()
    usernames = [x[0] for x in username_tuples]
    if username in usernames:
        return True
    return False
def password_check(cursor, conn, username, password):
    res = cursor.execute("SELECT password FROM user WHERE username = ?", (username,))
    stored_hashed_password = res.fetchone()


    if stored_hashed_password:
        hashed_password = stored_hashed_password[0]
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    else:
        return False














#Features
def add_expense(expenses, expense_value):#adds the expense_value to total expenses
    new_value = expense_value + expenses
    return new_value


def make_transaction(expense_name, expense_price, date, category, expenses, user_id,transaction_id): #makes the transaction
    transaction = [expense_name, expense_price, date, category, expenses, user_id,transaction_id]
    return transaction


def get_date():#Gets Date From user and ensures it is in the right format
    while True:
        date = input("Date of Transaction (mm/dd/yyyy): ")
        date_list = date.split("/")
        if len(date_list) == 3 and len(date_list[0]) == 2 and len(date_list[1]) == 2 and len(date_list[2]) == 4:
            month, day, year = date_list
            return month, day, year
        else:
            print("Please enter a valid date (mm/dd/yyyy)")
def delete_transaction(cursor, conn, transaction_id):
    # Retrieve the transaction from the database
    res = cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
    transaction = res.fetchone()


    # Display the details and prompt for confirmation
    print("Transaction details:")


    confirmation = input("Do you want to delete this transaction? (yes/no): ")
    if confirmation.lower() == 'yes':
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
        conn.commit()
        print("Transaction deleted successfully")
    else:
        print("Transaction deletion canceled")




def get_transaction_values(transaction):#Gets values for ransactin
    expense_name = transaction[0]
    expense_price = transaction[1]
    date = transaction[2]
    category = transaction[3]
    expenses = transaction[4]
    return expense_name, expense_price, date, category, expenses


from datetime import datetime
from datetime import datetime
expense_price = 0
expenses = 0
running = True
transaction = []
username, user_id = welcome_page(cursor, conn)
if username is None:
    print("OK BYE")
    running = False


while running:
    print("Expense Tracker GTD-489")
    choice = int(input('1: Add Expense \n2: View Expenses\n3: Delete Transaction\n4: QUIT: \n'))
    if choice == 1:
        expense_name = input("Expense Name:")
        while True:
            try:
                expense_price = float(input("Price: "))
                break  # Exit the inner loop if the input is valid
            except ValueError:
                print("expense must be a number")
                choice = input("1: Try Again 2: Go Home 3: Quit")
                if choice == '3':
                    running = False
                elif choice == '2':
                    welcome_page(cursor, conn)  # Call the function with cursor and conn as arguments


        if not running:
            break  # Exit the main loop if running is set to False


        month, day, year = get_date()
        date = f"{month}/{day}/{year}"
        category = input("Category of expense: ")
        expenses = add_expense(expenses, expense_price)
        transaction_id = create_id(10)
        new_transaction = make_transaction(expense_name, expense_price, date, category, expenses, user_id, transaction_id)
        # transaction.append(new_transaction)
        if user_id:
            cursor.execute("INSERT INTO transactions (expense_name, expense_price, date, category, expenses, user_id, transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (expense_name, expense_price, date, category, expenses, user_id, transaction_id))  
            conn.commit()
            print("Transaction Logged")
        else:
            print("User not logged in.")
   
    elif choice == 2:
        res = cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = res.fetchall()


        if len(transactions) == 0:
            print("You have made no prior transactions")
        else:
            for transaction in transactions:
                expense_name, expense_price, date, category, expenses, _, _ = transaction
                print(f"On {date} you bought {expense_name} for ${expense_price}. This is held in the {category} category.")
            total_expenses = sum(transaction[1] for transaction in transactions)
            print(f"Your Total Expenses are {total_expenses}")
   
    elif choice == 3:
        res = cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = res.fetchall()
        if len(transactions) == 0:
            print("You have no transactions to delete.")
        else:
            for transaction in transactions:
                expense_name, _, _, _, _, _, transaction_id = transaction
                print(f"Transaction ID: {transaction_id}, Expense Name: {expense_name}")
            selected_transaction_id = input("Enter the transaction ID to delete: ")
            delete_transaction(cursor, conn, selected_transaction_id)
   
    elif choice == 4:
        print("Ok Bye")
        running = False


conn.close()





