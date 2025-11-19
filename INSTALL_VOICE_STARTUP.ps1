# Install Voice Wake Word Listener to Windows Startup
# Runs automatically when Windows starts

Write-Host "🎤 INSTALLING WAKE WORD LISTENER TO STARTUP" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Create startup shortcut
$WshShell = New-Object -ComObject WScript.Shell
$StartupFolder = [Environment]::GetFolderPath('Startup')
$ShortcutPath = "$StartupFolder\Claude Wake Word Listener.lnk"
$TargetPath = "C:\Users\dwrek\START_WAKE_WORD_LISTENER.bat"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = "C:\Users\dwrek\100X_DEPLOYMENT"
$Shortcut.Description = "Always-on voice listener for Claude - Say 'Hey Claude' to activate"
$Shortcut.IconLocation = "C:\Windows\System32\SpeechUX.dll,0"
$Shortcut.WindowStyle = 7  # Minimized
$Shortcut.Save()

Write-Host "✅ Installed to startup folder" -ForegroundColor Green
Write-Host "   Location: $ShortcutPath" -ForegroundColor Gray
Write-Host ""
Write-Host "🎵 Wake word listener will start automatically when Windows boots" -ForegroundColor Green
Write-Host "   Say: 'Hey Claude' or 'Hey Commander' to activate" -ForegroundColor Yellow
Write-Host ""
Write-Host "To test now, run:" -ForegroundColor Cyan
Write-Host "   START_WAKE_WORD_LISTENER.bat" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to close"
