#!/bin/bash
# Example training script for Linux/Mac

echo "SkinVision AI - CNN Training"
echo "=============================="

# Set data directory
export DATA_DIR="data/skin_disease_dataset"

# Activate virtual environment
source ../../.venv/bin/activate  # Adjust path as needed

# Install training dependencies
pip install -r requirements_training.txt

# Run training
python train_model.py

echo "Training complete!"
echo "Model saved to: model.h5"
