"""
Professional CNN Training Script for SkinVision AI
Deep Learning Engineer - Skin Disease Classification

This script implements a state-of-the-art CNN architecture for multi-class
skin disease classification with proper data handling, augmentation, and evaluation.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import EfficientNetB0, ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Precision, Recall
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

# Configuration
CONFIG = {
    'img_size': (224, 224),
    'batch_size': 32,
    'epochs': 100,
    'learning_rate': 1e-4,
    'num_classes': 5,
    'class_names': ['Melanoma', 'Nevus', 'BCC', 'AK', 'Benign'],
    'validation_split': 0.2,
    'test_split': 0.1,
    'data_augmentation': True,
    'use_pretrained': True,  # Use transfer learning
    'model_architecture': 'EfficientNetB0',  # Options: 'EfficientNetB0', 'ResNet50', 'CustomCNN'
    'early_stopping_patience': 15,
    'reduce_lr_patience': 5,
    'model_save_path': 'model.h5',
    'history_save_path': 'training_history.json',
    'plots_save_path': 'training_plots.png'
}


class SkinDiseaseDataset:
    """Professional dataset handler for skin disease images."""
    
    def __init__(self, data_dir: str, config: dict):
        self.data_dir = Path(data_dir)
        self.config = config
        self.class_names = config['class_names']
        self.num_classes = config['num_classes']
        
    def load_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Load images from directory structure.
        Expected structure:
        data_dir/
            Melanoma/
                img1.jpg, img2.jpg, ...
            Nevus/
                img1.jpg, img2.jpg, ...
            BCC/
                ...
            AK/
                ...
            Benign/
                ...
        """
        images = []
        labels = []
        
        print("Loading dataset...")
        for class_idx, class_name in enumerate(self.class_names):
            class_dir = self.data_dir / class_name
            if not class_dir.exists():
                print(f"Warning: Directory {class_dir} not found. Skipping class {class_name}.")
                continue
                
            image_files = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
            print(f"Found {len(image_files)} images for class: {class_name}")
            
            for img_path in image_files:
                try:
                    # Load and preprocess image
                    img = keras.preprocessing.image.load_img(
                        img_path, 
                        target_size=self.config['img_size'],
                        color_mode='rgb'
                    )
                    img_array = keras.preprocessing.image.img_to_array(img)
                    images.append(img_array)
                    labels.append(class_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
                    continue
        
        images = np.array(images, dtype=np.float32)
        labels = np.array(labels, dtype=np.int32)
        
        # Normalize images to [0, 1]
        images = images / 255.0
        
        # Convert labels to categorical (one-hot encoding)
        labels = keras.utils.to_categorical(labels, num_classes=self.num_classes)
        
        print(f"\nDataset loaded successfully!")
        print(f"Total images: {len(images)}")
        print(f"Image shape: {images.shape}")
        print(f"Labels shape: {labels.shape}")
        
        return images, labels
    
    def create_generators(self, 
                         X_train: np.ndarray, 
                         y_train: np.ndarray,
                         X_val: np.ndarray, 
                         y_val: np.ndarray) -> Tuple[ImageDataGenerator, ImageDataGenerator]:
        """Create data generators with augmentation for training."""
        
        # Training data generator with augmentation
        if self.config['data_augmentation']:
            train_datagen = ImageDataGenerator(
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,
                fill_mode='nearest',
                brightness_range=[0.8, 1.2],
                channel_shift_range=0.1
            )
        else:
            train_datagen = ImageDataGenerator()
        
        # Validation data generator (no augmentation)
        val_datagen = ImageDataGenerator()
        
        return train_datagen, val_datagen


class CNNArchitecture:
    """Professional CNN architectures for skin disease classification."""
    
    @staticmethod
    def build_custom_cnn(input_shape: Tuple[int, int, int], num_classes: int) -> models.Model:
        """
        Custom CNN architecture with modern deep learning practices.
        
        Architecture:
        - Multiple convolutional blocks with BatchNorm and Dropout
        - Progressive feature extraction
        - Global Average Pooling
        - Dense layers for classification
        """
        model = models.Sequential([
            # Input layer
            layers.Input(shape=input_shape),
            
            # Block 1: Initial feature extraction
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 2: Deeper features
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3: Advanced features
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 4: High-level features
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.5),
            
            # Global pooling and classification
            layers.GlobalAveragePooling2D(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation='softmax', name='predictions')
        ])
        
        return model
    
    @staticmethod
    def build_transfer_learning_model(base_model_name: str, 
                                      input_shape: Tuple[int, int, int], 
                                      num_classes: int,
                                      trainable_base: bool = False) -> models.Model:
        """
        Transfer learning using pre-trained models.
        
        Args:
            base_model_name: 'EfficientNetB0' or 'ResNet50'
            input_shape: Input image shape
            num_classes: Number of output classes
            trainable_base: Whether to fine-tune base model
        """
        if base_model_name == 'EfficientNetB0':
            base_model = EfficientNetB0(
                weights='imagenet',
                include_top=False,
                input_shape=input_shape
            )
        elif base_model_name == 'ResNet50':
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=input_shape
            )
        else:
            raise ValueError(f"Unknown base model: {base_model_name}")
        
        # Freeze or unfreeze base model
        base_model.trainable = trainable_base
        
        # Build complete model
        inputs = keras.Input(shape=input_shape)
        
        # Data augmentation layers (applied during training)
        x = layers.RandomRotation(0.1)(inputs)
        x = layers.RandomFlip("horizontal")(x)
        x = layers.RandomZoom(0.1)(x)
        
        # Base model
        x = base_model(x, training=False)
        
        # Global pooling
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.BatchNormalization()(x)
        
        # Classification head
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x)
        
        # Output layer
        outputs = layers.Dense(num_classes, activation='softmax', name='predictions')(x)
        
        model = models.Model(inputs, outputs)
        
        return model


class TrainingPipeline:
    """Professional training pipeline with callbacks and monitoring."""
    
    def __init__(self, config: dict):
        self.config = config
        self.history = None
        self.model = None
        
    def build_model(self, input_shape: Tuple[int, int, int], num_classes: int) -> models.Model:
        """Build the model architecture."""
        architecture = self.config['model_architecture']
        
        if architecture in ['EfficientNetB0', 'ResNet50']:
            print(f"Building {architecture} transfer learning model...")
            model = CNNArchitecture.build_transfer_learning_model(
                architecture, 
                input_shape, 
                num_classes,
                trainable_base=False  # Start with frozen base
            )
        else:
            print("Building custom CNN architecture...")
            model = CNNArchitecture.build_custom_cnn(input_shape, num_classes)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=self.config['learning_rate']),
            loss='categorical_crossentropy',
            metrics=['accuracy', Precision(name='precision'), Recall(name='recall')]
        )
        
        model.summary()
        return model
    
    def create_callbacks(self, checkpoint_dir: str = 'checkpoints') -> list:
        """Create training callbacks."""
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        callback_list = [
            # Model checkpointing
            callbacks.ModelCheckpoint(
                filepath=os.path.join(checkpoint_dir, 'best_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                save_weights_only=False,
                mode='max',
                verbose=1
            ),
            
            # Early stopping
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=self.config['early_stopping_patience'],
                restore_best_weights=True,
                verbose=1
            ),
            
            # Learning rate reduction
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=self.config['reduce_lr_patience'],
                min_lr=1e-7,
                verbose=1
            ),
            
            # CSV logger
            callbacks.CSVLogger('training_log.csv'),
            
            # TensorBoard (optional)
            # callbacks.TensorBoard(log_dir='./logs', histogram_freq=1)
        ]
        
        return callback_list
    
    def train(self, 
             model: models.Model,
             X_train: np.ndarray, 
             y_train: np.ndarray,
             X_val: np.ndarray, 
             y_val: np.ndarray,
             train_datagen: ImageDataGenerator,
             val_datagen: ImageDataGenerator) -> models.Model:
        """Train the model."""
        print("\n" + "="*50)
        print("Starting Training Pipeline")
        print("="*50)
        
        callbacks_list = self.create_callbacks()
        
        # Training
        history = model.fit(
            train_datagen.flow(X_train, y_train, batch_size=self.config['batch_size']),
            steps_per_epoch=len(X_train) // self.config['batch_size'],
            epochs=self.config['epochs'],
            validation_data=val_datagen.flow(X_val, y_val, batch_size=self.config['batch_size']),
            validation_steps=len(X_val) // self.config['batch_size'],
            callbacks=callbacks_list,
            verbose=1
        )
        
        self.history = history.history
        self.model = model
        
        return model
    
    def evaluate(self, 
                model: models.Model,
                X_test: np.ndarray, 
                y_test: np.ndarray,
                class_names: list) -> dict:
        """Comprehensive model evaluation."""
        print("\n" + "="*50)
        print("Model Evaluation")
        print("="*50)
        
        # Predictions
        y_pred = model.predict(X_test, verbose=1)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test, axis=1)
        
        # Metrics
        test_loss, test_accuracy, test_precision, test_recall = model.evaluate(
            X_test, y_test, verbose=1
        )
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(
            y_true_classes, 
            y_pred_classes, 
            target_names=class_names
        ))
        
        # Confusion matrix
        cm = confusion_matrix(y_true_classes, y_pred_classes)
        print("\nConfusion Matrix:")
        print(cm)
        
        # Per-class accuracy
        class_accuracies = {}
        for i, class_name in enumerate(class_names):
            class_mask = y_true_classes == i
            if class_mask.sum() > 0:
                class_acc = (y_pred_classes[class_mask] == i).sum() / class_mask.sum()
                class_accuracies[class_name] = class_acc
                print(f"{class_name} Accuracy: {class_acc:.4f}")
        
        results = {
            'test_loss': float(test_loss),
            'test_accuracy': float(test_accuracy),
            'test_precision': float(test_precision),
            'test_recall': float(test_recall),
            'class_accuracies': class_accuracies,
            'confusion_matrix': cm.tolist()
        }
        
        return results
    
    def plot_training_history(self, save_path: str = 'training_plots.png'):
        """Visualize training history."""
        if self.history is None:
            print("No training history available.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Accuracy
        axes[0, 0].plot(self.history['accuracy'], label='Training Accuracy')
        axes[0, 0].plot(self.history['val_accuracy'], label='Validation Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history['loss'], label='Training Loss')
        axes[0, 1].plot(self.history['val_loss'], label='Validation Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        if 'precision' in self.history:
            axes[1, 0].plot(self.history['precision'], label='Training Precision')
            axes[1, 0].plot(self.history['val_precision'], label='Validation Precision')
            axes[1, 0].set_title('Model Precision')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Precision')
            axes[1, 0].legend()
            axes[1, 0].grid(True)
        
        # Recall
        if 'recall' in self.history:
            axes[1, 1].plot(self.history['recall'], label='Training Recall')
            axes[1, 1].plot(self.history['val_recall'], label='Validation Recall')
            axes[1, 1].set_title('Model Recall')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Recall')
            axes[1, 1].legend()
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nTraining plots saved to: {save_path}")
        plt.close()


def main():
    """Main training pipeline."""
    print("="*60)
    print("SkinVision AI - CNN Training Pipeline")
    print("Deep Learning Engineer Implementation")
    print("="*60)
    
    # Initialize components
    data_dir = os.getenv('DATA_DIR', 'data/skin_disease_dataset')
    config = CONFIG.copy()
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"\nError: Data directory not found: {data_dir}")
        print("\nExpected directory structure:")
        print(f"{data_dir}/")
        print("  ├── Melanoma/")
        print("  ├── Nevus/")
        print("  ├── BCC/")
        print("  ├── AK/")
        print("  └── Benign/")
        print("\nPlease organize your dataset accordingly.")
        return
    
    # Load dataset
    dataset = SkinDiseaseDataset(data_dir, config)
    images, labels = dataset.load_data()
    
    if len(images) == 0:
        print("Error: No images loaded. Check your data directory structure.")
        return
    
    # Train/Val/Test split
    X_temp, X_test, y_temp, y_test = train_test_split(
        images, labels, 
        test_size=config['test_split'], 
        random_state=SEED,
        stratify=np.argmax(labels, axis=1)
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=config['validation_split'],
        random_state=SEED,
        stratify=np.argmax(y_temp, axis=1)
    )
    
    print(f"\nData Split:")
    print(f"  Training: {len(X_train)} samples")
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Test: {len(X_test)} samples")
    
    # Create data generators
    train_datagen, val_datagen = dataset.create_generators(
        X_train, y_train, X_val, y_val
    )
    
    # Initialize training pipeline
    pipeline = TrainingPipeline(config)
    
    # Build model
    input_shape = (*config['img_size'], 3)
    model = pipeline.build_model(input_shape, config['num_classes'])
    
    # Train model
    trained_model = pipeline.train(
        model, X_train, y_train, X_val, y_val,
        train_datagen, val_datagen
    )
    
    # Evaluate model
    results = pipeline.evaluate(
        trained_model, X_test, y_test, config['class_names']
    )
    
    # Save model
    model_path = config['model_save_path']
    trained_model.save(model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Save training history
    history_path = config['history_save_path']
    with open(history_path, 'w') as f:
        json.dump({
            'history': {k: [float(x) for x in v] for k, v in pipeline.history.items()},
            'config': config,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)
    print(f"Training history saved to: {history_path}")
    
    # Plot training history
    pipeline.plot_training_history(config['plots_save_path'])
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print(f"Final Test Accuracy: {results['test_accuracy']:.4f}")
    print(f"Model saved to: {model_path}")
    print("="*60)


if __name__ == "__main__":
    # Check GPU availability
    print(f"TensorFlow version: {tf.__version__}")
    print(f"GPU Available: {tf.config.list_physical_devices('GPU')}")
    
    # Run training
    main()
