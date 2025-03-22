import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("backend/user_face_database.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        embedding TEXT
    )
''')
conn.commit()

def save_user_embedding(username):
    """ Saves user embedding into database for future matching. """
    try:
        df = pd.read_csv("backend/user_embeddings/user_embedding.csv")
        embedding_str = ",".join(map(str, df.iloc[0].tolist()))

        cursor.execute("INSERT INTO user_embeddings (username, embedding) VALUES (?, ?)", 
                       (username, embedding_str))
        conn.commit()
        print("✅ User embedding stored successfully!")

    except Exception as e:
        print(f"⚠️ Error storing embedding: {e}")

# Example Usage:
save_user_embedding("john_doe")
