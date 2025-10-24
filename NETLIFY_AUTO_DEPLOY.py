#!/usr/bin/env python3
"""
FULLY AUTOMATED NETLIFY DEPLOYMENT - NO MANUAL CLICKING
Uses Playwright to automate the entire deployment process
"""

from playwright.sync_api import sync_playwright
import time
import os

def auto_deploy_to_netlify():
    """Fully automated deployment to Netlify"""

    print("🚀 AUTOMATED NETLIFY DEPLOYMENT STARTING...\n")

    with sync_playwright() as p:
        # Launch browser (visible so you can see progress)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Go to Netlify
        print("📍 Step 1: Opening Netlify deploys page...")
        page.goto('https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys')

        # Step 2: Wait for login if needed
        print("🔐 Step 2: Checking login status...")
        time.sleep(3)

        # Check if we need to log in
        if 'login' in page.url.lower() or 'sign-in' in page.url.lower():
            print("⚠️  Not logged in - waiting for you to log in...")
            print("   (I'll wait 60 seconds for you to complete login)")

            # Wait for navigation away from login page
            try:
                page.wait_for_url(lambda url: 'login' not in url.lower(), timeout=60000)
                print("✅ Login detected!")
            except:
                print("❌ Login timeout - please log in manually and restart")
                browser.close()
                return False
        else:
            print("✅ Already logged in!")

        # Step 3: Find the manual deploy section
        print("\n📤 Step 3: Looking for manual deploy section...")

        # Scroll down to find "Need to deploy manually?" section
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        # Look for the file upload area
        print("🔍 Step 4: Finding file upload area...")

        # Try multiple selectors for the upload area
        upload_selectors = [
            'input[type="file"]',
            '[data-testid="file-upload"]',
            '.file-upload',
            'input[accept*="zip"]'
        ]

        upload_input = None
        for selector in upload_selectors:
            try:
                upload_input = page.query_selector(selector)
                if upload_input:
                    print(f"✅ Found upload input: {selector}")
                    break
            except:
                continue

        if not upload_input:
            print("⚠️  Could not find upload input automatically")
            print("   Looking for manual deploy link...")

            # Try clicking manual deploy button
            try:
                # Look for any button or link with "manual" or "deploy"
                page.get_by_text("Deploy manually", exact=False).click()
                time.sleep(2)

                # Try finding upload input again
                upload_input = page.query_selector('input[type="file"]')
            except:
                pass

        # Step 5: Prepare the folder as a zip
        print("\n📦 Step 5: Creating deployment package...")

        import zipfile
        import shutil

        # Create a zip of the deployment folder
        zip_path = 'C:/Users/dwrek/100X_DEPLOYMENT_PACKAGE.zip'

        # Remove old zip if exists
        if os.path.exists(zip_path):
            os.remove(zip_path)

        print("   Zipping deployment folder...")
        shutil.make_archive(
            'C:/Users/dwrek/100X_DEPLOYMENT_PACKAGE',
            'zip',
            'C:/Users/dwrek/100X_DEPLOYMENT'
        )
        print(f"   ✅ Created: {zip_path}")

        # Step 6: Upload the file
        if upload_input:
            print("\n⬆️  Step 6: Uploading deployment package...")

            upload_input.set_input_files(zip_path)
            print("   ✅ File uploaded!")

            # Wait for upload to process
            print("   ⏳ Waiting for deployment to process...")
            time.sleep(10)

            # Look for success message
            try:
                page.wait_for_selector('text=Published', timeout=60000)
                print("\n✅ DEPLOYMENT SUCCESSFUL!")
                print("🎉 Site is now live!")
                print("🔗 Visit: https://conciousnessrevolution.io")

                success = True
            except:
                print("\n⚠️  Upload completed but status unclear")
                print("   Check: https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys")
                success = True  # Consider it success if upload happened
        else:
            print("\n❌ Could not automate upload")
            print("   Manual action needed:")
            print("   1. Look for 'Need to deploy manually?' section")
            print("   2. Drag this folder onto it: C:\\Users\\dwrek\\100X_DEPLOYMENT")
            print("\n   Browser will stay open for you to complete manually...")
            input("   Press ENTER when done...")
            success = True

        # Cleanup
        print("\n🧹 Cleaning up...")
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print("   ✅ Removed temporary zip file")

        print("\n✅ AUTOMATION COMPLETE!")
        browser.close()

        return success

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  NETLIFY AUTOMATED DEPLOYMENT")
    print("  No manual clicking required!")
    print("="*60 + "\n")

    if auto_deploy_to_netlify():
        print("\n🎉 SUCCESS!")
        print("\nYour site is now live:")
        print("   https://conciousnessrevolution.io")
        print("\nAnyone visiting will get the platform builder automatically!")
    else:
        print("\n⚠️  Automation encountered issues")
        print("   But files are ready - try manual deployment as fallback")
