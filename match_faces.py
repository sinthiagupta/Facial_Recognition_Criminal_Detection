import pandas as pd
import numpy as np
import sqlite3
from scipy.spatial.distance import cosine

# File Paths
user_embedding_path = "backend/user_embeddings/user_embedding.csv"
criminal_embedding_path = "backend/embeddings/face_embeddings.csv"
database_path = "backend/user_face_database.db"

# Connect to SQLite Database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS face_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_image TEXT,
        matched_criminal TEXT,
        distance REAL
    )
''')
conn.commit()

# Load Embeddings
user_df = pd.read_csv(user_embedding_path)
criminal_df = pd.read_csv(criminal_embedding_path)

# Convert embeddings to numpy arrays
user_embeddings = user_df.iloc[:, 1:].to_numpy(dtype=np.float64)  # All scanned users
criminal_embeddings = criminal_df.iloc[:, 1:].to_numpy(dtype=np.float64)  # All criminals

# Set similarity threshold
threshold = 0.4  # Adjust based on accuracy needs

# Iterate over all user embeddings and compare with criminal embeddings
for idx, user_embedding in enumerate(user_embeddings):
    user_image_path = user_df.iloc[idx, 0]
    match_found = False

    print(f"\n🔍 Checking User {idx+1}: {user_image_path}")

    for criminal_idx, criminal_embedding in enumerate(criminal_embeddings):
        # Ensure both vectors have the same length
        min_length = min(len(user_embedding), len(criminal_embedding))
        user_embedding = user_embedding[:min_length]
        criminal_embedding = criminal_embedding[:min_length]

        # Compute cosine similarity
        distance = cosine(user_embedding, criminal_embedding)

        print(f"🔹 Compared with Criminal {criminal_idx+1} (Distance: {distance:.4f})")

        if distance < threshold:  # If below threshold, it's a match
            matched_criminal = criminal_df.iloc[criminal_idx, 0]
            print(f"🚨 MATCH FOUND! User {user_image_path} is similar to {matched_criminal}")

            # Store result in database
            cursor.execute(
                "INSERT INTO face_matches (user_image, matched_criminal, distance) VALUES (?, ?, ?)",
                (user_image_path, matched_criminal, distance)
            )
            conn.commit()
            match_found = True
            break  # Stop checking once a match is found

    if not match_found:
        print(f"❌ No match found for User {user_image_path}.")

# Close database connection
conn.close()
