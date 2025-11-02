@echo off
REM Windows batch script to run tests

echo Running SkinVision AI Test Suite
echo ====================================

echo.
echo Select test suite to run:
echo 1) Backend only
echo 2) Frontend only  
echo 3) Both (Full test suite)
echo 4) Quick tests (no coverage)

set /p choice="Enter choice [1-4]: "

if "%choice%"=="1" goto backend
if "%choice%"=="2" goto frontend
if "%choice%"=="3" goto both
if "%choice%"=="4" goto quick
goto invalid

:backend
echo.
echo Running Backend Tests...
cd backend
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term --cov-report=html
cd ..
goto end

:frontend
echo.
echo Running Frontend Tests...
cd frontend
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
call npm run test:coverage
cd ..
goto end

:both
echo.
echo Running Backend Tests...
cd backend
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -q -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term --cov-report=html
cd ..
echo.
echo Running Frontend Tests...
cd frontend
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
call npm run test:coverage
cd ..
goto end

:quick
echo.
echo Running Quick Tests...
cd backend
pytest tests/ -v --no-cov
cd ..
cd frontend
call npm test
cd ..
goto end

:invalid
echo Invalid choice
exit /b 1

:end
echo.
echo Test suite completed!
pause
