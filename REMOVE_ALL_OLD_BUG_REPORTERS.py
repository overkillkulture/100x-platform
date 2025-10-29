#!/usr/bin/env python3
"""
NUCLEAR OPTION: Remove ALL old bug reporters from ALL HTML files
Keep ONLY the Bootstrap bug widget
"""

import os
import re

def clean_html_file(filepath):
    """Remove all old bug reporter code from an HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_length = len(content)

    # Pattern 1: FLOATING BUG REPORTER (inline JavaScript with style)
    content = re.sub(
        r'/\*\*.*?FLOATING BUG REPORTER.*?\*/.*?\}\);',
        '',
        content,
        flags=re.DOTALL
    )

    # Pattern 2: KINDERGARTEN BUG REPORTER (HTML + style + script)
    content = re.sub(
        r'<!-- 🐛 KINDERGARTEN.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )

    # Pattern 3: MULTI-CHANNEL BUG SIDEBAR
    content = re.sub(
        r'<!-- MULTI-CHANNEL BUG REPORTER.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )

    # Pattern 4: Any remaining bug-sidebar divs
    content = re.sub(
        r'<div class="bug-sidebar">.*?</div>(?:\s*<!--[^>]*-->)?',
        '',
        content,
        flags=re.DOTALL
    )

    # Pattern 5: Quick-send inputs
    content = re.sub(
        r'<input[^>]*id="quick-send"[^>]*>.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )

    bytes_removed = original_length - len(content)

    if bytes_removed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return bytes_removed

    return 0

# Clean all HTML files
total_removed = 0
files_cleaned = 0

for filename in os.listdir('.'):
    if filename.endswith('.html'):
        bytes_removed = clean_html_file(filename)
        if bytes_removed > 0:
            files_cleaned += 1
            total_removed += bytes_removed
            print(f"✅ {filename}: removed {bytes_removed} bytes")

print(f"\n🎉 COMPLETE:")
print(f"   Files cleaned: {files_cleaned}")
print(f"   Total bytes removed: {total_removed:,}")
print(f"\n   Only Bootstrap bug widget remains!")
