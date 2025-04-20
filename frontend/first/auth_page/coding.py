import tkinter as tk
from tkinter import filedialog, image_names
from PIL import Image, ImageTk
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        img = Image.open("C:\\Users\\DELL\\OneDrive\\Desktop\\Facial_recognition\\frontend\\first\\auth_page\\image.png")
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_names.config(image=img_tk)
        image_names.image = img_tk

def enter_dataset():
    print("Dataset upload clicked!")
root = tk.Tk()
root.title("Face++ Identity Verification UI")
root.geometry("1600x1000")
root.configure(bg="#0d0c2b")  # Dark background

# --- Navigation Bar ---

nav_frame = tk.Frame(root, bg="#000000")
nav_frame.pack(fill="x")

# Left nav buttons
left_nav_frame = tk.Frame(nav_frame, bg="#000000")
left_nav_frame.pack(side="left")

nav_buttons = ["Technologies", "Solutions", "Pricing", "Resources", "Support"]
for btn in nav_buttons:
    tk.Button(left_nav_frame, text=btn, bg="#000000", fg="blue", bd=0, font=("Arial", 10)).pack(side="left", padx=15, pady=10)

# Right nav (Dataset + Sign Up/Register)
right_nav_frame = tk.Frame(nav_frame, bg="#000000")
right_nav_frame.pack(side="right", padx=15)

# Enter Dataset Button
dataset_btn = tk.Button(
    right_nav_frame, text="Enter Your Dataset",
    bg="#ffffff", fg="#0d0c2b",
    font=("Arial", 10, "bold"), padx=10, pady=2,
    relief="flat", cursor="hand2", command=enter_dataset
)
dataset_btn.pack(side="right", padx=10, pady=5)

# Sign Up/Register Button
sign_up_btn = tk.Button(
    right_nav_frame, text="Sign Up/Register",
    bg="#5561ff", fg="blue",
    font=("Arial", 12, "bold"), padx=10, pady=2,
    relief="flat", cursor="hand2"
)
sign_up_btn.pack(side="right", pady=5)

# --- Main Banner (split into left and right frames) ---

banner_frame = tk.Frame(root, bg="#0d0c2b", pady=40)
banner_frame.pack(fill="x", padx=40)

# LEFT SIDE (Text)
text_frame = tk.Frame(banner_frame, bg="#0d0c2b")
text_frame.pack(side="left", anchor="n")

tk.Label(
    text_frame, text="Neighbourly",
    fg="white", bg="#0d0c2b",
    font=("Arial", 40, "bold"), justify="left"
).pack(anchor="w", pady=(0, 10))

tk.Label(
    text_frame, text="FaceID Identity\nVerification Solution",
    fg="white", bg="#0d0c2b",
    font=("Arial", 24, "bold"), justify="left"
).pack(anchor="w")

tk.Label(
    text_frame, text="Leading face-based authentication service\nRobust technique, high accuracy, fraud detection",
    fg="lightgray", bg="#0d0c2b", font=("Arial", 22), justify="left"
).pack(anchor="w", pady=(10, 20))

# RIGHT SIDE (Static Image)
image_frame = tk.Frame(banner_frame, bg="#0d0c2b")
image_frame.pack(side="right", padx=20)

# Load your uploaded image (update the path)
static_image = Image.open("frontend/first/auth_page/image.png")  # Make sure the path is correct
static_image = static_image.resize((500, 350))
static_image_tk = ImageTk.PhotoImage(static_image)

static_label = tk.Label(image_frame, image=static_image_tk, bg="#0d0c2b")
static_label.image = static_image_tk
static_label.pack()

# --- Technologies Section ---

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

tk.Label(
    tech_frame,
    text=about_text,
    font=("Arial", 16),
    fg="gray",
    bg="white",
    justify="left",
    wraplength=800
).pack(padx=40)

# --- Run App ---
root.mainloop()