"""
🎉 INJECT FUN EVERYWHERE
Automatically adds easter egg scripts to ALL HTML pages in PLATFORM folder
"""

import os
import re
from pathlib import Path

PLATFORM_DIR = Path(__file__).parent / "PLATFORM"

SCRIPTS_TO_ADD = """
    <!-- 🎮 Easter Egg System - Makes platform legendary -->
    <script src="easter-egg-engine.js"></script>
    <script src="fun-features.js"></script>"""

def inject_fun_into_file(filepath):
    """Add easter egg scripts to a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has easter egg scripts
        if 'easter-egg-engine.js' in content:
            print(f"  ⏭️  Already has fun: {filepath.name}")
            return False

        # Find closing body tag
        if '</body>' not in content:
            print(f"  ⚠️  No </body> tag: {filepath.name}")
            return False

        # Inject scripts before </body>
        new_content = content.replace('</body>', f'{SCRIPTS_TO_ADD}\n</body>')

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ Added fun to: {filepath.name}")
        return True

    except Exception as e:
        print(f"  ❌ Error with {filepath.name}: {e}")
        return False

def main():
    print("🎉 INJECTING FUN INTO ALL PAGES...\n")

    if not PLATFORM_DIR.exists():
        print(f"❌ PLATFORM directory not found: {PLATFORM_DIR}")
        return

    # Find all HTML files
    html_files = list(PLATFORM_DIR.glob("*.html"))

    if not html_files:
        print("❌ No HTML files found in PLATFORM directory")
        return

    print(f"Found {len(html_files)} HTML files\n")

    success_count = 0
    skip_count = 0

    for html_file in sorted(html_files):
        if inject_fun_into_file(html_file):
            success_count += 1
        else:
            skip_count += 1

    print(f"\n{'='*50}")
    print(f"✅ Added fun to: {success_count} pages")
    print(f"⏭️  Skipped: {skip_count} pages (already had fun)")
    print(f"🎮 Total processed: {len(html_files)} pages")
    print(f"{'='*50}\n")

    print("🎉 FUN HAS BEEN INJECTED EVERYWHERE!")
    print("🎮 All pages now have 30+ hidden easter eggs!")
    print("🏆 14 achievements to unlock!")
    print("⚡ Platform is now LEGENDARY!\n")

if __name__ == "__main__":
    main()
