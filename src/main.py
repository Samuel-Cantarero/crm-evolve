#import necessary libraries
import sqlite3
import re
from datetime import datetime
import os

# Paths for database file and schema SQL
DB_PATH = "../database/database_crm.db"
SCHEMA_PATH = "../database/crm_schema.sql"

def initialize_database():
    """
Connects to the SQLite database and runs the schema script to ensure all tables exist.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        #Execute schema SQL
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()
            cursor.executescript(schema)
        conn.commit()
        return conn, cursor
    except (sqlite3.Error, FileNotFoundError, Exception) as e:
        print(f"Error initializing the database: {e}")
        exit(1)

# Initialize the database and get the connection/cursor
conn, cursor = initialize_database()

def menu():
    """
    Menu for the CRM system.
    """
    while True:
        print("\n=== CRM SYSTEM ===")
        print("1. Register new user")
        print("2. Search user")
        print("3. Create invoice for user")
        print("4. Show all users")
        print("5. Show invoices for a user")
        print("6. Financial summary per user")
        print("7. Exit")
        option = input("Choose an option: ")

        if option == "1":
            register_user()
        elif option == "2":
            search_user()
        elif option == "3":
            create_invoice()
        elif option == "4":
            show_users()
        elif option == "5":
            show_user_invoices()
        elif option == "6":
            financial_summary()
        elif option == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

def register_user():
    """
    Registers a new user in the database with basic input validation.
    """
    print("\n=== REGISTER NEW USER ===")
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    email = input("Enter email: ").strip()
    if not first_name or not last_name or not email:
        print("First name, last name, and email are required.")
        return
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email.")
        return
    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            print("Email is already registered.")
            return
        phone = input("Enter phone (optional): ").strip()
        address = input("Enter address (optional): ").strip()
        registration_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0] + 1
        code = f"USR{str(count).zfill(3)}"
        # Insert the new user into the users table
        cursor.execute(
            '''INSERT INTO users (code, first_name, last_name, email, phone, address, registration_date)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (code, first_name, last_name, email, phone if phone else None, address if address else None, registration_date)
        )
        conn.commit()
        print("\nUser registered successfully!")
        print(f"Assigned ID: {code}")
        print(f"Registration date: {registration_date}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def search_user():
    """
    Allows searching for a user by email or first name.
    """
    print("\n=== SEARCH USER ===")
    print("1. Search by email")
    print("2. Search by first name")
    option = input("Choose search method: ")
    try:
        if option == "1":
            email = input("Enter email: ").strip()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            if user:
                show_user_info(user)
            else:
                print("User not found.")
        elif option == "2":
            first_name = input("Enter first name: ").strip()
            cursor.execute("SELECT * FROM users WHERE first_name LIKE ?", (f"%{first_name}%",))
            users = cursor.fetchall()
            if users:
                for user in users:
                    show_user_info(user)
            else:
                print("User not found.")
        else:
            print("Invalid option.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def show_user_info(user):
    """
    Displays user details given a user tuple.
    """
    print("\n--- USER FOUND ---")
    print(f"ID: {user[1]}")
    print(f"Name: {user[2]} {user[3]}")
    print(f"Email: {user[4]}")
    print(f"Phone: {user[5] if user[5] else 'Not specified'}")
    print(f"Address: {user[6] if user[6] else 'Not specified'}")
    print(f"Registration date: {user[7]}")

def create_invoice():
    """
    Creates a new invoice for an existing user.
    """
    print("\n=== CREATE INVOICE ===")
    email = input("Enter user's email: ").strip()
    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if not user:
            print("User not found.")
            return
        print(f"\nUser found: {user[2]} {user[3]}")
        description = input("Enter service/product description: ").strip()
        try:
            amount = float(input("Enter total amount: ").replace(",", "."))
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount.")
            return
        print("Select status:")
        print("1. Pending")
        print("2. Paid")
        print("3. Cancelled")
        statuses = { "1": "Pending", "2": "Paid", "3": "Cancelled"}
        status_option = input("Status: ")
        status = statuses.get(status_option)
        if not status:
            print("Invalid status.")
            return
        cursor.execute("SELECT COUNT(*) FROM invoices")
        count = cursor.fetchone()[0] + 1
        number = f"INV{str(count).zfill(3)}"
        issue_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Insert the new invoice into the invoices table
        cursor.execute(
            '''INSERT INTO invoices (number, user_id, issue_date, description, amount, status)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (number, user[0], issue_date, description, amount, status)
        )
        conn.commit()
        print("\nInvoice created successfully!")
        print(f"Invoice number: {number}")
        print(f"Issue date: {issue_date}")
        print(f"Client: {user[2]} {user[3]}")
        print(f"Description: {description}")
        print(f"Amount: ${amount:.2f}")
        print(f"Status: {status}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def show_users():
    """
    Lists all registered users.
    """
    print("\n=== USER LIST ===")
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if not users:
            print("No users registered.")
            return
        for idx, user in enumerate(users, 1):
            print(f"\nUser #{idx}:")
            print(f"ID: {user[1]}")
            print(f"Name: {user[2]} {user[3]}")
            print(f"Email: {user[4]}")
            print(f"Phone: {user[5] if user[5] else 'Not specified'}")
            print(f"Registration date: {user[7]}")
        print(f"\nTotal registered users: {len(users)}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def show_user_invoices():
    """
    Displays all invoices for a given user by email.
    """
    print("\n=== USER INVOICES ===")
    email = input("Enter user's email: ").strip()
    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if not user:
            print("User not found.")
            return
        print(f"\n--- INVOICES FOR {user[2]} {user[3]} ---")
        cursor.execute("SELECT * FROM invoices WHERE user_id=?", (user[0],))
        invoices = cursor.fetchall()
        if not invoices:
            print("No invoices for this user.")
            return
        total_amount = 0
        pending_amount = 0
        for idx, invoice in enumerate(invoices, 1):
            print(f"\nInvoice #{idx}:")
            print(f"Number: {invoice[1]}")
            print(f"Issue date: {invoice[3]}")
            print(f"Description: {invoice[4]}")
            print(f"Amount: ${invoice[5]:.2f}")
            print(f"Status: {invoice[6]}")
            total_amount += invoice[5]
            if invoice[6] == "Pending":
                pending_amount += invoice[5]
        print(f"\nTotal invoices: {len(invoices)}")
        print(f"Total invoiced amount: ${total_amount:.2f}")
        print(f"Pending amount: ${pending_amount:.2f}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def financial_summary():
    """
    Shows a financial summary per user and overall.
    """
    print("\n=== FINANCIAL SUMMARY ===")
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        total_invoices = 0
        total_income = 0
        received_income = 0
        pending_income = 0
        for user in users:
            cursor.execute("SELECT amount, status FROM invoices WHERE user_id=?", (user[0],))
            invoices = cursor.fetchall()
            n_invoices = len(invoices)
            total = sum(i[0] for i in invoices)
            paid = sum(i[0] for i in invoices if i[1] == "Paid")
            pending = sum(i[0] for i in invoices if i[1] == "Pending")
            print(f"\nUser: {user[2]} {user[3]} ({user[4]})")
            print(f"- Total invoices: {n_invoices}")
            print(f"- Total amount: ${total:.2f}")
            print(f"- Paid invoices: ${paid:.2f}")
            print(f"- Pending invoices: ${pending:.2f}")
            total_invoices += n_invoices
            total_income += total
            received_income += paid
            pending_income += pending
        print("\n--- OVERALL SUMMARY ---")
        print(f"Total users: {len(users)}")
        print(f"Total invoices issued: {total_invoices}")
        print(f"Total income: ${total_income:.2f}")
        print(f"Received income: ${received_income:.2f}")
        print(f"Pending income: ${pending_income:.2f}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Entry point
if __name__ == "__main__":
    menu()
    # Close the database connection when done
    conn.close()
