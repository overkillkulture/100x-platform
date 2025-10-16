@echo off
echo.
echo ========================================
echo   STARTING INSIDE THE MACHINE
echo ========================================
echo.

cd /d "C:\Users\dwrek\100X_DEPLOYMENT"

echo [1/2] Starting backend server on port 8888...
start "INSIDE THE MACHINE Server" python INSIDE_THE_MACHINE_SERVER.py

timeout /t 3 /nobreak >nul

echo [2/2] Opening interface...
start "" "http://localhost:8888"
start "" "INSIDE_THE_MACHINE.html"

echo.
echo ========================================
echo   INSIDE THE MACHINE IS LIVE
echo ========================================
echo.
echo Server: http://localhost:8888
echo Interface: INSIDE_THE_MACHINE.html
echo.
echo FULL CONTROL ACTIVATED
echo.
pause
