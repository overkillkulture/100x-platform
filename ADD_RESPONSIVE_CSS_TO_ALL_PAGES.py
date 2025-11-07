#!/usr/bin/env python3
"""
ADD RESPONSIVE CSS TO ALL PLATFORM PAGES
Priority #2: Mobile Responsiveness - Automated deployment script

Trinity C1 Mechanic - Autonomous Session
Adds universal responsive CSS framework to all 127 platform pages
Fixes incorrect viewport meta tags
"""

import os
import re
from pathlib import Path

# Configuration
PLATFORM_DIR = Path("PLATFORM")
RESPONSIVE_CSS = '<link rel="stylesheet" href="shared/responsive-mobile.css">'
CORRECT_VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

# Stats tracking
stats = {
    'total_files': 0,
    'added_css': 0,
    'fixed_viewport': 0,
    'already_has_css': 0,
    'already_correct_viewport': 0,
    'errors': []
}

def fix_viewport_tag(content):
    """Fix incorrect viewport meta tags"""

    # Pattern to match any viewport meta tag
    viewport_pattern = r'<meta\s+name="viewport"\s+content="[^"]*">'

    if re.search(viewport_pattern, content):
        # Check if it's already correct
        if CORRECT_VIEWPORT in content:
            stats['already_correct_viewport'] += 1
            return content, False

        # Replace with correct viewport
        new_content = re.sub(viewport_pattern, CORRECT_VIEWPORT, content)
        stats['fixed_viewport'] += 1
        return new_content, True

    # If no viewport tag exists, add it after charset
    if '<meta charset' in content:
        new_content = content.replace(
            '<meta charset="UTF-8">',
            f'<meta charset="UTF-8">\n    {CORRECT_VIEWPORT}',
            1
        )
        stats['fixed_viewport'] += 1
        return new_content, True

    return content, False

def add_responsive_css(content):
    """Add responsive CSS link to HTML file"""

    # Check if already has responsive CSS
    if 'responsive-mobile.css' in content:
        stats['already_has_css'] += 1
        return content, False

    # Try to add after last stylesheet link in <head>
    if '</head>' in content:
        # Find last stylesheet or style tag before </head>
        head_end = content.find('</head>')
        head_content = content[:head_end]

        # Find last style or link element
        last_style_pos = max(
            head_content.rfind('</style>'),
            head_content.rfind('<link rel="stylesheet"'),
            head_content.rfind('<style>')
        )

        if last_style_pos > 0:
            # Find end of that element
            if '</style>' in content[last_style_pos:last_style_pos+500]:
                insert_pos = content.find('</style>', last_style_pos) + 8
            else:
                insert_pos = content.find('>', last_style_pos) + 1

            new_content = (
                content[:insert_pos] +
                f'\n    {RESPONSIVE_CSS}' +
                content[insert_pos:]
            )
            stats['added_css'] += 1
            return new_content, True

        # If no styles found, add before </head>
        new_content = content.replace(
            '</head>',
            f'    {RESPONSIVE_CSS}\n</head>',
            1
        )
        stats['added_css'] += 1
        return new_content, True

    return content, False

def process_html_file(file_path):
    """Process a single HTML file"""

    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Make modifications
        modified = False

        # Fix viewport
        content, viewport_changed = fix_viewport_tag(content)
        if viewport_changed:
            modified = True

        # Add responsive CSS
        content, css_added = add_responsive_css(content)
        if css_added:
            modified = True

        # Write back if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        stats['errors'].append(f"{file_path.name}: {str(e)}")
        return False

def main():
    """Main execution"""

    print("=" * 60)
    print("MOBILE RESPONSIVENESS DEPLOYMENT")
    print("Priority #2: Auto-adding responsive CSS to all pages")
    print("=" * 60)
    print()

    # Find all HTML files
    html_files = list(PLATFORM_DIR.glob("*.html"))
    stats['total_files'] = len(html_files)

    print(f"Found {stats['total_files']} HTML files in PLATFORM/")
    print()
    print("Processing files...")
    print()

    # Process each file
    modified_files = []
    for file_path in html_files:
        was_modified = process_html_file(file_path)
        if was_modified:
            modified_files.append(file_path.name)
            print(f"✓ Modified: {file_path.name}")

    # Report
    print()
    print("=" * 60)
    print("DEPLOYMENT COMPLETE")
    print("=" * 60)
    print()
    print(f"Total files processed:         {stats['total_files']}")
    print(f"Files modified:                {len(modified_files)}")
    print()
    print(f"Responsive CSS added:          {stats['added_css']}")
    print(f"Already had responsive CSS:    {stats['already_has_css']}")
    print()
    print(f"Viewport tags fixed:           {stats['fixed_viewport']}")
    print(f"Already correct viewport:      {stats['already_correct_viewport']}")
    print()

    if stats['errors']:
        print("ERRORS:")
        for error in stats['errors']:
            print(f"  ✗ {error}")
        print()

    # Success summary
    success_rate = ((stats['added_css'] + stats['already_has_css']) / stats['total_files']) * 100

    print(f"Success Rate: {success_rate:.1f}%")
    print()
    print("=" * 60)
    print()

    if len(modified_files) > 0:
        print(f"✅ {len(modified_files)} files updated with mobile responsiveness")
        print()
        print("NEXT STEPS:")
        print("1. Test on mobile device or Chrome DevTools mobile emulation")
        print("2. Commit changes to git")
        print("3. Push to deployment")
        print()
        print("Files can now be tested at:")
        print("- iPhone SE (320px wide)")
        print("- iPhone 12 (390px wide)")
        print("- iPad (768px wide)")
        print()
    else:
        print("✓ All files already have responsive CSS!")
        print()

    print("Trinity C1 Mechanic - Mobile responsiveness deployment complete")
    print()

if __name__ == "__main__":
    main()
