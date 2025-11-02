# Quick Start Training Guide

## 🚀 Fastest Way to Train Your Model

### Step 1: Organize Your Dataset

Create this folder structure:
```
backend/app/ml/data/skin_disease_dataset/
├── Melanoma/
│   └── (your melanoma images)
├── Nevus/
│   └── (your nevus images)
├── BCC/
│   └── (your BCC images)
├── AK/
│   └── (your AK images)
└── Benign/
    └── (your benign images)
```

### Step 2: Install Dependencies

```bash
cd backend/app/ml
pip install -r requirements_training.txt
```

### Step 3: Run Training

**Option A: Full Training (Recommended)**
```bash
python train_model.py
```

**Option B: Quick Test Training**
```bash
python quick_train.py
```

### Step 4: Deploy Model

After training completes, the model is automatically saved as `model.h5`. Copy it:

```bash
# Windows
copy model.h5 ..\model.h5

# Linux/Mac
cp model.h5 ../model.h5
```

The backend will automatically load it!

## 📊 What to Expect

### Training Output:
- Real-time progress with accuracy/loss metrics
- Best model automatically saved
- Training plots generated
- Comprehensive evaluation report

### Typical Training Time:
- **Quick Test**: 10-30 minutes (100 images/class)
- **Full Training**: 1-5 hours (500+ images/class, GPU recommended)

### Model Quality:
- **Good**: >85% accuracy on test set
- **Excellent**: >90% accuracy with balanced classes
- **Production Ready**: >92% accuracy with proper validation

## 🎯 Configuration Tips

Edit `CONFIG` in `train_model.py`:

```python
# For faster training (lower accuracy)
'batch_size': 64,
'epochs': 50,
'model_architecture': 'CustomCNN'

# For better accuracy (slower training)
'batch_size': 16,
'epochs': 100,
'model_architecture': 'EfficientNetB0'
```

## ✅ Verification

After training, test your model:
1. Copy `model.h5` to `backend/app/ml/model.h5`
2. Restart backend server
3. Use Swagger UI to test `/predict` endpoint
4. Upload a skin image and see real predictions!

---

**Need help?** See `README_TRAINING.md` for detailed documentation.
