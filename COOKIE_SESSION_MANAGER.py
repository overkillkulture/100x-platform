#!/usr/bin/env python3
"""
COOKIE SESSION MANAGER
Saves browser sessions so automation never needs to login again

WHAT IT DOES:
- Extracts cookies from your Chrome browser
- Saves them encrypted
- Playwright can reuse them to stay logged in
- Never type password twice

SOLVES:
- Yesterday's Namecheap login nightmare
- Any automation that needs authenticated sessions
- Cookie-based session management

USAGE:
  python COOKIE_SESSION_MANAGER.py save namecheap
  python COOKIE_SESSION_MANAGER.py load namecheap
"""

import browser_cookie3
import json
import pickle
from pathlib import Path
from cryptography.fernet import Fernet
from datetime import datetime
import sys

class CookieSessionManager:
    def __init__(self):
        self.sessions_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/SESSIONS")
        self.sessions_dir.mkdir(exist_ok=True)

        # Encryption key (in production, use Windows DPAPI or secure vault)
        self.key_file = self.sessions_dir / "session.key"
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)

    def _get_or_create_key(self):
        """Get existing encryption key or create new one"""
        if self.key_file.exists():
            return self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            return key

    def save_session(self, site_name, domain):
        """
        Save cookies from Chrome for specified domain

        Args:
            site_name: friendly name (e.g., 'namecheap')
            domain: cookie domain (e.g., '.namecheap.com')
        """
        print(f"🔓 Extracting cookies from Chrome for {domain}...")

        try:
            # Get cookies from Chrome
            cookies = browser_cookie3.chrome(domain_name=domain)

            # Convert to list of dicts for Playwright
            cookie_list = []
            for cookie in cookies:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'expires': cookie.expires,
                    'httpOnly': False,
                    'secure': cookie.secure,
                    'sameSite': 'Lax'
                }
                cookie_list.append(cookie_dict)

            if not cookie_list:
                print(f"❌ No cookies found for {domain}")
                print(f"   Make sure you're logged in to {site_name} in Chrome")
                return False

            # Save encrypted
            session_data = {
                'site_name': site_name,
                'domain': domain,
                'cookies': cookie_list,
                'saved_at': datetime.now().isoformat()
            }

            # Encrypt and save
            json_data = json.dumps(session_data).encode()
            encrypted = self.cipher.encrypt(json_data)

            session_file = self.sessions_dir / f"{site_name}.session"
            session_file.write_bytes(encrypted)

            print(f"✅ Saved {len(cookie_list)} cookies for {site_name}")
            print(f"   File: {session_file}")
            return True

        except Exception as e:
            print(f"❌ Error saving session: {e}")
            return False

    def load_session(self, site_name):
        """
        Load saved cookies for Playwright

        Args:
            site_name: friendly name (e.g., 'namecheap')

        Returns:
            list of cookie dicts for Playwright
        """
        session_file = self.sessions_dir / f"{site_name}.session"

        if not session_file.exists():
            print(f"❌ No saved session for {site_name}")
            print(f"   Run: python COOKIE_SESSION_MANAGER.py save {site_name}")
            return None

        try:
            # Decrypt and load
            encrypted = session_file.read_bytes()
            json_data = self.cipher.decrypt(encrypted)
            session_data = json.loads(json_data)

            print(f"✅ Loaded {len(session_data['cookies'])} cookies for {site_name}")
            print(f"   Saved: {session_data['saved_at']}")

            return session_data['cookies']

        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None

    def list_sessions(self):
        """List all saved sessions"""
        session_files = list(self.sessions_dir.glob("*.session"))

        if not session_files:
            print("📭 No saved sessions")
            return

        print(f"\n📋 Saved sessions ({len(session_files)}):\n")

        for session_file in session_files:
            try:
                encrypted = session_file.read_bytes()
                json_data = self.cipher.decrypt(encrypted)
                session_data = json.loads(json_data)

                print(f"  • {session_data['site_name']}")
                print(f"    Domain: {session_data['domain']}")
                print(f"    Cookies: {len(session_data['cookies'])}")
                print(f"    Saved: {session_data['saved_at']}")
                print()

            except Exception as e:
                print(f"  • {session_file.stem} (error reading)")
                print()

# Predefined site configurations
SITES = {
    'namecheap': '.namecheap.com',
    'netlify': '.netlify.com',
    'stripe': '.stripe.com',
    'github': '.github.com',
    'instagram': '.instagram.com',
    'twitter': '.twitter.com',
    'godaddy': '.godaddy.com',
}

def main():
    """CLI interface"""
    manager = CookieSessionManager()

    if len(sys.argv) < 2:
        print("""
🍪 COOKIE SESSION MANAGER

USAGE:
  python COOKIE_SESSION_MANAGER.py save <site>
  python COOKIE_SESSION_MANAGER.py load <site>
  python COOKIE_SESSION_MANAGER.py list

SITES:
  namecheap, netlify, stripe, github, instagram, twitter, godaddy

EXAMPLES:
  # Save your Namecheap login session
  python COOKIE_SESSION_MANAGER.py save namecheap

  # Load it in automation
  python COOKIE_SESSION_MANAGER.py load namecheap

  # See all saved sessions
  python COOKIE_SESSION_MANAGER.py list

HOW IT WORKS:
  1. Login to site in Chrome manually (once)
  2. Save the session with this tool
  3. Automation uses saved session forever
  4. Never type password again
        """)
        return

    command = sys.argv[1]

    if command == 'list':
        manager.list_sessions()

    elif command == 'save':
        if len(sys.argv) < 3:
            print("Usage: python COOKIE_SESSION_MANAGER.py save <site>")
            print(f"Sites: {', '.join(SITES.keys())}")
            return

        site_name = sys.argv[2]

        if site_name not in SITES:
            print(f"Unknown site: {site_name}")
            print(f"Known sites: {', '.join(SITES.keys())}")
            return

        domain = SITES[site_name]
        manager.save_session(site_name, domain)

    elif command == 'load':
        if len(sys.argv) < 3:
            print("Usage: python COOKIE_SESSION_MANAGER.py load <site>")
            return

        site_name = sys.argv[2]
        cookies = manager.load_session(site_name)

        if cookies:
            # Print for use in scripts
            print("\n# Copy this into your Playwright script:")
            print("cookies = " + json.dumps(cookies, indent=2))

    else:
        print(f"Unknown command: {command}")
        print("Commands: save, load, list")

if __name__ == '__main__':
    main()
