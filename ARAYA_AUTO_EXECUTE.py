"""
ARAYA AUTO-EXECUTE MODE
Detects when user wants to edit files and executes automatically
"""

import re
import requests

def detect_edit_intent(message):
    """Detect if user wants to edit a file"""
    edit_keywords = [
        'fix', 'edit', 'change', 'update', 'modify',
        'replace', 'correct', 'adjust', 'rewrite'
    ]

    message_lower = message.lower()
    for keyword in edit_keywords:
        if keyword in message_lower:
            return True
    return False

def extract_file_and_changes(message, araya_response):
    """
    Extract file path and what to change from conversation
    Returns: (file_path, find_text, replace_text) or (None, None, None)
    """

    # Try to find file path in message
    file_patterns = [
        r'(?:in|file|path)\s+([^\s]+\.(?:py|js|html|css|json|md))',
        r'([A-Z_]+\.(?:py|js|html|css|json|md))',
        r'(C:[^\s]+\.(?:py|js|html|css|json|md))',
    ]

    file_path = None
    for pattern in file_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            file_path = match.group(1)
            break

    # If Araya's response contains code blocks, extract them
    code_blocks = re.findall(r'```(?:python|javascript|html|css)?\n(.*?)```', araya_response, re.DOTALL)

    if file_path and len(code_blocks) >= 2:
        # First block = old code, second block = new code
        return file_path, code_blocks[0].strip(), code_blocks[1].strip()

    return None, None, None

def execute_edit(file_path, find_text, replace_text):
    """Execute the file edit via Araya's API"""
    try:
        response = requests.post('http://localhost:6666/api/edit-file', json={
            'file_path': file_path,
            'find_text': find_text,
            'replace_text': replace_text
        })
        return response.json()
    except Exception as e:
        return {'success': False, 'error': str(e)}

# This will be integrated into ARAYA_UPGRADED_V2.py
