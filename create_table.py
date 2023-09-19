import sqlite3

def connect_db():
    # Create or connect to the SQLite database file
    conn = sqlite3.connect("arqdb.db")

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create a table for user data
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,  
        wallet REAL DEFAULT 200.0,  -- Default wallet balance of 200
        coinvalue REAL,
        connections TEXT     
    )''')
    # Create a table for transactions
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database created successfully.")