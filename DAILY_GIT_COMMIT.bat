@echo off
REM DAILY GIT AUTO-COMMIT
REM Automatically commits daily work to preserve it

echo.
echo ========================================
echo    DAILY GIT AUTO-COMMIT
echo ========================================
echo.

cd /d "C:\Users\dwrek\100X_DEPLOYMENT"

echo Checking for changes...
git status --short

git diff --quiet
if %errorlevel% == 0 (
    git diff --cached --quiet
    if %errorlevel% == 0 (
        echo.
        echo No changes to commit.
        echo Working tree is clean.
        goto :end
    )
)

echo.
echo Changes detected! Creating daily checkpoint...
echo.

REM Add all changes
git add .

REM Create commit with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

set COMMIT_MSG=Daily checkpoint: %mydate% %mytime%

echo Commit message: %COMMIT_MSG%
echo.

git commit -m "%COMMIT_MSG%"

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo    COMMIT SUCCESSFUL
    echo ========================================
    echo.
    echo Your work has been saved to git history.
    echo This protects against:
    echo   • Accidental deletion
    echo   • System crashes
    echo   • Bad edits (can revert)
    echo.
    echo To push to GitHub: git push
    echo.
) else (
    echo.
    echo ========================================
    echo    COMMIT FAILED
    echo ========================================
    echo.
    echo Check git status for issues.
    echo.
)

:end
echo.
pause
