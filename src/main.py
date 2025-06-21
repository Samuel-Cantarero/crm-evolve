#Import necessary libraries
import sqlite3
import re
from datetime import datetime
import os

#Paths for database file and schema SQL
DB_PATH = "database/database_crm.db"
SCHEMA_PATH = "database/crm_schema.sql"

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

#Main menu
def menu():
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

# 1. Register user
def register_user():
    """
    Registers a new user in the database with basic input validation.
    """
    print("\n=== REGISTER NEW USER ===")
    first_name = input("Enter first name: ").strip()
    last_name  = input("Enter last name:  ").strip()
    email      = input("Enter email: ").strip()

    # Data validation
    if not first_name or not last_name or not email:
        print("First name, last name, and email are required.")
        return
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email.")
        return

    try:
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print("Email is already registered.")
            return

        # Phone: optional, digits only
        phone_str = input("Enter phone (digits only, optional): ").strip()
        try:
            phone = int(phone_str) if phone_str else None
        except ValueError:
            print("Invalid phone number: digits only.")
            return

        # Address: optional
        address = input("Enter address (optional): ").strip() or None

        registration_date = datetime.now().strftime("%Y-%m-%d")

        # Insert the new user into the users table
        cursor.execute(
            """
            INSERT INTO users 
                (first_name, last_name, email, phone, address, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (first_name,
             last_name,
             email,
             phone,
             address,
             registration_date)
        )
        conn.commit()

        print("\nUser registered successfully!")
        user_id = cursor.lastrowid
        print(f"Assigned ID: {user_id}")
        print(f"Registration date: {registration_date}")

    except sqlite3.Error as e:
        print(f"Error registering user: {e}")

#2. Search user
def search_user():
    """
    Searches for a user by email or by full name (first and last) and displays their information.
    """
    print("\n=== SEARCH USER ===")
    print("1. Search by email")
    print("2. Search by full name")
    option = input("Choose search method: ").strip()

    if option == "1":
        email = input("Enter email: ").strip()
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user:
                show_user_info(user)
            else:
                print("User not found.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    elif option == "2":
        full_name = input("Enter full name (first and last): ").strip()
        parts = full_name.split(None, 1)
        if len(parts) < 2:
            print("Please enter both first and last name.")
            return
        first_input, last_input = parts
        pattern_fn = f"%{first_input}%"
        pattern_ln = f"%{last_input}%"
        try:
            cursor.execute(
                "SELECT * FROM users WHERE first_name LIKE ? AND last_name LIKE ?", 
                (pattern_fn, pattern_ln)
            )
            users = cursor.fetchall()
            if users:
                for user in users:
                    show_user_info(user)
            else:
                print("User not found.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    else:
        print("Invalid option.")

def show_user_info(user):
    """
    Prints detailed information about a user.
    """
    print("\n--- USER FOUND ---")
    print(f"ID: {user[0]}")
    print(f"Name: {user[1]} {user[2]}")
    print(f"Email: {user[3]}")
    print(f"Phone: {user[4] if user[4] else 'Not specified'}")
    print(f"Address: {user[5] if user[5] else 'Not specified'}")
    print(f"Registration date: {user[6]}")

#3. Create invoice for user
def create_invoice():
    """
    Creates an invoice for a user identified by email.
    """
    print("\n=== CREATE INVOICE ===")
    email = input("Enter user's email: ").strip()
    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if not user:
            print("User not found.")
            return
        print(f"\nUser found: {user[1]} {user[2]}")
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
        issue_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Insert the invoice into the invoices table
        cursor.execute(
            '''INSERT INTO invoices (user_id, issue_date, description, amount, status)
               VALUES (?, ?, ?, ?, ?)''',
            (user[0], issue_date, description, amount, status)
        )
        conn.commit()
        print("\nInvoice created successfully!")
        invoice_id = cursor.lastrowid
        print(f"Invoice ID: {invoice_id}")
        print(f"Issue date: {issue_date}")
        print(f"Client: {user[1]} {user[2]}")
        print(f"Description: {description}")
        print(f"Amount: ${amount:.2f}")
        print(f"Status: {status}")
    except sqlite3.Error as e:
        print(f"Error creating invoice: {e}")

# 4. Show all users
def show_users():
    """
    Displays all users in the database.
    """
    print("\n=== USER LIST ===")
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        if not users:
            print("No users registered.")
            return
        for inx, user in enumerate(users, 1):
            print(f"\nUser #{inx}:")
            print(f"ID: {user[0]}")
            print(f"Name: {user[1]} {user[2]}")
            print(f"Email: {user[3]}")
            print(f"Phone: {user[4] if user[4] else 'Not specified'}")
            print(f"Registration date: {user[6]}")
        print(f"\nTotal registered users: {len(users)}")
    except sqlite3.Error as e:
        print(f"Error displaying users: {e}")

# 5. Show invoices for a user
def show_user_invoices():
    """
    Displays all invoices associated with a user identified by email.
    """
    print("\n=== USER INVOICES ===")
    email = input("Enter user's email: ").strip()
    try:
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        if not user:
            print("User not found.")
            return
        print(f"\n--- INVOICES FOR {user[1]} {user[2]} ---")
        cursor.execute("SELECT * FROM invoices WHERE user_id=?", (user[0],))
        invoices = cursor.fetchall()
        if not invoices:
            print("No invoices for this user.")
            return
        total_amount = 0
        pending_amount = 0
        for inx, invoice in enumerate(invoices, 1):
            print(f"\nInvoice #{inx}:")
            print(f"ID: {invoice[0]}")
            print(f"Issue date: {invoice[2]}")
            print(f"Description: {invoice[3]}")
            print(f"Amount: ${invoice[4]:.2f}")
            print(f"Status: {invoice[5]}")
            total_amount += invoice[4]
            if invoice[5] == "Pending":
                pending_amount += invoice[4]
        print(f"\nTotal invoices: {len(invoices)}")
        print(f"Total invoiced amount: ${total_amount:.2f}")
        print(f"Pending amount: ${pending_amount:.2f}")
    except sqlite3.Error as e:
        print(f"Error displaying user invoices: {e}")

#6. Financial summary per user
def financial_summary():
    """
    Prints a financial summary for all users in the database.
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
            print(f"\nUser: {user[1]} {user[2]} ({user[3]})")
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
        print(f"Error generating financial summary: {e}")

#Main execution
if __name__ == "__main__":
    menu()
    conn.close()
