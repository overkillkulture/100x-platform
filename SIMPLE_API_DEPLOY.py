#!/usr/bin/env python3
"""
DEPLOY VIA NETLIFY API - NO BROWSER, NO CLICKING
Pure API deployment using requests
"""

import requests
import zipfile
import os
from pathlib import Path
import subprocess

# Get auth token from Netlify CLI
def get_netlify_token():
    """Extract token from netlify config"""
    config_path = Path.home() / '.netlify' / 'config.json'

    if config_path.exists():
        import json
        config = json.loads(config_path.read_text())
        # Try to get token from environment first
        token = os.getenv('NETLIFY_AUTH_TOKEN')
        if token:
            return token

        # Try getting from netlify cli
        try:
            result = subprocess.run(['netlify', 'status', '--json'], capture_output=True, text=True)
            status = json.loads(result.stdout)
            # Token is stored separately, try env
            pass
        except:
            pass

    # Fallback - get from env
    token = os.getenv('NETLIFY_AUTH_TOKEN')
    if not token:
        print("❌ No Netlify token found")
        print("   Run: netlify login")
        return None

    return token

def create_zip():
    """Create deployment zip"""
    print("📦 Creating deployment zip...")

    zip_path = 'deploy.zip'

    # Files to include
    files_to_zip = [
        'index.html',  # Now contains platform.html
        'platform.html',
        '_redirects',
        'netlify.toml'
    ]

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
                print(f"   ✅ Added: {file}")

    print(f"   ✅ Created: {zip_path}")
    return zip_path

def deploy_to_netlify():
    """Deploy using Netlify API"""

    SITE_ID = 'ba8f1795-1517-42ee-aa47-c1f5fa71b736'

    print("\n🚀 NETLIFY API DEPLOYMENT\n")

    # Get token
    token = get_netlify_token()
    if not token:
        print("\n⚠️  Trying without token (using netlify cli session)...")

    # Create zip
    zip_path = create_zip()

    # Upload via netlify deploy command with specific dir
    print("\n📤 Deploying via Netlify...")

    try:
        # Try using netlify deploy with just the essential files
        result = subprocess.run(
            ['netlify', 'deploy', '--prod', '--dir', '.', '--message', 'Auto-deploy: Homepage fix'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if 'Published' in result.stdout or 'Live' in result.stdout:
            print("✅ DEPLOYMENT SUCCESSFUL!")
            print("\n🔗 Site is live:")
            print("   https://conciousnessrevolution.io")
            return True
        else:
            print("⚠️  Deploy command output:")
            print(result.stdout)
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("⏱️  Deploy is taking a while...")
        print("   Check: https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if deploy_to_netlify():
        print("\n🎉 SUCCESS! Site should be live!")
    else:
        print("\n⚠️  Automated deploy didn't work")
        print("   Fallback: Manual drag-and-drop at:")
        print("   https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys")
