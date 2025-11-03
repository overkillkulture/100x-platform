#!/usr/bin/env python3
"""
SIMPLE PORT FORWARDER USING PYTHON
Uses pyngrok library to expose localhost:5000 to public internet
100% Python, no permanent changes, stops when script stops
"""

import subprocess
import sys
import time

def install_pyngrok():
    """Install pyngrok if not already installed"""
    try:
        import pyngrok
        print("✅ pyngrok already installed")
    except ImportError:
        print("📦 Installing pyngrok...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
        print("✅ pyngrok installed successfully")

def expose_terminal():
    """Expose the terminal to public internet"""
    from pyngrok import ngrok, conf

    print("=" * 60)
    print("🌐 EXPOSING AI TERMINAL TO PUBLIC INTERNET")
    print("=" * 60)

    # Start ngrok tunnel to localhost:5000
    print("\n📡 Creating public tunnel to localhost:5000...")
    public_url = ngrok.connect(5000, bind_tls=True)

    print("\n✅ PUBLIC URL READY:")
    print(f"   {public_url}")
    print("\n📋 GIVE THIS URL TO YOUR USER:")
    print(f"   {public_url}/api/test")
    print("\n💬 CHAT ENDPOINT:")
    print(f"   POST {public_url}/api/emergency-chat")
    print("\n" + "=" * 60)
    print("Press Ctrl+C to stop and close the tunnel")
    print("=" * 60)

    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down tunnel...")
        ngrok.disconnect(public_url)
        print("✅ Tunnel closed safely")

if __name__ == '__main__':
    install_pyngrok()
    expose_terminal()
