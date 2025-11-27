import zipfile
import shutil
from pathlib import Path
import os
import random

# Config
ZIP_PATH = Path("EcoSort/data/trashnet_repo/data/dataset-resized.zip")
DATA_DIR = Path("EcoSort/data")
TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"
TEMP_DIR = DATA_DIR / "temp_extract"

# Mapping
# Organic: trash (assuming general waste/organic for this demo)
# Recyclable: cardboard, glass, metal, paper, plastic
CLASS_MAPPING = {
    "trash": "Organic",
    "cardboard": "Recyclable",
    "glass": "Recyclable",
    "metal": "Recyclable",
    "paper": "Recyclable",
    "plastic": "Recyclable"
}

def setup_directories():
    if TRAIN_DIR.exists():
        shutil.rmtree(TRAIN_DIR)
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)
        
    for category in ["Organic", "Recyclable"]:
        (TRAIN_DIR / category).mkdir(parents=True, exist_ok=True)
        (TEST_DIR / category).mkdir(parents=True, exist_ok=True)

def organize_data():
    print(f"Unzipping {ZIP_PATH}...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)
    
    # The zip usually contains a folder named 'dataset-resized'
    extracted_root = TEMP_DIR / "dataset-resized"
    
    if not extracted_root.exists():
        print(f"Expected folder {extracted_root} not found. Checking contents...")
        print(list(TEMP_DIR.iterdir()))
        return

    print("Organizing data...")
    setup_directories()
    
    total_moved = 0
    
    for class_folder in extracted_root.iterdir():
        if not class_folder.is_dir():
            continue
            
        class_name = class_folder.name
        target_category = CLASS_MAPPING.get(class_name)
        
        if not target_category:
            print(f"Skipping unknown class: {class_name}")
            continue
            
        images = list(class_folder.glob("*.jpg"))
        random.shuffle(images)
        
        # 80/20 split
        split_idx = int(len(images) * 0.8)
        train_imgs = images[:split_idx]
        test_imgs = images[split_idx:]
        
        for img_path in train_imgs:
            shutil.copy(img_path, TRAIN_DIR / target_category / img_path.name)
            total_moved += 1
            
        for img_path in test_imgs:
            shutil.copy(img_path, TEST_DIR / target_category / img_path.name)
            total_moved += 1
            
    print(f"Moved {total_moved} images.")
    
    # Cleanup
    shutil.rmtree(TEMP_DIR)
    print("Cleanup complete.")

if __name__ == "__main__":
    organize_data()
