@echo off
title SETTING UP CENTRAL STORAGE HUB
color 0A

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo       ⚡ SETTING UP CENTRAL STORAGE HUB ⚡
echo.
echo       Single source of truth for all computers
echo       - Git-based version control
echo       - Automatic synchronization
echo       - Works offline
echo       - FREE and permanent
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

echo Step 1: Creating central hub directory...
if not exist "C:\Users\dwrek\.consciousness" mkdir "C:\Users\dwrek\.consciousness"
if not exist "C:\Users\dwrek\.consciousness\central_hub" mkdir "C:\Users\dwrek\.consciousness\central_hub"
echo ✅ Directory created
echo.

echo Step 2: Initializing bare Git repository (central hub)...
cd "C:\Users\dwrek\.consciousness\central_hub"
git init --bare
echo ✅ Central hub initialized
echo.

echo Step 3: Creating Computer 1 workspace...
cd "C:\Users\dwrek\.consciousness"
if exist "computer_1" rmdir /s /q "computer_1"
git clone "C:\Users\dwrek\.consciousness\central_hub" "computer_1"
echo ✅ Workspace created
echo.

echo Step 4: Copying current work to central...
xcopy "C:\Users\dwrek\100X_DEPLOYMENT\*" "C:\Users\dwrek\.consciousness\computer_1\code\" /E /I /Y
echo ✅ Files copied
echo.

echo Step 5: Initial commit...
cd "C:\Users\dwrek\.consciousness\computer_1"
git add .
git commit -m "Initial commit: Computer 1 work - Central Storage established"
git push origin master
echo ✅ Initial commit pushed to central hub
echo.

echo.
echo ═══════════════════════════════════════════════════════════════
echo   ✅ CENTRAL STORAGE HUB READY!
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Location: C:\Users\dwrek\.consciousness\
echo.
echo   Structure:
echo     central_hub/     - Master repository (all computers sync here)
echo     computer_1/      - This computer's workspace
echo     computer_2/      - (will be created when Computer 2 connects)
echo     computer_3/      - (will be created when Computer 3 connects)
echo.
echo   All work now saved to central hub automatically!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
