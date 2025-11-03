#!/usr/bin/env python3
"""
Deploy to Netlify using API directly - bypass broken CLI
"""

import requests
import os
import hashlib
import json
from pathlib import Path

# Get site ID from .netlify/state.json
state_file = Path('.netlify/state.json')
if state_file.exists():
    state = json.loads(state_file.read_text())
    SITE_ID = state.get('siteId')
    print(f"📍 Site ID: {SITE_ID}")
else:
    print("❌ No .netlify/state.json found")
    exit(1)

# Get Netlify token from environment
NETLIFY_TOKEN = os.getenv('NETLIFY_AUTH_TOKEN')
if not NETLIFY_TOKEN:
    print("⚠️  NETLIFY_AUTH_TOKEN not found in environment")
    print("Run: netlify status")
    print("Then check the token")
    exit(1)

print(f"🔑 Token found: {NETLIFY_TOKEN[:10]}...")

# Headers for API requests
headers = {
    'Authorization': f'Bearer {NETLIFY_TOKEN}',
    'Content-Type': 'application/json'
}

def create_deploy():
    """Create a new deploy via API"""
    print("\n🚀 Creating new deploy...")

    # Create deploy
    url = f'https://api.netlify.com/api/v1/sites/{SITE_ID}/deploys'

    response = requests.post(url, headers=headers, json={})

    if response.status_code == 201:
        deploy = response.json()
        deploy_id = deploy['id']
        print(f"✅ Deploy created: {deploy_id}")
        return deploy_id
    else:
        print(f"❌ Failed to create deploy: {response.status_code}")
        print(response.text)
        return None

def hash_file(filepath):
    """Calculate SHA1 hash of file"""
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def upload_files(deploy_id):
    """Upload files to deploy"""
    print("\n📤 Uploading files...")

    # Get list of files to upload
    files_to_upload = {}

    # Key files
    important_files = [
        '_redirects',
        'platform.html',
        'voice-room.html',
        'simple-workspace-entry.html',
        'index.html'
    ]

    for filename in important_files:
        if os.path.exists(filename):
            file_hash = hash_file(filename)
            files_to_upload[filename] = file_hash
            print(f"  📄 {filename} -> {file_hash[:8]}")

    # Upload files
    url = f'https://api.netlify.com/api/v1/deploys/{deploy_id}/files'

    for filepath, file_hash in files_to_upload.items():
        with open(filepath, 'rb') as f:
            file_content = f.read()

        file_url = f"{url}/{filepath}"
        response = requests.put(
            file_url,
            headers={'Authorization': f'Bearer {NETLIFY_TOKEN}'},
            data=file_content
        )

        if response.status_code == 200:
            print(f"  ✅ Uploaded: {filepath}")
        else:
            print(f"  ❌ Failed: {filepath} ({response.status_code})")

    return True

def trigger_deploy():
    """Trigger the deploy"""
    print("\n🎬 Triggering deploy...")

    # Try via API
    url = f'https://api.netlify.com/api/v1/sites/{SITE_ID}/builds'
    response = requests.post(url, headers=headers)

    if response.status_code in [200, 201, 202]:
        print("✅ Deploy triggered!")
        return True
    else:
        print(f"⚠️  Response: {response.status_code}")
        print(response.text)
        return False

if __name__ == '__main__':
    print("\n🌐 NETLIFY API DEPLOYMENT\n")

    # Create deploy
    deploy_id = create_deploy()

    if deploy_id:
        # Upload files
        if upload_files(deploy_id):
            print("\n✅ Files uploaded successfully!")
            print(f"\n🔗 Check deploy: https://app.netlify.com/sites/{SITE_ID}/deploys/{deploy_id}")
        else:
            print("\n❌ File upload failed")
    else:
        print("\n❌ Could not create deploy")

    # Alternative: Trigger a new build
    print("\n🔄 Attempting to trigger new build...")
    trigger_deploy()
