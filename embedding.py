import os
import pandas as pd
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np

# Load FaceNet model
mtcnn = MTCNN(image_size=160, margin=0, keep_all=False)
model = InceptionResnetV1(pretrained='vggface2').eval()

def get_face_embedding(img_path):
    """ Extract face embeddings from an image. """
    try:
        img = Image.open(img_path).convert('RGB')
        face = mtcnn(img)
        if face is None:
            print(f"❌ No face detected in: {img_path}")
            return None

        face = face.unsqueeze(0)
        with torch.no_grad():
            embedding = model(face)
        
        return embedding.numpy().flatten()

    except Exception as e:
        print(f"⚠️ Error processing {img_path}: {e}")
        return None

def process_dataset():
    """ Process ANY dataset and save embeddings dynamically. """
    dataset_path = "backend/processed_dataset"
    # Ensure the embeddings directory exists
    os.makedirs("backend/embeddings", exist_ok=True)

    save_path = "backend/embeddings/face_embeddings.csv"

    if not os.path.exists(dataset_path):
        print("❌ No dataset found. Please upload it first.")
        return

    image_files = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    embeddings = []

    for img_file in image_files:
        img_path = os.path.join(dataset_path, img_file)
        embedding = get_face_embedding(img_path)
        if embedding is not None:
            embeddings.append([img_file] + embedding.tolist())

    if embeddings:
        df = pd.DataFrame(embeddings, columns=["image_name"] + [f"dim_{i}" for i in range(len(embedding))])
        df.to_csv(save_path, index=False)
        print(len(df.iloc[0, 1:].tolist()))  # Check the embedding dimension
        print(f"✅ Embeddings saved to {save_path}")
    else:
        print("\n❌ No valid embeddings found.")

process_dataset()