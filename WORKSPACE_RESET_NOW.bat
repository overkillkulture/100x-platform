@echo off
echo ====================================
echo WORKSPACE RESET PROTOCOL
echo ====================================
echo.
echo Step 1: Exporting all user data...
cd C:\Users\dwrek\100X_DEPLOYMENT
python USER_DATA_EXPORT_SYSTEM.py
echo.
echo Step 2: Clearing workspace stuck state...
curl -X POST http://localhost:7779/workspace/clear-stuck
echo.
echo Step 3: Opening fresh workspace...
start http://localhost:8003/workspace-v3.html
echo.
echo ====================================
echo RESET COMPLETE!
echo ====================================
echo.
echo Users can now access the updated workspace at:
echo http://localhost:8003/workspace-v3.html
echo.
echo Their data has been exported to:
echo C:\Users\dwrek\100X_DEPLOYMENT\USER_EXPORTS
echo.
pause
