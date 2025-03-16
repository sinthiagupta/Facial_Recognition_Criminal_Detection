import os
import torch
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np

# Load pre-trained FaceNet model
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)  # Keep only one face per image
model = InceptionResnetV1(pretrained='vggface2').eval()

def get_face_embedding(img_path):
    """ Extract face embeddings from an image. """
    try:
        img = Image.open(img_path).convert('RGB')
        face = mtcnn(img)
        
        if face is None:
            print(f"❌ No face detected in: {img_path}")
            return None

        face = face.unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            embedding = model(face)
        
        return embedding.numpy().flatten()  # Convert to 1D array

    except Exception as e:
        print(f"⚠️ Error processing {img_path}: {e}")
        return None

def process_dataset(folder_path, save_path="face_embeddings.csv"):
    """ Process all images in a folder and save embeddings to CSV. """
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    embeddings = []
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        embedding = get_face_embedding(img_path)

        if embedding is not None:
            embeddings.append([img_file] + embedding.tolist())

    if embeddings:
        df = pd.DataFrame(embeddings)
        df.to_csv(save_path, index=False)
        print(f"\n✅ Embeddings saved to {save_path}")
    else:
        print("\n❌ No valid embeddings found.")

# Ask user for dataset path
dataset_path = input("Enter the path to the dataset folder: ")
if os.path.exists(dataset_path):
    process_dataset(dataset_path)
else:
    print("❌ Invalid folder path. Please check and try again.")
