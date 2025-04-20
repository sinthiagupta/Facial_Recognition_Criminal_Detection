import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import webbrowser
import os
import shutil

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        img = Image.open("frontend/first/auth_page/image.png")
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

def enter_dataset():
    response = messagebox.askquestion("Upload Dataset", "Do you want to upload a new dataset folder or file?")
    
    if response != "yes":
        return

    # Ask the user to select folder or file
    choice = messagebox.askquestion("Select Type", "Do you want to upload a folder?\nClick 'No' to upload a file.")
    
    if choice == "yes":
        source_path = filedialog.askdirectory(title="Select Dataset Folder")
    else:
        source_path = filedialog.askopenfilename(title="Select Dataset File (e.g. zip)")

    if not source_path:
        return

    target_path = "backend/dataset"

    # Delete old dataset completely
    if os.path.exists(target_path):
        try:
            shutil.rmtree(target_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete old dataset: {e}")
            return

    try:
        # If it's a folder
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)
        else:
            # If it's a zip file
            os.makedirs(target_path, exist_ok=True)
            if source_path.endswith(".zip"):
                with zipfile.ZipFile(source_path, 'r') as zip_ref:
                    zip_ref.extractall(target_path)
            else:
                shutil.copy2(source_path, target_path)

        messagebox.showinfo("Success", f"✅ Dataset uploaded successfully to {target_path}")

    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to copy dataset: {e}")
        return

    # Augmentation
    try:
        subprocess.run([sys.executable, "augmentation.py"], check=True)
        messagebox.showinfo("Augmentation", "✅ Data augmentation completed.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Augmentation Error", f"❌ Augmentation failed: {e}")

    # Embedding
    try:
        subprocess.run([sys.executable, "embedding.py"], check=True)
        messagebox.showinfo("Embedding", "✅ Embedding completed.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Embedding Error", f"❌ Embedding failed: {e}")


def open_signup_window():
    signup_window = tk.Toplevel()
    signup_window.title("Register New User")
    signup_window.geometry("400x500")
    signup_window.configure(bg="#0d0c2b")

    tk.Label(signup_window, text="Register", font=("Arial", 20, "bold"), bg="#0d0c2b", fg="white").pack(pady=20)

    tk.Label(signup_window, text="Full Name", bg="#0d0c2b", fg="white").pack()
    name_entry = ttk.Entry(signup_window, width=40)
    name_entry.pack(pady=5)

    tk.Label(signup_window, text="Email", bg="#0d0c2b", fg="white").pack()
    email_entry = ttk.Entry(signup_window, width=40)
    email_entry.pack(pady=5)

    tk.Label(signup_window, text="Password", bg="#0d0c2b", fg="white").pack()
    password_entry = ttk.Entry(signup_window, width=40, show="*")
    password_entry.pack(pady=5)

    def submit_signup():
        name = name_entry.get()
        email = email_entry.get()
        pwd = password_entry.get()
        if name and email and pwd:
            messagebox.showinfo("Success", f"✅ Registered {name} successfully!")
            signup_window.destroy()
            subprocess.Popen([sys.executable, "C:/Users/DELL/OneDrive/Desktop/Facial_recognition/frontend/secondpage.py", email])
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
        user_id = email_entry.get().strip()
        if user_id:
            login_window.destroy()
            subprocess.Popen([sys.executable, "C:/Users/DELL/OneDrive/Desktop/Facial_recognition/frontend/secondpage.py", user_id])
        else:
            messagebox.showerror("Error", "Please enter your email or phone")

    def on_google_signin():
        webbrowser.open("https://accounts.google.com/signin")

    tk.Button(login_window, text="Sign In", bg='#5561ff', fg='black', font=("Arial", 12, "bold"),
              width=30, pady=5, relief="flat", cursor="hand2", command=on_sign_in).pack(pady=15)

    tk.Button(login_window, text="Or sign in with Google", bg='black', fg='white', font=("Arial", 12),
              width=30, pady=5, relief="flat", cursor="hand2", command=on_google_signin).pack(pady=10)

    sign_up_frame = tk.Frame(login_window, bg='#0d0c2b')
    sign_up_frame.pack(pady=20)
    tk.Label(sign_up_frame, text="Don't have an account?", bg='#0d0c2b', fg='lightgray').pack(side=tk.LEFT)

    sign_up_link = tk.Label(sign_up_frame, text="Sign up now", fg='skyblue', bg='#0d0c2b', cursor="hand2")
    sign_up_link.pack(side=tk.RIGHT)
    sign_up_link.bind("<Button-1>", lambda e: open_signup_window())

# --- Main UI ---

root = tk.Tk()
root.title("Face++ Identity Verification UI")
root.geometry("1600x1000")
root.configure(bg="#0d0c2b")

nav_frame = tk.Frame(root, bg="#000000")
nav_frame.pack(fill="x")

left_nav_frame = tk.Frame(nav_frame, bg="#000000")
left_nav_frame.pack(side="left")

for btn in ["Technologies", "Solutions", "Pricing", "Resources", "Support"]:
    tk.Button(left_nav_frame, text=btn, bg="#000000", fg="blue", bd=0, font=("Arial", 10)).pack(side="left", padx=15, pady=10)

right_nav_frame = tk.Frame(nav_frame, bg="#000000")
right_nav_frame.pack(side="right", padx=15)

tk.Button(right_nav_frame, text="Enter Your Dataset", bg="#ffffff", fg="#0d0c2b",
          font=("Arial", 10, "bold"), padx=10, pady=2, relief="flat", cursor="hand2",
          command=enter_dataset).pack(side="right", padx=10, pady=5)

tk.Button(right_nav_frame, text="Sign Up/Register", bg="#5561ff", fg="blue",
          font=("Arial", 12, "bold"), padx=10, pady=2, relief="flat", cursor="hand2",
          command=open_login_window).pack(side="right", pady=5)

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
    static_image = Image.open("frontend/first/auth_page/image.png")
    static_image = static_image.resize((500, 350))
    static_image_tk = ImageTk.PhotoImage(static_image)
except:
    static_image_tk = None

image_label = tk.Label(image_frame, image=static_image_tk, bg="#0d0c2b")
image_label.image = static_image_tk
image_label.pack()

tech_frame = tk.Frame(root, bg="white", pady=20)
tech_frame.pack(fill="both", expand=True)

tk.Label(tech_frame, text="About Us", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

about_text = (
    "Neighbourly is a cutting-edge identity verification platform that leverages "
    "advanced face recognition and artificial intelligence to ensure secure and "
    "seamless user authentication. Our mission is to provide robust, scalable, "
    "and user-friendly technology solutions that help businesses and users build "
    "trust in digital interactions.\n\n\n"
    "With high accuracy and fraud detection capabilities, Neighbourly empowers "
    "organizations to verify identities effortlessly and prevent unauthorized access."
)

tk.Label(tech_frame, text=about_text, font=("Arial", 16), fg="gray", bg="white", justify="left", wraplength=800).pack(padx=40)
root.mainloop()