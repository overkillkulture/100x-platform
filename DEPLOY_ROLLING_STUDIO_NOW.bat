@echo off
REM ========================================
REM ROLLING STUDIO ONE-CLICK DEPLOYMENT
REM No PowerShell. No sword fighting. Just works.
REM ========================================

echo.
echo ========================================
echo    ROLLING STUDIO DEPLOYMENT
echo ========================================
echo.
echo This will set up your rolling studio automation.
echo No manual config. No PowerShell battles.
echo Just answer a few questions and we're done.
echo.
pause

REM Check Python installed
echo.
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ERROR: Python not found!
    echo    Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo    OK: Python installed

REM Check if we're in the right folder
echo.
echo [2/5] Checking location...
if not exist "AI_ROLLING_STUDIO_PROCESSOR.py" (
    echo    ERROR: Run this from 100X_DEPLOYMENT folder!
    pause
    exit /b 1
)
echo    OK: In correct folder

REM Install dependencies (if needed)
echo.
echo [3/5] Installing dependencies...
echo    This might take 2-3 minutes first time...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet requests
python -m pip install --quiet tweepy
echo    OK: Dependencies ready

REM Run setup wizard
echo.
echo [4/5] Running setup wizard...
python ROLLING_STUDIO_SETUP_WIZARD.py

if errorlevel 1 (
    echo    Setup cancelled or failed.
    pause
    exit /b 1
)

REM Done
echo.
echo [5/5] Deployment complete!
echo.
echo ========================================
echo    ROLLING STUDIO IS READY
echo ========================================
echo.
echo What you can do now:
echo   1. Test with video: DROP_VIDEO_HERE.bat
echo   2. Start auto-posting: START_AUTO_POSTER.bat
echo   3. View dashboard: ROLLING_STUDIO_DASHBOARD.bat
echo.
echo Instructions saved to: ROLLING_STUDIO_INSTRUCTIONS.txt
echo.
pause
