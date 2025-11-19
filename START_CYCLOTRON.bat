@echo off
echo.
echo ╔════════════════════════════════════════════════╗
echo ║        STARTING AUTONOMOUS CYCLOTRON           ║
echo ╚════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo Checking for Node.js...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found! Please install Node.js first.
    pause
    exit /b 1
)

echo Node.js found:
node --version
echo.

echo Starting Cyclotron Server...
echo.
node cyclotron_server.js

pause
