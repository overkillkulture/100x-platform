#!/usr/bin/env python3
"""
Quick script to get ngrok URL
"""

from pyngrok import ngrok
import sys

# Set auth token
ngrok.set_auth_token("33uQkzQLGA91pd27l77tXQvemdB_4WBc16JZqjomtG8tDQpzb")

# Start tunnel
print("Starting tunnel...", file=sys.stderr)
public_url = ngrok.connect(5000, bind_tls=True)

# Print just the URL (clean output)
print(str(public_url))
print(f"\nTest URL: {public_url}/api/test", file=sys.stderr)
print(f"Chat URL: {public_url}/api/emergency-chat", file=sys.stderr)

# Keep it running
print("\nTunnel is active. Press Ctrl+C to stop.", file=sys.stderr)
try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping...", file=sys.stderr)
    ngrok.disconnect(public_url)
