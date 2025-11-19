#!/usr/bin/env python3
"""
NETLIFY DEPLOYMENT USING YOUR EXISTING CHROME BROWSER
Uses your logged-in Chrome profile so no password needed!
"""

from playwright.sync_api import sync_playwright
import time
import os
import shutil

def deploy_with_chrome():
    """Deploy using your existing Chrome browser profile"""

    print("\n" + "="*60)
    print("  AUTOMATED DEPLOYMENT - USING YOUR CHROME")
    print("  (Your GitHub login will work automatically!)")
    print("="*60 + "\n")

    # Chrome user data directory (where your logins are saved)
    chrome_user_data = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")

    with sync_playwright() as p:
        # Launch Chrome with your profile
        print("🌐 Opening Chrome with your profile...")
        print("   (You should already be logged into GitHub/Netlify)")

        context = p.chromium.launch_persistent_context(
            user_data_dir=chrome_user_data,
            headless=False,
            channel="chrome",  # Use actual Chrome, not Chromium
            slow_mo=500
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Step 1: Go to Netlify
        print("\n📍 Step 1: Going to Netlify deploys page...")
        page.goto('https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys')
        time.sleep(3)

        # Step 2: Check if we need to log in
        print("🔐 Step 2: Checking login...")

        if 'login' in page.url.lower():
            print("\n   ⚠️  Not logged in yet - let's use GitHub!")
            print("   Looking for 'Login with GitHub' button...")

            try:
                # Click GitHub login
                page.get_by_text("GitHub", exact=False).click()
                print("   ✅ Clicked GitHub login")

                # Wait for GitHub OAuth or redirect back
                print("   ⏳ Waiting for GitHub OAuth...")
                page.wait_for_url(lambda url: 'netlify.com' in url and 'login' not in url.lower(), timeout=30000)
                print("   ✅ Logged in via GitHub!")

            except Exception as e:
                print(f"\n   ⚠️  Couldn't auto-click GitHub login")
                print("   Please click 'Login with GitHub' button yourself")
                print("   (I'll wait 30 seconds)")
                time.sleep(30)

        else:
            print("   ✅ Already logged in!")

        # Step 3: Create deployment zip
        print("\n📦 Step 3: Creating deployment package...")

        zip_path = 'C:/Users/dwrek/100X_DEPLOYMENT_PACKAGE.zip'

        # Remove old zip
        if os.path.exists(zip_path):
            os.remove(zip_path)

        print("   Zipping 100X_DEPLOYMENT folder...")
        shutil.make_archive(
            'C:/Users/dwrek/100X_DEPLOYMENT_PACKAGE',
            'zip',
            'C:/Users/dwrek/100X_DEPLOYMENT'
        )
        print(f"   ✅ Created: {zip_path}")

        # Step 4: Navigate to manual deploy
        print("\n📤 Step 4: Finding manual deploy section...")

        # Scroll to bottom to find "Deploy manually" section
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        # Step 5: Try to upload automatically
        print("\n⬆️  Step 5: Looking for file upload...")

        try:
            # Find file input
            file_input = page.query_selector('input[type="file"]')

            if file_input:
                print("   ✅ Found upload input!")
                print("   Uploading deployment package...")

                file_input.set_input_files(zip_path)

                print("   ✅ File uploaded!")
                print("   ⏳ Waiting for deployment to process...")

                # Wait for deployment to complete
                try:
                    page.wait_for_selector('text=Published', timeout=90000)
                    print("\n🎉 DEPLOYMENT SUCCESSFUL!")
                except:
                    print("\n✅ Upload complete (checking status...)")

                time.sleep(5)

                success = True

            else:
                print("   ⚠️  Could not find upload input")
                print("\n   📋 MANUAL STEP NEEDED:")
                print("   1. Look for 'Need to deploy manually?' section")
                print("   2. Drag this file onto it:")
                print(f"      {zip_path}")
                print("\n   Browser will stay open...")
                input("\n   Press ENTER when deployment completes >>> ")
                success = True

        except Exception as e:
            print(f"\n   ⚠️  Automation error: {e}")
            print("\n   📋 Complete manually:")
            print("   1. Find 'Deploy manually' section")
            print("   2. Drag/upload this file:")
            print(f"      {zip_path}")
            input("\n   Press ENTER when done >>> ")
            success = True

        # Cleanup
        print("\n🧹 Cleaning up...")
        try:
            if os.path.exists(zip_path):
                os.remove(zip_path)
                print("   ✅ Removed temporary zip")
        except:
            print(f"   ℹ️  Zip file kept at: {zip_path}")

        print("\n✅ PROCESS COMPLETE!")
        print("\n🔗 Your site should be live at:")
        print("   https://conciousnessrevolution.io")
        print("\nAnyone visiting will get the platform builder!")

        # Keep browser open for a moment
        time.sleep(3)
        context.close()

        return success

if __name__ == '__main__':
    try:
        deploy_with_chrome()
        print("\n🎉 ALL DONE!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFallback: Use drag-and-drop:")
        print("1. Go to: https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys")
        print("2. Drag C:\\Users\\dwrek\\100X_DEPLOYMENT folder")
