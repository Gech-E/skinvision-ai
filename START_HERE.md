# 🚀 Quick Start Guide - Run SkinVision AI Locally

Follow these simple steps to run the application on your local machine.

## Prerequisites Check

Before starting, make sure you have:

- ✅ **Python 3.11+** installed - Check: `python --version`
- ✅ **Node.js 20+** installed - Check: `node --version`
- ✅ **Backend running** on port 8000
- ✅ **Frontend running** on port 3000

---

## Step 1: Start Backend Server

### Open Terminal 1 (Backend)

**Windows PowerShell:**
```powershell
cd skinvision-ai\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or use the quick script:**
```powershell
cd skinvision-ai
.\start-backend.ps1
```

**What you should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Success!** Backend is running.

**Test it:** Open http://localhost:8000/docs in your browser

---

## Step 2: Start Frontend Server

### Open Terminal 2 (Frontend)

**Windows PowerShell:**
```powershell
cd skinvision-ai\frontend
npm install
npm run dev
```

**What you should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ **Success!** Frontend is running.

---

## Step 3: Access the Application

1. **Open your browser**
2. **Go to:** http://localhost:3000
3. **You should see the SkinVision AI home page!**

---

## Quick Test

1. **Upload an image** → Go to Upload page
2. **Try signup** → Create an account (first user = admin)
3. **Check API docs** → http://localhost:8000/docs

---

## Troubleshooting

### Backend won't start?
- Check if port 8000 is free: `netstat -ano | findstr :8000`
- Make sure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start?
- Check if port 3000 is free
- Install dependencies: `npm install`
- Clear cache: Delete `node_modules` and reinstall

### Can't connect frontend to backend?
- Check `frontend/.env.local` exists with: `VITE_API_BASE=http://localhost:8000`
- Restart frontend after creating `.env.local`

### See detailed troubleshooting?
- Check [README.md](README.md) Troubleshooting section
- Check [fix-signup-issue.md](fix-signup-issue.md) for signup problems

---

## Stopping the Servers

Press `Ctrl+C` in each terminal window to stop the servers.

---

**Need help?** Check the main [README.md](README.md) for detailed documentation.
