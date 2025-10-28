@echo off
echo ======================================================================
echo 🚀 DEPLOYING ARAYA EXTENSION - PROFESSIONAL BETA PACKAGE
echo ======================================================================
echo.
echo This will deploy the following updates:
echo   ✅ Auto-installer page (ARAYA_AUTO_INSTALLER.html)
echo   ✅ Clean extension package (ARAYA_EXTENSION_BETA_v1.0.zip)
echo   ✅ Updated download pages
echo.
echo Press CTRL+C to cancel, or
pause

echo.
echo 📦 Files being deployed:
echo   - ARAYA_AUTO_INSTALLER.html
echo   - ARAYA_EXTENSION_BETA_v1.0.zip
echo   - download-jarvis.html (updated)
echo   - downloads.html (updated)
echo.

cd "C:\Users\dwrek\100X_DEPLOYMENT"

echo 🌐 Deploying to Netlify...
netlify deploy --prod

echo.
echo ======================================================================
echo ✅ DEPLOYMENT COMPLETE!
echo ======================================================================
echo.
echo 📍 Live URLs:
echo   https://conciousnessrevolution.io/ARAYA_AUTO_INSTALLER.html
echo   https://conciousnessrevolution.io/download-jarvis.html
echo   https://conciousnessrevolution.io/downloads.html
echo.
echo 📢 Ready to announce to beta testers!
echo.
pause
