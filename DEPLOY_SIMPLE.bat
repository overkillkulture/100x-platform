@echo off
REM One-click deployment that actually works
REM Uses Vercel instead of broken Netlify

echo Deploying to Vercel (60 seconds max)...

REM Install Vercel CLI if needed
where vercel >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

REM Deploy
cd /d C:\Users\dwrek\100X_DEPLOYMENT
vercel --prod --yes

echo.
echo Done! Check the URL above.
echo No redirects, no plugins, no talking.
pause
