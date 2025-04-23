import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Canvas, Toplevel, Label, Button
from PIL import Image, ImageTk
import subprocess
import sys
import webbrowser
import os
import shutil
import cv2
import pandas as pd
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import cosine
import time
import numpy as np

# -------------- FaceNet Initialization --------------
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

image_save_dir = "scanned_faces"
embedding_save_path = "backend/user_embeddings/user_embedding.csv"
criminal_embedding_path = "backend/embeddings/face_embeddings.csv"
os.makedirs(image_save_dir, exist_ok=True)
os.makedirs(os.path.dirname(embedding_save_path), exist_ok=True)

THRESHOLD = 0.4

def show_access_result(scanned_image_path, user_embedding):
    result_window = Toplevel()
    result_window.title("Access Result")
    result_window.geometry("500x550")
    result_window.configure(bg="#020d26")

    Label(result_window, text="NEIGHBOURLY", font=("Arial", 30, "bold"), bg="#020d26", fg="white").pack(pady=(30, 10))

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

    access_granted.config(state="normal", bg="green", fg="white")
    access_denied.config(state="disabled", bg="white", fg="red")
    tk.Label(result_window, text="No criminal match found. Access Granted ✅", fg="limegreen", bg="#020d26", font=("Arial", 12)).pack()

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

# ---------------- Info Page Popup -------------------
def open_info_page(title, content):
    page = Toplevel()
    page.title(title)
    page.geometry("900x600")
    page.configure(bg="#0d0c2b")

    Label(page, text=title, font=("Arial", 28, "bold"), bg="#0d0c2b", fg="white").pack(pady=20)
    Label(page, text=content, wraplength=800, justify="left", font=("Arial", 14),
          bg="#0d0c2b", fg="lightgray").pack(padx=30, pady=10)

root = tk.Tk()
root.title("Face++ Identity Verification UI")
root.geometry("1600x1000")
root.configure(bg="#0d0c2b")

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        img = Image.open("frontend/first/auth_page/image.png")
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        
def enter_dataset():
    # Ensure the backend dataset folder exists
    dataset_folder = os.path.join(os.getcwd(), 'backend', 'dataset')
    os.makedirs(dataset_folder, exist_ok=True)

    # Ask whether the user wants to upload a folder or a single image
    user_choice = messagebox.askquestion("Upload Type", "Do you want to upload a folder of images? Click 'No' to select a single image.")

    if user_choice == 'yes':  # Folder upload
        folder_path = filedialog.askdirectory()
        if folder_path:
            try:
                image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
                image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]

                if not image_files:
                    messagebox.showwarning("No Images Found", "No image files found in the selected folder.")
                    return

                for image_name in image_files:
                    src_path = os.path.join(folder_path, image_name)
                    dest_path = os.path.join(dataset_folder, image_name)
                    shutil.copy(src_path, dest_path)

                messagebox.showinfo("Upload Success", f"{len(image_files)} image(s) uploaded to backend/dataset.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload images. Error: {e}")
        else:
            messagebox.showwarning("No Folder Selected", "No folder was selected.")

    else:  # Single file upload
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])
        if file_path:
            try:
                image_name = os.path.basename(file_path)
                dest_path = os.path.join(dataset_folder, image_name)
                shutil.copy(file_path, dest_path)

                messagebox.showinfo("Upload Success", f"Image uploaded to backend/dataset:\n{image_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload image. Error: {e}")
        else:
            messagebox.showwarning("No File Selected", "No image file was selected.")

def open_signup_window():
    signup_window = tk.Toplevel()
    signup_window.title("Register New User")
    signup_window.geometry("400x500")
    signup_window.configure(bg="#0d0c2b")

    tk.Label(signup_window, text="Register", font=("Arial", 20, "bold"), bg="#0d0c2b", fg="white").pack(pady=20)
    name_entry = ttk.Entry(signup_window, width=40)
    email_entry = ttk.Entry(signup_window, width=40)
    password_entry = ttk.Entry(signup_window, width=40, show="*")

    for label, entry in [("Full Name", name_entry), ("Email", email_entry), ("Password", password_entry)]:
        tk.Label(signup_window, text=label, bg="#0d0c2b", fg="white").pack()
        entry.pack(pady=5)

    def submit_signup():
        name = name_entry.get()
        email = email_entry.get()
        pwd = password_entry.get()
        if name and email and pwd:
            messagebox.showinfo("Success", f"✅ Registered {name} successfully!")
            signup_window.destroy()
            scan_face()
        else:
            messagebox.showwarning("Incomplete", "Please fill all fields.")

    tk.Button(signup_window, text="Register", bg="#5561ff", fg="white", font=("Arial", 12, "bold"),
              command=submit_signup).pack(pady=20)

def open_login_window():
    login_window = tk.Toplevel()
    login_window.title("Neighbourly Login")
    login_window.geometry("500x600")
    login_window.configure(bg='#0d0c2b')

    logo_frame = tk.Frame(login_window, bg='#0d0c2b')
    logo_frame.pack(pady=20)
    tk.Label(logo_frame, text="\U0001F464", font=("Arial", 50), bg='#0d0c2b', fg='white').pack()
    tk.Label(logo_frame, text="NEIGHBOURLY", font=("Arial", 22, "bold"), bg='#0d0c2b', fg='white').pack()

    tk.Label(login_window, text="Nice to see you again", font=("Arial", 16, "bold"), bg='#0d0c2b', fg='lightgray').pack(pady=10)

    email_entry = ttk.Entry(login_window, width=40, font=("Arial", 12))
    email_entry.insert(0, "Email or phone number")
    email_entry.pack(pady=20)

    password_frame = tk.Frame(login_window, bg='#0d0c2b')
    password_frame.pack(pady=5)

    password_entry = ttk.Entry(password_frame, width=33, font=("Arial", 12), show="*")
    password_entry.pack(side=tk.LEFT)

    eyeball = tk.Label(password_frame, text="\U0001F441", font=("Arial", 14), bg='#0d0c2b', fg='white', cursor="hand2")
    eyeball.pack(side=tk.RIGHT, padx=5)

    def toggle_password():
        password_entry['show'] = "" if password_entry['show'] == "*" else "*"

    eyeball.bind("<Button-1>", lambda e: toggle_password())

    options_frame = tk.Frame(login_window, bg='#0d0c2b')
    options_frame.pack(pady=5)

    tk.Checkbutton(options_frame, text="Remember me", bg='#0d0c2b', fg='white',
                   selectcolor='#0d0c2b', activebackground='#0d0c2b').pack(side=tk.LEFT)

    forgot = tk.Label(options_frame, text="Forgot password?", fg='skyblue', bg='#0d0c2b', cursor="hand2")
    forgot.pack(side=tk.RIGHT)
    forgot.bind("<Button-1>", lambda e: print("Forgot Password Clicked"))
    
    def on_sign_in():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        if not email or not password:
            messagebox.showwarning("Input Required", "Please enter both email and password.")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return
        login_window.destroy()
        scan_face()



    tk.Button(login_window, text="Sign In", bg='#5561ff', fg='black', font=("Arial", 12, "bold"),
              width=30, pady=5, relief="flat", command=on_sign_in).pack(pady=15)

    tk.Button(login_window, text="Or sign in with Google", bg='black', fg='white', font=("Arial", 12),
              width=30, pady=5, relief="flat", command=lambda: webbrowser.open("https://accounts.google.com/signin")).pack(pady=10)

    tk.Label(login_window, text="Don't have an account?", bg='#0d0c2b', fg='gray').pack()
    tk.Button(login_window, text="Sign Up", command=open_signup_window,
              bg="black", fg="skyblue", relief="flat").pack()


# NAVIGATION BAR
nav_frame = tk.Frame(root, bg="#000000")
nav_frame.pack(fill="x")
left_nav_frame = tk.Frame(nav_frame, bg="#000000")
left_nav_frame.pack(side="left")
def open_info_page(title, content):
    page = tk.Toplevel()
    page.title(title)
    page.geometry("900x600")
    page.configure(bg="#0d0c2b")

    tk.Label(page, text=title, font=("Arial", 28, "bold"), bg="#0d0c2b", fg="white").pack(pady=20)

    tk.Label(page, text=content, wraplength=800, justify="left", font=("Arial", 14),
             bg="#0d0c2b", fg="lightgray").pack(padx=30, pady=10)

nav_buttons = {
    "Technologies": "Neighbourly uses cutting-edge models like FaceNet (MTCNN + InceptionResnetV1) for embedding and face detection...",
    "Solutions": "Our system provides real-time criminal detection, identity verification, database embedding comparison, and UI-driven authentication process...",
    "Pricing": "Currently available for academic/demo use. Enterprise features & pricing coming soon...",
    "Resources": "Built with: Python, Tkinter, OpenCV, facenet-pytorch, Pinecone (for vector DB), and Figma for UI/UX design...",
    "Support": "Have questions?\nContact us at:\nsinthiagupta@gmail.com"
}

for btn, content in nav_buttons.items():
    tk.Button(left_nav_frame, text=btn, bg="#000000", fg="blue", bd=0, font=("Arial", 10),
              command=lambda b=btn, c=content: open_info_page(b, c)).pack(side="left", padx=15, pady=10)


right_nav_frame = tk.Frame(nav_frame, bg="#000000")
right_nav_frame.pack(side="right", padx=15)
tk.Button(right_nav_frame, text="Enter Your Dataset", bg="#ffffff", fg="#0d0c2b",
          font=("Arial", 10, "bold"), command=enter_dataset).pack(side="right", padx=10, pady=5)
tk.Button(right_nav_frame, text="Sign Up/Register", bg="#5561ff", fg="blue",
          font=("Arial", 12, "bold"), command=open_login_window).pack(side="right", pady=5)


# --- Banner ---
banner_frame = tk.Frame(root, bg="#0d0c2b", pady=40)
banner_frame.pack(fill="x", padx=40)

text_frame = tk.Frame(banner_frame, bg="#0d0c2b")
text_frame.pack(side="left", anchor="n")

tk.Label(text_frame, text="Neighbourly", fg="white", bg="#0d0c2b", font=("Arial", 40, "bold")).pack(anchor="w", pady=(0, 10))
tk.Label(text_frame, text="FaceID Identity\nVerification Solution", fg="white", bg="#0d0c2b", font=("Arial", 24, "bold")).pack(anchor="w")
tk.Label(text_frame, text="Leading face-based authentication service\nRobust technique, high accuracy, fraud detection",
         fg="lightgray", bg="#0d0c2b", font=("Arial", 22), justify="left").pack(anchor="w", pady=(10, 20))

image_frame = tk.Frame(banner_frame, bg="#0d0c2b")
image_frame.pack(side="right", padx=20)

try:
    static_image = Image.open("frontend/first/auth_page/image.png").resize((500, 350))
    static_image_tk = ImageTk.PhotoImage(static_image)
except:
    static_image_tk = None

image_label = tk.Label(image_frame, image=static_image_tk, bg="#0d0c2b")
image_label.image = static_image_tk
image_label.pack()

tech_frame = tk.Frame(root, bg="white", pady=20)
tech_frame.pack(fill="both", expand=True)

tk.Label(tech_frame, text="About Us", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

tk.Label(tech_frame, text=(
    "Neighbourly is a cutting-edge identity verification platform that leverages "
    "advanced face recognition and artificial intelligence to ensure secure and "
    "seamless user authentication. Our mission is to provide robust, scalable, "
    "and user-friendly technology solutions that help businesses and users build "
    "trust in digital interactions.\n\n\n"
    "With high accuracy and fraud detection capabilities, Neighbourly empowers "
    "organizations to verify identities effortlessly and prevent unauthorized access."
), font=("Arial", 16), fg="gray", bg="white", justify="left", wraplength=800).pack(padx=40)

root.mainloop()
