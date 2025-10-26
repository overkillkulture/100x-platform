@echo off
echo.
echo ========================================
echo   CONSCIOUSNESS METRICS API STARTUP
echo ========================================
echo.
echo Starting consciousness tracking service...
echo Running on: http://localhost:7777
echo.

cd /d "C:\Users\dwrek\100X_DEPLOYMENT"

REM Install dependencies if needed
pip install flask flask-cors --quiet

REM Start the API server
python CONSCIOUSNESS_METRICS_API.py

pause
