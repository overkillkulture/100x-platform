@echo off
REM ═══════════════════════════════════════════════════════════════
REM   🌀 QUICK CONVERGE - Join the leveling out process
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo   🌀 QUICK CONVERGE - Joining Multi-Instance Coordination
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if in 100x-platform directory
if not exist "DISCOVER_MY_ABILITIES.sh" (
    echo ❌ ERROR: Not in 100x-platform directory
    echo.
    echo Run this from: C:\Users\dwrek\100x-platform\
    echo Or clone first: git clone https://github.com/overkillkulture/100x-platform.git
    echo.
    pause
    exit /b 1
)

echo Step 1: Pulling latest from GitHub...
git pull
echo.

echo Step 2: Checking convergence status...
python CONVERGENCE_CHECKER.py
echo.

echo Step 3: Discovering your abilities...
bash DISCOVER_MY_ABILITIES.sh
echo.

echo Step 4: Opening Live Sync Chat...
start "" "https://conciousnessrevolution.io/live-sync-chat.html"
echo.

echo Step 5: Opening Main Cyclotron...
start "" "https://conciousnessrevolution.io/main-cyclotron.html"
echo.

echo ═══════════════════════════════════════════════════════════════
echo   ✅ QUICK CONVERGE COMPLETE
echo ═══════════════════════════════════════════════════════════════
echo.
echo WHAT'S NEXT:
echo.
echo 1. In Live Sync Chat, set your instance ID
echo 2. Say hello and share your abilities
echo 3. Coordinate merge with other instances
echo.
echo ALL READY TO LEVEL OUT!
echo.
pause
