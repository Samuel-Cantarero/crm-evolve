#Import necessary libraries
import sqlite3

# Connect to the database 
try:
    conn = sqlite3.connect('database/database_crm.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# List of users to insert 
sample_users = [
    ('Lucía', 'Martínez López', 'lucia.martinez@email.com', '612345678', 'Calle Olmo 12'),
    ('Hugo', 'García Pérez', 'hugo.garcia@email.com', '611112223', 'Av. Andalucía 45'),
    ('Martina', 'Sánchez Ruiz', 'martina.sanchez@email.com', '600334455', 'Calle Real 89'),
    ('Pablo', 'Díaz Martín', 'pablo.diaz@email.com', '655443322', 'Plaza Mayor 3'),
    ('Sofía', 'Romero Torres', 'sofia.romero@email.com', '622778899', 'Calle Larga 101'),
    ('Daniel', 'Fernández Gómez', 'daniel.fernandez@email.com', '688990011', 'Camino Alto 77'),
    ('Valeria', 'Moreno Navarro', 'valeria.moreno@email.com', '699887766', 'Callejón del Sol 8'),
    ('Alejandro', 'Jiménez Ramos', 'alejandro.jimenez@email.com', '677221133', 'Av. de la Vega 23'),
    ('Paula', 'Ruiz Molina', 'paula.ruiz@email.com', '644556677', 'Ronda Norte 5'),
    ('Javier', 'Hernández Castro', 'javier.hernandez@email.com', '666999888', 'Calle Jardines 33'),
]

#Insert each user using INSERT OR IGNORE
inserted = 0
for user in sample_users:
    cursor.execute("""
        INSERT OR IGNORE INTO users (first_name, last_name, email, phone, address)
        VALUES (?, ?, ?, ?, ?)
    """, user)
    if cursor.rowcount == 1:
        inserted += 1

#Save and close
conn.commit()
conn.close()

print(f"{inserted} users inserted successfully.")
