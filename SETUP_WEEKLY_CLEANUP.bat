@echo off
REM Setup Windows Task Scheduler to run desktop cleanup every Sunday

echo.
echo ========================================
echo    SETUP WEEKLY DESKTOP CLEANUP
echo ========================================
echo.
echo This will create a scheduled task to run every Sunday at 10 AM
echo.

REM Create scheduled task
schtasks /create /tn "Desktop Weekly Cleanup" /tr "C:\Users\dwrek\100X_DEPLOYMENT\WEEKLY_DESKTOP_CLEANUP.bat" /sc weekly /d SUN /st 10:00 /f

echo.
if %errorlevel% == 0 (
    echo ✅ SUCCESS: Weekly cleanup scheduled!
    echo.
    echo Task Details:
    echo   Name: Desktop Weekly Cleanup
    echo   Schedule: Every Sunday at 10:00 AM
    echo   Action: Organize desktop files
    echo.
    echo To run manually: WEEKLY_DESKTOP_CLEANUP.bat
    echo To disable: schtasks /delete /tn "Desktop Weekly Cleanup"
) else (
    echo ❌ ERROR: Could not create scheduled task
    echo You may need to run this as Administrator
)

echo.
pause
