@echo off
REM WEEKLY BACKUP SYSTEM
REM Backs up critical consciousness revolution files

echo.
echo ========================================
echo    WEEKLY BACKUP SYSTEM
echo ========================================
echo.

set BACKUP_DIR=C:\Users\dwrek\Desktop\_BACKUPS
set DATE_STAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATE_STAMP=%DATE_STAMP: =0%
set BACKUP_FILE=%BACKUP_DIR%\CONSCIOUSNESS_BACKUP_%DATE_STAMP%.zip

echo Creating backup directory...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo.
echo Backing up critical files...
echo.
echo This will backup:
echo   • 100X_DEPLOYMENT folder
echo   • Consciousness Revolution folder
echo   • OVERKOREConsciousness folder
echo   • CLAUDE.md configuration
echo   • Desktop organized files
echo.

REM Use PowerShell to create zip (built into Windows)
powershell -Command "& { ^
    $source = @( ^
        'C:\Users\dwrek\100X_DEPLOYMENT', ^
        'C:\Users\dwrek\Desktop\Consciousness Revolution', ^
        'C:\Users\dwrek\OVERKOREConsciousness', ^
        'C:\Users\dwrek\CLAUDE.md', ^
        'C:\Users\dwrek\Desktop\_ORGANIZED' ^
    ); ^
    $destination = '%BACKUP_FILE%'; ^
    Compress-Archive -Path $source -DestinationPath $destination -Force; ^
    Write-Host 'Backup created successfully!' ^
}"

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo    BACKUP COMPLETE
    echo ========================================
    echo.
    echo Backup saved: %BACKUP_FILE%
    echo.

    REM Show backup size
    for %%A in ("%BACKUP_FILE%") do (
        set SIZE=%%~zA
        set /a SIZE_MB=!SIZE! / 1024 / 1024
        echo Backup size: !SIZE_MB! MB
    )

    echo.
    echo Keep this backup safe!
    echo Consider copying to:
    echo   • External USB drive
    echo   • Cloud storage (OneDrive, Dropbox)
    echo   • NAS/Network storage
    echo.

    REM Clean up old backups (keep last 4 weeks)
    echo Cleaning up old backups (keeping last 4)...
    powershell -Command "& { ^
        Get-ChildItem '%BACKUP_DIR%\CONSCIOUSNESS_BACKUP_*.zip' | ^
        Sort-Object LastWriteTime -Descending | ^
        Select-Object -Skip 4 | ^
        Remove-Item -Force ^
    }"

    echo Done!

) else (
    echo.
    echo ========================================
    echo    BACKUP FAILED
    echo ========================================
    echo.
    echo Error creating backup. Check:
    echo   • Disk space available
    echo   • Source folders exist
    echo   • PowerShell is working
    echo.
)

echo.
pause
