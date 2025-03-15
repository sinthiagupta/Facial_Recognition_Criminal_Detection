from deepface import DeepFace
import os

# Ask user to input dataset path
dataset_path = input("Enter the dataset folder path: ").strip()

# Function to process all images in the dataset
def recognize_faces(dataset_path):
    if not os.path.exists(dataset_path):
        print("\n❌ Error: Dataset path does not exist.\n")
        return

    image_files = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    if not image_files:
        print("\n⚠ No images found in the dataset folder.\n")
        return

    print(f"\n✅ Found {len(image_files)} images in '{dataset_path}'. Processing...\n")

    for idx, filename in enumerate(image_files, 1):
        image_path = os.path.join(dataset_path, filename)
        print(f"\n🖼 Processing {idx}/{len(image_files)}: {filename}")
        analyze_face(image_path)

# Function to analyze face using DeepFace
def analyze_face(image_path):
    try:
        result = DeepFace.analyze(image_path, actions=['age', 'gender', 'race', 'emotion'])
        
        # Extract useful data
        age = result[0]['age']
        gender = result[0]['dominant_gender']
        race = result[0]['dominant_race']
        emotion = result[0]['dominant_emotion']

        # Display formatted output
        print("\n🔍 **Analysis Result:**")
        print(f"   📌 Age: {age}")
        print(f"   📌 Gender: {gender}")
        print(f"   📌 Race: {race}")
        print(f"   📌 Emotion: {emotion}")
        print("-" * 40)

    except Exception as e:
        print(f"\n❌ Error analyzing {image_path}: {e}")

# Run face recognition on user-provided dataset
recognize_faces(dataset_path)
