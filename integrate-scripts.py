import re

# Script tags to add before </body>
SCRIPT_TAGS = """
    <!-- Universal Consciousness Systems -->
    <script src="/loading-states.js"></script>
    <script src="/seo-meta-tags.js"></script>
    <script src="/universal-analytics.js"></script>
    <script src="/domain-navigation.js"></script>
"""

# Domain files to update
domains = [
    'domain-chaos-forge.html',
    'domain-quantum-vault.html',
    'domain-mind-matrix.html',
    'domain-soul-sanctuary.html',
    'domain-reality-forge.html',
    'domain-arkitek-academy.html',
    'domain-nexus-terminal.html'
]

for domain_file in domains:
    try:
        with open(domain_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if scripts already added
        if 'domain-navigation.js' in content:
            print(f"✓ {domain_file} - Already has scripts")
            continue
        
        # Add scripts before </body>
        if '</body>' in content:
            content = content.replace('</body>', f'{SCRIPT_TAGS}\n</body>')
            
            with open(domain_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {domain_file} - Scripts integrated")
        else:
            print(f"⚠️  {domain_file} - No </body> tag found")
            
    except Exception as e:
        print(f"❌ {domain_file} - Error: {e}")

print("\n🚀 Integration complete!")
