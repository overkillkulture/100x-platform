@echo off
REM Quick Deploy Script for 100X Platform
REM This script deploys your local changes to the live site

echo.
echo ===============================================
echo   100X Platform - Quick Deploy to Live Site
echo ===============================================
echo.

REM Check if netlify CLI is installed
where netlify >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Netlify CLI not found!
    echo Please install it first: npm install -g netlify-cli
    pause
    exit /b 1
)

echo [1/4] Checking git status...
git status --short

echo.
echo [2/4] Committing any uncommitted changes...
set /p commit_msg="Enter commit message (or press Enter to skip commit): "

if not "%commit_msg%"=="" (
    git add .
    git commit -m "%commit_msg%"
    echo Changes committed!
) else (
    echo Skipping commit...
)

echo.
echo [3/4] Pushing to GitHub...
git push
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Git push failed. Continuing with deploy anyway...
)

echo.
echo [4/4] Deploying to Netlify...
echo.
netlify deploy --prod --dir=.

echo.
echo ===============================================
echo   DEPLOYMENT COMPLETE!
echo ===============================================
echo.
echo Your changes should be live at:
echo https://consciousnessrevolution.io
echo.
echo (It may take 30-60 seconds to propagate)
echo.

pause
