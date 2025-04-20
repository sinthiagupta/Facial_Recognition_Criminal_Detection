import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def on_google_sign_in():
    print("Google Sign-In Clicked")

def on_sign_in():
    print("Sign-In Clicked")

def on_sign_up():
    print("Sign-Up Clicked")

def on_forgot_password():
    print("Forgot Password Clicked")

root = tk.Tk()
root.title("Neighbourly Login")
root.geometry("500x600")
root.configure(bg='#0d0c2b')  # Dark theme background

# --- Logo Section ---
logo_frame = tk.Frame(root, bg='#0d0c2b')
logo_frame.pack(pady=20)

logo_label = tk.Label(logo_frame, text="\U0001F464", font=("Arial", 50), bg='#0d0c2b', fg='white')
logo_label.pack()

title_label = tk.Label(logo_frame, text="NEIGHBOURLY", font=("Arial", 22, "bold"), bg='#0d0c2b', fg='white')
title_label.pack()

# --- Welcome Message ---
welcome_label = tk.Label(root, text="Nice to see you again", font=("Arial", 16, "bold"), bg='#0d0c2b', fg='lightgray')
welcome_label.pack(pady=10)

# --- Email Entry ---
email_entry = ttk.Entry(root, width=40, font=("Arial", 12))
email_entry.insert(0, "Email or phone number")
email_entry.pack(pady=20)

# --- Password Entry ---
password_frame = tk.Frame(root, bg='#0d0c2b')

password_frame.pack(pady=5)

password_entry = ttk.Entry( password_frame, width=33, font=("Arial", 12), show="*")
password_entry.pack(side=tk.LEFT)

eyeball = tk.Label(password_frame, text="\U0001F441", font=("Arial", 14), bg='#0d0c2b', fg='white', cursor="hand2")
eyeball.pack(side=tk.RIGHT, padx=5)

def toggle_password():
    if password_entry['show'] == "*":
        password_entry['show'] = ""
    else:
        password_entry['show'] = "*"
eyeball.bind("<Button-1>", lambda event: toggle_password())

# --- Options Section (Remember Me & Forgot) ---
options_frame = tk.Frame(root, bg='#0d0c2b')
options_frame.pack(pady=5)

remember_me = tk.Checkbutton(options_frame, text="Remember me", bg='#0d0c2b', fg='white', selectcolor='#0d0c2b', activebackground='#0d0c2b', activeforeground='white')
remember_me.pack(side=tk.LEFT)

forgot_password = tk.Label(options_frame, text="Forgot password?", fg='skyblue', bg='#0d0c2b', cursor="hand2")
forgot_password.pack(side=tk.RIGHT)
forgot_password.bind("<Button-1>", lambda event: on_forgot_password())

# --- Sign-In Button ---
sign_in_button = tk.Button(
    root, text="Sign In", bg='#5561ff', fg='black',
    font=("Arial", 12, "bold"), width=30, pady=5,
    relief="flat", cursor="hand2", activebackground="#4047d0"
)
sign_in_button.pack(pady=15)
sign_in_button.config(command=on_sign_in)

# --- Google Sign-In Button ---
google_button = tk.Button(
    root, text="Or sign in with Google", bg='black', fg='black',
    font=("Arial", 12), width=30, pady=5,
    relief="flat", cursor="hand2", activebackground="#333333"
)
google_button.pack(pady=10)
google_button.config(command=on_google_sign_in)

# --- Sign-Up Option ---
sign_up_frame = tk.Frame(root, bg='#0d0c2b')
sign_up_frame.pack(pady=20)

sign_up_label = tk.Label(sign_up_frame, text="Don't have an account?", bg='#0d0c2b', fg='lightgray')
sign_up_label.pack(side=tk.LEFT)

sign_up_link = tk.Label(sign_up_frame, text="Sign up now", fg='skyblue', bg='#0d0c2b', cursor="hand2")
sign_up_link.pack(side=tk.RIGHT)
sign_up_link.bind("<Button-1>", lambda event: on_sign_up())

root.mainloop()