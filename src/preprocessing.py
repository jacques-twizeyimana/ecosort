import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class ImagePreprocessor:
    def __init__(self, target_size=(224, 224), batch_size=32):
        self.target_size = target_size
        self.batch_size = batch_size
        
        # Augmentation for training
        self.train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=0.2 # Use 20% for validation if loading from same dir
        )
        
        # Only rescaling for validation/test
        self.test_datagen = ImageDataGenerator(rescale=1./255)

    def create_train_generator(self, data_dir):
        return self.train_datagen.flow_from_directory(
            data_dir,
            target_size=self.target_size,
            batch_size=self.batch_size,
            class_mode='binary', # Organic vs Recyclable
            subset='training'
        )

    def create_validation_generator(self, data_dir):
        return self.train_datagen.flow_from_directory(
            data_dir,
            target_size=self.target_size,
            batch_size=self.batch_size,
            class_mode='binary',
            subset='validation'
        )
        
    def create_test_generator(self, data_dir):
        return self.test_datagen.flow_from_directory(
            data_dir,
            target_size=self.target_size,
            batch_size=self.batch_size,
            class_mode='binary',
            shuffle=False
        )
