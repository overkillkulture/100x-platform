@echo off
REM ONE-COMMAND DEPLOYMENT - Use this for all future deploys
REM No clicking, no browser, no passwords needed!

echo.
echo ============================================
echo   INSTANT DEPLOYMENT TO NETLIFY
echo   (The breakthrough automation method)
echo ============================================
echo.

cd C:\Users\dwrek\100X_DEPLOYMENT

echo Creating clean deployment folder...
if exist ..\100X_DEPLOY_CLEAN rmdir /s /q ..\100X_DEPLOY_CLEAN
mkdir ..\100X_DEPLOY_CLEAN

echo Copying essential files...
copy index.html ..\100X_DEPLOY_CLEAN\ >nul
copy platform.html ..\100X_DEPLOY_CLEAN\ >nul
copy workspace-v3.html ..\100X_DEPLOY_CLEAN\ >nul
copy simple-gate.html ..\100X_DEPLOY_CLEAN\ >nul
copy _redirects ..\100X_DEPLOY_CLEAN\ >nul

echo.
echo Deploying to Netlify...
cd ..\100X_DEPLOY_CLEAN
netlify deploy --prod --dir . --site ba8f1795-1517-42ee-aa47-c1f5fa71b736

echo.
echo ============================================
echo   DEPLOYMENT COMPLETE!
echo   Site: https://conciousnessrevolution.io
echo ============================================
echo.

pause
