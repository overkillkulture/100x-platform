@echo off
echo.
echo ========================================
echo   SOCIAL MEDIA AUTOMATION LAUNCHER
echo ========================================
echo.
echo Choose an option:
echo.
echo [1] Full Automation (Create video + Post to all platforms)
echo [2] Quick Repost (Use existing videos)
echo [3] Analytics Dashboard
echo [4] Test All Platforms
echo [5] Setup APIs (First-time only)
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto full
if "%choice%"=="2" goto quick
if "%choice%"=="3" goto analytics
if "%choice%"=="4" goto test
if "%choice%"=="5" goto setup
goto end

:full
echo.
echo Starting Full Automation...
python FULL_SOCIAL_AUTOMATION.py
goto end

:quick
echo.
echo Starting Quick Repost...
python FULL_SOCIAL_AUTOMATION.py --quick
goto end

:analytics
echo.
echo Starting Analytics Dashboard...
echo Dashboard will open at: http://localhost:8888
python ANALYTICS_DASHBOARD.py
goto end

:test
echo.
echo Testing All Platforms...
echo.
echo Testing Late API (TikTok/LinkedIn/Facebook)...
python LATE_API_WRAPPER.py
echo.
echo Testing YouTube...
python YOUTUBE_UPLOADER.py
echo.
echo Testing Twitter...
python TWITTER_PLAYWRIGHT_POSTER.py
echo.
echo Testing Instagram Helper...
python INSTAGRAM_HELPER.py
goto end

:setup
echo.
echo API SETUP GUIDE
echo ========================================
echo.
echo 1. Late API:
echo    - Go to: https://appsumo.com/products/late/
echo    - Buy for $59 (one-time)
echo    - Get API key
echo    - Run: setx LATE_API_KEY "your_key_here"
echo.
echo 2. YouTube API:
echo    - Go to: https://console.cloud.google.com/
echo    - Create project + Enable YouTube Data API v3
echo    - Create OAuth credentials
echo    - Save as youtube_client_secrets.json
echo.
echo 3. Twitter:
echo    - Run: python TWITTER_PLAYWRIGHT_POSTER.py --setup
echo.
echo Full guide: SETUP_INSTRUCTIONS.md
echo.
pause
goto end

:end
echo.
pause
