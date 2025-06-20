#Import necessary libraries
import sqlite3
import os
import pytest
from datetime import datetime

#Path to the test database
TEST_DB_PATH = "test/test_crm.db"

@pytest.fixture
def db_connection():
    """
    Creates a temporary SQLite database and initializes the required schema.
    Yields the connection object and deletes the database file after the test.
    """
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    # Create required tables
    cursor.executescript("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        address TEXT,
        registration_date TEXT NOT NULL DEFAULT (datetime('now'))
    );
    CREATE TABLE invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL DEFAULT (datetime('now')),
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    yield conn
    conn.close()
    os.remove(TEST_DB_PATH)

#Test inserting user
def test_insert_user(db_connection):
    """
    Inserts a new user and verifies it was stored correctly.
    """
    cursor = db_connection.cursor()
    user = ("Ana", "López", "ana.lopez@email.com", "600123456", "Calle Falsa 123")
    cursor.execute("""
        INSERT INTO users (first_name, last_name, email, phone, address)
        VALUES (?, ?, ?, ?, ?)
    """, user)
    db_connection.commit()
    cursor.execute("SELECT * FROM users WHERE email = ?", (user[2],))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "Ana"
    assert result[2] == "López"

#Test inserting user and invoice
def test_insert_invoice(db_connection):
    """
    Inserts a user and an invoice for that user, then checks invoice values.
    """
    cursor = db_connection.cursor()
    # Insert test user
    cursor.execute("""
        INSERT INTO users (first_name, last_name, email, phone, address)
        VALUES ('Juan', 'Pérez', 'juan.perez@email.com', '611000000', 'Av. Central')
    """)
    user_id = cursor.lastrowid
    # Insert test invoice
    cursor.execute("""
        INSERT INTO invoices (user_id, description, amount, status)
        VALUES (?, ?, ?, ?)
    """, (user_id, "Servicio de soporte técnico", 200.0, "Paid"))
    db_connection.commit()
    cursor.execute("SELECT * FROM invoices WHERE user_id = ?", (user_id,))
    invoice = cursor.fetchone()
    assert invoice is not None
    assert invoice[3] == "Servicio de soporte técnico"
    assert invoice[4] == 200.0
