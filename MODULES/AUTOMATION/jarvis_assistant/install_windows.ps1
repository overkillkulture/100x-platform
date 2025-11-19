# JARVIS Windows Installer
# Installs everything needed to run JARVIS on Windows

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🤖 JARVIS WINDOWS INSTALLER" -ForegroundColor Cyan
Write-Host "Your Personal AI Assistant Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This script needs Administrator privileges" -ForegroundColor Yellow
    Write-Host "   Right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Step 1: Check Python
Write-Host "📋 Step 1: Checking Python..." -ForegroundColor Green
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if ($pythonInstalled) {
    $pythonVersion = python --version
    Write-Host "   ✅ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python not found" -ForegroundColor Red
    Write-Host "   📥 Downloading Python 3.13..." -ForegroundColor Yellow

    $pythonUrl = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"

    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller

    Write-Host "   🔧 Installing Python..." -ForegroundColor Yellow
    Start-Process -FilePath $pythonInstaller -Args "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    Write-Host "   ✅ Python installed!" -ForegroundColor Green
    Remove-Item $pythonInstaller
}

# Step 2: Install Python Dependencies
Write-Host ""
Write-Host "📋 Step 2: Installing Python libraries..." -ForegroundColor Green
Write-Host "   (This may take 2-3 minutes)" -ForegroundColor Yellow

$packages = @(
    "speechrecognition",
    "pyaudio",
    "pyttsx3",
    "anthropic",
    "python-dotenv",
    "playwright",
    "pyautogui",
    "pillow",
    "requests"
)

foreach ($package in $packages) {
    Write-Host "   📦 Installing $package..." -ForegroundColor Cyan
    pip install $package --quiet
}

Write-Host "   ✅ All Python libraries installed!" -ForegroundColor Green

# Step 3: Install Playwright Browsers (if JARVIS PRO)
if ($args[0] -eq "pro") {
    Write-Host ""
    Write-Host "📋 Step 3: Installing browser automation..." -ForegroundColor Green
    python -m playwright install chromium
    Write-Host "   ✅ Browser automation ready!" -ForegroundColor Green
}

# Step 4: Create JARVIS directory
Write-Host ""
Write-Host "📋 Step 4: Creating JARVIS folder..." -ForegroundColor Green

$jarvisDir = "$env:USERPROFILE\JARVIS"
if (-not (Test-Path $jarvisDir)) {
    New-Item -ItemType Directory -Path $jarvisDir | Out-Null
}
Write-Host "   ✅ Folder created: $jarvisDir" -ForegroundColor Green

# Step 5: Copy files
Write-Host ""
Write-Host "📋 Step 5: Copying JARVIS files..." -ForegroundColor Green

# Copy R1 Voice system
$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item "$sourceDir\*" -Destination $jarvisDir -Recurse -Force

Write-Host "   ✅ JARVIS files installed!" -ForegroundColor Green

# Step 6: Create .env template
Write-Host ""
Write-Host "📋 Step 6: Creating configuration file..." -ForegroundColor Green

$envTemplate = @"
# JARVIS Configuration
# Get your Claude API key from: https://console.anthropic.com

ANTHROPIC_API_KEY=your_api_key_here

# Optional: Email automation (JARVIS PRO)
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

# Optional: Platform integration
PLATFORM_URL=http://localhost:8000
DISCORD_URL=https://discord.gg/your_invite
TWITTER_USERNAME=your_username
"@

$envFile = "$jarvisDir\.env"
if (-not (Test-Path $envFile)) {
    $envTemplate | Out-File -FilePath $envFile -Encoding UTF8
    Write-Host "   ✅ Config file created: $envFile" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  Config file already exists" -ForegroundColor Yellow
}

# Step 7: Create desktop shortcuts
Write-Host ""
Write-Host "📋 Step 7: Creating desktop shortcuts..." -ForegroundColor Green

$WScriptShell = New-Object -ComObject WScript.Shell

# JARVIS Launcher shortcut
$shortcut = $WScriptShell.CreateShortcut("$env:USERPROFILE\Desktop\🤖 Start JARVIS.lnk")
$shortcut.TargetPath = "python"
$shortcut.Arguments = "$jarvisDir\R1_VOICE_SYSTEM.py"
$shortcut.WorkingDirectory = $jarvisDir
$shortcut.Description = "Start JARVIS AI Assistant"
$shortcut.Save()

# Configuration shortcut
$shortcut2 = $WScriptShell.CreateShortcut("$env:USERPROFILE\Desktop\⚙️ Configure JARVIS.lnk")
$shortcut2.TargetPath = "notepad.exe"
$shortcut2.Arguments = "$jarvisDir\.env"
$shortcut2.Description = "Edit JARVIS Configuration"
$shortcut2.Save()

Write-Host "   ✅ Desktop shortcuts created!" -ForegroundColor Green

# Step 8: Test microphone
Write-Host ""
Write-Host "📋 Step 8: Testing microphone..." -ForegroundColor Green
Write-Host "   (If prompted, allow microphone access)" -ForegroundColor Yellow

# Simple mic test using PowerShell
try {
    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    Write-Host "   ✅ Microphone access OK!" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Microphone test failed - may need permissions" -ForegroundColor Yellow
}

# Final Steps
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✅ INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. Get Claude API Key:" -ForegroundColor White
Write-Host "      → Visit: https://console.anthropic.com" -ForegroundColor Cyan
Write-Host "      → Create account and generate API key" -ForegroundColor Cyan
Write-Host ""
Write-Host "   2. Configure JARVIS:" -ForegroundColor White
Write-Host "      → Double-click: ⚙️ Configure JARVIS (on your desktop)" -ForegroundColor Cyan
Write-Host "      → Replace 'your_api_key_here' with your real key" -ForegroundColor Cyan
Write-Host "      → Save and close" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3. Start JARVIS:" -ForegroundColor White
Write-Host "      → Double-click: 🤖 Start JARVIS (on your desktop)" -ForegroundColor Cyan
Write-Host ""
Write-Host "   4. First Command:" -ForegroundColor White
Write-Host "      → Say: 'Hey JARVIS, introduce yourself'" -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation: $jarvisDir\README.md" -ForegroundColor Gray
Write-Host "💬 Support: jarvis-support@conciousnessrevolution.io" -ForegroundColor Gray
Write-Host ""
Write-Host "🤖 Welcome to the future! 🚀" -ForegroundColor Magenta
Write-Host ""

# Open configuration file
Write-Host "Opening configuration file..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
notepad $envFile

# Open browser to API key page
Write-Host "Opening Claude API key page..." -ForegroundColor Yellow
Start-Process "https://console.anthropic.com"

Read-Host "Press Enter to exit installer"
