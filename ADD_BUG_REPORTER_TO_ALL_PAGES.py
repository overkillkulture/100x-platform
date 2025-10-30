"""
Fix Bug #73: Add bug reporter to ALL HTML pages
Injects SIMPLE_BUG_REPORTER.js before closing </body> tag
"""

import os
import glob
from pathlib import Path

# Get all HTML files in the deployment folder
html_files = glob.glob('*.html')

print(f"Found {len(html_files)} HTML files")

# The script tag to inject
BUG_REPORTER_SCRIPT = '<script src="/SIMPLE_BUG_REPORTER.js"></script>'

added_count = 0
skipped_count = 0

for html_file in html_files:
    print(f"\nProcessing: {html_file}")

    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Check if already has the bug reporter
    if 'SIMPLE_BUG_REPORTER.js' in content:
        print(f"  ✓ Already has bug reporter - skipping")
        skipped_count += 1
        continue

    # Check if has </body> tag
    if '</body>' not in content.lower():
        print(f"  ⚠️ No </body> tag found - skipping")
        skipped_count += 1
        continue

    # Inject before closing </body> tag (case-insensitive)
    # Find the last occurrence of </body>
    body_close_index = content.lower().rfind('</body>')

    if body_close_index == -1:
        print(f"  ⚠️ Could not find </body> - skipping")
        skipped_count += 1
        continue

    # Insert the script tag
    new_content = (
        content[:body_close_index] +
        '\n    ' + BUG_REPORTER_SCRIPT + '\n' +
        content[body_close_index:]
    )

    # Write back
    with open(html_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(new_content)

    print(f"  ✅ Added bug reporter")
    added_count += 1

print("\n" + "="*60)
print(f"COMPLETE!")
print(f"  ✅ Added to {added_count} files")
print(f"  ⏭️ Skipped {skipped_count} files (already had it or no </body>)")
print(f"  📊 Total files: {len(html_files)}")
print("="*60)
print("\nBug #73 FIXED: Bug reporter now on all pages!")
print("Users can report bugs from any page, page URL is auto-captured")
