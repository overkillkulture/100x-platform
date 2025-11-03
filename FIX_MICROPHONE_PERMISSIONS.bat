@echo off
REM One-click microphone permission fixer for Windows 11
REM Opens Windows Settings directly to microphone privacy page

echo.
echo ========================================
echo    MICROPHONE PERMISSION FIX
echo ========================================
echo.
echo This will open Windows Settings to enable microphone access.
echo.
echo STEPS TO FIX:
echo 1. Turn ON "Microphone access"
echo 2. Turn ON "Let apps access your microphone"
echo 3. Scroll down to "Let desktop apps access your microphone"
echo 4. Turn this ON (CRITICAL - Python is a desktop app!)
echo.
echo Opening Settings in 3 seconds...
timeout /t 3

REM Open Windows Settings directly to microphone privacy page
start ms-settings:privacy-microphone

echo.
echo ========================================
echo After enabling permissions:
echo 1. Close Settings
echo 2. Run: CHECK_MICROPHONE.bat
echo 3. Then try voice system again
echo ========================================
echo.
pause
