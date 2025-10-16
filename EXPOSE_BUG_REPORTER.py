#!/usr/bin/env python3
"""
EXPOSE BUG REPORTER API TO PUBLIC INTERNET
Uses pyngrok to expose localhost:5001
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

def expose_bug_reporter():
    """Expose the bug reporter API to public internet"""
    from pyngrok import ngrok

    print("=" * 60)
    print("🐛 EXPOSING BUG REPORTER API TO PUBLIC INTERNET")
    print("=" * 60)

    # Start ngrok tunnel to localhost:5001
    print("\n📡 Creating public tunnel to localhost:5001...")
    public_url = ngrok.connect(5001, bind_tls=True)

    print("\n✅ PUBLIC URL READY:")
    print(f"   {public_url}")
    print("\n🐛 BUG REPORT ENDPOINT:")
    print(f"   POST {public_url}/api/bug-report")
    print("\n📝 UPDATE THIS URL IN:")
    print("   100X_DEPLOYMENT/PLATFORM/bug-reporter-widget.js")
    print("   (Change CONFIG.submitURL)")
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
    expose_bug_reporter()
