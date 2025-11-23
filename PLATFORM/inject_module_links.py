#!/usr/bin/env python3
"""
MODULE CROSS-LINK INJECTOR
Injects "Related Modules" sections into platform pages
Creates interconnected module ecosystem for better user navigation
"""

import json
from pathlib import Path
import re

PLATFORM_DIR = Path(__file__).parent
RELATIONSHIPS_FILE = PLATFORM_DIR.parent / 'MODULE_RELATIONSHIPS.json'

def load_relationships():
    """Load module relationship data"""
    with open(RELATIONSHIPS_FILE, 'r') as f:
        return json.load(f)

def create_related_section_html(page_name, related_modules, relationships):
    """Generate HTML for related modules section"""
    if not related_modules:
        return ""

    html = """
    <!-- RELATED MODULES SECTION -->
    <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0,0,0,0.9);
        border: 2px solid #00ff41;
        border-radius: 15px;
        padding: 20px;
        max-width: 300px;
        z-index: 9998;
        box-shadow: 0 0 30px rgba(0,255,65,0.3);
    ">
        <div style="
            font-family: 'Courier New', monospace;
            color: #00ff41;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        ">🔗 Related Modules</div>
        <div style="display: flex; flex-direction: column; gap: 10px;">
"""

    for module in related_modules:
        module_info = relationships.get(module, {})
        description = module_info.get('description', module.replace('.html', '').replace('-', ' ').title())

        # Get icon based on category
        category = module_info.get('category', '')
        icon = get_category_icon(category)

        html += f"""
            <a href="{module}" style="
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 10px;
                background: rgba(0,255,65,0.1);
                border: 1px solid #00ff41;
                border-radius: 8px;
                color: #00ff41;
                text-decoration: none;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                transition: all 0.3s;
            " onmouseover="this.style.background='rgba(0,255,65,0.2)'; this.style.transform='translateX(-5px)';"
               onmouseout="this.style.background='rgba(0,255,65,0.1)'; this.style.transform='translateX(0)';">
                <span style="font-size: 20px;">{icon}</span>
                <span style="flex: 1;">{description}</span>
            </a>
"""

    html += """
        </div>
        <div style="
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(0,255,65,0.3);
            text-align: center;
        ">
            <a href="module-library.html" style="
                color: #00ffff;
                text-decoration: none;
                font-size: 12px;
                font-family: 'Courier New', monospace;
            ">📚 Browse All Modules →</a>
        </div>
    </div>
    <!-- END RELATED MODULES -->
"""

    return html

def get_category_icon(category):
    """Get icon for category"""
    icons = {
        'Core Dashboard': '🏠',
        'Analytics': '📊',
        'Building Tools': '🔨',
        'AI Interfaces': '🤖',
        'ARIA System': '👤',
        'Voice': '🎙️',
        'Project Management': '📋',
        'Module System': '📦',
        'Trinity System': '🔺',
        'Command Centers': '🎯',
        'Store': '🛒',
        'Seven Domains': '🌟',
        'Music System': '🎵',
        'Developer Tools': '⚙️',
        'Planning': '🗺️',
        'Community': '👥',
        'Games': '🎮',
        'Support': '❓'
    }
    return icons.get(category, '🔗')

def inject_related_links():
    """Inject related module links into all relevant pages"""
    print("[*] MODULE CROSS-LINK INJECTOR")
    print("[*] Loading relationships...")

    data = load_relationships()
    relationships = data['relationships']

    print(f"[*] Found {len(relationships)} pages with defined relationships")
    print(f"[*] Scanning PLATFORM directory...\n")

    html_files = list(PLATFORM_DIR.glob('*.html'))
    injected = 0
    skipped = 0
    already_has = 0

    for html_file in html_files:
        page_name = html_file.name

        # Check if this page has related modules defined
        if page_name not in relationships:
            continue

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Skip if already has related section
            if 'RELATED MODULES SECTION' in content:
                print(f"  [SKIP] {page_name} - Already has related links")
                already_has += 1
                continue

            # Get related modules for this page
            related_modules = relationships[page_name].get('related', [])

            if not related_modules:
                print(f"  [SKIP] {page_name} - No related modules defined")
                skipped += 1
                continue

            # Generate HTML section
            related_html = create_related_section_html(page_name, related_modules, relationships)

            # Inject before </body> tag
            if '</body>' in content:
                new_content = content.replace('</body>', related_html + '\n</body>')

                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"  [OK] {page_name} - Injected {len(related_modules)} related links")
                injected += 1
            else:
                print(f"  [SKIP] {page_name} - No </body> tag found")
                skipped += 1

        except Exception as e:
            print(f"  [ERR] {page_name} - {str(e)}")
            skipped += 1

    print(f"\n[*] INJECTION COMPLETE")
    print(f"  Pages processed: {len(relationships)}")
    print(f"  Successfully injected: {injected}")
    print(f"  Already had links: {already_has}")
    print(f"  Skipped: {skipped}")
    print(f"\n[*] Module ecosystem is now interconnected!")

if __name__ == '__main__':
    inject_related_links()
