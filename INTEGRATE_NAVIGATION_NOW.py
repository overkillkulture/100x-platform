"""
PERMANENT NAVIGATION INTEGRATION SCRIPT
Automatically injects universal navigation into all platform pages
"""

import os
import re
from pathlib import Path

# Pages to integrate navigation
PAGES_TO_INTEGRATE = [
    'workspace-v3.html',
    'COMMAND_CENTER_HUD_COMMS.html',
    'COMMAND_CENTER_MOBILE.html',
    'SITE_WALKTHROUGH_INTERACTIVE.html',
    'platform.html',
    'jarvis.html',
    'gta-hud.html'
]

DEPLOYMENT_DIR = Path(__file__).parent

def inject_navigation_script(html_path):
    """Inject universal navigation script into HTML file if not already present"""

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already integrated
    if 'UNIVERSAL_NAVIGATION.js' in content:
        print(f"  ✅ Already integrated: {html_path.name}")
        return False

    # Find closing </body> tag
    if '</body>' not in content:
        print(f"  ⚠️  No </body> tag found: {html_path.name}")
        return False

    # Injection code
    injection = '''
<!-- UNIVERSAL NAVIGATION SYSTEM - Auto-injected -->
<script src="/UNIVERSAL_NAVIGATION.js"></script>
</body>'''

    # Replace closing body tag with injection + body tag
    new_content = content.replace('</body>', injection)

    # Write updated content
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✨ Integrated: {html_path.name}")
    return True

def main():
    print("🌀 PERMANENT NAVIGATION INTEGRATION")
    print("=" * 60)
    print()

    integrated_count = 0
    already_integrated = 0
    errors = 0

    for page_name in PAGES_TO_INTEGRATE:
        page_path = DEPLOYMENT_DIR / page_name

        if not page_path.exists():
            print(f"  ⚠️  File not found: {page_name}")
            errors += 1
            continue

        try:
            if inject_navigation_script(page_path):
                integrated_count += 1
            else:
                already_integrated += 1
        except Exception as e:
            print(f"  ❌ Error with {page_name}: {e}")
            errors += 1

    print()
    print("=" * 60)
    print(f"✅ Newly Integrated: {integrated_count}")
    print(f"✅ Already Integrated: {already_integrated}")
    if errors > 0:
        print(f"⚠️  Errors: {errors}")
    print()
    print("🎯 Universal navigation system is now permanent across all pages!")
    print("   Navigation will auto-load on every page for seamless experience.")
    print()

if __name__ == '__main__':
    main()
