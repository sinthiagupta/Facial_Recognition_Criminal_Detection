import tkinter as tk
from tkinter import Canvas, Label, Button
import cv2
import os
import sqlite3
import pandas as pd
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import cosine
import numpy as np
import sys
user_id = sys.argv[1] if len(sys.argv) > 1 else "default_user"
print(f"🔐 User: {user_id}")


# ------------------- Initialization -------------------
# Face recognition model
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Paths
image_save_dir = "scanned_faces"
embedding_save_path = "backend/user_embeddings/user_embedding.csv"
criminal_embedding_path = "backend/embeddings/face_embeddings.csv"
db_path = "backend/user_face_database.db"
os.makedirs(image_save_dir, exist_ok=True)
os.makedirs(os.path.dirname(embedding_save_path), exist_ok=True)

# ------------------- Helper Functions -------------------
def save_user_embedding_to_db(username, embedding):
    """ Saves user embedding into database """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            embedding TEXT
        )
    ''')
    embedding_str = ",".join(map(str, embedding))
    cursor.execute("INSERT OR REPLACE INTO user_embeddings (username, embedding) VALUES (?, ?)",
                   (username, embedding_str))
    conn.commit()
    conn.close()

def save_user_embedding_to_csv(image_path, embedding):
    """ Saves the user embedding into CSV """
    embedding_data = [image_path] + list(embedding)
    df_new = pd.DataFrame([embedding_data])
    df_new.columns = ["image_name"] + [f"dim_{i}" for i in range(len(embedding))]

    if not os.path.exists(embedding_save_path):
        df_new.to_csv(embedding_save_path, index=False)
    else:
        df_new.to_csv(embedding_save_path, mode='a', header=False, index=False)

def match_with_criminal_database(user_image_path, user_embedding):
    """ Compare the scanned embedding with the criminal database """
    if not os.path.exists(criminal_embedding_path):
        print("❌ Criminal embedding file not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS face_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_image TEXT,
            matched_criminal TEXT,
            distance REAL
        )
    ''')
    conn.commit()

    criminal_df = pd.read_csv(criminal_embedding_path)
    criminal_embeddings = criminal_df.iloc[:, 1:].to_numpy(dtype=np.float64)

    threshold = 0.4
    match_found = False

    for idx, criminal_embedding in enumerate(criminal_embeddings):
        dist = cosine(user_embedding, criminal_embedding)
        criminal_name = criminal_df.iloc[idx, 0]
        print(f"🔍 Compared with {criminal_name} | Distance: {dist:.4f}")

        if dist < threshold:
            print(f"🚨 Match found: {criminal_name}")
            cursor.execute(
                "INSERT INTO face_matches (user_image, matched_criminal, distance) VALUES (?, ?, ?)",
                (user_image_path, criminal_name, dist)
            )
            conn.commit()
            match_found = True
            break

    if not match_found:
        print("❌ No match found.")
    conn.close()

# ------------------- GUI Scan Action -------------------
import uuid
import time

def scan_face():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    print("📷 Press 's' to scan | 'q' to quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        cv2.imshow("Press 's' to scan | 'q' to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            print("🟢 's' key pressed – capturing image...")

            # Automatically generate a user ID using timestamp or UUID
            user_id = f"user_{int(time.time())}"  # or use: uuid.uuid4().hex[:8]

            image_path = f"{image_save_dir}/{user_id}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"✅ Image saved: {image_path}")

            # Convert to RGB and process
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            face = mtcnn(img_pil)

            if face is not None:
                print("🧠 Face detected – generating embedding...")
                embedding = resnet(face.unsqueeze(0)).detach().numpy().flatten()

                save_user_embedding_to_csv(image_path, embedding)
                save_user_embedding_to_db(user_id, embedding)
                match_with_criminal_database(image_path, embedding)
            else:
                print("⚠ No face detected in image. Please try again.")

            break

        elif key == ord('q'):
            print("🔴 Quit without scanning.")
            break

    cap.release()
    cv2.destroyAllWindows()


# ------------------- GUI Design -------------------
root = tk.Tk()
root.title("Neighbourly - Scan Page")
root.geometry("900x800")
root.configure(bg="#0B1120")

Label(root, text="NEIGHBOURLY", font=("Arial", 40, "bold"), bg="#0B1120", fg="white").pack(pady=(30, 10))
Label(root, text="SCAN HERE", font=("Arial", 24, "bold"), bg="#0B1120", fg="white").pack(pady=10)

canvas = Canvas(root, width=500, height=500, bg="#0B1120", highlightthickness=3, highlightbackground="#1E90FF")
canvas.pack(pady=10)
canvas.create_line(0, 0, 30, 0, fill="#1E90FF", width=3)
canvas.create_line(0, 0, 0, 30, fill="#1E90FF", width=3)
canvas.create_line(500, 0, 470, 0, fill="#1E90FF", width=3)
canvas.create_line(500, 0, 500, 30, fill="#1E90FF", width=3)
canvas.create_line(0, 500, 0, 470, fill="#1E90FF", width=3)
canvas.create_line(0, 500, 30, 500, fill="#1E90FF", width=3)
canvas.create_line(500, 500, 470, 500, fill="#1E90FF", width=3)
canvas.create_line(500, 500, 500, 470, fill="#1E90FF", width=3)

Button(root, text="CLICK TO SCAN", font=("Arial", 12, "bold"),
       bg="#1E90FF", fg="white", padx=20, pady=10, command=scan_face).pack(pady=20)

Label(root, text="Face should fit in frame properly\nFirst move left then move right",
      font=("Arial", 10), bg="#0B1120", fg="white", justify="center").pack(pady=10)

root.mainloop()
