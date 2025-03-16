import cv2
import os

# Step 1: Take user input for original dataset path
original_dataset = input("Enter the path to your original dataset: ").strip()

# Step 2: Set default processed dataset path
default_processed_path = os.path.join(os.path.dirname(original_dataset), "processed_dataset")

# Step 3: Ask user for processed dataset path
processed_dataset = input(f"Enter the path to save processed images (Press Enter for default: {default_processed_path}): ").strip()
if processed_dataset == "":
    processed_dataset = default_processed_path

# Step 4: Create processed folder if not exists
os.makedirs(processed_dataset, exist_ok=True)

# Step 5: Process images
for img_name in os.listdir(original_dataset):
    img_path = os.path.join(original_dataset, img_name)
    
    # Read image
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"❌ Error reading {img_name}, skipping...")
        continue
    
    # Resize (Example: 224x224)
    img = cv2.resize(img, (224, 224))

    # Save processed image
    save_path = os.path.join(processed_dataset, img_name)
    cv2.imwrite(save_path, img)

    print(f"✅ Processed & Saved: {save_path}")

print("\n🎉 **Processing Complete!** 🎉")
print(f"Processed images saved in: {processed_dataset}")

# Step 6: Take input for further processing
user_path = input("\nEnter the path to your processed dataset for embedding: ").strip()

# Step 7: Validate the input path
if os.path.exists(user_path):
    print(f"✅ Valid path! Proceeding with {user_path} for embeddings...")
else:
    print(f"❌ Invalid path! Please check and run the script again.")
