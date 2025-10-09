@echo off
REM WEEKLY DESKTOP CLEANUP
REM Runs every Sunday to keep desktop organized

echo.
echo ========================================
echo    WEEKLY DESKTOP CLEANUP
echo ========================================
echo.
echo Running desktop organizer...
echo.

python "C:\Users\dwrek\100X_DEPLOYMENT\DESKTOP_ORGANIZER.py" --execute

echo.
echo ========================================
echo    CLEANUP COMPLETE
echo ========================================
echo.
echo Your desktop is organized!
echo Check _ORGANIZED folder for all files.
echo.

pause
