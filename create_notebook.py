import json
import os

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EcoSort: Waste Classification Project\n",
    "\n",
    "## Objective\n",
    "Demonstrate an end-to-end Machine Learning process for classifying waste as Organic or Recyclable.\n",
    "\n",
    "## Steps\n",
    "1. Data Acquisition & Preprocessing\n",
    "2. Model Creation (MobileNetV2)\n",
    "3. Model Training\n",
    "4. Evaluation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import tensorflow as tf\n",
    "from tensorflow.keras.preprocessing.image import ImageDataGenerator\n",
    "from tensorflow.keras.applications import MobileNetV2\n",
    "from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout\n",
    "from tensorflow.keras.models import Model\n",
    "from tensorflow.keras.optimizers import Adam\n",
    "import matplotlib.pyplot as plt\n",
    "import pandas as pd\n",
    "from pathlib import Path"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Data Preprocessing\n",
    "We use `ImageDataGenerator` for augmentation and rescaling."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "BATCH_SIZE = 32\n",
    "TARGET_SIZE = (224, 224)\n",
    "DATA_DIR = Path(\"data\")\n",
    "TRAIN_DIR = DATA_DIR / \"train\"\n",
    "TEST_DIR = DATA_DIR / \"test\"\n",
    "\n",
    "train_datagen = ImageDataGenerator(\n",
    "    rescale=1./255,\n",
    "    rotation_range=20,\n",
    "    width_shift_range=0.2,\n",
    "    height_shift_range=0.2,\n",
    "    horizontal_flip=True,\n",
    "    validation_split=0.2\n",
    ")\n",
    "\n",
    "test_datagen = ImageDataGenerator(rescale=1./255)\n",
    "\n",
    "train_generator = train_datagen.flow_from_directory(\n",
    "    TRAIN_DIR,\n",
    "    target_size=TARGET_SIZE,\n",
    "    batch_size=BATCH_SIZE,\n",
    "    class_mode='binary',\n",
    "    subset='training'\n",
    ")\n",
    "\n",
    "validation_generator = train_datagen.flow_from_directory(\n",
    "    TRAIN_DIR,\n",
    "    target_size=TARGET_SIZE,\n",
    "    batch_size=BATCH_SIZE,\n",
    "    class_mode='binary',\n",
    "    subset='validation'\n",
    ")\n",
    "\n",
    "test_generator = test_datagen.flow_from_directory(\n",
    "    TEST_DIR,\n",
    "    target_size=TARGET_SIZE,\n",
    "    batch_size=BATCH_SIZE,\n",
    "    class_mode='binary',\n",
    "    shuffle=False\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Model Creation\n",
    "We use MobileNetV2 with transfer learning."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))\n",
    "base_model.trainable = False\n",
    "\n",
    "x = base_model.output\n",
    "x = GlobalAveragePooling2D()(x)\n",
    "x = Dense(128, activation='relu')(x)\n",
    "x = Dropout(0.5)(x)\n",
    "predictions = Dense(1, activation='sigmoid')(x)\n",
    "\n",
    "model = Model(inputs=base_model.input, outputs=predictions)\n",
    "\n",
    "model.compile(optimizer=Adam(learning_rate=0.0001),\n",
    "              loss='binary_crossentropy',\n",
    "              metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])\n",
    "\n",
    "model.summary()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Training"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "history = model.fit(\n",
    "    train_generator,\n",
    "    epochs=10,\n",
    "    validation_data=validation_generator\n",
    ")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Evaluation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "results = model.evaluate(test_generator)\n",
    "print(f\"Test Loss: {results[0]}\")\n",
    "print(f\"Test Accuracy: {results[1]}\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

os.makedirs("notebook", exist_ok=True)
with open("notebook/EcoSort_Project.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=1)
