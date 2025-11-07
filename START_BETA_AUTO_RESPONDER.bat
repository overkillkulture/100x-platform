@echo off
title Beta Tester Auto-Responder
color 0E

echo ========================================
echo   BETA TESTER AUTO-RESPONDER
echo ========================================
echo.
echo Monitoring GitHub for bug submissions...
echo Auto-updating leaderboard...
echo Running every 5 minutes...
echo.
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

cd /d C:\Users\dwrek\100X_DEPLOYMENT
python BETA_TESTER_AUTO_RESPONDER.py

pause
