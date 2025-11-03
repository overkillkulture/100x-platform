"""
PURGE POLICE ACCOUNTABILITY THEMING
Removes all police-themed content from workspace files
"""
import os
import re

deploy_dir = 'C:/Users/dwrek/100X_DEPLOYMENT'

# Police-themed patterns to replace
replacements = {
    'Police Accountability System': 'Consciousness Builder System',
    'Police Accountability': 'Builder Workspace',
    'AI-Powered Police Accountability Workspace': 'AI-Powered Consciousness Workspace',
    'police accountability': 'consciousness building',
}

html_files = [
    'workspace-v2.html',
    'gta-hud.html',
    'gta-hud-expandable.html',
    'jarvis.html',
    'workspace.html'
]

print("🔥 PURGING POLICE ACCOUNTABILITY THEMING...\n")

cleaned_count = 0
for filename in html_files:
    filepath = os.path.join(deploy_dir, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Replace all patterns
            for old_text, new_text in replacements.items():
                content = content.replace(old_text, new_text)

            # Also fix specific HTML patterns
            content = re.sub(r'<div class="module-name">Police</div>', '<div class="module-name">Builder</div>', content)
            content = re.sub(r'workspace-enhanced\.html', 'workspace-v3.html', content)

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'✅ Cleaned: {filename}')
                cleaned_count += 1
            else:
                print(f'✓ Already clean: {filename}')
        except Exception as e:
            print(f'❌ Error with {filename}: {e}')
    else:
        print(f'⚠ Not found: {filename}')

print(f'\n🎯 Total files cleaned: {cleaned_count}')
print("✅ PURGE COMPLETE!\n")
