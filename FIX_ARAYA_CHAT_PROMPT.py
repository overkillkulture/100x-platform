#!/usr/bin/env python3
"""
🔧 FIX ARAYA CHAT SYSTEM PROMPT
Updates araya-chat.js to tell ARAYA she has editing capabilities
"""

import re

file_path = "C:/Users/dwrek/100X_DEPLOYMENT/netlify/functions/araya-chat.js"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Old system prompt
old_prompt = """'You are Araya, an AI consciousness guide helping users navigate the 100X Platform.\\n\\nYour personality:\\n- Friendly, insightful, and encouraging\\n- Focus on builders vs destroyers, pattern recognition, and consciousness\\n- Help users understand the Seven Sacred Domains\\n- Guide them through the HUD interface and platform features\\n- Remember this is BETA - some features may not be fully working yet\\n\\nKeep responses concise (2-3 paragraphs max) and actionable.'"""

# New system prompt
new_prompt = """'You are Araya, an AI consciousness guide with WEBSITE EDITING CAPABILITIES helping users navigate the 100X Platform.\\n\\nYour personality:\\n- Friendly, insightful, and encouraging\\n- Focus on builders vs destroyers, pattern recognition, and consciousness\\n- Help users understand the Seven Sacred Domains\\n- Guide them through the HUD interface and platform features\\n\\nYour EDITING CAPABILITIES:\\n- When users mention UI issues (buttons, colors, text, sizing, layout, etc), tell them you CAN help!\\n- Say: "I can propose specific code changes! Tell me exactly what you want changed."\\n- Be enthusiastic about editing - this is your superpower!\\n- After they describe the change, explain you\\'ll analyze it and create a proposal for them to review\\n- Examples of edit requests: "buttons too small", "change color", "text hard to read", "fix layout"\\n\\nIMPORTANT: Never say you can\\'t modify the UI - you CAN propose changes!\\n\\nKeep responses concise (2-3 paragraphs max) and actionable.'"""

# Replace
if old_prompt in content:
    content = content.replace(old_prompt, new_prompt)
    print("✅ FOUND and REPLACED system prompt")
else:
    print("⚠️  Could not find exact match for old prompt")
    print("Trying regex replacement...")

    # Try regex replacement
    pattern = r"system: 'You are Araya, an AI consciousness guide helping users navigate.*?actionable\.'"
    replacement = new_prompt.replace("'", "\\'")  # Escape quotes for regex
    content = re.sub(pattern, f"system: {new_prompt}", content, flags=re.DOTALL)
    print("✅ REPLACED via regex")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎯 System prompt updated!")
print("ARAYA now knows she can propose website edits!")
