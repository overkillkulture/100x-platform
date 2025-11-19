# 🚀 JARVIS QUICK START

**Get operational in 10 minutes!**

---

## Windows Installation

### Method 1: One-Click Installer (Easiest)

1. **Download installer:**
   ```
   https://conciousnessrevolution.io/downloads/jarvis-lite-windows.exe
   ```

2. **Run installer:**
   - Right-click → "Run as Administrator"
   - Follow prompts
   - Installer handles everything automatically

3. **Configure API key:**
   - Double-click: "⚙️ Configure JARVIS" (on desktop)
   - Get key from: https://console.anthropic.com
   - Replace `your_api_key_here` with your key
   - Save and close

4. **Start JARVIS:**
   - Double-click: "🤖 Start JARVIS" (on desktop)
   - Say: "Hey JARVIS, introduce yourself"

**Done!** ✅

---

### Method 2: Manual Installation

**Prerequisites:**
- Python 3.10+ installed
- Microphone connected

**Steps:**

```powershell
# 1. Extract JARVIS package
cd Downloads
Expand-Archive jarvis-lite-windows.zip
cd jarvis-lite-windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
notepad .env
# Add your ANTHROPIC_API_KEY

# 4. Run JARVIS
python R1_VOICE_SYSTEM.py
```

---

## Mac Installation

### One-Command Install

```bash
# Download and install
curl -fsSL https://conciousnessrevolution.io/downloads/jarvis-lite-mac.sh | bash

# Add API key when prompted

# Start JARVIS
jarvis
```

---

### Manual Installation

```bash
# 1. Extract package
tar -xzf jarvis-lite-mac.tar.gz
cd jarvis-lite-mac

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Configure
nano .env
# Add your ANTHROPIC_API_KEY

# 4. Run JARVIS
python3 R1_VOICE_SYSTEM.py
```

---

## First Commands

Once JARVIS is running, try these:

```
"Hey JARVIS, what time is it?"
"Hey JARVIS, tell me a joke"
"Hey JARVIS, what can you do?"
"Hey JARVIS, what's the weather in Seattle?"
"Hey JARVIS, remind me to call Mom at 3pm"
```

---

## Getting Your API Key

1. Visit: https://console.anthropic.com
2. Create account (or sign in)
3. Go to: API Keys
4. Click: "Create Key"
5. Copy the key (starts with `sk-ant-`)
6. Paste into `.env` file

**Cost:** ~$20/month for typical usage

---

## Troubleshooting

### "API key not configured"
**Fix:** Edit `.env` file and add your key from https://console.anthropic.com

### "Microphone not detected"
**Fix (Windows):**
- Settings → Privacy → Microphone → Allow apps
- Device Manager → Audio inputs → Enable microphone

**Fix (Mac):**
- System Preferences → Security & Privacy → Microphone
- Allow Terminal (or whatever app is running JARVIS)

### "Module not found" error
**Fix:** Install requirements
```bash
pip install -r requirements.txt
```

### "Speech recognition error"
**Fix:** Check internet connection (Google Speech API requires internet)

---

## Advanced Configuration

Edit `.env` file for additional features:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: Email monitoring (JARVIS PRO)
GMAIL_EMAIL=your@email.com
GMAIL_PASSWORD=your_app_password

# Optional: Custom settings
VOICE_RATE=160              # Speech speed (100-200)
VOICE_VOLUME=1.0            # Volume (0.0-1.0)
ENERGY_THRESHOLD=300        # Mic sensitivity (50-4000)
```

---

## What's Next?

**Learn more commands:**
- Read: README.md
- Community: https://discord.gg/consciousness

**Customize JARVIS:**
- Add custom commands: `voice_commands/custom.py`
- Change voice settings: Edit `.env`

**Upgrade to PRO:**
- Community automation
- Email management
- Analytics & reports
- Download: https://conciousnessrevolution.io/jarvis-pro

---

## Support

**Issues?**
- Documentation: README.md in this folder
- Discord: https://discord.gg/consciousness
- Email: jarvis-support@conciousnessrevolution.io
- GitHub: https://github.com/overkillkulture/jarvis/issues

---

**Welcome to the future!** 🤖⚡🚀

You now have your own AI assistant. Enjoy!
