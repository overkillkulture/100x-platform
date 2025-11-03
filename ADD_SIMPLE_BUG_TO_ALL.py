import os
import re

# Find all HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in html_files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has the simple bug widget
        if 'SIMPLE_BUG_WIDGET.js' in content:
            print(f"✓ {filename} - already has simple widget")
            continue
        
        # Add the script tag before closing body tag
        if '</body>' in content:
            script_tag = '\n    <!-- Simple Bug Reporter -->\n    <script src="/SIMPLE_BUG_WIDGET.js"></script>\n</body>'
            content = content.replace('</body>', script_tag)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filename} - added simple bug widget")
        else:
            print(f"⚠️  {filename} - no closing body tag")
            
    except Exception as e:
        print(f"❌ {filename} - error: {e}")

print("\nDone! Simple bug reporter added to all pages.")
