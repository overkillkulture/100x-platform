@echo off
echo ========================================
echo ANALYTICS DASHBOARD BACKEND LAUNCHER
echo ========================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

REM Start the server
echo Starting Analytics Dashboard Backend on http://localhost:5100
echo.
python app.py

pause
