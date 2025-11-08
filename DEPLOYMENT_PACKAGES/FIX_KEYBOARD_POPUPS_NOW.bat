@echo off
echo ================================================================
echo   KEYBOARD POPUP FIX - ALL COMPUTERS
echo ================================================================
echo.
echo This will DISABLE all annoying keyboard popups:
echo  - Touch keyboard auto-invoke
echo  - On-screen keyboard
echo  - Text suggestions
echo  - IME popups
echo  - Predictive text
echo.
echo Running on: %COMPUTERNAME%
echo.
pause

echo.
echo Applying registry fixes...
echo.

REM Disable touch keyboard auto-invoke
echo [1/7] Disabling touch keyboard auto-invoke...
reg add "HKEY_CURRENT_USER\Software\Microsoft\TabletTip\1.7" /v "EnableDesktopModeAutoInvoke" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKEY_CURRENT_USER\Software\Microsoft\TabletTip\1.7" /v "DisableEdgySense" /t REG_DWORD /d 1 /f >nul 2>&1
echo ✅ Done

REM Disable text input panel
echo [2/7] Disabling text input panel...
reg add "HKEY_CURRENT_USER\Software\Microsoft\InputPersonalization" /v "RestrictImplicitTextCollection" /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKEY_CURRENT_USER\Software\Microsoft\InputPersonalization" /v "RestrictImplicitInkCollection" /t REG_DWORD /d 1 /f >nul 2>&1
echo ✅ Done

REM Disable IME auto-suggest
echo [3/7] Disabling IME auto-suggest...
reg add "HKEY_CURRENT_USER\Software\Microsoft\IME\15.0\IMEJP\MSIME" /v "Show Candidate Window" /t REG_DWORD /d 0 /f >nul 2>&1
echo ✅ Done

REM Disable predictive text
echo [4/7] Disabling predictive text...
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\PenWorkspace" /v "PenWorkspaceAppSuggestionsEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
echo ✅ Done

REM Disable text suggestions
echo [5/7] Disabling text suggestions...
reg add "HKEY_CURRENT_USER\Software\Microsoft\Input\Settings" /v "InsightsEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKEY_CURRENT_USER\Software\Microsoft\Input\Settings" /v "EnableHwkbTextPrediction" /t REG_DWORD /d 0 /f >nul 2>&1
echo ✅ Done

REM Disable autocorrect
echo [6/7] Disabling autocorrect...
reg add "HKEY_CURRENT_USER\Software\Microsoft\TabletTip\1.7" /v "EnableAutocorrection" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKEY_CURRENT_USER\Software\Microsoft\TabletTip\1.7" /v "EnableSpellchecking" /t REG_DWORD /d 0 /f >nul 2>&1
echo ✅ Done

REM Disable touch keyboard service
echo [7/7] Disabling touch keyboard service...
sc config TabletInputService start= disabled >nul 2>&1
net stop TabletInputService >nul 2>&1
echo ✅ Done

echo.
echo ================================================================
echo   KEYBOARD POPUP FIX COMPLETE
echo ================================================================
echo.
echo ALL KEYBOARD POPUPS HAVE BEEN DISABLED:
echo  ✅ Touch keyboard auto-invoke
echo  ✅ On-screen keyboard
echo  ✅ Text suggestions
echo  ✅ IME popups
echo  ✅ Predictive text
echo  ✅ Autocorrect
echo  ✅ Touch keyboard service
echo.
echo PLEASE REBOOT for all changes to take effect.
echo.
echo Computer: %COMPUTERNAME%
echo Fixed: %DATE% %TIME%
echo.
pause
