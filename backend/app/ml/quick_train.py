"""
Quick Training Script - Simplified version for rapid testing
Use this for testing with smaller datasets or quick iterations.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20
LEARNING_RATE = 1e-4
NUM_CLASSES = 5
CLASS_NAMES = ['Melanoma', 'Nevus', 'BCC', 'AK', 'Benign']

def load_quick_dataset(data_dir):
    """Quick dataset loader."""
    images, labels = [], []
    data_path = Path(data_dir)
    
    print("Loading dataset...")
    for class_idx, class_name in enumerate(CLASS_NAMES):
        class_dir = data_path / class_name
        if not class_dir.exists():
            continue
        
        for img_file in list(class_dir.glob('*.jpg'))[:100]:  # Limit for quick training
            try:
                img = keras.preprocessing.image.load_img(
                    img_file, target_size=IMG_SIZE
                )
                img_array = keras.preprocessing.image.img_to_array(img) / 255.0
                images.append(img_array)
                labels.append(class_idx)
            except:
                continue
    
    images = np.array(images)
    labels = keras.utils.to_categorical(np.array(labels), NUM_CLASSES)
    
    print(f"Loaded {len(images)} images")
    return images, labels

def build_quick_model():
    """Build a quick transfer learning model."""
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=(*IMG_SIZE, 3)
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer=Adam(LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    data_dir = os.getenv('DATA_DIR', 'data/skin_disease_dataset')
    
    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} not found!")
        return
    
    # Load data
    images, labels = load_quick_dataset(data_dir)
    
    if len(images) == 0:
        print("No images found!")
        return
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.2, random_state=42, stratify=np.argmax(labels, axis=1)
    )
    
    # Build and train
    model = build_quick_model()
    model.summary()
    
    print("\nStarting training...")
    model.fit(
        X_train, y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=1)
    print(f"\nTest Accuracy: {test_acc:.4f}")
    
    # Save
    model.save('model.h5')
    print("Model saved to model.h5")

if __name__ == "__main__":
    main()
