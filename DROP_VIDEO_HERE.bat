@echo off
REM ========================================
REM ROLLING STUDIO - DROP VIDEO HERE
REM Simplest possible test. No config needed.
REM ========================================

echo.
echo ========================================
echo    ROLLING STUDIO TEST
echo ========================================
echo.
echo This will process any video you drop here.
echo.
echo INSTRUCTIONS:
echo   1. Drag and drop ANY video file onto this batch file
echo   2. OR: Rename your video to "test_drive_footage.mp4"
echo.

REM Check if a file was dragged onto this batch file
if not "%~1"=="" (
    echo Detected file: %~nx1
    echo.
    echo Processing...
    python AI_ROLLING_STUDIO_PROCESSOR.py "%~1"
    goto end
)

REM Otherwise look for test_drive_footage.mp4
if exist "test_drive_footage.mp4" (
    echo Found: test_drive_footage.mp4
    echo.
    echo Processing...
    python AI_ROLLING_STUDIO_PROCESSOR.py test_drive_footage.mp4
    goto end
)

REM No video found
echo.
echo ERROR: No video file found!
echo.
echo Please either:
echo   - Drag and drop a video onto this batch file
echo   - OR: Place a video named "test_drive_footage.mp4" in this folder
echo.
pause
exit /b 1

:end
echo.
echo ========================================
echo    PROCESSING COMPLETE!
echo ========================================
echo.
echo Results saved to: rolling_studio_output\
echo.
echo You'll find:
echo   - Transcript (what you said)
echo   - Clips (best moments)
echo   - Captions (SRT files)
echo   - Posting schedule (when to post)
echo.
explorer rolling_studio_output
pause
