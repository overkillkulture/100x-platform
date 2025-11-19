@echo off
REM Quick fix to make homepage show login page instead of "Coming Soon"

echo.
echo ============================================
echo   FIXING HOMEPAGE - ONE COMMAND
echo ============================================
echo.

cd C:\Users\dwrek\100X_DEPLOYMENT

echo Updating _redirects to point to login page...
echo /  /simple-gate.html  302 > _redirects
echo /screening  /simple-gate.html  302 >> _redirects

echo.
echo Updated! Now deploying...
echo.

call INSTANT_DEPLOY.bat

echo.
echo ============================================
echo   DONE!
echo   Visit: https://conciousnessrevolution.io
echo   Should now show LOGIN PAGE
echo ============================================
echo.

pause
