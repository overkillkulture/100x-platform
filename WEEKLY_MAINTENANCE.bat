@echo off
REM MASTER WEEKLY MAINTENANCE
REM Runs all weekly maintenance tasks in sequence

echo.
echo ========================================
echo    WEEKLY MAINTENANCE - STARTING
echo ========================================
echo.
echo This runs every Sunday to keep systems healthy
echo.
echo Tasks:
echo   1. Desktop Organization
echo   2. Security Check
echo   3. Health Check
echo   4. Backup
echo.

set START_TIME=%time%

REM 1. DESKTOP ORGANIZATION
echo.
echo ========================================
echo [1/4] DESKTOP ORGANIZATION
echo ========================================
echo.
python "C:\Users\dwrek\100X_DEPLOYMENT\DESKTOP_ORGANIZER.py" --execute
echo.

REM 2. SECURITY CHECK
echo.
echo ========================================
echo [2/4] SECURITY CHECK
echo ========================================
echo.
python "C:\Users\dwrek\100X_DEPLOYMENT\WEEKLY_SECURITY_CHECK.py"
echo.

REM 3. HEALTH CHECK
echo.
echo ========================================
echo [3/4] HEALTH CHECK
echo ========================================
echo.
python "C:\Users\dwrek\100X_DEPLOYMENT\WEEKLY_HEALTH_CHECK.py"
echo.

REM 4. BACKUP
echo.
echo ========================================
echo [4/4] BACKUP
echo ========================================
echo.
call "C:\Users\dwrek\100X_DEPLOYMENT\WEEKLY_BACKUP.bat"
echo.

set END_TIME=%time%

echo.
echo ========================================
echo    WEEKLY MAINTENANCE - COMPLETE
echo ========================================
echo.
echo Started: %START_TIME%
echo Finished: %END_TIME%
echo.
echo All weekly tasks completed successfully!
echo.
echo Check these reports:
echo   • SECURITY_REPORT_*.txt
echo   • HEALTH_REPORT_*.txt
echo   • Desktop\_BACKUPS\
echo.
echo Next maintenance: Next Sunday
echo.

pause
