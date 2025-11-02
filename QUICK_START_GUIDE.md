# 🚀 Quick Start Guide - Run SkinVision AI Locally

## Prerequisites Checklist

- [x] Python 3.11+ installed
- [x] Node.js 18+ installed
- [x] PostgreSQL (optional - uses SQLite by default for local dev)

---

## Option 1: Quick Start (PowerShell Scripts)

### For Windows PowerShell:

**Step 1: Open PowerShell in project root**
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai
```

**Step 2: Start Backend**
```powershell
.\start-backend.ps1
```

**Step 3: Open a NEW PowerShell window and start Frontend**
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai
.\start-frontend.ps1
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

---

## Option 2: Manual Step-by-Step Commands

### Part 1: Backend Setup & Run

**Step 1: Navigate to backend directory**
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\backend
```

**Step 2: Create virtual environment (if not exists)**
```powershell
python -m venv .venv
```

**Step 3: Activate virtual environment**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Step 4: Install dependencies**
```powershell
pip install -r requirements.txt
```

**Step 5: Set Python path (for Windows)**
```powershell
$env:PYTHONPATH = $PWD
```

**Step 6: Start the backend server**
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend is now running on http://localhost:8000**

**To verify:**
- Open browser: http://localhost:8000/docs (Swagger UI)
- Or: http://localhost:8000 (should show JSON response)

---

### Part 2: Frontend Setup & Run

**Step 1: Open a NEW PowerShell/Terminal window**

**Step 2: Navigate to frontend directory**
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\frontend
```

**Step 3: Install dependencies (if not installed)**
```powershell
npm install
```

**Step 4: Start the frontend server**
```powershell
npm run dev
```

**✅ Frontend is now running on http://localhost:3000**

**To verify:**
- Open browser: http://localhost:3000
- You should see the SkinVision AI landing page

---

## 📋 Complete Command Sequence (Copy-Paste Ready)

### Terminal 1 (Backend):
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\backend
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
pip install -q -r requirements.txt
$env:PYTHONPATH = $PWD
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 (Frontend):
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\frontend
if (-not (Test-Path node_modules)) { npm install }
npm run dev
```

---

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application UI |
| **Backend API** | http://localhost:8000 | REST API endpoint |
| **Swagger Docs** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |

---

## 🛑 Stopping the Servers

### To stop backend:
- Press `CTRL + C` in the backend terminal
- Or close the terminal window

### To stop frontend:
- Press `CTRL + C` in the frontend terminal
- Or close the terminal window

---

## ⚙️ Environment Variables (Optional)

If you want to customize settings, create a `.env` file in the `backend` directory:

```env
# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///./skinvision.db

# JWT Secret (optional - defaults to devsecret)
JWT_SECRET=your-secret-key-here

# Email Notifications (optional)
EMAIL_NOTIFICATIONS_ENABLED=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=your-email@gmail.com

# SMS Notifications (optional)
SMS_NOTIFICATIONS_ENABLED=false
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=+1234567890

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

---

## 🔧 Troubleshooting

### Backend Issues:

**Problem: ModuleNotFoundError: No module named 'app'**
```powershell
# Solution: Set PYTHONPATH
$env:PYTHONPATH = $PWD
```

**Problem: Port 8000 already in use**
```powershell
# Solution: Use a different port
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Problem: Virtual environment not activating**
```powershell
# Solution: Run this first
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Frontend Issues:

**Problem: Port 3000 already in use**
```powershell
# Solution: Use a different port
$env:PORT=3001
npm run dev
```

**Problem: node_modules not found**
```powershell
# Solution: Install dependencies
npm install
```

**Problem: Backend connection errors**
- Ensure backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify `VITE_API_URL` in frontend `.env` file

---

## ✅ Verification Checklist

After starting both servers, verify:

- [ ] Backend responds at http://localhost:8000/docs
- [ ] Frontend loads at http://localhost:3000
- [ ] Can sign up a new user
- [ ] Can log in with credentials
- [ ] Can upload an image
- [ ] Prediction result appears

---

## 📱 Default Admin Credentials

When you create the first user, they automatically become admin.

**To test:**
1. Sign up with any email (e.g., `admin@example.com`)
2. First user = Admin role
3. Subsequent users = Regular user role

---

## 🎯 Quick Test Commands

### Test Backend API:
```powershell
# Health check
curl http://localhost:8000

# Test prediction (requires image file)
curl -X POST "http://localhost:8000/predict" -F "file=@path/to/image.jpg"
```

### Test Frontend:
- Just open http://localhost:3000 in browser!

---

## 📚 Next Steps

1. **Test the application:**
   - Sign up a new account
   - Upload a skin image
   - View prediction results
   - Check admin dashboard (if first user)

2. **Configure notifications** (optional):
   - See `NOTIFICATIONS_SETUP.md` for email/SMS setup

3. **Train ML model** (optional):
   - See `backend/app/ml/TRAINING_QUICKSTART.md`

4. **Run tests:**
   ```powershell
   # Backend tests
   cd backend
   pytest tests/ -v

   # Frontend tests
   cd frontend
   npm test
   ```

---

## 💡 Pro Tips

1. **Use two terminals** - One for backend, one for frontend
2. **Check logs** - Both terminals show useful debug info
3. **Hot reload** - Both servers auto-reload on code changes
4. **Swagger UI** - Great for testing API endpoints directly

---

**Need help?** Check the main `README.md` for more details!
