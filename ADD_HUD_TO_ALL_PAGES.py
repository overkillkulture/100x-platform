#!/usr/bin/env python3
"""
🎮 ADD HUD TO ALL PAGES 🎮
Automatically adds universal-hud-embed.js to all HTML pages
"""

import os
import re

# Pages that shouldn't have HUD (redirects, admin, etc.)
EXCLUDE = [
    'jarvis.html',  # HUD itself
    'index.html',  # Redirect page
    'simple-gate.html',  # Auth gate
    'login.html',  # Login page
    'auth.html',  # Auth page
    'test-',  # Test pages
    'backup',  # Backups
    '_old',  # Old versions
]

# The script to add (before </body>)
HUD_SCRIPT = """
<!-- 🎮 UNIVERSAL HUD - Auto-injected -->
<script src="/universal-hud-embed.js"></script>
"""

def should_process(filepath):
    """Check if file should have HUD added"""
    filename = os.path.basename(filepath)

    # Skip excluded patterns
    for pattern in EXCLUDE:
        if pattern in filename:
            return False

    # Only process HTML files
    if not filename.endswith('.html'):
        return False

    return True

def has_hud_script(content):
    """Check if HUD script already exists"""
    return 'universal-hud-embed.js' in content or 'UNIVERSAL_AI_HUD.js' in content

def add_hud_script(filepath):
    """Add HUD script to file if needed"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has HUD
        if has_hud_script(content):
            print(f"✅ SKIP: {filepath} (already has HUD)")
            return False

        # Find </body> tag
        if '</body>' not in content.lower():
            print(f"⚠️  SKIP: {filepath} (no </body> tag)")
            return False

        # Add HUD script before </body>
        pattern = re.compile(r'(</body>)', re.IGNORECASE)
        new_content = pattern.sub(f'{HUD_SCRIPT}\\1', content)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ ADDED: {filepath}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {filepath} - {e}")
        return False

def main():
    """Process all HTML files in directory"""
    deployment_dir = os.path.dirname(__file__)

    added_count = 0
    skipped_count = 0

    print("🎮 ADDING UNIVERSAL HUD TO ALL PAGES 🎮\n")

    # Process all HTML files
    for filename in os.listdir(deployment_dir):
        filepath = os.path.join(deployment_dir, filename)

        if not os.path.isfile(filepath):
            continue

        if not should_process(filepath):
            continue

        if add_hud_script(filepath):
            added_count += 1
        else:
            skipped_count += 1

    print(f"\n📊 SUMMARY:")
    print(f"✅ Added HUD: {added_count} pages")
    print(f"⏭️  Skipped: {skipped_count} pages")
    print(f"\n🚀 HUD will now follow you on {added_count} more pages!")

if __name__ == '__main__':
    main()
