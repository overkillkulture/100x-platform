"""
Auto-inject Universal HUD into all HTML pages
Adds the game-like frame around every page
"""
import os
import re
from pathlib import Path

# HUD injection code
HUD_INJECTION = '''
<!-- Universal HUD - Auto-injected -->
<script src="/UNIVERSAL_AI_HUD.js"></script>
'''

def inject_hud_into_page(html_path):
    """Inject HUD script into HTML page if not already there"""
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Check if already injected
    if 'UNIVERSAL_AI_HUD.js' in content:
        return False, "Already has HUD"

    # Find </body> tag and inject before it
    if '</body>' in content:
        content = content.replace('</body>', f'{HUD_INJECTION}\n</body>')
    elif '</html>' in content:
        # Fallback: inject before </html>
        content = content.replace('</html>', f'{HUD_INJECTION}\n</html>')
    else:
        return False, "No </body> or </html> tag found"

    # Write back
    with open(html_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)

    return True, "HUD injected"

def main():
    deployment_dir = Path('C:/Users/dwrek/100X_DEPLOYMENT')

    # Find all HTML files
    html_files = list(deployment_dir.glob('*.html'))

    print("🎮 UNIVERSAL HUD INJECTOR 🎮")
    print("=" * 60)
    print(f"Found {len(html_files)} HTML files")
    print()

    injected = 0
    skipped = 0
    errors = 0

    for html_file in html_files:
        # Skip certain files
        skip_files = ['jarvis.html', 'TRINITY_MISSION_CONTROL.html']  # These already have their own HUD
        if html_file.name in skip_files:
            print(f"⏭️  SKIP: {html_file.name} (has own HUD)")
            skipped += 1
            continue

        try:
            success, message = inject_hud_into_page(html_file)
            if success:
                print(f"✅ INJECT: {html_file.name}")
                injected += 1
            else:
                print(f"⏭️  SKIP: {html_file.name} - {message}")
                skipped += 1
        except Exception as e:
            print(f"❌ ERROR: {html_file.name} - {e}")
            errors += 1

    print()
    print("=" * 60)
    print(f"✅ Injected: {injected}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Errors: {errors}")
    print()
    print("🎮 Universal HUD now loads on all pages!")
    print("   - Top HUD bar: Trinity Power, Consciousness %, Visitors")
    print("   - Araya (bottom right): Computer control AI")
    print("   - Philosopher (bottom left): Pattern Theory advisor")
    print()
    print("Press Ctrl+H to toggle HUD on any page")

if __name__ == '__main__':
    main()
