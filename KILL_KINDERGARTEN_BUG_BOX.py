#!/usr/bin/env python3
"""
Kill the kindergarten bug box that keeps showing up
"""

import os
import re

def remove_kindergarten_bug(filepath):
    """Remove kindergarten bug reporter from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_length = len(content)

    # Pattern: Find <style> with kindergarten-bug-box through </script> after submitKindergartenBug
    pattern = r'<style>\s*\.kindergarten-bug-box.*?submitKindergartenBug.*?</script>'

    content = re.sub(pattern, '', content, flags=re.DOTALL)

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
        bytes_removed = remove_kindergarten_bug(filename)
        if bytes_removed > 0:
            files_cleaned += 1
            total_removed += bytes_removed
            print(f"✅ {filename}: removed {bytes_removed} bytes")

print(f"\n🎉 Kindergarten bug box KILLED:")
print(f"   Files cleaned: {files_cleaned}")
print(f"   Total bytes removed: {total_removed:,}")
