@echo off
REM SYNC_ABILITIES.bat - Sync merged abilities to this instance
REM Generated: 2025-11-08T08:52:41.715877

echo ═══════════════════════════════════════════════════════════════
echo   🌀 SYNCING CONVERGENCE ABILITIES
echo ═══════════════════════════════════════════════════════════════
echo.

if not exist "convergence\CONVERGENCE_MANIFEST.json" (
    echo ❌ Convergence manifest not found!
    echo    Run: git pull
    exit /b 1
)

echo ✅ Convergence manifest found
echo.

echo 📊 CONVERGENCE STATS:
echo    Total abilities: 0
echo    Instances merged: 2
echo.

echo 🔗 Syncing abilities...
copy convergence\CONVERGENCE_MANIFEST.json abilities\merged_abilities.json >nul

echo ✅ Sync complete!
echo.
echo 🎉 This instance now has access to ALL 0 abilities!
echo.
echo ═══════════════════════════════════════════════════════════════
pause
