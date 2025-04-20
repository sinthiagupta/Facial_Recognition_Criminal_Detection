import tkinter as tk
from tkinter import Canvas, Label, Button, Toplevel
import cv2
import os
import sqlite3
import pandas as pd
import torch
from PIL import Image, ImageTk
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import cosine
import numpy as np
import time

# ------------------- Initialization -------------------
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Paths
image_save_dir = "scanned_faces"
embedding_save_path = "backend/user_embeddings/user_embedding.csv"
criminal_embedding_path = "backend/embeddings/face_embeddings.csv"
db_path = "backend/user_face_database.db"
os.makedirs(image_save_dir, exist_ok=True)
os.makedirs(os.path.dirname(embedding_save_path), exist_ok=True)

# Threshold
THRESHOLD = 0.4

# ------------------- Access Result Page -------------------
def show_access_result(scanned_image_path, user_embedding):
    result_window = Toplevel()
    result_window.title("Access Result")
    result_window.geometry("500x550")
    result_window.configure(bg="#020d26")

    Label(result_window, text="NEIGHBOURLY", font=("Arial", 30, "bold"), bg="#020d26", fg="white").pack(pady=(30, 10))

    # Image Preview
    img = Image.open(scanned_image_path).resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)
    image_preview = Label(result_window, image=img_tk, bg="#020d26")
    image_preview.image = img_tk
    image_preview.pack(pady=10)

    container = tk.Frame(result_window, bg="#020d26")
    container.pack()

    access_granted = Button(container, text="ACCESS GRANTED", font=("Helvetica", 12, "bold"),
                            bg="white", fg="limegreen", width=20, state="disabled")
    access_granted.pack(pady=10)

    access_denied = Button(container, text="ACCESS DENIED", font=("Helvetica", 12, "bold"),
                           bg="white", fg="red", width=20, state="disabled")
    access_denied.pack(pady=10)

    # Match logic
    if not os.path.exists(criminal_embedding_path):
        return

    df = pd.read_csv(criminal_embedding_path)
    criminal_embeddings = df.iloc[:, 1:].values
    criminal_names = df.iloc[:, 0].values

    for idx, criminal_emb in enumerate(criminal_embeddings):
        dist = cosine(user_embedding, criminal_emb)
        if dist < THRESHOLD:
            matched_name = criminal_names[idx]
            access_granted.config(state="disabled", bg="white", fg="green")
            access_denied.config(state="normal", bg="red", fg="white")
            tk.Label(result_window, text=f"Matched Criminal: {matched_name}", fg="red", bg="#020d26", font=("Arial", 12)).pack()
            return

    # If no match
    access_granted.config(state="normal", bg="green", fg="white")
    access_denied.config(state="disabled", bg="white", fg="red")
    tk.Label(result_window, text="No criminal match found. Access Granted ✅", fg="limegreen", bg="#020d26", font=("Arial", 12)).pack()

# ------------------- Face Scan Logic -------------------
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
            user_id = f"user_{int(time.time())}"
            image_path = os.path.join(image_save_dir, f"{user_id}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"✅ Image saved: {image_path}")

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            face = mtcnn(img_pil)

            if face is not None:
                embedding = resnet(face.unsqueeze(0)).detach().numpy().flatten()
                show_access_result(image_path, embedding)
            else:
                print("⚠ No face detected in image.")

            break

        elif key == ord('q'):
            print("🔴 Quit without scanning.")
            break

    cap.release()
    cv2.destroyAllWindows()

# ------------------- GUI -------------------
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
