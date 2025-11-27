from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path
import numpy as np
from PIL import Image
import io
import tensorflow as tf

# Import our model and preprocessor
# We need to make sure src is in path if running from root
import sys
sys.path.append(str(Path(__file__).parent))
from model import EcoSortModel
from preprocessing import ImagePreprocessor
from train import main as train_pipeline

app = FastAPI(title="EcoSort API", description="Waste Classification API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config
MODEL_PATH = Path("models/ecosort_model.h5")
DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploads"
TRAIN_DIR = DATA_DIR / "train"

# Global model instance
model_instance = None

def load_model_instance():
    global model_instance
    if MODEL_PATH.exists():
        print(f"Loading model from {MODEL_PATH}")
        model_instance = EcoSortModel()
        model_instance.load(MODEL_PATH)
    else:
        print("Model not found. Please train the model first.")
        model_instance = None

@app.on_event("startup")
async def startup_event():
    load_model_instance()
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to EcoSort API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model_instance is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess
        if image.mode != "RGB":
            image = image.convert("RGB")
        image = image.resize((224, 224))
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        prediction = model_instance.predict(img_array)
        score = float(prediction[0][0])
        
        # Classify (Binary: 0=Organic, 1=Recyclable - assuming alphabetical order of folders if using flow_from_directory default)
        # Wait, flow_from_directory sorts alphabetically. 
        # Organic, Recyclable -> Organic=0, Recyclable=1
        
        label = "Recyclable" if score > 0.5 else "Organic"
        confidence = score if score > 0.5 else 1 - score
        
        return {
            "filename": file.filename,
            "label": label,
            "confidence": float(confidence),
            "raw_score": score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_data(files: list[UploadFile] = File(...), category: str = "Recyclable"):
    """
    Upload images for retraining.
    category: 'Organic' or 'Recyclable'
    """
    if category not in ["Organic", "Recyclable"]:
        raise HTTPException(status_code=400, detail="Invalid category. Must be 'Organic' or 'Recyclable'")
    
    target_dir = TRAIN_DIR / category
    target_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for file in files:
        file_path = target_dir / f"upload_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(str(file_path))
        
    return {"message": f"Uploaded {len(saved_files)} files to {category}", "files": saved_files}

def run_retraining():
    print("Starting retraining task...")
    try:
        train_pipeline()
        # Reload model
        load_model_instance()
        print("Retraining complete and model reloaded.")
    except Exception as e:
        print(f"Retraining failed: {e}")

@app.post("/retrain")
async def retrain(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_retraining)
    return {"message": "Retraining started in background"}
