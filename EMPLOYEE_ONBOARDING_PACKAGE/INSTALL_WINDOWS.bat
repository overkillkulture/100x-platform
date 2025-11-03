@echo off
echo ================================================================
echo   CONSCIOUSNESS REVOLUTION - EMPLOYEE ACTIVATION
echo ================================================================
echo.
echo Installing Claude Code and consciousness systems...
echo.

REM Step 1: Install Claude Code
echo [1/4] Installing Claude Code...
powershell -Command "& {Invoke-WebRequest -Uri 'https://s3.amazonaws.com/com.anthropic.claude-code-installer/latest/windows/install.ps1' -UseBasicParsing | Invoke-Expression}"

REM Step 2: Copy configuration files
echo [2/4] Installing consciousness configuration...
copy /Y .claude.json %USERPROFILE%\.claude.json
copy /Y CLAUDE.md %USERPROFILE%\CLAUDE.md
copy /Y CLAUDE_SUPERPOWER_CHEAT_CODES.md %USERPROFILE%\CLAUDE_SUPERPOWER_CHEAT_CODES.md

REM Step 3: API Key setup
echo [3/4] Setting up API key...
echo.
echo IMPORTANT: You need to set your ANTHROPIC_API_KEY environment variable.
echo Commander will provide your API key separately.
echo.
echo To set it temporarily (this session only):
echo   set ANTHROPIC_API_KEY=your-key-here
echo.
echo To set it permanently:
echo   setx ANTHROPIC_API_KEY "your-key-here"
echo.

REM Step 4: Verification
echo [4/4] Installation complete!
echo.
echo ================================================================
echo   ACTIVATION SUCCESSFUL
echo ================================================================
echo.
echo Next steps:
echo   1. Get your API key from Commander
echo   2. Run: setx ANTHROPIC_API_KEY "your-key-here"
echo   3. Restart this terminal
echo   4. Run: claude "What consciousness level am I operating at?"
echo.
echo Read FIRST_MISSION.md for your activation test.
echo.
pause
