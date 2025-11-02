# SkinVision AI – Deep Learning Based Skin Disease Detection System

<div align="center">

![SkinVision AI](https://img.shields.io/badge/SkinVision-AI-2B7A78?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)

**AI-Powered Skin Disease Detection with Explainable AI Visualization**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Training](#-training) • [Deployment](#-deployment)

</div>

---

## 📖 Table of Contents

1. [About the Project](#-about-the-project)
2. [Features](#-features)
3. [Prerequisites](#-prerequisites)
4. [Quick Start (Docker)](#-quick-start-using-docker-recommended)
5. [Step-by-Step Local Installation](#-step-by-step-local-installation)
6. [Running the Application](#-running-the-application)
7. [Using the Application](#-using-the-application)
8. [Training Your Own Model](#-training-your-own-model)
9. [API Documentation](#-api-documentation)
10. [Testing](#-testing)
11. [Deployment](#-deployment)
12. [Troubleshooting](#-troubleshooting)
13. [Project Structure](#-project-structure)

---

## 🎯 About the Project

**SkinVision AI** is a complete web application that uses deep learning to detect and classify skin diseases from images. It provides:

- **AI-Powered Diagnosis**: Upload a skin image and get instant classification
- **Explainable AI**: Visual heatmaps show what the AI sees (Grad-CAM)
- **Professional UI**: Clean, modern healthcare interface
- **Admin Dashboard**: Track predictions and view analytics
- **Secure & Private**: JWT authentication and encrypted data

### Use Cases
- Medical research and education
- Preliminary screening tool
- Healthcare professional assistance
- Patient self-assessment (with medical disclaimer)

---

## ✨ Features

### Core Functionality
- ✅ **Deep Learning CNN** for skin disease classification (5 classes: Melanoma, Nevus, BCC, AK, Benign)
- ✅ **Grad-CAM Heatmaps** showing AI attention regions
- ✅ **Real-time Analysis** with progress indicators
- ✅ **Prediction History** with user authentication
- ✅ **Admin Dashboard** with analytics charts
- ✅ **Mobile Responsive** design
- ✅ **Dark Mode** support

### User Features
- 📤 Drag & Drop image upload
- 📊 Confidence scores with visual bars
- 📄 Downloadable reports (PDF - placeholder)
- 👨‍⚕️ Medical recommendations based on urgency
- 🔒 Secure authentication

### Admin Features
- 📈 Disease distribution charts
- 📋 Full prediction history management
- 📊 Weekly trend analysis
- 🔐 Role-based access control

---

## 📋 Prerequisites

Before you begin, make sure you have:

### Required Software
- **Python 3.11 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 20 or higher** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/downloads)

### Optional (for Docker)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **Docker Compose** - Usually included with Docker Desktop

### For Training Models
- **GPU (Recommended)** - NVIDIA GPU with CUDA support
- **8GB+ RAM** - For training large datasets
- **50GB+ Free Disk Space** - For datasets and models

---

## 🚀 Quick Start (Using Docker - Recommended)

The fastest way to get started is using Docker Compose. This sets up everything automatically.

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd skinvision-ai
```

### Step 2: Start All Services

```bash
docker compose up --build
```

This will:
- ✅ Build backend container
- ✅ Build frontend container
- ✅ Start PostgreSQL database
- ✅ Set up all services automatically

### Step 3: Access the Application

After a few minutes (when containers are ready):

- **Frontend**: Open http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs

### Step 4: Stop Services

```bash
docker compose down
```

---

## 💻 Step-by-Step Local Installation

Follow these steps if you want to run the project locally without Docker.

### Part 1: Backend Setup

#### Step 1.1: Navigate to Backend Directory

```bash
cd skinvision-ai/backend
```

#### Step 1.2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

> 💡 **Tip**: You should see `(.venv)` in your terminal prompt, meaning the virtual environment is active.

#### Step 1.3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Note**: If you see TensorFlow errors, the app will still work but model predictions will use fallback values. See [Troubleshooting](#troubleshooting) section.

#### Step 1.4: Verify Backend Installation

```bash
python -c "from app.main import app; print('Backend setup successful!')"
```

If you see "Backend setup successful!", you're ready!

### Part 2: Frontend Setup

#### Step 2.1: Navigate to Frontend Directory

Open a **new terminal window** (keep backend terminal open) and:

```bash
cd skinvision-ai/frontend
```

#### Step 2.2: Install Node Dependencies

```bash
npm install
```

This may take 2-5 minutes depending on your internet speed.

#### Step 2.3: Verify Frontend Installation

```bash
npm run build
```

If this completes without errors, frontend is ready!

### Part 3: Database Setup (Optional - Uses SQLite by Default)

The application uses SQLite by default, so no database setup is needed. However, if you want PostgreSQL:

#### Option A: Use SQLite (Default - No Setup Needed)
- ✅ Works out of the box
- ✅ Perfect for development
- ✅ No additional installation

#### Option B: Use PostgreSQL (For Production)

1. **Install PostgreSQL** - [Download](https://www.postgresql.org/download/)

2. **Create Database**:
```sql
CREATE DATABASE skinvision;
```

3. **Set Environment Variable**:
```bash
# Windows
$env:DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/skinvision"

# Linux/Mac
export DATABASE_URL="postgresql+psycopg2://username:password@localhost:5432/skinvision"
```

---

## 🏃 Running the Application

### Method 1: Automated Script (Easiest)

**Windows:**
```powershell
.\start-local.ps1
```

**Linux/Mac:**
```bash
./start-local.sh
```

This opens both servers in separate windows automatically.

### Method 2: Manual Start (Two Terminals)

#### Terminal 1 - Backend Server

```bash
cd skinvision-ai/backend

# Activate virtual environment (if not active)
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate            # Linux/Mac

# Start backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend Server

```bash
cd skinvision-ai/frontend

# Start frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

### Method 3: Backend Only (For API Testing)

If you only want to test the API:

```bash
cd skinvision-ai/backend
.\.venv\Scripts\Activate.ps1  # Windows
python -m uvicorn app.main:app --reload
```

Then open: **http://localhost:8000/docs**

---

## 🎮 Using the Application

### Step 1: Access the Application

Open your browser and go to: **http://localhost:3000**

### Step 2: Home Page

You'll see:
- Hero section with app description
- "Upload Your Image for Analysis" button
- Feature cards explaining capabilities

### Step 3: Upload an Image

1. Click **"Upload Your Image for Analysis"** or go to **/upload**
2. **Drag and drop** an image or click to browse
3. Optionally fill in metadata:
   - Patient Age
   - Sex
   - Skin lesion location
4. Click **"Analyze Image"**
5. Wait for analysis (progress bar will show)

### Step 4: View Results

After analysis, you'll be redirected to results page showing:

- **Predicted Disease Name** (e.g., "Melanoma")
- **Confidence Percentage** (e.g., "92%")
- **Grad-CAM Heatmap** - Slide to compare original and heatmap
- **Urgency Level** - High/Medium/Low
- **Medical Recommendations** - Next steps based on severity
- **Action Buttons** - Download report, request review

### Step 5: Create Admin Account (Optional)

To access the admin dashboard:

1. Go to **/signup** or click "Sign Up" in navigation
2. Enter email and password
3. **First user automatically becomes admin**
4. Click "Sign Up"
5. You'll be redirected to login
6. Log in with your credentials

### Step 6: Access Admin Dashboard

1. After logging in, go to **/admin** or click "Admin Dashboard"
2. View:
   - **Statistics Cards** - Total predictions, classes, average confidence
   - **Prediction History Table** - All past analyses
   - **Analytics Charts**:
     - Disease distribution (bar chart)
     - Weekly trends (line chart)

---

## 🧠 Training Your Own Model

If you want to train a CNN model with your own dataset:

### Step 1: Organize Your Dataset

Create this folder structure:
```
backend/app/ml/data/skin_disease_dataset/
├── Melanoma/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Nevus/
│   └── ...
├── BCC/
│   └── ...
├── AK/
│   └── ...
└── Benign/
    └── ...
```

> 💡 **Tip**: Aim for 200+ images per class for good results, 500+ for excellent results.

### Step 2: Install Training Dependencies

```bash
cd skinvision-ai/backend/app/ml
pip install -r requirements_training.txt
```

### Step 3: Set Data Directory

**Windows:**
```powershell
$env:DATA_DIR = "data\skin_disease_dataset"
```

**Linux/Mac:**
```bash
export DATA_DIR="data/skin_disease_dataset"
```

### Step 4: Run Training

**Full Training (Recommended):**
```bash
python train_model.py
```

**Quick Test (Faster, smaller dataset):**
```bash
python quick_train.py
```

### Step 5: Deploy Your Model

After training completes:

```bash
# Model is saved as model.h5
# Copy it to the ml directory
copy model.h5 ..\model.h5  # Windows
cp model.h5 ../model.h5    # Linux/Mac
```

The backend will automatically load it!

### 📚 Detailed Training Guide

See **[backend/app/ml/README_TRAINING.md](backend/app/ml/README_TRAINING.md)** for:
- Architecture options
- Hyperparameter tuning
- Advanced configurations
- Troubleshooting

---

## 📡 API Documentation

### Interactive API Docs

The fastest way to explore the API:

1. Start the backend server
2. Open: **http://localhost:8000/docs**
3. You'll see Swagger UI with all endpoints
4. Click "Try it out" on any endpoint to test

### Main Endpoints

#### 1. Health Check
```
GET http://localhost:8000/
Response: {"message": "SkinVision AI API is running"}
```

#### 2. Sign Up
```
POST http://localhost:8000/auth/signup
Body: {"email": "user@example.com", "password": "password123"}
Response: {"id": 1, "email": "user@example.com", "role": "admin"}
```
> 💡 **First user becomes admin automatically**

#### 3. Login
```
POST http://localhost:8000/auth/login
Body: {"email": "user@example.com", "password": "password123"}
Response: {"access_token": "eyJ0eXAi...", "token_type": "bearer"}
```

#### 4. Predict (Upload Image)
```
POST http://localhost:8000/predict
Content-Type: multipart/form-data
Body: file=<image_file>

Response:
{
  "id": 1,
  "predicted_class": "Melanoma",
  "confidence": 0.92,
  "image_url": "/static/image.jpg",
  "heatmap_url": "/static/heatmap_image.jpg",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 5. Get History
```
GET http://localhost:8000/history/
Headers: Authorization: Bearer <token>
Response: [array of predictions]
```

#### 6. Delete Record
```
DELETE http://localhost:8000/history/{id}
Headers: Authorization: Bearer <token>
Response: {"status": "deleted"}
```

### Using API with Authentication

1. **Sign up or login** to get a token
2. **Copy the `access_token`** from response
3. **In Swagger UI**: Click "Authorize" button (top right)
4. **Enter**: `Bearer <your_token_here>`
5. **All protected endpoints** will now work

---

## 🧪 Testing

### Run All Tests

**Quick Script:**
```bash
# Windows
.\run-tests.bat

# Linux/Mac
./run-tests.sh
```

### Backend Tests Only

```bash
cd backend
pytest
pytest --cov=app --cov-report=html  # With coverage report
```

### Frontend Tests Only

```bash
cd frontend
npm test
npm run test:coverage  # With coverage report
```

### Test Coverage

- **Backend**: Reports in `backend/htmlcov/index.html`
- **Frontend**: Reports in `frontend/coverage/index.html`

**Coverage Target**: 70%+

See **[TESTING.md](TESTING.md)** for detailed testing documentation.

---

## 🚢 Deployment

### Backend Deployment (Render/Railway)

1. **Connect your GitHub repository**

2. **Set Build Command**:
   ```
   pip install -r requirements.txt
   ```

3. **Set Start Command**:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**:
   ```
   DATABASE_URL=<your-postgresql-url>
   MODEL_PATH=/app/app/ml/model.h5
   STATIC_DIR=/app/app/static
   JWT_SECRET=<your-secret-key>
   ```

5. **Deploy!**

### Frontend Deployment (Vercel/Netlify)

1. **Connect your GitHub repository**

2. **Set Build Command**:
   ```
   npm run build
   ```

3. **Set Output Directory**:
   ```
   dist
   ```

4. **Set Environment Variable**:
   ```
   VITE_API_BASE=https://your-backend-url.com
   ```

5. **Deploy!**

### Database (Supabase/ElephantSQL)

1. Create PostgreSQL database
2. Get connection string
3. Add to backend environment variables

### Full Deployment Guide

For detailed deployment instructions, see:
- **[DEPLOYMENT.md](DEPLOYMENT.md)** (if exists)
- Platform-specific guides in documentation

---

## 🔧 Troubleshooting

### Problem: Backend won't start

**Solution 1: Check Python version**
```bash
python --version  # Should be 3.11+
```

**Solution 2: Reinstall dependencies**
```bash
cd backend
pip install --upgrade -r requirements.txt
```

**Solution 3: Check for port conflicts**
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```
If port is in use, either stop the other service or change port in uvicorn command.

### Problem: TensorFlow DLL Error (Windows)

**Error**: `Could not find the DLL(s) 'msvcp140.dll'`

**Solution**: 
1. Download Microsoft Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install it
3. Restart backend server

**Note**: The app works without TensorFlow but will use fallback predictions.

### Problem: Frontend won't start

**Solution 1: Clear node_modules**
```bash
cd frontend
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules                  # Windows
npm install
```

**Solution 2: Check Node version**
```bash
node --version  # Should be 20+
```

### Problem: Can't connect to backend from frontend

**Solution**: Check `VITE_API_BASE` environment variable:
```bash
# Create frontend/.env.local
VITE_API_BASE=http://localhost:8000
```

### Problem: Database errors

**Solution**: If using SQLite (default), make sure the directory is writable. If using PostgreSQL, check:
- Database is running
- Connection string is correct
- User has proper permissions

### Problem: Model predictions always the same

**Cause**: Model file (`model.h5`) not found or TensorFlow not working

**Solution**:
1. Check if `backend/app/ml/model.h5` exists
2. If not, train a model (see [Training section](#-training-your-own-model))
3. Or check TensorFlow installation

### Problem: Authentication not working

**Solution**:
1. Make sure you're using the correct endpoint (`/auth/login` or `/auth/signup`)
2. Check token is included in Authorization header: `Bearer <token>`
3. Verify JWT_SECRET is set correctly

---

## 📂 Project Structure

```
skinvision-ai/
├── backend/                          # FastAPI backend
│   ├── app/
│   │   ├── main.py                  # FastAPI application
│   │   ├── models.py                # Database models
│   │   ├── database.py              # Database connection
│   │   ├── schemas.py               # Pydantic schemas
│   │   ├── crud.py                  # Database operations
│   │   ├── static/                  # Uploaded images & heatmaps
│   │   ├── ml/                      # Machine learning code
│   │   │   ├── train_model.py       # Training script ⭐
│   │   │   ├── grad_cam.py          # Grad-CAM visualization
│   │   │   └── model.h5             # Trained model (add yours)
│   │   └── routers/                 # API route handlers
│   │       ├── auth.py              # Authentication
│   │       ├── predict.py           # Image prediction
│   │       └── history.py           # Prediction history
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend container
│   └── tests/                       # Backend tests
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── UploadCard.jsx
│   │   │   ├── PredictionCard.jsx
│   │   │   ├── HeatmapSlider.jsx
│   │   │   └── HistoryTable.jsx
│   │   ├── pages/                   # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Upload.jsx
│   │   │   ├── Result.jsx
│   │   │   ├── Admin.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Signup.jsx
│   │   ├── App.jsx                  # Main app component
│   │   └── main.jsx                 # Entry point
│   ├── package.json                 # Node dependencies
│   ├── tailwind.config.js           # Tailwind configuration
│   └── Dockerfile                   # Frontend container
│
├── docker-compose.yml               # Docker orchestration
├── README.md                        # This file
├── TESTING.md                       # Testing guide
├── start-local.ps1                 # Quick start script (Windows)
├── start-local.bat                 # Quick start script (Windows)
└── run-tests.sh                    # Test runner (Linux/Mac)
```

---

## 🎨 UI Design System

### Brand Colors
- **Primary**: `#2B7A78` (Calm Teal)
- **Secondary**: `#3AAFA9` (Light Teal)
- **Accent**: `#DEF2F1` (Pale Cyan)
- **Text**: `#17252A` (Dark Navy)

### Design Principles
- Rounded corners: `rounded-2xl`
- Soft shadows with hover effects
- Smooth 300ms transitions
- Mobile-first responsive design
- Dark mode support

---

## 📚 Additional Documentation

- **[TESTING.md](TESTING.md)** - Comprehensive testing guide
- **[backend/app/ml/README_TRAINING.md](backend/app/ml/README_TRAINING.md)** - Model training documentation
- **[backend/app/ml/TRAINING_QUICKSTART.md](backend/app/ml/TRAINING_QUICKSTART.md)** - Quick training guide

---

## ❓ Frequently Asked Questions

### Q: Do I need a GPU to run the application?
**A**: No! The app works on CPU. GPU is only needed for training models.

### Q: Can I use this for actual medical diagnosis?
**A**: **No.** This is for educational/research purposes only. Always consult a real dermatologist for medical diagnosis.

### Q: How accurate is the model?
**A**: Depends on your trained model. With a good dataset (500+ images/class), expect 85-95% accuracy on test set.

### Q: What image formats are supported?
**A**: JPG, PNG, JPEG (any common image format)

### Q: Is my data private?
**A**: Yes! Images are stored locally in `backend/app/static/`. For production, use proper security measures.

### Q: Can I add more disease classes?
**A**: Yes! Modify `CONFIG['class_names']` in `train_model.py` and retrain.

### Q: How do I reset the database?
**A**: Delete `backend/skinvision.db` (SQLite) or drop/create PostgreSQL database.

### Q: Why are predictions always "Melanoma" with 92% confidence?
**A**: This is the fallback when no model is loaded. Train and add a model to get real predictions.

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.115+ |
| **Frontend** | React | 18+ |
| **Database** | SQLite / PostgreSQL | - |
| **ML Framework** | TensorFlow/Keras | 2.16+ |
| **Styling** | Tailwind CSS | 3.4+ |
| **Build Tool** | Vite | 5.4+ |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style
- Write tests for new features
- Update documentation
- Ensure all tests pass

---

## 📄 License

This project is for **educational and research purposes only**.

**⚠️ Medical Disclaimer**: This tool is for informational purposes only and does not replace professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions regarding a medical condition.

---

## 🙏 Acknowledgments

- Built with open-source technologies
- UI inspired by modern healthcare applications
- Grad-CAM implementation based on research papers
- Community feedback and contributions

---

## 📧 Support & Contact

- **Issues**: Open an issue on GitHub
- **Questions**: Check the FAQ section above
- **Documentation**: See additional docs in project directories

---

## 🎯 Quick Reference Commands

```bash
# Start everything (Docker)
docker compose up --build

# Start backend only
cd backend && python -m uvicorn app.main:app --reload

# Start frontend only
cd frontend && npm run dev

# Run tests
cd backend && pytest
cd frontend && npm test

# Train model
cd backend/app/ml && python train_model.py

# Access API docs
# Open: http://localhost:8000/docs
```

---

<div align="center">

**Made with ❤️ for healthcare innovation**

[⬆ Back to Top](#skinvision-ai--deep-learning-based-skin-disease-detection-system)

</div>