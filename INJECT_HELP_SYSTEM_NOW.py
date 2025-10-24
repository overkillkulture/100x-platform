#!/usr/bin/env python3
"""
INJECT UNIVERSAL HELP SYSTEM
Automatically adds help system to all platform pages
"""

import os
import re

# Pages to inject help system
PAGES_TO_UPDATE = [
    'workspace-v3.html',
    'COMMAND_CENTER_HUD_COMMS.html',
    'COMMAND_CENTER_MOBILE.html',
    'SITE_WALKTHROUGH_INTERACTIVE.html',
    'platform.html',
    'jarvis.html',
    'simple-gate.html',
    'simple-gate-v2.html',
    'araya-chat.html'
]

HELP_SCRIPT_TAG = '<script src="/UNIVERSAL_HELP_SYSTEM.js"></script>'

def inject_help_system(file_path):
    """Inject help system script before closing body tag"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already injected
        if 'UNIVERSAL_HELP_SYSTEM.js' in content:
            print(f"⏭️  Already has help: {file_path}")
            return False

        # Find closing body tag
        if '</body>' not in content:
            print(f"⚠️  No </body> tag: {file_path}")
            return False

        # Inject before </body>
        new_content = content.replace('</body>', f'\n{HELP_SCRIPT_TAG}\n</body>')

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Injected help: {file_path}")
        return True

    except Exception as e:
        print(f"❌ Error with {file_path}: {e}")
        return False

def main():
    print("="*60)
    print("🌀 UNIVERSAL HELP SYSTEM INJECTION")
    print("="*60)
    print()

    base_dir = 'C:/Users/dwrek/100X_DEPLOYMENT'
    injected_count = 0

    for page in PAGES_TO_UPDATE:
        file_path = os.path.join(base_dir, page)

        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {page}")
            continue

        if inject_help_system(file_path):
            injected_count += 1

    print()
    print("="*60)
    print(f"✅ COMPLETE: Injected help system into {injected_count} pages")
    print("="*60)

if __name__ == '__main__':
    main()
