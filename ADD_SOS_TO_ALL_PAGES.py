"""
ADD SOS (HELP SYSTEM + BUG NOTEPAD) TO ALL WORKSPACE PAGES
Injects Universal Help System and Bug Notepad V2 to every page after the gate
"""

import os
import re

# Pages that should get the SOS system (after the gate)
WORKSPACE_PAGES = [
    'workspace-v3.html',
    'workspace-v2.html',
    'workspace.html',
    'admin-workspace-dashboard.html',
    'consciousness-workspace.html',
    'builder-workspace-docking.html',
    'simple-workspace-entry.html',
    'COMMAND_CENTER_HUD_COMMS.html',
    'cockpit.html',
    'platform.html',
    'tools-hub.html',
    'trinity-hub.html',
    'business-hub.html',
    'analytics-hub.html'
]

# The SOS script tags to inject
SOS_SCRIPTS = '''
<!-- 🆘 UNIVERSAL HELP SYSTEM + BUG NOTEPAD 🆘 -->
<script src="/UNIVERSAL_HELP_SYSTEM.js"></script>
<script src="/UNIVERSAL_BUG_NOTEPAD_V2.js"></script>'''

def add_sos_to_page(filepath):
    """Add SOS system to a page if it doesn't have it already"""

    if not os.path.exists(filepath):
        print(f"⏭️  Skipping {os.path.basename(filepath)} - file not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has SOS
    if 'UNIVERSAL_HELP_SYSTEM.js' in content or 'UNIVERSAL_BUG_NOTEPAD' in content:
        print(f"✅ {os.path.basename(filepath)} - Already has SOS")
        return False

    # Find closing </body> tag
    if '</body>' not in content:
        print(f"⚠️  {os.path.basename(filepath)} - No </body> tag found")
        return False

    # Inject SOS scripts before </body>
    updated_content = content.replace('</body>', f'{SOS_SCRIPTS}\n</body>')

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"🆘 {os.path.basename(filepath)} - SOS ADDED!")
    return True

def main():
    base_path = 'C:/Users/dwrek/100X_DEPLOYMENT'

    print("🆘 ADDING SOS TO ALL WORKSPACE PAGES 🆘")
    print("=" * 60)

    added_count = 0

    for page in WORKSPACE_PAGES:
        filepath = os.path.join(base_path, page)
        if add_sos_to_page(filepath):
            added_count += 1

    print("=" * 60)
    print(f"✅ SOS added to {added_count} pages!")
    print("\nSOS System Includes:")
    print("  📞 Universal Help System - Three-tier help on every screen")
    print("  🐛 Bug Notepad V2 - Auto-capture errors + Commander responses")
    print("\nUsers can now:")
    print("  - Click help button to get AI guidance")
    print("  - Report bugs with one click")
    print("  - Get context-aware tips")
    print("  - Receive Commander responses to bug reports")

if __name__ == '__main__':
    main()
