@echo off
echo.
echo ============================================================
echo   CONSCIOUSNESS REVOLUTION - USB COPY UTILITY
echo ============================================================
echo.
echo This script will copy all files to your USB drive.
echo.
echo BEFORE YOU RUN THIS:
echo 1. Plug in your USB drive
echo 2. Note the drive letter (e.g., E:, F:, G:)
echo 3. Make sure USB has at least 200MB free space
echo.
pause

echo.
set /p USB_LETTER="Enter your USB drive letter (e.g., E): "

echo.
echo Checking if drive %USB_LETTER%: exists...
if not exist %USB_LETTER%:\ (
    echo ERROR: Drive %USB_LETTER%: not found!
    echo Please check the drive letter and try again.
    pause
    exit /b
)

echo Drive found!
echo.
echo Copying files to %USB_LETTER%:\...
echo.

xcopy /E /I /Y "DASHBOARDS" "%USB_LETTER%:\DASHBOARDS"
xcopy /E /I /Y "DATA" "%USB_LETTER%:\DATA"
copy /Y "autorun.inf" "%USB_LETTER%:\"
copy /Y "START_HERE.bat" "%USB_LETTER%:\"
copy /Y "START_HERE.command" "%USB_LETTER%:\"
copy /Y "QUICK_START.txt" "%USB_LETTER%:\"
copy /Y "README.txt" "%USB_LETTER%:\"
copy /Y "statistics-engine.js" "%USB_LETTER%:\"

echo.
echo ============================================================
echo   COPY COMPLETE!
echo ============================================================
echo.
echo Your USB drive at %USB_LETTER%: is now ready!
echo.
echo NEXT STEPS:
echo 1. Safely eject the USB
echo 2. Test it on another computer
echo 3. Ship to recipient!
echo.
echo See SHIPPING_CHECKLIST.md for full shipping guide.
echo.
pause
