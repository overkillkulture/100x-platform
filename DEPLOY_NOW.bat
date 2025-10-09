@echo off
echo.
echo ========================================
echo   DEPLOYING OVERKOR TEKNOLOGIES SITE
echo   TO NETLIFY
echo ========================================
echo.

cd C:\Users\dwrek\100X_DEPLOYMENT

echo Deploying complete catalog (12 products: 9 kits + 3 courses)...
echo.

netlify deploy --prod --dir=. --site=fantastic-twilight-28b317

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your site is now live at:
echo https://fantastic-twilight-28b317.netlify.app
echo.
echo OR if domain connected:
echo https://overkillkulture.com
echo.
pause
