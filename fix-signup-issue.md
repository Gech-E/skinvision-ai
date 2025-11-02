# Fixing Signup "Signup failed" Error

## Quick Diagnosis

The signup endpoint works (tested successfully), so the issue is likely a frontend connection problem.

## Step-by-Step Fix

### Step 1: Verify Backend is Running

1. Check the backend terminal window
2. You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`
3. Open browser: http://localhost:8000/docs
4. If Swagger UI loads → Backend is running ✅

### Step 2: Test Backend Connection

**Option A: Use Test Page**
1. Open: http://localhost:3000/test-backend.html
2. Click "Test Backend Connection"
3. Click "Test Signup Endpoint"

**Option B: Use Browser Console**
1. Open browser console (F12)
2. Go to Network tab
3. Try signing up
4. Check if request to `http://localhost:8000/auth/signup` appears
5. Click on it to see error details

### Step 3: Check Frontend Environment

The frontend needs to know the backend URL. 

**Check if `.env.local` exists:**
```bash
cd frontend
cat .env.local  # Linux/Mac
type .env.local  # Windows
```

**If missing, create it:**
```bash
# Create frontend/.env.local
echo "VITE_API_BASE=http://localhost:8000" > .env.local
```

**Then restart frontend:**
1. Stop frontend (Ctrl+C)
2. Start again: `npm run dev`

### Step 4: Check CORS

The backend should have CORS enabled. Check `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should allow all origins
    ...
)
```

### Step 5: Check Browser Console

1. Open browser console (F12)
2. Go to Console tab
3. Try signing up
4. Look for red error messages
5. Common errors:
   - "Network Error" → Backend not running or wrong URL
   - "CORS" → CORS configuration issue
   - "404" → Wrong endpoint URL
   - "500" → Backend error (check backend terminal)

### Step 6: Manual API Test

Test signup directly via Swagger:

1. Open http://localhost:8000/docs
2. Find `POST /auth/signup`
3. Click "Try it out"
4. Enter:
```json
{
  "email": "getchew@example.com",
  "password": "yourpassword"
}
```
5. Click "Execute"

If this works → Frontend connection issue
If this fails → Backend issue (check backend logs)

## Common Solutions

### Solution 1: Restart Frontend

```bash
cd frontend
# Stop (Ctrl+C if running)
npm run dev  # Start again
```

### Solution 2: Clear Browser Cache

- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Or clear browser cache

### Solution 3: Check API URL

In browser console, check what URL frontend is using:
```javascript
console.log(import.meta.env.VITE_API_BASE)
```

Should output: `http://localhost:8000`

### Solution 4: Verify Backend URL

Make sure backend is accessible:
```bash
# PowerShell
Invoke-WebRequest http://localhost:8000

# Should return: {"message": "SkinVision AI API is running"}
```

## Still Not Working?

1. **Check both terminals:**
   - Backend terminal: Any error messages?
   - Frontend terminal: Any build errors?

2. **Check browser console:**
   - Open F12 → Console tab
   - Look for errors when clicking "Sign Up"

3. **Check Network tab:**
   - Open F12 → Network tab
   - Try signing up
   - Find the `/auth/signup` request
   - Check status code and response

4. **Try different email:**
   - The email might already exist
   - Try: `newuser${Date.now()}@example.com`

## Expected Behavior

✅ **Success:**
- Form submits
- Error message disappears
- Success message appears
- Redirects to login page after 1.5 seconds

❌ **Failure:**
- Error message appears
- Check error text for details
- Check browser console for more info

---

**Need more help?** Check the backend terminal window for detailed error messages!
