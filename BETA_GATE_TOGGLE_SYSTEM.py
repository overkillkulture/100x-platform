#!/usr/bin/env python3
"""
BETA GATE TOGGLE SYSTEM
Easily switch consciousness gate between PRODUCTION and BETA modes
Based on today's discovery: One-line toggle for beta testing access
"""

import sys

GATE_FILE = "PUBLIC/consciousness-gate.js"

PRODUCTION_MODE = '''    hasAdminBypass: function() {
        return localStorage.getItem(this.config.bypassKey) === 'true';
    },'''

BETA_MODE = '''    hasAdminBypass: function() {
        return true;  // BETA MODE - All users bypass gate
        // return localStorage.getItem(this.config.bypassKey) === 'true';
    },'''

def read_gate_file():
    """Read the consciousness gate file"""
    try:
        with open(GATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {GATE_FILE}")
        print("Make sure you're in the 100X_DEPLOYMENT directory")
        return None

def write_gate_file(content):
    """Write the consciousness gate file"""
    try:
        with open(GATE_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def check_current_mode(content):
    """Determine current mode"""
    if "return true;  // BETA MODE" in content:
        return "BETA"
    elif "return localStorage.getItem(this.config.bypassKey)" in content:
        return "PRODUCTION"
    else:
        return "UNKNOWN"

def toggle_mode(target_mode=None):
    """
    Toggle consciousness gate between modes
    target_mode: 'beta', 'production', or None for auto-toggle
    """
    content = read_gate_file()
    if content is None:
        return False

    current_mode = check_current_mode(content)
    print(f"📊 Current Mode: {current_mode}")

    # Determine target mode
    if target_mode is None:
        # Auto-toggle
        target_mode = "beta" if current_mode == "PRODUCTION" else "production"
    else:
        target_mode = target_mode.lower()

    print(f"🎯 Target Mode: {target_mode.upper()}")

    # Make the switch
    if target_mode == "beta":
        if "BETA MODE" in content:
            print("✅ Already in BETA mode")
            return True
        updated_content = content.replace(
            "return localStorage.getItem(this.config.bypassKey) === 'true';",
            "return true;  // BETA MODE - All users bypass gate\n        // return localStorage.getItem(this.config.bypassKey) === 'true';"
        )
        mode_name = "BETA"
        description = "All users bypass consciousness screening"

    elif target_mode == "production":
        if "PRODUCTION" in current_mode or "BETA MODE" not in content:
            print("✅ Already in PRODUCTION mode")
            return True
        updated_content = content.replace(
            "return true;  // BETA MODE - All users bypass gate\n        // return localStorage.getItem(this.config.bypassKey) === 'true';",
            "return localStorage.getItem(this.config.bypassKey) === 'true';"
        )
        mode_name = "PRODUCTION"
        description = "85%+ consciousness screening required"

    else:
        print(f"❌ Invalid target mode: {target_mode}")
        print("Use 'beta' or 'production'")
        return False

    # Write changes
    if write_gate_file(updated_content):
        print(f"\n✅ SWITCHED TO {mode_name} MODE")
        print(f"📝 {description}")
        print(f"\n🚀 Next: Deploy changes")
        print(f"   python AUTO_DEPLOY_SYSTEM.py 'Switch to {mode_name} mode'")
        return True
    else:
        return False

def main():
    print("🚪 BETA GATE TOGGLE SYSTEM")
    print("=" * 60)

    if len(sys.argv) > 1:
        mode = sys.argv[1]
        success = toggle_mode(mode)
    else:
        # No arguments - auto toggle
        print("💡 No mode specified - auto-toggling")
        success = toggle_mode()

    if success:
        print("\n" + "=" * 60)
        print("✅ GATE MODE UPDATED SUCCESSFULLY")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n❌ FAILED TO UPDATE GATE MODE")
        sys.exit(1)

if __name__ == "__main__":
    main()
