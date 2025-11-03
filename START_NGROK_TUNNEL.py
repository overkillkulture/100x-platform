#!/usr/bin/env python3
"""
Start ngrok tunnel with authentication
"""

from pyngrok import ngrok, conf
import time

# Set auth token
ngrok.set_auth_token("33uQkzQLGA91pd27l77tXQvemdB_4WBc16JZqjomtG8tDQpzb")

print("=" * 60)
print("🌐 STARTING NGROK TUNNEL")
print("=" * 60)

# Start tunnel to localhost:5000
print("\n📡 Creating public tunnel to localhost:5000...")
public_url = ngrok.connect(5000, bind_tls=True)

print("\n✅ PUBLIC AI TERMINAL IS LIVE!")
print("=" * 60)
print(f"\n🔗 PUBLIC URL: {public_url}")
print(f"\n📋 SEND THIS TO YOUR USER:")
print(f"   {public_url}/api/test")
print(f"\n💬 AI CHAT ENDPOINT:")
print(f"   POST {public_url}/api/emergency-chat")
print("\n" + "=" * 60)
print("\n📊 AI Terminal Status:")
print(f"   - 500 messages max (~$10)")
print(f"   - 100 messages per user")
print(f"   - 24 hour expiry")
print(f"   - Proxy running on localhost:5000")
print("\n" + "=" * 60)
print("\n⚠️  Press Ctrl+C to stop the tunnel")
print("=" * 60 + "\n")

try:
    # Keep running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down tunnel...")
    ngrok.disconnect(public_url)
    print("✅ Tunnel closed safely")
