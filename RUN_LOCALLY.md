# 🚀 Run SkinVision AI Locally

## Quick Start (Easiest Method)

### Option 1: Use the Scripts

**In PowerShell, run these commands:**

```powershell
cd skinvision-ai

# Terminal 1 - Backend
.\start-backend.ps1

# Terminal 2 - Frontend (open new terminal)
.\start-frontend.ps1
```

### Option 2: Manual Commands

#### Terminal 1 - Backend Server

```powershell
cd skinvision-ai\backend

# Create virtual environment (first time only)
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend Server

```powershell
cd skinvision-ai\frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

## Access the Application

Once both servers are running:

- ✅ **Frontend**: http://localhost:3000
- ✅ **Backend API**: http://localhost:8000
- ✅ **API Documentation**: http://localhost:8000/docs

## What You Should See

### Backend Terminal:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     Started reloader process
```

### Frontend Terminal:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

## Features Available

- ✅ **AI Diagnosis** - Upload skin images for analysis
- ✅ **Email Notifications** - (Optional, see NOTIFICATIONS_SETUP.md)
- ✅ **SMS Notifications** - (Optional, see NOTIFICATIONS_SETUP.md)
- ✅ **Admin Dashboard** - View all predictions
- ✅ **Prediction History** - Track all diagnoses
- ✅ **Responsive UI** - Works on mobile & desktop

## Troubleshooting

### Backend won't start?
- Make sure Python 3.11+ is installed
- Check if port 8000 is free: `netstat -ano | findstr :8000`
- Activate virtual environment: `.\backend\.venv\Scripts\Activate.ps1`

### Frontend won't start?
- Make sure Node.js 20+ is installed
- Check if port 3000 is free
- Install dependencies: `npm install`

### Dependencies missing?
```powershell
# Backend
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Next Steps

1. **Create an account** - First user becomes admin
2. **Upload an image** - Test the AI diagnosis
3. **Check admin dashboard** - View analytics
4. **Enable notifications** - See NOTIFICATIONS_SETUP.md

---

**Happy coding! 🎉**
