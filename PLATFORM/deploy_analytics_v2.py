#!/usr/bin/env python3
"""
DEPLOY ANALYTICS TRAPS V2
Replaces old visitor tracking snippet with enhanced V2 analytics
"""

import os
import re
from pathlib import Path

PLATFORM_DIR = Path(__file__).parent
OLD_SNIPPET_PATH = '../VISITOR_TRACKING_SNIPPET.js'
NEW_SNIPPET_PATH = '../VISITOR_TRACKING_SNIPPET_V2.js'

def read_snippet(path):
    """Read JavaScript snippet file"""
    with open(PLATFORM_DIR / path, 'r', encoding='utf-8') as f:
        return f.read()

def deploy_to_html_files():
    """Deploy V2 tracking snippet to all HTML files"""

    print("[*] ANALYTICS TRAPS V2 - DEPLOYMENT")
    print("[*] Reading new tracking snippet...")

    new_snippet = read_snippet(NEW_SNIPPET_PATH)

    print(f"[*] New snippet loaded: {len(new_snippet)} bytes")
    print(f"[*] Scanning HTML files in {PLATFORM_DIR}...\n")

    html_files = list(PLATFORM_DIR.glob('*.html'))
    total = len(html_files)
    updated = 0
    already_v2 = 0
    added_new = 0
    errors = 0

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if already has V2
            if 'VISITOR_TRACKING_SNIPPET_V2' in content or 'Analytics Traps' in content:
                print(f"  [SKIP] {html_file.name} - Already has V2")
                already_v2 += 1
                continue

            # Check if has old snippet
            if '<script src="VISITOR_TRACKING_SNIPPET.js"></script>' in content:
                # Replace old with new
                new_content = content.replace(
                    '<script src="VISITOR_TRACKING_SNIPPET.js"></script>',
                    '<script src="VISITOR_TRACKING_SNIPPET_V2.js"></script>'
                )

                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"  [OK] {html_file.name} - Upgraded to V2")
                updated += 1

            elif 'VISITOR_TRACKING_SNIPPET' not in content:
                # No tracking snippet at all - add new one
                # Try to add before </body> tag
                if '</body>' in content:
                    new_content = content.replace(
                        '</body>',
                        '    <script src="VISITOR_TRACKING_SNIPPET_V2.js"></script>\n</body>'
                    )

                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"  [ADD] {html_file.name} - Added V2")
                    added_new += 1
                else:
                    print(f"  [SKIP] {html_file.name} - No </body> tag found")

        except Exception as e:
            print(f"  [ERR] {html_file.name} - {str(e)}")
            errors += 1

    print(f"\n[*] DEPLOYMENT COMPLETE")
    print(f"  Total HTML files: {total}")
    print(f"  Upgraded to V2: {updated}")
    print(f"  Already had V2: {already_v2}")
    print(f"  Added V2: {added_new}")
    print(f"  Errors: {errors}")
    print(f"\n[*] Analytics Traps V2 is now DEPLOYED!")

if __name__ == '__main__':
    deploy_to_html_files()
