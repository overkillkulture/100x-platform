#!/usr/bin/env python3
"""Fix Araya's memory persistence by adding conversation history to Ollama calls"""

# Read the file
with open('ARAYA_UPGRADED_V2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update call_ollama function to accept user_id and include conversation history
old_call_ollama = '''def call_ollama(user_message):
    """Call Ollama locally - NO INTERNET"""
    prompt = f"{ARAYA_SYSTEM_PROMPT}\\n\\nUser: {user_message}\\n\\nAraya:"

    try:
        result = subprocess.run(
            ['ollama', 'run', 'deepseek-r1:8b', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        response = result.stdout.strip()

        # Remove thinking tags if present
        if "<think>" in response:
            parts = response.split("</think>")
            if len(parts) > 1:
                response = parts[1].strip()

        return response

    except Exception as e:
        return f"Araya is temporarily offline. Error: {e}"'''

new_call_ollama = '''def call_ollama(user_message, user_id='anonymous'):
    """Call Ollama locally with conversation history - NO INTERNET"""

    # Load conversation history for context
    conversation_context = ""
    try:
        profile = UserProfile.load(user_id)
        if hasattr(profile, 'araya_conversations') and profile.araya_conversations:
            # Get last 5 conversations for context (avoid token limits)
            recent_conversations = profile.araya_conversations[-5:]
            for conv in recent_conversations:
                user_msg = conv.get('user_message', '')
                araya_response = conv.get('araya_response', '')
                conversation_context += f"User: {user_msg}\\nAraya: {araya_response}\\n\\n"
    except:
        pass  # If profile doesn't load, continue without history

    # Build prompt with history
    if conversation_context:
        prompt = f"{ARAYA_SYSTEM_PROMPT}\\n\\n## Previous Conversation:\\n{conversation_context}\\n## Current Question:\\nUser: {user_message}\\n\\nAraya:"
    else:
        prompt = f"{ARAYA_SYSTEM_PROMPT}\\n\\nUser: {user_message}\\n\\nAraya:"

    try:
        result = subprocess.run(
            ['ollama', 'run', 'deepseek-r1:8b', prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        response = result.stdout.strip()

        # Remove thinking tags if present
        if "<think>" in response:
            parts = response.split("</think>")
            if len(parts) > 1:
                response = parts[1].strip()

        return response

    except Exception as e:
        return f"Araya is temporarily offline. Error: {e}"'''

content = content.replace(old_call_ollama, new_call_ollama)

# Fix 2: Update all call_ollama() calls to pass user_id
# In the chat endpoint (around line 355, 351, 359)
content = content.replace(
    'araya_response = call_ollama(user_message)',
    'araya_response = call_ollama(user_message, user_id)'
)

# Write the fixed version
with open('ARAYA_UPGRADED_V2.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed Araya memory persistence!")
print("   - call_ollama() now accepts user_id")
print("   - Loads last 5 conversations for context")
print("   - Includes conversation history in prompt")
