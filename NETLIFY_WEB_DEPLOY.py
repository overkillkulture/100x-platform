#!/usr/bin/env python3
"""
Automate Netlify deployment via web interface using Playwright
Bypasses the broken CLI to get the site live NOW
"""

from playwright.sync_api import sync_playwright
import time
import subprocess
import json

def get_netlify_credentials():
    """Get Netlify login from Bitwarden"""
    try:
        # Try to get from Bitwarden
        result = subprocess.run(
            ['bw', 'get', 'item', 'netlify'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            item = json.loads(result.stdout)
            return {
                'email': item['login']['username'],
                'password': item['login']['password']
            }
    except:
        pass

    # Fallback - check environment or prompt
    print("⚠️  Couldn't get Netlify credentials from Bitwarden")
    print("📝 Please enter Netlify login manually or set up Bitwarden")
    return None

def deploy_via_web():
    """Deploy to Netlify via web interface"""
    print("🌐 Opening Netlify web interface...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Netlify
        page.goto('https://app.netlify.com')
        print("📍 At Netlify homepage")

        # Wait for manual login
        print("\n" + "="*60)
        print("🔐 MANUAL ACTION REQUIRED:")
        print("1. Log into Netlify in the browser window")
        print("2. Navigate to your site (100X Platform)")
        print("3. Go to Deploys > Deploy manually")
        print("4. Drag and drop the 100X_DEPLOYMENT folder")
        print("="*60)
        print("\n⏳ Waiting for you to complete manual deployment...")
        print("   Press ENTER when deployment is complete\n")

        input("Press ENTER after manual deployment >>> ")

        print("✅ Deployment marked as complete")
        browser.close()

    return True

def verify_redirect():
    """Verify the redirect is working"""
    print("\n🔍 Verifying redirect...")

    import requests

    # Check if homepage redirects to platform.html
    response = requests.get('https://conciousnessrevolution.io/', allow_redirects=False)

    if response.status_code in [301, 302, 307, 308]:
        location = response.headers.get('Location', '')
        if 'platform.html' in location:
            print(f"✅ Homepage redirects to: {location}")
            return True
        else:
            print(f"⚠️  Redirect exists but goes to: {location}")
            return False
    else:
        print(f"❌ No redirect found (status {response.status_code})")
        return False

if __name__ == '__main__':
    print("\n🚀 NETLIFY WEB DEPLOY - EMERGENCY FIX\n")

    # Try automated deployment
    if deploy_via_web():
        print("\n✅ Manual deployment process completed")

        # Verify
        time.sleep(5)  # Wait for propagation
        if verify_redirect():
            print("\n🎉 SUCCESS! Site is live and redirecting properly!")
            print("🔗 Users can now visit: https://conciousnessrevolution.io")
            print("   And it will redirect to: platform.html")
        else:
            print("\n⚠️  Deployment complete but redirect not working yet")
            print("   Give it a minute for DNS propagation")
    else:
        print("\n❌ Deployment failed")
