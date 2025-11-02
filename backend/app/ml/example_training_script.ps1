# PowerShell script for training on Windows

Write-Host "SkinVision AI - CNN Training" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Set data directory
$env:DATA_DIR = "data\skin_disease_dataset"

# Navigate to ml directory
cd $PSScriptRoot

# Activate virtual environment (adjust path as needed)
& "..\..\..venv\Scripts\Activate.ps1"

# Install training dependencies
pip install -r requirements_training.txt

# Run training
python train_model.py

Write-Host "`nTraining complete!" -ForegroundColor Green
Write-Host "Model saved to: model.h5" -ForegroundColor Green
