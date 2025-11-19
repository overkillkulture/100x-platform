import re
from pathlib import Path
import json

def extract_all_links(html_content):
    links = set()

    # Links
    for match in re.finditer(r'href=["\']([^"\']+)["\']', html_content, re.IGNORECASE):
        link = match.group(1)
        if link and link != '#' and not link.startswith('javascript:') and not link.startswith('mailto:'):
            links.add(link)

    # Window.location
    for match in re.finditer(r'(?:window\.location|location\.href)\s*=\s*["\']([^"\']+)["\']', html_content):
        links.add(match.group(1))

    return list(links)

# Scan ALL files
site_map = {}
all_files = set()
all_targets = set()

html_files = list(Path('.').glob('*.html'))

for file_path in html_files:
    all_files.add(file_path.name)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            links = extract_all_links(content)

            # Extract just filenames from links
            clean_links = []
            for link in links:
                # Remove query params and anchors
                clean = link.split('?')[0].split('#')[0]
                # Get just filename if it's a relative path
                if not clean.startswith('http'):
                    clean = clean.strip('/')
                    if clean and not clean.startswith('data:'):
                        clean_links.append(clean)
                        all_targets.add(clean)

            if clean_links:
                site_map[file_path.name] = clean_links
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Find broken links (targets that don't exist)
broken_links = {}
for page, targets in site_map.items():
    broken = [t for t in targets if t not in all_files and t.endswith('.html')]
    if broken:
        broken_links[page] = broken

# Find entry points (pages not linked from anywhere)
all_linked_pages = set()
for targets in site_map.values():
    for t in targets:
        if t in all_files:
            all_linked_pages.add(t)

orphan_pages = all_files - all_linked_pages

# Save to JSON
output = {
    'total_pages': len(all_files),
    'pages_with_links': len(site_map),
    'total_unique_targets': len(all_targets),
    'broken_links_count': sum(len(v) for v in broken_links.values()),
    'orphan_pages_count': len(orphan_pages),
    'site_map': site_map,
    'broken_links': broken_links,
    'orphan_pages': sorted(list(orphan_pages)),
    'all_pages': sorted(list(all_files))
}

with open('SITE_MAP.json', 'w') as f:
    json.dump(output, f, indent=2)

print('✅ Complete site map created!')
print(f'📄 Total pages: {len(all_files)}')
print(f'🔗 Pages with links: {len(site_map)}')
print(f'❌ Broken links found: {sum(len(v) for v in broken_links.values())}')
print(f'🏝️  Orphan pages (not linked): {len(orphan_pages)}')
print()

if broken_links:
    print('=== TOP BROKEN LINKS ===')
    for page, broken in list(broken_links.items())[:10]:
        print(f'\n📄 {page}:')
        for link in broken[:5]:
            print(f'  ❌ {link}')

if orphan_pages:
    print(f'\n=== ORPHAN PAGES (First 20) ===')
    for page in sorted(list(orphan_pages))[:20]:
        print(f'  🏝️  {page}')

print('\n💾 Full data saved to: SITE_MAP.json')
