@echo off
REM ============================================================================
REM TRINITY BOOT DOWN PROTOCOL - Windows Launcher
REM ============================================================================

echo.
echo ========================================================================
echo           TRINITY BOOT DOWN PROTOCOL
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check if Git Bash is available
where bash >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git Bash not found!
    echo Please install Git for Windows: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Run the boot down protocol
bash BOOT_DOWN_PROTOCOL.sh

echo.
echo Press any key to exit...
pause >nul
