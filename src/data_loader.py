import os
import shutil
from pathlib import Path
import subprocess
import sys

# Ensure required packages are installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from datasets import load_dataset
except ImportError:
    print("Installing datasets library...")
    install("datasets")
    from datasets import load_dataset

from PIL import Image
from tqdm import tqdm

# Configuration
DATASET_ID = "rootstrap-org/waste-classifier"
DATA_DIR = Path("data")
TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"

# Class Mapping
# Organic: compost, trash
# Recyclable: cardboard, glass, metal, paper, plastic
CLASS_MAPPING = {
    "compost": "Organic",
    "trash": "Organic",
    "cardboard": "Recyclable",
    "glass": "Recyclable",
    "metal": "Recyclable",
    "paper": "Recyclable",
    "plastic": "Recyclable"
}

def setup_directories():
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    
    for category in ["Organic", "Recyclable"]:
        (TRAIN_DIR / category).mkdir(parents=True, exist_ok=True)
        (TEST_DIR / category).mkdir(parents=True, exist_ok=True)

def save_image(image, label_name, split):
    target_category = CLASS_MAPPING.get(label_name)
    if not target_category:
        return # Skip unknown classes if any

    # Determine directory
    directory = TRAIN_DIR if split == "train" else TEST_DIR
    
    # Generate filename
    filename = f"{label_name}_{image.filename if hasattr(image, 'filename') else 'img'}_{os.urandom(4).hex()}.jpg"
    save_path = directory / target_category / filename
    
    # Save
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(save_path)

def main():
    print(f"Downloading dataset: {DATASET_ID}...")
    
    # Load dataset
    # Using 'train' split for everything first, then we can split manually or use provided splits if available
    # This dataset might just have 'train'
    dataset = load_dataset(DATASET_ID, split="train")
    
    print(f"Dataset loaded. Total examples: {len(dataset)}")
    print("Processing images...")

    setup_directories()

    # Simple 80/20 split
    train_count = int(len(dataset) * 0.8)
    
    for i, item in tqdm(enumerate(dataset), total=len(dataset)):
        image = item['image']
        label = item['label'] # This is likely an integer
        
        # Get label name
        # features['label'].int2str(label)
        label_name = dataset.features['label'].int2str(label)
        
        split = "train" if i < train_count else "test"
        
        save_image(image, label_name, split)

    print("Data download and processing complete!")
    print(f"Train data: {TRAIN_DIR}")
    print(f"Test data: {TEST_DIR}")

if __name__ == "__main__":
    main()
