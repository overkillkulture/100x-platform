@echo off
echo.
echo ========================================
echo   CONSCIOUSNESS REVOLUTION USB v1.0
echo ========================================
echo.
echo Starting dashboard...
echo.

REM Get the drive letter of this USB
set "USB_DRIVE=%~d0"

REM Launch the main dashboard
start "" "%USB_DRIVE%\DASHBOARDS\USB_CONSCIOUSNESS_COCKPIT.html"

echo.
echo Dashboard launched!
echo.
echo Keep this USB drive plugged in.
echo Your consciousness data is tracked here.
echo.
pause
