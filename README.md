# CRM Evolve

A Python-based CRM (Customer Relationship Management) system that manages user registration, invoicing, and financial reporting using a SQLite database.

## Features

- **User Registration**: Add new users with name, email, phone, address, and registration date.
- **Invoice Management**: Create, list and summarize invoices for each user.
- **User Search**: Find users by name or email.
- **Financial Summary**: Get total invoiced, paid, and pending amounts per user.
- **Sample Data Scripts**: Easily populate the database with sample users and invoices.
- **Test Suite**: Basic tests using `pytest` to verify user and invoice functionality.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Samuel-Cantarero/crm-evolve.git
cd crm-evolve
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate       
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
crm-evolve/
├── src/
│   └── main.py                  # Main menu-based CRM interface
│   └── insert_sample_data.py    # Script to insert sample users
│   └── insert_sample_invoices.py# Script to insert sample invoices
├── database/
│   └── crm_schema.sql           # Database schema
│   └── database_crm.db          # SQLite database
├── test/
│   └── test_crm.py              # Unit tests for users and invoices
├── requirements.txt
└── README.md
```

## Running Tests

To run all tests with `pytest`:

```bash
pytest test
```

Make sure you're in the root folder (`crm-evolve/`) when running tests.

## Usage

1. First, run the main application to initialize the database:

```bash
python src/main.py
```

**Important**: You must run `main.py` at least once before using the sample data scripts.
This is because the database and its tables must be created first.

2. Then, you can populate the system with test data:

```bash
python src/insert_sample_data.py
python src/insert_sample_invoices.py
```

3. After that, you can run the application normally:

```bash
python src/main.py
```

Use the interactive menu to:
- Register new users
- Create invoices
- View user information and invoices
- Get financial summaries

## Best Practices Implemented

1. **Modular Design**: Separation of concerns across `src/`, `database/`, and `test/`.
2. **SQLite Integration**: Persistent storage with minimal setup.
3. **Error Handling**: Basic exception management for user operations.
4. **Testing**: Unit tests to validate user and invoice functionality.
5. **Script Automation**: Easy database setup and data population scripts.

---

**Author**: Antonio Samuel Cantarero Malagón
**License**: MIT 

