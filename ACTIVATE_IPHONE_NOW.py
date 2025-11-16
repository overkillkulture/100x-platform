#!/usr/bin/env python3
"""
🌀 INSTANT iPHONE ACCESS - Creates public URL for conversational system

This script:
1. Starts the conversational system on port 9000
2. Creates ngrok tunnel to make it publicly accessible
3. Gives you a URL to access from your iPhone

Just run: python3 ACTIVATE_IPHONE_NOW.py
"""

from pyngrok import ngrok
import subprocess
import time
import sys
import os

# Set ngrok auth token (from existing START_NGROK_TUNNEL.py)
ngrok.set_auth_token("33uQkzQLGA91pd27l77tXQvemdB_4WBc16JZqjomtG8tDQpzb")

print("=" * 70)
print("🌀 ACTIVATING CONVERSATIONAL SYSTEM FOR iPHONE ACCESS")
print("=" * 70)

# Start conversational system in background
print("\n📡 Starting conversational system on localhost:9000...")
conv_process = subprocess.Popen(
    [sys.executable, "conversational_system.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=os.path.dirname(os.path.abspath(__file__))
)

# Give it a moment to start
print("⏳ Waiting for system to initialize...")
time.sleep(3)

# Create ngrok tunnel
print("🌐 Creating public tunnel via ngrok...")
public_url = ngrok.connect(9000, bind_tls=True)

print("\n" + "=" * 70)
print("✅ SYSTEM IS LIVE - ACCESSIBLE FROM YOUR iPHONE!")
print("=" * 70)
print(f"\n🔗 PUBLIC URL: {public_url}")
print("\n📱 ON YOUR iPHONE:")
print(f"   1. Open Safari")
print(f"   2. Go to: {public_url}")
print(f"   3. Ask questions like:")
print(f"      - What is Cyclotron?")
print(f"      - How do I file Monell claim?")
print(f"      - What is Trinity?")
print(f"      - What are destroyer companies?")
print("\n" + "=" * 70)
print("\n💡 THE SYSTEM:")
print("   - Searches all documentation automatically")
print("   - Natural language interface")
print("   - Access from anywhere")
print("   - Works until you close this terminal")
print("\n" + "=" * 70)
print("\n⚠️  Press Ctrl+C to stop the system and close tunnel")
print("=" * 70 + "\n")

try:
    # Keep running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    print("   Closing tunnel...")
    ngrok.disconnect(public_url)
    print("   Stopping conversational system...")
    conv_process.terminate()
    conv_process.wait()
    print("✅ System shut down safely")
