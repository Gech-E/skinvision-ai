# 🎯 START HERE - Run SkinVision AI in 3 Steps

## Quick Commands (PowerShell)

### Step 1: Start Backend (Terminal 1)
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Start Frontend (Terminal 2 - NEW WINDOW)
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\frontend
npm run dev
```

### Step 3: Open Browser
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## That's It! 🎉

Both servers will auto-reload when you make changes.

**To stop:** Press `CTRL + C` in each terminal.

---

📖 **For detailed instructions, see `QUICK_START_GUIDE.md`**