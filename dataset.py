import os
import shutil

def upload_dataset():
    """User inputs the dataset folder path, and it gets copied to the server."""
    dataset_path = input("📂 Enter the path to the new criminal dataset folder: ")

    if not os.path.exists(dataset_path):
        print("❌ Invalid folder path. Try again.")
        return

    target_path = "backend/dataset"
    
    # Delete previous dataset if exists
    if os.path.exists(target_path):
        shutil.rmtree(target_path)  

    shutil.copytree(dataset_path, target_path)  # Copy new dataset

    print(f"✅ New dataset uploaded successfully to {target_path}")

upload_dataset()
