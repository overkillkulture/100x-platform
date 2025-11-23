@echo off
echo ========================================
echo INTELLIGENT TERMINAL BACKEND LAUNCHER
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

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file to configure:
    echo   - ANTHROPIC_API_KEY for AI responses
    echo   - TERMINAL_CODEWORD for access control
    echo.
)

REM Start the server
echo Starting Intelligent Terminal Backend on http://localhost:5002
echo.
python app.py

pause
