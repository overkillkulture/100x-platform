@echo off
echo ========================================
echo EMERGENCY AI TERMINAL - STARTING
echo ========================================
echo.
echo This will start a public AI terminal for your website.
echo Duration: 24 hours (all day)
echo Limit: 500 messages total (100 per user)
echo Cost: ~$10 max (probably $0-1 with real traffic)
echo.
echo ========================================
echo.

cd /d "%~dp0BACKEND"

echo Checking API key...
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY environment variable not set!
    echo.
    echo Please set your API key first:
    echo   set ANTHROPIC_API_KEY=your-key-here
    echo.
    pause
    exit /b 1
)

echo API key found!
echo.
echo Starting emergency terminal proxy...
echo.

python emergency_terminal_proxy.py

pause
