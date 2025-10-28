#!/usr/bin/env python3
"""Improve Araya's conversation history prompt format for better R1 understanding"""

# Read the file
with open('ARAYA_UPGRADED_V2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the prompt building section with improved format
old_prompt_section = '''    # Build prompt with history
    if conversation_context:
        prompt = f"{ARAYA_SYSTEM_PROMPT}\\n\\n## Previous Conversation:\\n{conversation_context}\\n## Current Question:\\nUser: {user_message}\\n\\nAraya:"
    else:
        prompt = f"{ARAYA_SYSTEM_PROMPT}\\n\\nUser: {user_message}\\n\\nAraya:"'''

new_prompt_section = '''    # Build prompt with history - IMPROVED FORMAT
    if conversation_context:
        prompt = f"""{ARAYA_SYSTEM_PROMPT}

---
IMPORTANT: You have talked to this user before. Here is your previous conversation:

{conversation_context}---

The user's new message is:
User: {user_message}

Remember what they told you in the previous conversation. Use that context to answer their new question.

Araya:"""
    else:
        prompt = f"{ARAYA_SYSTEM_PROMPT}\\n\\nUser: {user_message}\\n\\nAraya:"'''

content = content.replace(old_prompt_section, new_prompt_section)

# Write the improved version
with open('ARAYA_UPGRADED_V2.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Improved conversation history format!")
print("   - Clearer separation of previous vs current messages")
print("   - Explicit instruction to remember previous context")
print("   - Better formatting for R1 model understanding")
