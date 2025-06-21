import os
import random
import shutil

# Paths
base_dir = "train"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

# Output folders
splits = ["train", "valid", "test"]
split_ratio = {
    "train": 0.7,
    "valid": 0.2,
    "test": 0.1
}

# Gather all images
images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]
random.shuffle(images)

# Compute split counts
total = len(images)
train_count = int(split_ratio["train"] * total)
valid_count = int(split_ratio["valid"] * total)

split_images = {
    "train": images[:train_count],
    "valid": images[train_count:train_count+valid_count],
    "test": images[train_count+valid_count:]
}

# Create folders and move files
for split in splits:
    for subdir in ['images', 'labels']:
        os.makedirs(os.path.join(base_dir, split, subdir), exist_ok=True)
    
    for image in split_images[split]:
        label = os.path.splitext(image)[0] + ".txt"
        shutil.copy(os.path.join(images_dir, image), os.path.join(base_dir, split, "images", image))
        shutil.copy(os.path.join(labels_dir, label), os.path.join(base_dir, split, "labels", label))

print("Dataset successfully split!")
