# 🔧 Troubleshooting Login Issues

## Common Login Error: "Login failed. Please check your connection and try again."

### ✅ Quick Fix Checklist

1. **Is the backend running?**
   ```powershell
   # Check if backend is accessible
   curl http://localhost:8000
   # Or open in browser: http://localhost:8000/docs
   ```

2. **Start the backend if not running:**
   ```powershell
   cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\backend
   .\.venv\Scripts\Activate.ps1
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify backend is accessible:**
   - Open: http://localhost:8000/docs
   - You should see Swagger UI

---

## 🔍 Diagnostic Steps

### Step 1: Check Backend Status

**Option A: Browser Test**
1. Open: http://localhost:8000
2. Should see: `{"message": "SkinVision AI API is running"}`

**Option B: PowerShell Test**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing
```

### Step 2: Check Login Endpoint

```powershell
# Test login endpoint directly
$body = @{
    email = "test@example.com"
    password = "test123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method Post -Body $body -ContentType "application/json"
```

### Step 3: Check Frontend Console

1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Look for errors like:
   - `Network Error`
   - `ERR_CONNECTION_REFUSED`
   - `CORS policy`

---

## 🚨 Common Issues & Solutions

### Issue 1: Backend Not Running

**Symptoms:**
- Login button does nothing
- Error: "Cannot connect to backend server"
- Network Error in console

**Solution:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

---

### Issue 2: Wrong Port

**Symptoms:**
- Backend running on different port (e.g., 8001)
- Frontend still trying 8000

**Solution:**
Create `.env` file in `frontend/` directory:
```env
VITE_API_BASE=http://localhost:8001
```

Then restart frontend.

---

### Issue 3: CORS Error

**Symptoms:**
- Console shows: "CORS policy: No 'Access-Control-Allow-Origin'"
- Network tab shows CORS errors

**Solution:**
Backend already allows all origins. If issue persists:
1. Check `backend/app/main.py` has CORS middleware
2. Restart backend server

---

### Issue 4: Invalid Credentials

**Symptoms:**
- Error: "Invalid email or password"
- Backend returns 401

**Solution:**
1. Sign up first if you don't have an account
2. Check email/password spelling
3. Verify user exists in database

---

### Issue 5: Database Connection

**Symptoms:**
- Backend crashes on login
- Database errors in backend terminal

**Solution:**
```powershell
cd backend
# Check database file exists
ls skinvision.db

# If missing, it will be created on first request
```

---

## 🧪 Test Backend Connection

Run this PowerShell script to test:

```powershell
$api = "http://localhost:8000"

# Test 1: Root endpoint
try {
    $response = Invoke-RestMethod -Uri "$api/" -Method Get
    Write-Host "✓ Backend is running: $($response.message)" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend is NOT running" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Login endpoint (will fail without valid user)
try {
    $body = @{ email = "test@example.com"; password = "test" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "$api/auth/login" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Login endpoint is accessible" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✓ Login endpoint works (401 = invalid credentials, which is expected)" -ForegroundColor Green
    } else {
        Write-Host "✗ Login endpoint error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

---

## 📋 Complete Startup Sequence

**Terminal 1 (Backend):**
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = $PWD
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 (Frontend):**
```powershell
cd C:\Users\getac\Desktop\deep_learning\skinvision-ai\frontend
npm run dev
```

**Wait for:**
```
  ➜  Local:   http://localhost:3000/
```

**Then:**
1. Open http://localhost:3000 in browser
2. The login page will automatically check backend connection
3. If backend is not running, you'll see a warning with instructions

---

## ✅ Verification

After starting both:

1. **Backend:** http://localhost:8000/docs (Swagger UI)
2. **Frontend:** http://localhost:3000
3. **Login page should:**
   - Show "Checking backend connection..." briefly
   - If backend is running: Show login form
   - If backend is not running: Show connection error with solution

---

## 💡 Still Having Issues?

1. **Check browser console** (F12 → Console tab)
2. **Check backend terminal** for error messages
3. **Verify ports are not blocked** by firewall
4. **Try incognito mode** to rule out cache issues
5. **Restart both servers** completely

---

## 🆘 Need More Help?

Check:
- `QUICK_START_GUIDE.md` - Full setup instructions
- `START_HERE.md` - Quick 3-step guide
- Backend logs in terminal
- Browser Developer Tools → Network tab
