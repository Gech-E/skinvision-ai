@echo off
echo Starting SkinVision AI - Backend and Frontend
echo ===============================================

echo.
echo Starting Backend Server (Port 8000)...
start "SkinVision Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server (Port 3000)...
start "SkinVision Frontend" cmd /k "cd /d %~dp0frontend && if not exist node_modules npm install && npm run dev"

echo.
echo ===============================================
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo ===============================================
echo.
echo Both servers are starting in separate windows.
echo Press any key to exit this window (servers will keep running)...
pause >nul
