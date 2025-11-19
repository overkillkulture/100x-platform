"""
ADD USER DISPLAY TO ALL PAGES
Injects UNIVERSAL_USER_DISPLAY.js into all HTML files
Bug #91 fix
"""

import os
import glob
from pathlib import Path

# Get all HTML files
html_files = glob.glob('*.html')
print(f"Found {len(html_files)} HTML files")

USER_DISPLAY_SCRIPT = '<script src="/UNIVERSAL_USER_DISPLAY.js"></script>'

added_count = 0
skipped_count = 0
errors = []

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Skip if already has user display
        if 'UNIVERSAL_USER_DISPLAY.js' in content:
            skipped_count += 1
            continue

        # Skip if no </body> tag
        if '</body>' not in content.lower():
            skipped_count += 1
            continue

        # Find last </body> tag and insert before it
        body_close_index = content.lower().rfind('</body>')
        new_content = (
            content[:body_close_index] +
            '\n    ' + USER_DISPLAY_SCRIPT + '\n' +
            content[body_close_index:]
        )

        # Write back
        with open(html_file, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(new_content)

        added_count += 1
        print(f"✓ Added to {html_file}")

    except Exception as e:
        errors.append(f"{html_file}: {str(e)}")
        print(f"✗ Error in {html_file}: {e}")

print(f"\n{'='*60}")
print(f"✅ Added to {added_count} files")
print(f"⏭️  Skipped {skipped_count} files (already had it or no </body>)")
if errors:
    print(f"❌ Errors in {len(errors)} files:")
    for error in errors[:10]:  # Show first 10 errors
        print(f"   {error}")
print(f"{'='*60}")
