import os
from preprocessing import ImagePreprocessor
from model import EcoSortModel
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Config
DATA_DIR = Path("data")
TRAIN_DIR = DATA_DIR / "train"
TEST_DIR = DATA_DIR / "test"
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "ecosort_model.h5"
BATCH_SIZE = 32
EPOCHS = 10

def plot_history(history, save_path="history.png"):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    epochs_range = range(len(acc))
    
    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.savefig(save_path)
    print(f"Training history saved to {save_path}")

def main():
    # Ensure model dir exists
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Initializing Preprocessor...")
    preprocessor = ImagePreprocessor(batch_size=BATCH_SIZE)
    
    print("Loading Data Generators...")
    train_gen = preprocessor.create_train_generator(TRAIN_DIR)
    val_gen = preprocessor.create_validation_generator(TRAIN_DIR)
    test_gen = preprocessor.create_test_generator(TEST_DIR)
    
    print("Building Model...")
    # Binary classification: Organic vs Recyclable
    model = EcoSortModel(num_classes=1) 
    
    print("Starting Training...")
    history = model.train(train_gen, val_gen, epochs=EPOCHS)
    
    print("Evaluating Model...")
    results = model.evaluate(test_gen)
    print(f"Test Loss: {results[0]}")
    print(f"Test Accuracy: {results[1]}")
    
    print(f"Saving Model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    
    plot_history(history)
    
    # Save metrics to CSV for dashboard
    metrics = pd.DataFrame(history.history)
    metrics.to_csv(MODEL_DIR / "training_metrics.csv", index=False)

if __name__ == "__main__":
    main()
