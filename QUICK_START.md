# 🚀 Quick Start - Run SkinVision AI Locally

## One-Command Start (Windows PowerShell)

```powershell
cd skinvision-ai
.\start-local.ps1
```

Or manually:

## Manual Start

### Terminal 1 - Backend
```powershell
cd skinvision-ai\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend
```powershell
cd skinvision-ai\frontend
npm install
npm run dev
```

## Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Features

✅ AI-Powered Diagnosis  
✅ Email & SMS Notifications (optional)  
✅ Admin Dashboard  
✅ Prediction History  
✅ Responsive UI  

## Notifications (Optional)

To enable notifications, see [NOTIFICATIONS_SETUP.md](NOTIFICATIONS_SETUP.md)

---
**Need help?** Check [README.md](README.md) for detailed documentation.
