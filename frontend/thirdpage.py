import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox
from PIL import Image, ImageTk
import os
import torch
import sqlite3
import numpy as np
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import cosine

# Initialize models
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# File paths
criminal_embedding_path = "backend/embeddings/face_embeddings.csv"

# Threshold
THRESHOLD = 0.4

# Setup window
root = tk.Tk()
root.title("Access Page")
root.geometry("500x550")
root.configure(bg="#020d26")

# Header
header = Label(root, text="NEIGHBOURLY", font=("Arial", 30, "bold"), bg="#020d26", fg="white")
header.pack(pady=(30, 10))

# Image preview
image_preview = Label(root, bg="#020d26")
image_preview.pack(pady=10)

# Frame container
container = tk.Frame(root, bg="#020d26")
container.pack()

# Access result buttons
access_granted = Button(container, text="ACCESS GRANTED", font=("Helvetica", 12, "bold"),
                        bg="white", fg="limegreen", width=20, state="disabled")
access_granted.pack(pady=10)

access_denied = Button(container, text="ACCESS DENIED", font=("Helvetica", 12, "bold"),
                       bg="white", fg="red", width=20, state="disabled")
access_denied.pack(pady=10)

# Process uploaded image
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        return

    # Preview
    img = Image.open(file_path).resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)
    image_preview.config(image=img_tk)
    image_preview.image = img_tk

    # Extract embedding from image
    image = Image.open(file_path).convert('RGB')
    face = mtcnn(image)
    if face is None:
        messagebox.showerror("Error", "No face detected in the uploaded image.")
        return

    with torch.no_grad():
        embedding = resnet(face.unsqueeze(0)).numpy().flatten()

    # Load criminal embeddings
    if not os.path.exists(criminal_embedding_path):
        messagebox.showerror("Error", "Criminal embeddings file not found.")
        return

    df = pd.read_csv(criminal_embedding_path)
    criminal_embeddings = df.iloc[:, 1:].values
    criminal_names = df.iloc[:, 0].values

    # Compare against each criminal
    for idx, criminal_emb in enumerate(criminal_embeddings):
        dist = cosine(embedding, criminal_emb)
        if dist < THRESHOLD:
            matched_name = criminal_names[idx]
            access_granted.config(state="normal", bg="green", fg="white")
            access_denied.config(state="disabled", bg="white", fg="red")
            messagebox.showinfo("Match Found", f"Access Denied: Matched criminal {matched_name}\nSimilarity: {1 - dist:.2f}")
            return

    # No match found
    access_denied.config(state="normal", bg="red", fg="white")
    access_granted.config(state="disabled", bg="white", fg="green")
    messagebox.showinfo("Access Granted", "No criminal match found. Access Granted ✅")

# Upload button
upload_button = Button(container, text="UPLOAD IMAGE", font=("Helvetica", 12, "bold"),
                       bg="white", fg="black", width=20, command=upload_image)
upload_button.pack(pady=10)

# Start GUI
root.mainloop()
