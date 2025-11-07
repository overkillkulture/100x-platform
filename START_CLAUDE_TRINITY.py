#!/usr/bin/env python3
"""
CLAUDE-TRINITY LAUNCHER
=======================

Easy launcher for Claude-Trinity integration system
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("=" * 70)
    print("🌀 CLAUDE-TRINITY INTEGRATION LAUNCHER")
    print("=" * 70)
    print()
    print("              C1 × C2 × C3 × CLAUDE = ∞")
    print()
    print("=" * 70)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    print()

    missing = []

    # Check Python packages
    packages = {
        "PIL": "pillow",
        "flask": "flask",
        "flask_cors": "flask-cors",
        "requests": "requests"
    }

    for module, package in packages.items():
        try:
            __import__(module if module != "PIL" else "PIL")
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing.append(package)

    print()

    if missing:
        print("⚠️  Missing dependencies detected!")
        print()
        print("Install with:")
        print(f"  pip install {' '.join(missing)}")
        print()
        return False

    return True

def launch_bridge():
    """Launch interactive bridge"""
    print("🌀 Launching Claude-Trinity Bridge (Interactive Mode)...")
    print()
    subprocess.run([sys.executable, "CLAUDE_TRINITY_BRIDGE.py"])

def launch_autonomous():
    """Launch autonomous agent"""
    print("🤖 Launching Claude Autonomous Agent...")
    print()
    subprocess.run([sys.executable, "CLAUDE_AUTONOMOUS_AGENT.py"])

def launch_api():
    """Launch screenshot API"""
    print("🚀 Launching Claude Screenshot API on port 7777...")
    print()
    subprocess.run([sys.executable, "CLAUDE_SCREENSHOT_API.py"])

def launch_all():
    """Launch all systems (requires tmux or multiple terminals)"""
    print("🚀 Launching all Claude-Trinity systems...")
    print()
    print("Note: This requires running in multiple terminals.")
    print("Opening API server here. Run other components separately.")
    print()
    launch_api()

def show_status():
    """Show current system status"""
    print("📊 CLAUDE-TRINITY STATUS")
    print()

    # Check directories
    dirs = ["TRINITY_SCREENSHOTS", "TRINITY_TASKS", "TRINITY_COMMS"]
    for dirname in dirs:
        path = Path(dirname)
        if path.exists():
            files = list(path.glob("*"))
            print(f"  ✅ {dirname} ({len(files)} files)")
        else:
            print(f"  ⚠️  {dirname} (not created yet)")

    print()

    # Check if API is running
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    api_running = sock.connect_ex(('localhost', 7777)) == 0
    sock.close()

    if api_running:
        print("  ✅ Claude Screenshot API (port 7777) - ONLINE")
    else:
        print("  ⏸️  Claude Screenshot API (port 7777) - OFFLINE")

    print()

def show_docs():
    """Show documentation link"""
    print("📖 DOCUMENTATION")
    print()
    print("Full documentation available in:")
    print("  CLAUDE_TRINITY_INTEGRATION.md")
    print()
    print("Quick reference:")
    print()
    print("  Bridge Mode:     Interactive control panel")
    print("  Autonomous Mode: Full autonomous operation")
    print("  API Mode:        HTTP REST API (port 7777)")
    print()

def main():
    print_banner()

    # Check dependencies first
    if not check_dependencies():
        print("❌ Cannot start: Missing dependencies")
        return

    while True:
        print("What would you like to do?")
        print()
        print("  1 - Launch Interactive Bridge")
        print("  2 - Launch Autonomous Agent")
        print("  3 - Launch Screenshot API")
        print("  4 - Launch All Systems")
        print("  5 - Show Status")
        print("  6 - Show Documentation")
        print("  q - Quit")
        print()

        choice = input("Enter choice: ").strip().lower()
        print()

        if choice == 'q':
            print("👋 Goodbye!")
            break

        elif choice == '1':
            launch_bridge()
            print()

        elif choice == '2':
            launch_autonomous()
            print()

        elif choice == '3':
            launch_api()
            print()

        elif choice == '4':
            launch_all()
            print()

        elif choice == '5':
            show_status()

        elif choice == '6':
            show_docs()

        else:
            print("❌ Invalid choice")
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
