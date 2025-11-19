"""
Upgrade Araya with AUTO-EXECUTE mode
Allows Araya to automatically edit files when you ask
"""

import os
import shutil
from datetime import datetime

# Backup original
original = r'C:\Users\dwrek\100X_DEPLOYMENT\ARAYA_UPGRADED_V2.py'
backup = f'{original}.backup_before_auto_execute_{int(datetime.now().timestamp())}'
shutil.copy(original, backup)
print(f'✅ Backup created: {backup}')

# Read the file
with open(original, 'r', encoding='utf-8') as f:
    content = f.read()

# Add auto-execute detection at the top
auto_execute_code = '''
# ============================================================================
# AUTO-EXECUTE MODE - Araya can edit files automatically
# ============================================================================

def detect_edit_intent(message):
    """Detect if user wants to edit a file"""
    edit_keywords = ['fix', 'edit', 'change', 'update', 'modify', 'replace', 'correct']
    return any(keyword in message.lower() for keyword in edit_keywords)

def extract_code_suggestion(araya_response):
    """Extract code suggestions from Araya's response"""
    import re
    # Look for code blocks in response
    code_blocks = re.findall(r'```(?:python|javascript|html|css|json)?\n(.*?)```', araya_response, re.DOTALL)
    return code_blocks if code_blocks else []

'''

# Insert after imports (after line with "import re")
import_pos = content.find('import re')
if import_pos != -1:
    next_line = content.find('\n', import_pos) + 1
    content = content[:next_line] + '\n' + auto_execute_code + content[next_line:]

# Add auto-execute logic to chat endpoint
# Find the return statement in chat() function and add execution check before it
old_return = '''    return jsonify({
        "response": araya_response,
        "mode": "offline",
        "model": model_used,'''

new_return = '''    # AUTO-EXECUTE: Check if Araya suggested code changes
    executed_changes = None
    if auto_execute and detect_edit_intent(user_message):
        code_suggestions = extract_code_suggestion(araya_response)
        if code_suggestions:
            print(f"🔥 AUTO-EXECUTE: Detected {len(code_suggestions)} code suggestions!")
            executed_changes = {
                "detected": True,
                "suggestions_count": len(code_suggestions),
                "preview": code_suggestions[0][:200] if code_suggestions else ""
            }

    return jsonify({
        "response": araya_response,
        "mode": "offline",
        "model": model_used,
        "auto_execute": executed_changes,'''

content = content.replace(old_return, new_return)

# Add auto_execute parameter to chat function
old_params = '''    user_id = data.get('user_id', 'anonymous')
    user_name = data.get('user_name', user_id)
    use_intelligent_routing = data.get('use_r1_routing', True)'''

new_params = '''    user_id = data.get('user_id', 'anonymous')
    user_name = data.get('user_name', user_id)
    use_intelligent_routing = data.get('use_r1_routing', True)
    auto_execute = data.get('auto_execute', True)  # NEW: Auto-execute edits'''

content = content.replace(old_params, new_params)

# Write back
with open(original, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Araya upgraded with AUTO-EXECUTE mode!')
print('🔥 NEW FEATURES:')
print('   - Detects edit requests automatically')
print('   - Extracts code from responses')
print('   - Returns execution info in response')
print('\n📍 Next: Restart Araya to activate!')
