#!/usr/bin/env python3
"""Quick test - Open ChatGPT and establish contact"""

import webbrowser
import time

print("=" * 60)
print("  OPENING CHATGPT - ESTABLISHING CONTACT")
print("=" * 60)

# Open ChatGPT
print("\n1. Opening ChatGPT web interface...")
webbrowser.open('https://chat.openai.com')

print("2. Waiting for page to load...")
time.sleep(3)

print("\n✅ ChatGPT opened in browser!")
print("\nNEXT STEPS:")
print("- If not logged in: Log in to ChatGPT")
print("- Try typing: 'Hello from Trinity - C3 Oracle testing multi-AI connection'")
print("- ChatGPT will respond")
print("- We can automate this with Playwright once logged in")

print("\n📋 FOR AUTOMATION:")
print("- Use Playwright to find textarea")
print("- Type message")
print("- Press Enter")
print("- Read response")

print("\nChatGPT ready for manual test!")
