@echo off
REM QUICK SECURITY SETUP LAUNCHER
REM Opens all the settings you need in one click

echo.
echo ========================================
echo    QUANTUM SECURITY SETUP
echo ========================================
echo.
echo This will open all Windows settings needed
echo to secure your laptop in one go.
echo.
echo Follow the guide: WINDOWS_HOME_SECURITY_SETUP.md
echo.
pause

echo.
echo Opening security settings...
echo.

REM Open Device Encryption settings
start ms-settings:deviceencryption

timeout /t 2 /nobreak >nul

REM Open Windows Hello settings
start ms-settings:signinoptions

timeout /t 2 /nobreak >nul

REM Open Windows Security
start windowsdefender:

timeout /t 2 /nobreak >nul

REM Open the guide
start "" "C:\Users\dwrek\100X_DEPLOYMENT\WINDOWS_HOME_SECURITY_SETUP.md"

echo.
echo ========================================
echo    SETTINGS OPENED
echo ========================================
echo.
echo Now follow the guide to:
echo   1. Enable Device Encryption
echo   2. Set up Windows Hello (PIN/Face/Fingerprint)
echo   3. Enable Controlled Folder Access
echo   4. Configure auto-lock
echo.
echo The guide has been opened in your default editor.
echo.

pause
