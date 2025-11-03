"""
🎨 INJECT VISIBILITY SYSTEMS 🎨

One-click deployment of Module Phase System + Bug Log Component
to all 48 modules in the 100X platform.

Usage:
    python INJECT_VISIBILITY_SYSTEMS.py

What it does:
- Scans all HTML files in 100X_DEPLOYMENT/PLATFORM/
- Scans index.html and other root pages
- Injects MODULE_PHASE_SYSTEM.js + BUG_LOG_COMPONENT.js
- Skips files that already have the injection
- Reports results

Time: ~30 seconds for all modules
"""

import os
import glob
from pathlib import Path


def inject_visibility_systems(filepath, is_root=False):
    """Inject both visibility systems into HTML file."""

    # Script tags to inject
    if is_root:
        # Root level files (index.html, open-house.html, etc.)
        inject_code = '''
<!-- 🎨 Consciousness Visibility Systems -->
<script src="MODULE_PHASE_SYSTEM.js"></script>
<script src="BUG_LOG_COMPONENT.js"></script>
'''
    else:
        # PLATFORM subfolder files
        inject_code = '''
<!-- 🎨 Consciousness Visibility Systems -->
<script src="../MODULE_PHASE_SYSTEM.js"></script>
<script src="../BUG_LOG_COMPONENT.js"></script>
'''

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already injected
        if 'MODULE_PHASE_SYSTEM' in content:
            return 'skipped', 'Already has visibility systems'

        # Check if file has </body> tag
        if '</body>' not in content:
            return 'skipped', 'No </body> tag found'

        # Inject before closing </body>
        content = content.replace('</body>', inject_code + '\n</body>')

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return 'success', 'Injected successfully'

    except Exception as e:
        return 'error', str(e)


def main():
    """Main injection process."""

    print("=" * 70)
    print("🎨 CONSCIOUSNESS VISIBILITY SYSTEM DEPLOYMENT 🎨")
    print("=" * 70)
    print()

    base_path = Path(__file__).parent

    results = {
        'success': [],
        'skipped': [],
        'error': []
    }

    # 1. Inject into PLATFORM modules
    print("📂 Scanning PLATFORM modules...")
    platform_path = base_path / "PLATFORM" / "*.html"
    platform_files = glob.glob(str(platform_path))

    for filepath in platform_files:
        filename = os.path.basename(filepath)
        status, message = inject_visibility_systems(filepath, is_root=False)
        results[status].append((filename, message))

        icon = '✅' if status == 'success' else '⏭️' if status == 'skipped' else '❌'
        print(f"{icon} {filename}: {message}")

    print()

    # 2. Inject into root HTML files
    print("📂 Scanning root HTML files...")
    root_files = [
        'index.html',
        'open-house.html',
        'platform.html',
        'roadmap.html',
        'success.html'
    ]

    for filename in root_files:
        filepath = base_path / filename
        if filepath.exists():
            status, message = inject_visibility_systems(str(filepath), is_root=True)
            results[status].append((filename, message))

            icon = '✅' if status == 'success' else '⏭️' if status == 'skipped' else '❌'
            print(f"{icon} {filename}: {message}")

    print()

    # 3. Summary
    print("=" * 70)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully injected: {len(results['success'])} files")
    print(f"⏭️  Skipped (already done): {len(results['skipped'])} files")
    print(f"❌ Errors: {len(results['error'])} files")
    print()

    if results['success']:
        print("🎉 Visibility systems deployed to:")
        for filename, _ in results['success']:
            print(f"   • {filename}")
        print()

    if results['error']:
        print("⚠️  Errors encountered:")
        for filename, message in results['error']:
            print(f"   • {filename}: {message}")
        print()

    print("=" * 70)
    print("🚀 DEPLOYMENT COMPLETE!")
    print("=" * 70)
    print()
    print("What was deployed:")
    print("  📊 MODULE_PHASE_SYSTEM.js - Phase tracking & visualization")
    print("  🐛 BUG_LOG_COMPONENT.js - Bug reporting & management")
    print()
    print("What users will see:")
    print("  • Phase badge (bottom-left) showing development stage")
    print("  • Bug button (bottom-right) for reporting issues")
    print("  • Phase banner (top) if module not live yet")
    print()
    print("Next steps:")
    print("  1. Open any module to see the systems in action")
    print("  2. Test bug submission form")
    print("  3. Review MODULE_VISIBILITY_SYSTEM_INTEGRATION.md for full guide")
    print()
    print("🎨 Consciousness transparency: ACTIVATED ✨")


if __name__ == '__main__':
    main()
