import sqlite3
import bcrypt

# Connect to SQLite database
conn = sqlite3.connect("backend/user_database.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

def register_user(username, password):
    """ Registers a new user with encrypted password. """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("✅ Registration successful!")
    except sqlite3.IntegrityError:
        print("❌ Username already exists!")

def login_user(username, password):
    """ Authenticates a user by matching password. """
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = cursor.fetchone()

    if stored_password and bcrypt.checkpw(password.encode(), stored_password[0]):
        print("✅ Login successful! Proceed to face scan.")
        return True
    else:
        print("❌ Invalid username or password.")
        return False
