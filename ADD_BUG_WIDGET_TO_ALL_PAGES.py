#!/usr/bin/env python3
"""
ADD BUG REPORTER WIDGET TO ALL PLATFORM PAGES
Injects <script src="bug-reporter-widget.js"></script> before </body> tag
"""

import os
import glob

# Configuration
PLATFORM_DIR = 'C:/Users/dwrek/100X_DEPLOYMENT/PLATFORM'
SCRIPT_TAG = '    <script src="bug-reporter-widget.js"></script>\n</body>'

def add_bug_widget_to_file(filepath):
    """Add bug widget script to a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has bug widget
        if 'bug-reporter-widget.js' in content:
            print(f"⏭️  SKIP: {os.path.basename(filepath)} (already has widget)")
            return False

        # Check if has </body> tag
        if '</body>' not in content:
            print(f"⚠️  WARN: {os.path.basename(filepath)} (no </body> tag found)")
            return False

        # Replace last </body> with script + </body>
        content = content.replace('</body>', SCRIPT_TAG, 1)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ ADDED: {os.path.basename(filepath)}")
        return True

    except Exception as e:
        print(f"❌ ERROR: {os.path.basename(filepath)} - {e}")
        return False

def main():
    """Add bug widget to all HTML files in PLATFORM directory"""
    print("=" * 80)
    print("🐛 ADDING BUG REPORTER WIDGET TO ALL PLATFORM PAGES")
    print("=" * 80)
    print()

    # Find all HTML files
    html_files = glob.glob(f"{PLATFORM_DIR}/*.html")

    print(f"Found {len(html_files)} HTML files\n")

    # Process each file
    added_count = 0
    skipped_count = 0
    error_count = 0

    for filepath in sorted(html_files):
        result = add_bug_widget_to_file(filepath)
        if result:
            added_count += 1
        elif 'already has widget' in str(result):
            skipped_count += 1
        else:
            error_count += 1

    # Summary
    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Added widget: {added_count} files")
    print(f"⏭️  Skipped (already had widget): {skipped_count} files")
    print(f"❌ Errors: {error_count} files")
    print(f"📁 Total processed: {len(html_files)} files")
    print("=" * 80)
    print()
    print("🎉 DONE! Bug reporter widget is now on all platform pages")
    print("   Users can press Ctrl+Shift+B or click the floating button to report bugs")
    print()

if __name__ == '__main__':
    main()
