# CNN Model Training Guide

## Professional Deep Learning Training Pipeline for SkinVision AI

This guide explains how to train a CNN model for skin disease classification using professional deep learning practices.

## 📋 Prerequisites

1. **Python Environment**: Python 3.8+ with virtual environment
2. **GPU** (Recommended): NVIDIA GPU with CUDA support for faster training
3. **Dataset**: Organized skin disease images

## 📁 Dataset Structure

Organize your dataset in the following structure:

```
data/
└── skin_disease_dataset/
    ├── Melanoma/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── Nevus/
    │   ├── image1.jpg
    │   └── ...
    ├── BCC/
    │   └── ...
    ├── AK/
    │   └── ...
    └── Benign/
        └── ...
```

**Recommended Dataset Size:**
- Minimum: 100-200 images per class
- Optimal: 500-1000+ images per class
- Balanced classes for best results

## 🚀 Setup

### 1. Install Training Dependencies

```bash
cd backend/app/ml
pip install -r requirements_training.txt
```

### 2. Set Data Directory

Set the environment variable or modify the script:

```bash
# Windows PowerShell
$env:DATA_DIR = "path/to/your/dataset"

# Linux/Mac
export DATA_DIR="path/to/your/dataset"
```

Or edit `train_model.py` and change:
```python
data_dir = os.getenv('DATA_DIR', 'data/skin_disease_dataset')
```

## 🏋️ Training

### Basic Training

```bash
cd backend/app/ml
python train_model.py
```

### With Custom Configuration

Edit the `CONFIG` dictionary in `train_model.py`:

```python
CONFIG = {
    'img_size': (224, 224),           # Image dimensions
    'batch_size': 32,                 # Batch size (adjust based on GPU memory)
    'epochs': 100,                    # Training epochs
    'learning_rate': 1e-4,            # Learning rate
    'model_architecture': 'EfficientNetB0',  # or 'ResNet50', 'CustomCNN'
    'data_augmentation': True,        # Enable augmentation
    'use_pretrained': True,           # Transfer learning
    # ... more options
}
```

## 🏗️ Model Architectures

### 1. EfficientNetB0 (Recommended)
- **Pros**: Best accuracy/size ratio, modern architecture
- **Cons**: Slightly slower than Custom CNN
- **Use case**: Production deployment

### 2. ResNet50
- **Pros**: Proven architecture, good performance
- **Cons**: Larger model size
- **Use case**: High accuracy requirements

### 3. Custom CNN
- **Pros**: Lightweight, fast inference
- **Cons**: Lower accuracy on complex datasets
- **Use case**: Resource-constrained environments

## 📊 Training Features

### Automatic Features:
- ✅ **Data Augmentation**: Rotation, flipping, zoom, brightness adjustment
- ✅ **Early Stopping**: Prevents overfitting
- ✅ **Learning Rate Reduction**: Adaptive LR scheduling
- ✅ **Model Checkpointing**: Saves best model during training
- ✅ **Stratified Splitting**: Maintains class distribution
- ✅ **Comprehensive Evaluation**: Metrics, confusion matrix, classification report

### Output Files:
- `model.h5` - Trained model (ready for deployment)
- `training_history.json` - Training metrics and configuration
- `training_plots.png` - Visualization of training curves
- `training_log.csv` - Detailed epoch-by-epoch log
- `checkpoints/best_model.h5` - Best model checkpoint

## 📈 Monitoring Training

### View Training Progress:
- Real-time console output
- `training_log.csv` for detailed metrics
- `training_plots.png` for visual analysis

### Key Metrics:
- **Accuracy**: Overall classification accuracy
- **Precision**: Per-class precision scores
- **Recall**: Per-class recall scores
- **F1-Score**: Harmonic mean of precision and recall

## 🔧 Advanced Configuration

### GPU Training:
```python
# Automatically detects and uses GPU if available
# Check GPU: print(tf.config.list_physical_devices('GPU'))
```

### Fine-tuning Transfer Learning:
```python
# In CNNArchitecture.build_transfer_learning_model()
trainable_base = True  # Unfreeze base model for fine-tuning
```

### Custom Hyperparameters:
```python
CONFIG = {
    'early_stopping_patience': 20,  # Increase for longer training
    'reduce_lr_patience': 5,         # LR reduction patience
    'batch_size': 64,                # Larger batches with more GPU memory
    'learning_rate': 1e-5,           # Lower LR for fine-tuning
}
```

## 🎯 Best Practices

1. **Data Quality**: Ensure high-quality, labeled images
2. **Class Balance**: Aim for balanced dataset across classes
3. **Validation**: Always use validation set to monitor overfitting
4. **Augmentation**: Use augmentation for limited datasets
5. **Transfer Learning**: Start with pre-trained models for better results
6. **Hyperparameter Tuning**: Experiment with learning rates and batch sizes
7. **Multiple Runs**: Train multiple models and ensemble for best results

## 📝 Expected Training Time

- **CPU**: 10-50 hours (depending on dataset size)
- **GPU (NVIDIA)**: 1-5 hours (depending on GPU and dataset)

## 🚨 Troubleshooting

### Out of Memory (OOM) Errors:
```python
# Reduce batch size
'batch_size': 16  # or 8

# Use smaller model
'model_architecture': 'CustomCNN'
```

### Slow Training:
- Use GPU if available
- Reduce image size: `'img_size': (128, 128)`
- Disable augmentation during debugging

### Poor Accuracy:
- Increase dataset size
- Use transfer learning: `'use_pretrained': True`
- Try different architectures
- Check data quality and labels

## 📚 Model Deployment

After training, the model (`model.h5`) is ready for deployment:

1. Copy to backend:
```bash
cp model.h5 backend/app/ml/model.h5
```

2. The backend automatically loads it from:
   - `MODEL_PATH` environment variable, or
   - `backend/app/ml/model.h5` (default)

3. Test the model:
   - Use Swagger UI: http://localhost:8000/docs
   - Try the `/predict` endpoint

## 🔬 Evaluation Metrics

The training script provides:
- **Overall accuracy**: Test set accuracy
- **Per-class accuracy**: Individual class performance
- **Confusion matrix**: Error analysis
- **Classification report**: Precision, recall, F1-score

## 📖 References

- EfficientNet: [Paper](https://arxiv.org/abs/1905.11946)
- ResNet: [Paper](https://arxiv.org/abs/1512.03385)
- Transfer Learning: [TensorFlow Guide](https://www.tensorflow.org/guide/keras/transfer_learning)

## 💡 Tips from Deep Learning Engineers

1. **Start Simple**: Begin with EfficientNetB0 and default settings
2. **Iterate**: Train, evaluate, adjust, repeat
3. **Monitor**: Watch validation loss for overfitting signs
4. **Save Everything**: Keep checkpoints and training logs
5. **Validate**: Always test on unseen data before deployment

---

**Happy Training! 🚀**
