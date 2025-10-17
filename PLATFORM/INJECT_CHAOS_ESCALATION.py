#!/usr/bin/env python3
"""
Inject CHAOS_ESCALATION_SYSTEM.js into all pages
The site gets MORE FUN every time you visit!
"""

import os

domain_files = [
    'computer-consciousness.html',
    'education-domain.html',
    'social-domain.html',
    'music-domain.html',
    'crypto-domain.html',
    'games-domain.html',
    'governance-domain.html',
    'seven-domains-navigator.html',
    'welcome.html',
    'user-dashboard.html',
    'community-activity.html',
    'aria-3d-futuristic.html',
    'for-the-builders.html',
    'debug-terminal.html'
]

platform_dir = r'C:\Users\dwrek\100X_DEPLOYMENT\PLATFORM'

injection_code = '''
    <!-- 🎮 CHAOS ESCALATION - IT GETS CRAZIER! 🎮 -->
    <script src="CHAOS_ESCALATION_SYSTEM.js"></script>
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
        if 'CHAOS_ESCALATION_SYSTEM.js' in content:
            results.append(f"✅ {filename} - ALREADY HAS CHAOS ESCALATION")
            continue

        # Inject before closing </body> tag
        if '</body>' in content:
            content = content.replace('</body>', injection_code + '</body>')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            results.append(f"🎮 {filename} - CHAOS ESCALATION INJECTED!")
        else:
            results.append(f"⚠️  {filename} - NO </body> TAG FOUND")

    except Exception as e:
        results.append(f"❌ {filename} - ERROR: {str(e)}")

print("\n" + "="*70)
print("🎮 CHAOS ESCALATION INJECTION REPORT 🎮")
print("="*70 + "\n")

for result in results:
    print(result)

print("\n" + "="*70)
success_count = len([r for r in results if '🎮' in r or '✅' in r])
print(f"✅ COMPLETE: {success_count}/{len(domain_files)} pages have escalation system")
print("="*70 + "\n")

print("🎮 THE SITE NOW GETS MORE FUN EVERY TIME PEOPLE VISIT!")
print("🎮 8 CHAOS LEVELS - From birthday party to GODMODE!")
print("🎮 Visitors will keep coming back to see what happens next!")
