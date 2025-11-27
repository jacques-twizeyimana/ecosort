# EcoSort: Intelligent Waste Classification

EcoSort is an end-to-end Machine Learning application that classifies waste items as **Organic** or **Recyclable**. It features a trained MobileNetV2 model, a FastAPI backend, and a modern React frontend.

## Features

- **Real-time Prediction**: Upload an image to classify it.
- **Retraining Pipeline**: Upload new data and trigger model retraining.
- **Dashboard**: Visualize model metrics (Accuracy, Loss) and system status.
- **Load Testing**: Locust configuration included for stress testing.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+

### 1. Backend Setup

```bash
cd EcoSort
pip install -r requirements.txt
python3 src/train.py  # Train the initial model
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd EcoSort/frontend
npm install
npm run dev
```

Access the UI at `http://localhost:5173`.

### 3. Load Testing

```bash
cd EcoSort
locust -f locustfile.py
```

Access Locust at `http://localhost:8089`.

## Project Structure

- `notebook/`: Jupyter Notebooks (`EcoSort_Project.ipynb`).
- `src/`: Python source code (Model, API, Preprocessing).
- `frontend/`: React application.
- `data/`: Dataset directory.
- `models/`: Saved model artifacts.

## Demo Video

[Link to YouTube Demo] (To be added)
