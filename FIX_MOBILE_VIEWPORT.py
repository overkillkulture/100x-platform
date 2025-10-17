#!/usr/bin/env python3
"""
Fix mobile viewport - Force desktop view on mobile devices
Changes viewport from responsive to fixed desktop width
"""

import os
import re

def fix_viewport(file_path):
    """Update viewport meta tag to force desktop view"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find existing viewport tag
        viewport_pattern = r'<meta\s+name="viewport"\s+content="[^"]*">'

        # Desktop viewport (forces desktop view, allows zoom)
        new_viewport = '<meta name="viewport" content="width=1200, initial-scale=0.5, user-scalable=yes">'

        if re.search(viewport_pattern, content):
            # Replace existing viewport
            updated = re.sub(viewport_pattern, new_viewport, content)

            if updated != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated)
                return True

        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

# Find all HTML files
updated_count = 0
for root, dirs, files in os.walk('C:/Users/dwrek/100X_DEPLOYMENT'):
    # Skip node_modules and other large folders
    if 'node_modules' in root or '.git' in root:
        continue

    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            if fix_viewport(file_path):
                updated_count += 1
                print(f"✓ Updated: {file}")

print(f"\n✅ Updated {updated_count} HTML files with desktop viewport")
print("📱 Mobile devices will now show desktop view (zoomable)")
