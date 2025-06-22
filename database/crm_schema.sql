-- Table to store users
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Unique user ID
    first_name TEXT NOT NULL,                      -- First name of the user
    last_name TEXT NOT NULL,                       --Last name of the user
    email TEXT NOT NULL UNIQUE,                    --Email address (must be unique)
    phone INTEGER,                                    --Optional phone number
    address TEXT,                                  -- Optional address
    registration_date TEXT NOT NULL DEFAULT (datetime('now')) --Registration date (YYYY-MM-DD)
);

--Table to store invoices
CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,              --Unique invoice ID
    user_id INTEGER NOT NULL,                          --Foreign key to users table
    issue_date TEXT NOT NULL DEFAULT (datetime('now')), --Date and time of the invoice
    description TEXT NOT NULL,                         -- Description of product/service
    amount REAL NOT NULL,                              -- Invoice amount
    status TEXT NOT NULL,                              --Status (Pending, Paid, Cancelled)
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
