@echo off
echo ========================================
echo MASTER BOOT ORCHESTRATOR v1.0
echo ========================================
echo.
echo Starting orchestrator...
echo Dashboard will be at: http://localhost:8888
echo.

cd /d "%~dp0"
python orchestrator.py

pause
