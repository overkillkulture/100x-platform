#!/usr/bin/env python3
"""
100X PLATFORM - RESPONSIVE CSS INJECTION SCRIPT
Injects shared/responsive.css into all HTML files
"""

import os
import re
from pathlib import Path

PLATFORM_DIR = Path(__file__).parent
RESPONSIVE_LINK = '    <link rel="stylesheet" href="shared/responsive.css">'

def inject_responsive_css(html_file):
    """Inject responsive.css link into HTML file if not already present"""

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has responsive.css
    if 'responsive.css' in content:
        return False

    # Find insertion point - after <head> tag or after last meta/title tag
    if '<head>' in content:
        # Try to insert after meta viewport or title tags
        if '<meta name="viewport"' in content:
            # Insert after viewport tag
            content = re.sub(
                r'(<meta name="viewport"[^>]*>)',
                r'\1\n' + RESPONSIVE_LINK,
                content,
                count=1
            )
        elif '<title>' in content and '</title>' in content:
            # Insert after title closing tag
            content = re.sub(
                r'(</title>)',
                r'\1\n' + RESPONSIVE_LINK,
                content,
                count=1
            )
        elif '<head>' in content:
            # Insert right after <head> tag
            content = re.sub(
                r'(<head>)',
                r'\1\n' + RESPONSIVE_LINK,
                content,
                count=1
            )
        else:
            print(f"  [SKIP] {html_file.name} - Could not find insertion point")
            return False

        # Write updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    else:
        print(f"  [SKIP] {html_file.name} - No <head> tag found")
        return False

def main():
    """Main injection process"""

    print("[*] 100X PLATFORM - RESPONSIVE CSS INJECTION")
    print("[*] Target: shared/responsive.css")
    print("[*] Scanning PLATFORM directory...\n")

    html_files = list(PLATFORM_DIR.glob('*.html'))
    total = len(html_files)
    injected = 0
    skipped = 0

    for html_file in html_files:
        if inject_responsive_css(html_file):
            print(f"  [OK] {html_file.name}")
            injected += 1
        else:
            skipped += 1

    print(f"\n[*] INJECTION COMPLETE")
    print(f"  Total HTML files: {total}")
    print(f"  Injected: {injected}")
    print(f"  Skipped (already present or no head tag): {skipped}")
    print(f"\n[*] All pages now have mobile-responsive CSS!")

if __name__ == '__main__':
    main()
