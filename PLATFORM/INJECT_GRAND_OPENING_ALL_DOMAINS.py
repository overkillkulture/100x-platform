#!/usr/bin/env python3
"""
Inject GRAND_OPENING_INJECTOR.js into all Seven Domain pages
Part of Birthday Grand Opening autonomous execution
"""

import os
import re

# List of all domain pages to inject
domain_files = [
    'computer-consciousness.html',
    'education-domain.html',
    'social-domain.html',
    'music-domain.html',
    'crypto-domain.html',
    'games-domain.html',
    'governance-domain.html',
    'welcome.html',
    'user-dashboard.html',
    'community-activity.html'
]

platform_dir = r'C:\Users\dwrek\100X_DEPLOYMENT\PLATFORM'

injection_code = '''
    <!-- 🎂 BIRTHDAY GRAND OPENING CELEBRATION 🎂 -->
    <script src="GRAND_OPENING_INJECTOR.js"></script>
'''

results = []

for filename in domain_files:
    filepath = os.path.join(platform_dir, filename)

    if not os.path.exists(filepath):
        results.append(f"❌ {filename} - FILE NOT FOUND")
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already injected
        if 'GRAND_OPENING_INJECTOR.js' in content:
            results.append(f"✅ {filename} - ALREADY INJECTED")
            continue

        # Inject before closing </body> tag
        if '</body>' in content:
            content = content.replace('</body>', injection_code + '</body>')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            results.append(f"🎉 {filename} - INJECTED SUCCESSFULLY")
        else:
            results.append(f"⚠️  {filename} - NO </body> TAG FOUND")

    except Exception as e:
        results.append(f"❌ {filename} - ERROR: {str(e)}")

print("\n" + "="*60)
print("🎂 GRAND OPENING INJECTION REPORT 🎂")
print("="*60 + "\n")

for result in results:
    print(result)

print("\n" + "="*60)
print(f"✅ COMPLETE: {len([r for r in results if '🎉' in r or '✅' in r])}/{len(domain_files)} pages ready")
print("="*60 + "\n")
