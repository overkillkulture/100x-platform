#!/usr/bin/env python3
"""
DEPLOY ANALYTICS TO ALL PAGES
Adds UNIVERSAL_ANALYTICS_TRACKER.js to all HTML files that don't have it
"""

import os
import re
from pathlib import Path

# Analytics tracker script tag
ANALYTICS_SCRIPT = '<script src="UNIVERSAL_ANALYTICS_TRACKER.js"></script>'

def has_analytics(html_content):
    """Check if HTML already has analytics tracker"""
    return 'UNIVERSAL_ANALYTICS_TRACKER' in html_content

def add_analytics_before_closing_body(html_content):
    """Add analytics script before </body> tag"""
    # Find </body> tag
    if '</body>' in html_content.lower():
        # Add script just before </body>
        pattern = re.compile(r'(</body>)', re.IGNORECASE)
        new_content = pattern.sub(f'    {ANALYTICS_SCRIPT}\n\\1', html_content)
        return new_content, True
    elif '</html>' in html_content.lower():
        # Fallback: add before </html>
        pattern = re.compile(r'(</html>)', re.IGNORECASE)
        new_content = pattern.sub(f'    {ANALYTICS_SCRIPT}\n\\1', html_content)
        return new_content, True
    else:
        # No closing tags found - append at end
        new_content = html_content + f'\n{ANALYTICS_SCRIPT}\n'
        return new_content, True

def process_html_file(file_path):
    """Process single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check if already has analytics
        if has_analytics(content):
            return 'SKIP', 'Already has analytics'

        # Add analytics
        new_content, modified = add_analytics_before_closing_body(content)

        if modified:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return 'ADDED', 'Analytics tracker added'
        else:
            return 'FAIL', 'Could not add analytics'

    except Exception as e:
        return 'ERROR', str(e)

def main():
    """Main deployment function"""
    print("=" * 70)
    print("DEPLOYING ANALYTICS TO ALL HTML PAGES")
    print("=" * 70)

    base_dir = Path('C:/Users/dwrek/100X_DEPLOYMENT')

    # Find all HTML files (excluding node_modules and backups)
    exclude_dirs = {'node_modules', 'BACKUP_HTML', '.git', 'coverage'}

    html_files = []
    for root, dirs, files in os.walk(base_dir):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)

    print(f"\nFound {len(html_files)} HTML files")
    print(f"Checking for analytics integration...\n")

    stats = {
        'ADDED': [],
        'SKIP': [],
        'FAIL': [],
        'ERROR': []
    }

    for i, file_path in enumerate(html_files, 1):
        relative_path = file_path.relative_to(base_dir)
        status, message = process_html_file(file_path)
        stats[status].append((relative_path, message))

        if status == 'ADDED':
            print(f"[{i:3d}/{len(html_files)}] ✅ ADDED: {relative_path}")
        elif status == 'SKIP':
            # Don't print skips (too verbose)
            pass
        elif status in ['FAIL', 'ERROR']:
            print(f"[{i:3d}/{len(html_files)}] ❌ {status}: {relative_path} - {message}")

    print("\n" + "=" * 70)
    print("DEPLOYMENT COMPLETE")
    print("=" * 70)
    print(f"\n✅ Analytics ADDED:    {len(stats['ADDED'])} files")
    print(f"⏭️  Already tracked:   {len(stats['SKIP'])} files")
    print(f"❌ Failed:            {len(stats['FAIL'])} files")
    print(f"⚠️  Errors:            {len(stats['ERROR'])} files")

    print(f"\n📊 COVERAGE: {len(stats['SKIP']) + len(stats['ADDED'])}/{len(html_files)} files now tracked")
    coverage_pct = ((len(stats['SKIP']) + len(stats['ADDED'])) / len(html_files)) * 100
    print(f"📈 PERCENTAGE: {coverage_pct:.1f}% of pages have analytics")

    # Show sample of added files
    if stats['ADDED']:
        print(f"\n📝 Sample of files updated (first 10):")
        for path, msg in stats['ADDED'][:10]:
            print(f"   - {path}")

    # Show any errors
    if stats['FAIL'] or stats['ERROR']:
        print(f"\n⚠️  Files that need manual review:")
        for path, msg in (stats['FAIL'] + stats['ERROR'])[:10]:
            print(f"   - {path}: {msg}")

    print("\n" + "=" * 70)

    # Create summary report
    summary_file = base_dir / 'ANALYTICS_DEPLOYMENT_REPORT.txt'
    with open(summary_file, 'w') as f:
        f.write("ANALYTICS DEPLOYMENT REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total HTML files: {len(html_files)}\n")
        f.write(f"Analytics added: {len(stats['ADDED'])}\n")
        f.write(f"Already tracked: {len(stats['SKIP'])}\n")
        f.write(f"Failed: {len(stats['FAIL'])}\n")
        f.write(f"Errors: {len(stats['ERROR'])}\n")
        f.write(f"Coverage: {coverage_pct:.1f}%\n\n")

        if stats['ADDED']:
            f.write("FILES UPDATED:\n")
            for path, msg in stats['ADDED']:
                f.write(f"  - {path}\n")

        if stats['FAIL'] or stats['ERROR']:
            f.write("\nFILES NEEDING REVIEW:\n")
            for path, msg in (stats['FAIL'] + stats['ERROR']):
                f.write(f"  - {path}: {msg}\n")

    print(f"📄 Full report saved to: {summary_file}")
    print("\n✅ Analytics deployment complete!")

if __name__ == '__main__':
    main()
