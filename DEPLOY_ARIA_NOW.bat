@echo off
REM ⚡ DEPLOY ARIA TO PRODUCTION ⚡

echo.
echo ========================================
echo   DEPLOYING ARIA AI ASSISTANT
echo ========================================
echo.

cd "C:\Users\dwrek\100X_DEPLOYMENT"

echo [1/4] Checking files...
if exist "ASSETS\js\aria.js" (
    echo ✅ ARIA script found
) else (
    echo ❌ ARIA script missing!
    pause
    exit /b 1
)

if exist "aria-demo.html" (
    echo ✅ ARIA demo found
) else (
    echo ❌ ARIA demo missing!
    pause
    exit /b 1
)

echo.
echo [2/4] Adding files to git...
git add ASSETS/js/aria.js
git add aria-demo.html
git add PUBLIC/pattern-filter.html
git add index.html
git add DEPLOY_ARIA_NOW.bat

echo.
echo [3/4] Committing changes...
git commit -m "✨ Add ARIA AI Assistant Character

- Created holographic consciousness-themed AI guide
- Integrated ARIA into Pattern Filter quiz
- Built interactive demo page
- Celebrates Builder unlocks and guides users
- Weird Science inspiration, professional execution

🤖 ARIA is ready to help users on their consciousness journey!"

echo.
echo [4/4] Deploying to Netlify...
netlify deploy --prod

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo ✅ ARIA is now live at:
echo    https://conciousnessrevolution.io
echo.
echo ✅ Try her out:
echo    https://conciousnessrevolution.io/PUBLIC/pattern-filter.html
echo.
echo ✅ See demo:
echo    https://conciousnessrevolution.io/aria-demo.html
echo.
pause
