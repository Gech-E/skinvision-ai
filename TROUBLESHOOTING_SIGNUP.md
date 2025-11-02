# Troubleshooting Signup Issues

## Common Signup Errors and Solutions

### Error: "Signup failed"

**Possible Causes and Solutions:**

#### 1. Backend Server Not Running

**Check:**
- Is the backend running on http://localhost:8000?
- Open http://localhost:8000/docs in browser - do you see Swagger UI?

**Solution:**
```bash
cd backend
.\.venv\Scripts\Activate.ps1  # Windows
python -m uvicorn app.main:app --reload
```

#### 2. Frontend Cannot Connect to Backend

**Check:**
- Open browser console (F12) - look for network errors
- Check if `VITE_API_BASE` is set correctly

**Solution:**
Create `frontend/.env.local`:
```
VITE_API_BASE=http://localhost:8000
```

#### 3. Database Issues

**Check:**
- Database file should be at `backend/skinvision.db` (SQLite)
- Check file permissions

**Solution:**
```bash
cd backend
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### 4. Email Already Exists

**Error:** "Email already registered"

**Solution:**
- Use a different email address, or
- Delete the existing user from database

#### 5. CORS Issues

**Check:**
- Backend console for CORS errors
- Browser console for CORS messages

**Solution:**
CORS is already configured in `backend/app/main.py` with `allow_origins=["*"]`

### Testing Signup via Swagger UI

1. Open http://localhost:8000/docs
2. Find `POST /auth/signup`
3. Click "Try it out"
4. Enter:
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```
5. Click "Execute"
6. Check the response - you should see the user data

### Testing Signup via PowerShell

```powershell
$body = @{
    email = "test@example.com"
    password = "password123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/auth/signup" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Checking Backend Logs

Look at the backend terminal/console window for error messages. Common errors:

- `Database locked` - Close other connections or restart
- `Table doesn't exist` - Run database initialization
- `Module not found` - Install missing dependencies
- `Connection refused` - Backend not running

### Quick Diagnostic

Run these checks:

```bash
# 1. Check backend is running
curl http://localhost:8000

# 2. Check signup endpoint
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# 3. Check database
cd backend
python -c "from app.database import SessionLocal; from app.models import User; db = SessionLocal(); print(f'Users: {db.query(User).count()}'); db.close()"
```