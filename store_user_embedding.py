import sqlite3
import pandas as pd
import cv2
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import os

# Initialize face detector and embedding model
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Paths
image_save_dir = "scanned_faces"
embedding_save_path = "backend/user_embeddings/user_embedding.csv"
db_path = "backend/user_face_database.db"  # SQLite DB file

# Ensure directories exist
os.makedirs(image_save_dir, exist_ok=True)
os.makedirs(os.path.dirname(embedding_save_path), exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect(db_path)
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

# Function to save user embedding into SQLite database
def save_user_embedding_to_db(username, embedding):
    """ Saves user embedding into database for future matching. """
    try:
        # Convert embedding to string (comma-separated)
        embedding_str = ",".join(map(str, embedding))
        
        cursor.execute("INSERT INTO user_embeddings (username, embedding) VALUES (?, ?)", 
                       (username, embedding_str))
        conn.commit()
        print("✅ User embedding stored successfully in database!")
    except Exception as e:
        print(f"⚠️ Error storing embedding in database: {e}")

# Function to save user embedding to CSV
def save_user_embedding_to_csv(image_path, embedding):
    """ Appends the user's embedding to the CSV file. """
    try:
        # Convert embedding to dataframe
        embedding_data = [image_path] + list(embedding)
        df_new = pd.DataFrame([embedding_data])
        df_new.columns = ["image_name"] + [f"dim_{i}" for i in range(len(embedding))]

        # Append to CSV
        if not os.path.exists(embedding_save_path):
            df_new.to_csv(embedding_save_path, index=False)
        else:
            df_new.to_csv(embedding_save_path, mode='a', header=False, index=False)

        print("✅ Embedding saved to CSV:", embedding_save_path)
    except Exception as e:
        print(f"⚠️ Error saving embedding to CSV: {e}")

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Press 's' to scan | 'q' to quit", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Press 's' to capture
        user_id = input("Enter user ID: ").strip()  # Prompt for user ID
        image_path = f"{image_save_dir}/{user_id}.jpg"
        
        # Save the image
        cv2.imwrite(image_path, frame)
        print(f"✅ Image saved: {image_path}")
        
        # Convert to RGB and process embedding
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        face = mtcnn(img_pil)

        if face is not None:
            embedding = resnet(face.unsqueeze(0)).detach().numpy().flatten()
            
            # Save the embedding to CSV and Database
            save_user_embedding_to_csv(image_path, embedding)
            save_user_embedding_to_db(user_id, embedding)
        else:
            print("⚠ No face detected!")
    
    elif key == ord('q'):  # Quit
        break

# Release camera
cap.release()
cv2.destroyAllWindows()

# Close database connection
conn.close()
