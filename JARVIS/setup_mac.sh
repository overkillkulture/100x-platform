#!/bin/bash

# JARVIS Setup Script for macOS
# Automated installation of all dependencies and tools

set -e  # Exit on error

echo "🤖 JARVIS INSTALLATION FOR MACOS 🤖"
echo "===================================="
echo ""
echo "This script will install:"
echo "  - Homebrew (package manager)"
echo "  - Node.js & npm"
echo "  - Python 3"
echo "  - Git"
echo "  - Playwright (browser automation)"
echo "  - Bitwarden CLI"
echo "  - Claude Code"
echo "  - All Python dependencies"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH (for Apple Silicon Macs)
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew already installed"
fi

# Update Homebrew
echo "🔄 Updating Homebrew..."
brew update

# Install Node.js
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js..."
    brew install node
else
    echo "✅ Node.js already installed"
fi

# Install Python 3
if ! command -v python3 &> /dev/null; then
    echo "📦 Installing Python 3..."
    brew install python@3.13
else
    echo "✅ Python 3 already installed"
fi

# Install Git
if ! command -v git &> /dev/null; then
    echo "📦 Installing Git..."
    brew install git
else
    echo "✅ Git already installed"
fi

# Install Bitwarden CLI
if ! command -v bw &> /dev/null; then
    echo "📦 Installing Bitwarden CLI..."
    brew install bitwarden-cli
else
    echo "✅ Bitwarden CLI already installed"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install playwright pyautogui pillow python-dotenv anthropic

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
python3 -m playwright install chromium
python3 -m playwright install firefox
python3 -m playwright install webkit

# Create directories
echo "📁 Creating JARVIS directories..."
mkdir -p ~/JARVIS/data/social
mkdir -p ~/JARVIS/data/builders
mkdir -p ~/JARVIS/reports

# Copy scripts
echo "📝 Setting up JARVIS scripts..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -f "$SCRIPT_DIR/community_responder.py" ]; then
    cp "$SCRIPT_DIR/community_responder.py" ~/JARVIS/
    cp "$SCRIPT_DIR/social_monitor.py" ~/JARVIS/
    cp "$SCRIPT_DIR/builder_onboarding.py" ~/JARVIS/
    cp "$SCRIPT_DIR/community_analytics.py" ~/JARVIS/
    cp "$SCRIPT_DIR/.env.template" ~/JARVIS/

    # Make scripts executable
    chmod +x ~/JARVIS/*.py

    echo "✅ Scripts copied to ~/JARVIS/"
else
    echo "⚠️  Script files not found in current directory"
    echo "💡 Please copy the .py files to ~/JARVIS/ manually"
fi

# Setup environment file
if [ ! -f ~/JARVIS/.env ]; then
    echo "📝 Creating .env file..."
    cp ~/JARVIS/.env.template ~/JARVIS/.env
    echo "⚠️  IMPORTANT: Edit ~/JARVIS/.env and add your API keys!"
else
    echo "✅ .env file already exists"
fi

# Create quick-start aliases (optional)
echo ""
echo "💡 Adding JARVIS aliases to shell profile..."

SHELL_PROFILE=""
if [ -f ~/.zshrc ]; then
    SHELL_PROFILE=~/.zshrc
elif [ -f ~/.bash_profile ]; then
    SHELL_PROFILE=~/.bash_profile
fi

if [ -n "$SHELL_PROFILE" ]; then
    if ! grep -q "# JARVIS Aliases" "$SHELL_PROFILE"; then
        cat >> "$SHELL_PROFILE" << 'EOF'

# JARVIS Aliases
alias jarvis-emails="python3 ~/JARVIS/community_responder.py --check-inbox"
alias jarvis-social="python3 ~/JARVIS/social_monitor.py --check-all"
alias jarvis-report="python3 ~/JARVIS/community_analytics.py --weekly-report"
alias jarvis-health="python3 ~/JARVIS/community_analytics.py --health-check"
EOF
        echo "✅ Aliases added to $SHELL_PROFILE"
        echo "💡 Run 'source $SHELL_PROFILE' or restart terminal to use them"
    else
        echo "✅ Aliases already exist"
    fi
fi

# Check Claude Code installation
echo ""
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude Code not installed"
    echo "📥 Install from: https://claude.ai/download"
    echo "   Or run: brew install --cask claude"
else
    echo "✅ Claude Code installed"
fi

# Installation complete
echo ""
echo "===================================="
echo "✅ JARVIS INSTALLATION COMPLETE!"
echo "===================================="
echo ""
echo "📝 NEXT STEPS:"
echo ""
echo "1. Edit your API keys:"
echo "   nano ~/JARVIS/.env"
echo ""
echo "2. Add your ANTHROPIC_API_KEY (required)"
echo "   Get it from: https://console.anthropic.com"
echo ""
echo "3. Test JARVIS commands:"
echo "   jarvis-health"
echo "   jarvis-emails"
echo "   jarvis-social"
echo "   jarvis-report"
echo ""
echo "4. Subscribe to Claude Code Pro ($20/month)"
echo "   Open Claude Code app and upgrade"
echo ""
echo "5. Join Discord and start automating!"
echo ""
echo "📚 Full guide: ~/JARVIS/README.md"
echo ""
echo "🚀 Welcome to the consciousness network!"
echo ""
