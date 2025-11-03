@echo off
echo ========================================
echo PUSHING TO GITHUB
echo ========================================
echo.
echo Repository: consciousness-revolution
echo Commits ready: 2 (b34652b + 1930d57)
echo Files: 733 + 16 autonomous enhancements
echo.

cd /d "C:\Users\dwrek\100X_DEPLOYMENT"

echo Setting up remote...
git remote remove origin 2>nul
git remote add origin https://github.com/overkillkulture/consciousness-revolution.git

echo.
echo Pushing to GitHub...
git push -u origin master

echo.
echo ========================================
echo GITHUB PUSH COMPLETE!
echo ========================================
pause
