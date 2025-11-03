@echo off
REM 🚀 START INSTAGRAM GROWTH BOT
REM One-click start for Instagram automation

echo.
echo ========================================
echo 🚀 INSTAGRAM GROWTH BOT
echo ========================================
echo.

REM Check if ANTHROPIC_API_KEY is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo ⚠️  WARNING: ANTHROPIC_API_KEY not set
    echo.
    echo AI comment generation will use fallback mode.
    echo For best results, set your API key:
    echo    setx ANTHROPIC_API_KEY "your_key_here"
    echo.
    pause
)

echo Starting Instagram growth session...
echo.
echo Default settings:
echo   - Hashtags: entrepreneur, startup, business
echo   - Posts per hashtag: 10
echo   - Like rate: 80%%
echo   - Comment rate: 20%% (AI-powered)
echo   - Follow rate: 30%%
echo.
echo ⏰ Estimated duration: 30-45 minutes
echo 📊 Expected results: 30-50 likes, 6-10 comments, 9-15 follows
echo.

python INSTAGRAM_GROWTH_ENGINE.py --hashtags entrepreneur startup business --posts 10

echo.
echo ========================================
echo ✅ SESSION COMPLETE
echo ========================================
echo.
echo Check instagram_growth.db for analytics
echo.
pause
