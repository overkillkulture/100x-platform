@echo off
echo ================================================================
echo  STARTING LOCAL NERVOUS SYSTEM
echo ================================================================
echo.
echo  Port 6000: Local Nerve Collector (visitor tracking)
echo  Port 7776: Communication Nervous System
echo.
echo  Analytics will work IN-HOUSE (no cloud dependency)
echo.
echo ================================================================
echo.

start "Local Nerve Collector" cmd /c "cd C:\Users\dwrek\100X_DEPLOYMENT && python LOCAL_NERVE_COLLECTOR.py"

timeout /t 2 /nobreak > nul

start "Nervous System Analytics" "C:\Users\dwrek\100X_DEPLOYMENT\NERVOUS_SYSTEM_ANALYTICS.html"

echo.
echo  All systems started!
echo  Open: NERVOUS_SYSTEM_ANALYTICS.html to see the nerves fire
echo.
pause
