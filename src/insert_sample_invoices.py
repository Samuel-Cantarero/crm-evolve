#Import necessary libraries
import sqlite3

#Connect to the database
try:
    conn = sqlite3.connect('database/database_crm.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# List of user emails
emails = [
    "lucia.martinez@email.com",
    "hugo.garcia@email.com",
    "martina.sanchez@email.com",
    "pablo.diaz@email.com",
    "sofia.romero@email.com",
    "daniel.fernandez@email.com",
    "valeria.moreno@email.com",
    "alejandro.jimenez@email.com",
    "paula.ruiz@email.com",
    "javier.hernandez@email.com"
]

#Invoice details
description = "Servicio mensual de mantenimiento web"
amount = 300.00
status = "Paid"

# Insert one invoice per user
inserted = 0
for email in emails:
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
        cursor.execute("""
            INSERT INTO invoices (user_id, description, amount, status)
            VALUES (?, ?, ?, ?)
        """, (user_id, description, amount, status))
        if cursor.rowcount == 1:
            inserted += 1

#Save and close
conn.commit()
conn.close()

print(f"{inserted} invoices inserted successfully.")

