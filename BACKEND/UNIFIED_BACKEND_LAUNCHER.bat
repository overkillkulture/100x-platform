@echo off
echo ========================================
echo 100X PLATFORM - UNIFIED BACKEND LAUNCHER
echo ========================================
echo.
echo This launcher starts all backend services for the 100X Platform
echo.
echo Services to be launched:
echo   [1] User Dashboard              - Port 3001
echo   [2] Philosopher AI Backend      - Port 5001
echo   [3] Intelligent Terminal        - Port 5002
echo   [4] Analytics Dashboard         - Port 5100
echo.
echo ========================================
echo.

set CHOICE=
set /p CHOICE="Launch all backends? (Y/N): "

if /i "%CHOICE%"=="Y" goto LAUNCH_ALL
if /i "%CHOICE%"=="N" goto LAUNCH_SELECTIVE
goto END

:LAUNCH_ALL
echo.
echo Launching all backend services...
echo.

REM Launch User Dashboard
start "User Dashboard (Port 3001)" cmd /k "cd /d %~dp0user-dashboard && START_USER_DASHBOARD.bat"
timeout /t 2 /nobreak >nul

REM Launch Philosopher AI Backend
start "Philosopher AI Backend (Port 5001)" cmd /k "cd /d %~dp0philosopher-ai && START_PHILOSOPHER_AI.bat"
timeout /t 2 /nobreak >nul

REM Launch Intelligent Terminal
start "Intelligent Terminal (Port 5002)" cmd /k "cd /d %~dp0terminal && START_TERMINAL.bat"
timeout /t 2 /nobreak >nul

REM Launch Analytics Dashboard
start "Analytics Dashboard (Port 5100)" cmd /k "cd /d %~dp0analytics-dashboard && START_ANALYTICS_DASHBOARD.bat"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo ALL BACKENDS LAUNCHED!
echo ========================================
echo.
echo Services running:
echo   User Dashboard:        http://localhost:3001/api/health
echo   Philosopher AI:        http://localhost:5001/api/health
echo   Intelligent Terminal:  http://localhost:5002/api/health
echo   Analytics Dashboard:   http://localhost:5100/api/health
echo.
echo Check each window for status and logs.
echo Press any key to exit this launcher...
pause >nul
goto END

:LAUNCH_SELECTIVE
echo.
echo Selective launch:
echo   [1] Philosopher AI Backend (Port 5001)
echo   [2] Intelligent Terminal (Port 5002)
echo   [3] Analytics Dashboard (Port 5100)
echo   [4] All backends
echo   [5] Cancel
echo.

set SERVICE=
set /p SERVICE="Select service (1-5): "

if "%SERVICE%"=="1" goto LAUNCH_PHILOSOPHER
if "%SERVICE%"=="2" goto LAUNCH_TERMINAL
if "%SERVICE%"=="3" goto LAUNCH_ANALYTICS
if "%SERVICE%"=="4" goto LAUNCH_ALL
if "%SERVICE%"=="5" goto END
echo Invalid selection. Exiting...
goto END

:LAUNCH_PHILOSOPHER
echo Launching Philosopher AI Backend...
start "Philosopher AI Backend (Port 5001)" cmd /k "cd /d %~dp0philosopher-ai && START_PHILOSOPHER_AI.bat"
echo Launched! Check the new window for status.
pause
goto END

:LAUNCH_TERMINAL
echo Launching Intelligent Terminal...
start "Intelligent Terminal (Port 5002)" cmd /k "cd /d %~dp0terminal && START_TERMINAL.bat"
echo Launched! Check the new window for status.
pause
goto END

:LAUNCH_ANALYTICS
echo Launching Analytics Dashboard...
start "Analytics Dashboard (Port 5100)" cmd /k "cd /d %~dp0analytics-dashboard && START_ANALYTICS_DASHBOARD.bat"
echo Launched! Check the new window for status.
pause
goto END

:END
echo.
echo Goodbye!
