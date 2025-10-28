#!/usr/bin/env python3
"""Fix Araya memory by using Ollama HTTP API instead of subprocess"""

# Read the file
with open('ARAYA_UPGRADED_V2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add requests import at the top (after other imports)
if "import requests" not in content:
    content = content.replace("import subprocess", "import subprocess\nimport requests")

# Replace the entire call_ollama function with HTTP API version
old_function = '''def call_ollama(user_message, user_id='anonymous'):
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

    # Build prompt with history - IMPROVED FORMAT
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

new_function = '''def call_ollama(user_message, user_id='anonymous'):
    """Call Ollama HTTP API with proper conversation history - NO INTERNET"""

    # Build messages array with conversation history
    messages = [{"role": "system", "content": ARAYA_SYSTEM_PROMPT}]

    # Load conversation history
    try:
        profile = UserProfile.load(user_id)
        if hasattr(profile, 'araya_conversations') and profile.araya_conversations:
            # Get last 5 conversations for context (avoid token limits)
            recent_conversations = profile.araya_conversations[-5:]
            for conv in recent_conversations:
                user_msg = conv.get('user_message', '')
                araya_response = conv.get('araya_response', '')
                # Strip thinking tags from stored responses
                if "...done thinking." in araya_response:
                    araya_response = araya_response.split("...done thinking.")[1].strip()
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": araya_response})
    except:
        pass  # If profile doesn't load, continue without history

    # Add current message
    messages.append({"role": "user", "content": user_message})

    try:
        # Call Ollama HTTP API with conversation history
        response = requests.post('http://localhost:11434/api/chat', json={
            "model": "deepseek-r1:8b",
            "messages": messages,
            "stream": False
        }, timeout=60)

        result = response.json()
        araya_response = result.get('message', {}).get('content', '')

        # Remove thinking tags if present
        if "<think>" in araya_response:
            parts = araya_response.split("</think>")
            if len(parts) > 1:
                araya_response = parts[1].strip()

        # Also handle "...done thinking." format
        if "...done thinking." in araya_response:
            araya_response = araya_response.split("...done thinking.")[1].strip()

        return araya_response

    except Exception as e:
        return f"Araya is temporarily offline. Error: {e}"'''

content = content.replace(old_function, new_function)

# Write the fixed version
with open('ARAYA_UPGRADED_V2.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Switched to Ollama HTTP API!")
print("   - Uses proper message history array")
print("   - Much better conversation context handling")
print("   - Native multi-turn conversation support")
