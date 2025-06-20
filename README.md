# CRM System with SQLite

A simple CRM (Customer Relationship Management) system using Python and SQLite.  
It allows user registration, invoice management, and financial reporting from the command line.

## Features

- Register and manage users (name, email, phone, etc.).
- Create and manage invoices per user.
- View all users and their invoices.
- Generate financial summaries.

## Usage

1. Clone the repository.
2. Install Python >=3.8.
3. Run the database schema in `/database/crm_schema.sql` to create the tables (this is usually done automatically).
4. Execute the main program in `/src/main.py`.

## Structure

```
project-root/
│
├── database/
│   ├── crm_schema.sql
│   └── database_crm.db
│
├── src/
│   └── main.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

## License

MIT License.
