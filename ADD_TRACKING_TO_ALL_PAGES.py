#!/usr/bin/env python3
"""
AUTO-INJECT VISITOR TRACKING TO ALL PAGES
Adds VISITOR_TRACKING_SNIPPET.js to every HTML page
"""

import os
import glob
from pathlib import Path

# Tracking script to inject
TRACKING_INJECTION = """
<!-- 🔍 VISITOR TRACKING & INTERCOM SYSTEM -->
<script src="/VISITOR_TRACKING_SNIPPET.js"></script>
</body>"""

def add_tracking_to_page(file_path):
    """Add tracking snippet before </body> tag"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has tracking
        if 'VISITOR_TRACKING_SNIPPET' in content:
            return f"⏭️  SKIP: {file_path} (already has tracking)"

        # Skip if no </body> tag
        if '</body>' not in content:
            return f"⚠️  SKIP: {file_path} (no </body> tag)"

        # Inject tracking before </body>
        updated = content.replace('</body>', TRACKING_INJECTION)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated)

        return f"✅ ADDED: {file_path}"

    except Exception as e:
        return f"❌ ERROR: {file_path} - {e}"

def main():
    # Find all HTML files in 100X_DEPLOYMENT
    base_dir = Path(__file__).parent
    html_files = list(base_dir.glob('*.html'))

    print(f"🔍 Found {len(html_files)} HTML files")
    print(f"📍 Adding visitor tracking & intercom system...\n")

    added = 0
    skipped = 0
    errors = 0

    for html_file in html_files:
        result = add_tracking_to_page(html_file)
        print(result)

        if '✅ ADDED' in result:
            added += 1
        elif '⏭️  SKIP' in result:
            skipped += 1
        else:
            errors += 1

    print(f"\n" + "="*60)
    print(f"📊 TRACKING INJECTION COMPLETE")
    print(f"="*60)
    print(f"✅ Added tracking: {added} pages")
    print(f"⏭️  Skipped: {skipped} pages")
    print(f"❌ Errors: {errors} pages")
    print(f"📍 Total processed: {len(html_files)} pages")
    print(f"\n🚀 Now deploy to Netlify to go live!")
    print(f"   cd C:/Users/dwrek/100X_DEPLOYMENT")
    print(f"   netlify deploy --prod")

if __name__ == '__main__':
    main()
