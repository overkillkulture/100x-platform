@echo off
echo.
echo ==========================================
echo   SET SHOKZ AS DEFAULT MICROPHONE
echo ==========================================
echo.
echo Opening Windows Sound Settings...
echo.
echo STEPS:
echo 1. Find "Input" section
echo 2. Click dropdown under "Choose your input device"
echo 3. Select "Headset (OpenRun Pro by Shokz)"
echo 4. Close Settings window
echo.
echo That's it! Then try voice listener again.
echo.
timeout /t 2
start ms-settings:sound
echo.
echo Settings opened! Make the change above.
echo.
pause
