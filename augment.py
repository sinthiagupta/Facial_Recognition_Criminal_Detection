from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import os
import random

# Paths
input_folder = "backend/dataset"
output_folder = "backend/augmented_dataset"
os.makedirs(output_folder, exist_ok=True)

TARGET_SIZE = (160, 160)

def simulate_side_and_partial_faces(img):
    """Simulates partial face views and side face crops."""
    w, h = img.size

    transforms = [
        lambda x: x.crop((0, 0, w // 2, h)).resize((w, h)),  # Left side only
        lambda x: x.crop((w // 2, 0, w, h)).resize((w, h)),  # Right side only
        lambda x: x.rotate(random.choice([-45, 45])),        # Side rotation
        lambda x: x.crop((int(w * 0.1), int(h * 0.1), int(w * 0.9), int(h * 0.9))).resize((w, h)),  # Zoom-in center
        lambda x: x.crop((0, 0, w, int(h * 0.5))).resize((w, h)),  # Top half
        lambda x: x.crop((0, int(h * 0.5), w, h)).resize((w, h)),  # Bottom half
    ]

    return [t(img.copy()) for t in transforms]

def basic_augmentations(img):
    """Applies brightness, contrast, blur, noise, flip etc."""
    augmentations = []

    enhancer = ImageEnhance.Brightness(img)
    augmentations.append(enhancer.enhance(0.5))  # Dark
    augmentations.append(enhancer.enhance(1.5))  # Bright

    contrast = ImageEnhance.Contrast(img)
    augmentations.append(contrast.enhance(0.5))
    augmentations.append(contrast.enhance(2.0))

    augmentations.append(img.transpose(Image.FLIP_LEFT_RIGHT))  # Mirror flip
    augmentations.append(img.filter(ImageFilter.GaussianBlur(radius=2)))  # Blur

    return augmentations

def augment_images():
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Found {len(image_files)} images. Starting augmentation...")

    for img_name in image_files:
        img_path = os.path.join(input_folder, img_name)
        try:
            img = Image.open(img_path).convert("RGB").resize(TARGET_SIZE)
            all_augmented = simulate_side_and_partial_faces(img) + basic_augmentations(img)

            for idx, aug_img in enumerate(all_augmented):
                save_name = f"{os.path.splitext(img_name)[0]}_aug_{idx}.png"
                save_path = os.path.join(output_folder, save_name)
                aug_img.save(save_path)
            print(f"✅ Augmented {img_name} with {len(all_augmented)} variants.")

        except Exception as e:
            print(f"⚠️ Error processing {img_name}: {e}")

augment_images()