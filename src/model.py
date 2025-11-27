import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
import os

class EcoSortModel:
    def __init__(self, input_shape=(224, 224, 3), num_classes=1, learning_rate=0.0001):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.model = self._build_model()

    def _build_model(self):
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=self.input_shape)
        
        # Freeze base model layers
        base_model.trainable = False
        
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.5)(x)
        
        # Binary classification (sigmoid) or Multi-class (softmax)
        activation = 'sigmoid' if self.num_classes == 1 else 'softmax'
        predictions = Dense(self.num_classes, activation=activation)(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        loss = 'binary_crossentropy' if self.num_classes == 1 else 'categorical_crossentropy'
        
        model.compile(optimizer=Adam(learning_rate=self.learning_rate),
                      loss=loss,
                      metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
        return model

    def train(self, train_generator, validation_generator, epochs=10, callbacks=None):
        return self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=callbacks
        )

    def evaluate(self, test_generator):
        return self.model.evaluate(test_generator)

    def save(self, filepath):
        self.model.save(filepath)

    def load(self, filepath):
        self.model = load_model(filepath)
        
    def predict(self, image_array):
        return self.model.predict(image_array)
