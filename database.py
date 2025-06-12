import sqlite3

DB_FILE = "expense_tracker.db"

def connect_db():
    return sqlite3.connect(DB_FILE)

def create_tables():
    """Create transactions and budget tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        description TEXT,
        category TEXT,
        type TEXT,
        payment_method TEXT,
        date TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
        category TEXT PRIMARY KEY,
        amount REAL
    )''')

    conn.commit()
    conn.close()

# --- TRANSACTION FUNCTIONS ---
def add_transaction(amount, description, category, txn_type, payment_method, txn_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (amount, description, category, type, payment_method, date) VALUES (?, ?, ?, ?, ?, ?)", 
                   (amount, description, category, txn_type, payment_method, txn_date))
    conn.commit()
    conn.close()

def get_transactions():
    """Retrieve all transactions."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def edit_transaction(transaction_id, amount, description, category, txn_type, payment_method, txn_date):
    """Edit an existing transaction."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET amount=?, description=?, category=?, type=?, payment_method=?, date=?
        WHERE id=?
    """, (amount, description, category, txn_type, payment_method, txn_date, transaction_id))
    conn.commit()
    conn.close()

def delete_transaction(transaction_id):
    """Delete a transaction by ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()

# --- BUDGET FUNCTIONS ---
def set_budget(category, budget_amount):
    """Set or update budget for a category."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO budgets (category, amount) VALUES (?, ?) ON CONFLICT(category) DO UPDATE SET amount=?", 
                   (category, budget_amount, budget_amount))
    conn.commit()
    conn.close()

def get_budgets():
    """Retrieve all budgets."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budgets")
    budgets = cursor.fetchall()
    conn.close()
    return budgets

def reset_data():
    """Reset all stored transactions and budgets."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM budgets")
    conn.commit()
    conn.close()
