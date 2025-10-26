"""
INJECT BUG REPORTER EVERYWHERE
Adds the floating bug reporter widget to ALL HTML pages in 100X_DEPLOYMENT
"""

import os
import re
from pathlib import Path

DEPLOYMENT_DIR = r"C:\Users\dwrek\100X_DEPLOYMENT"
BUG_REPORTER_SCRIPT = '<script src="FLOATING_BUG_REPORTER.js"></script>'

# Pages to skip (already have it or don't need it)
SKIP_FILES = [
    'bug-report.html',
    'bug-reports-viewer.html',
    'bug-reports-viewer-v2.html',
    'COMMANDER_ANALYTICS_COCKPIT.html'
]

def has_bug_reporter(html_content):
    """Check if page already has bug reporter"""
    return 'FLOATING_BUG_REPORTER.js' in html_content

def inject_bug_reporter(html_content):
    """Inject bug reporter script before </body> tag"""
    if '</body>' in html_content:
        # Add before closing body tag
        return html_content.replace('</body>', f'    {BUG_REPORTER_SCRIPT}\n</body>')
    elif '</html>' in html_content:
        # Fallback: add before closing html tag
        return html_content.replace('</html>', f'    {BUG_REPORTER_SCRIPT}\n</html>')
    else:
        # Last resort: append to end
        return html_content + f'\n{BUG_REPORTER_SCRIPT}\n'

def process_html_files():
    """Find and process all HTML files"""
    html_files = list(Path(DEPLOYMENT_DIR).glob('*.html'))

    print(f"🔍 Found {len(html_files)} HTML files\n")

    injected_count = 0
    skipped_count = 0
    already_has_count = 0

    for html_file in html_files:
        filename = html_file.name

        # Skip certain files
        if filename in SKIP_FILES:
            print(f"⏭️  SKIPPED: {filename} (in skip list)")
            skipped_count += 1
            continue

        try:
            # Read file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if already has bug reporter
            if has_bug_reporter(content):
                print(f"✅ ALREADY HAS: {filename}")
                already_has_count += 1
                continue

            # Inject bug reporter
            updated_content = inject_bug_reporter(content)

            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"🐛 INJECTED: {filename}")
            injected_count += 1

        except Exception as e:
            print(f"❌ ERROR: {filename} - {str(e)}")

    print(f"\n{'='*60}")
    print(f"📊 SUMMARY:")
    print(f"   Total files: {len(html_files)}")
    print(f"   ✅ Already had reporter: {already_has_count}")
    print(f"   🐛 Newly injected: {injected_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"{'='*60}\n")

    if injected_count > 0:
        print(f"🎉 SUCCESS! Bug reporter now on {injected_count + already_has_count} pages!")
        print(f"\n📢 Message to users:")
        print(f"   'We check bugs every couple hours - report issues using the")
        print(f"    red button in the bottom-right corner of any page!'")

    return injected_count

if __name__ == "__main__":
    print("🐛 BUG REPORTER INJECTION SYSTEM")
    print("="*60 + "\n")

    injected = process_html_files()

    if injected > 0:
        print(f"\n✨ The floating bug reporter is now visible on every page!")
        print(f"💬 Big red button in bottom-right corner")
        print(f"⏰ 'We check bugs every couple hours' message included")
        print(f"📝 All bug reports saved automatically")
