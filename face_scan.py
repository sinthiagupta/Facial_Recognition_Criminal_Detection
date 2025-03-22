import cv2
import torch
import numpy as np
import os
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# Load FaceNet model
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
model = InceptionResnetV1(pretrained='vggface2').eval()

# Ensure embedding storage directory exists
embedding_folder = "backend/user_embeddings"
os.makedirs(embedding_folder, exist_ok=True)

# Capture video from the webcam
cap = cv2.VideoCapture(0)
print("📷 Press 's' to scan face | Press 'q' to quit")

def generate_embedding(img_rgb):
    """Generate face embedding from the captured image"""
    try:
        face = mtcnn(Image.fromarray(img_rgb))
        if face is None:
            print("❌ No face detected! Try again.")
            return None
        face = face.unsqueeze(0)
        with torch.no_grad():
            embedding = model(face)
        return embedding.numpy().flatten()
    except Exception as e:
        print(f"⚠️ Error generating embedding: {e}")
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture image. Exiting...")
        break

    # Show camera feed
    cv2.imshow("Face Scanner", frame)

    # Wait for keypress
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):  # Press 's' to scan face
        print("✅ Face captured!")
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        embedding = generate_embedding(img_rgb)

        if embedding is not None:
            user_id = input("Enter a valid User ID: ").strip()  # Ensure valid input
            if not user_id.isalnum():
                print("❌ Invalid User ID. Please enter only letters and numbers.")
                continue

            save_path = os.path.join(embedding_folder, f"{user_id}.csv")
            df = pd.DataFrame([embedding])
            df.to_csv(save_path, index=False)
            print(f"✅ Face embedding saved for {user_id} at {save_path}")

        break  # Exit after scanning

    elif key == ord('q'):  # Press 'q' to quit
        print("🚪 Exiting scanner...")
        break

# Release resources and close camera window
cap.release()
cv2.destroyAllWindows()
