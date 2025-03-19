import os
from PIL import Image

# Input and output folder paths
input_folder = "backend/dataset"  # Original images folder
output_folder = "backend/processed_dataset"  # Where cleaned images will be saved

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define target image size
TARGET_SIZE = (160, 160)

def preprocess_images():
    """Scans the dataset folder, cleans, resizes, and saves images."""
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("❌ No images found in dataset folder.")
        return
    
    print(f"🔍 Found {len(image_files)} images. Processing...")

    for img_name in image_files:
        img_path = os.path.join(input_folder, img_name)
        try:
            # Open image and convert to RGB
            img = Image.open(img_path).convert("RGB")
            # Resize image
            img_resized = img.resize(TARGET_SIZE)
            # Save processed image
            output_path = os.path.join(output_folder, img_name)
            img_resized.save(output_path, format="PNG")

            print(f"✅ Processed: {img_name} -> {output_path}")
        
        except Exception as e:
            print(f"⚠️ Error processing {img_name}: {e}")

if __name__ == "__main__":
    preprocess_images()
