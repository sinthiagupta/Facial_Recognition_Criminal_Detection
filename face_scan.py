import cv2
import torch
import pandas as pd
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import os

# Initialize face detector and embedding model
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Paths
image_save_dir = "scanned_faces"
embedding_save_path = "backend/user_embeddings/user_embedding.csv"

# Ensure directories exist
os.makedirs(image_save_dir, exist_ok=True)
os.makedirs(os.path.dirname(embedding_save_path), exist_ok=True)

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Press 's' to scan | 'q' to quit", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Press 's' to capture
        user_id = input("Enter user ID: ").strip()
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
            
            # Convert to dataframe
            df_new = pd.DataFrame([[image_path] + embedding.tolist()])
            df_new.columns = ["image_name"] + [f"dim_{i}" for i in range(len(embedding))]

            # Append to CSV
            if not os.path.exists(embedding_save_path):
                df_new.to_csv(embedding_save_path, index=False)
            else:
                df_new.to_csv(embedding_save_path, mode='a', header=False, index=False)

            print("✅ Embedding saved in:", embedding_save_path)
        else:
            print("⚠ No face detected!")

    elif key == ord('q'):  # Quit
        break

# Release camera
cap.release()
cv2.destroyAllWindows()
