"""
Netlify Deployment Helper - Use Playwright to automate manual deployment
"""
from playwright.sync_api import sync_playwright
import time
import os

print("🚀 Netlify Deployment Helper")
print("=" * 50)

deploy_path = r"C:\Users\dwrek\100X_DEPLOYMENT"

print(f"\n📁 Deployment folder: {deploy_path}")
print("\nThis script will:")
print("1. Open Netlify in your browser")
print("2. Navigate to your site")
print("3. Guide you to drag-and-drop deploy")
print("\nStarting browser...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Go to Netlify
        print("\n1️⃣ Opening Netlify...")
        page.goto('https://app.netlify.com/')
        time.sleep(3)

        # Check if we need to login
        if 'login' in page.url.lower():
            print("\n❗ Please login to Netlify in the browser window")
            print("Press Enter when you're logged in...")
            input()

        # Navigate to sites page
        print("\n2️⃣ Finding your sites...")
        page.goto('https://app.netlify.com/')
        time.sleep(2)

        # Try to find site link
        print("\n3️⃣ Looking for conciousnessrevolution site...")
        try:
            # Look for site with conciousness or 100x in name
            page.wait_for_selector('text=/conciousness|100x|revolution/i', timeout=5000)
            print("✅ Found site!")

            # Click on site
            page.click('text=/conciousness|100x|revolution/i')
            time.sleep(2)

            # Go to Deploys tab
            print("\n4️⃣ Opening Deploys tab...")
            page.click('text="Deploys"')
            time.sleep(2)

            print("\n" + "=" * 50)
            print("🎯 MANUAL DEPLOYMENT STEPS")
            print("=" * 50)
            print(f"\n1. In the browser window, find the deploy upload area")
            print(f"2. Drag this folder: {deploy_path}")
            print(f"3. Wait for upload to complete (30-60 seconds)")
            print(f"4. Press Enter here when deployment is done")
            print("\n" + "=" * 50)

            input("\nPress Enter when deployment complete...")

            print("\n✅ Deployment process complete!")
            print("🌐 Check: https://conciousnessrevolution.io/screening.html")

        except:
            print("\n❗ Could not find site automatically")
            print("\nManual steps:")
            print("1. In the browser, find your site (conciousnessrevolution)")
            print("2. Click on it")
            print("3. Go to Deploys tab")
            print(f"4. Drag folder: {deploy_path}")
            print("\nPress Enter when done...")
            input()

    finally:
        print("\n🏁 Closing browser...")
        browser.close()

print("\n" + "=" * 50)
print("📋 VERIFICATION CHECKLIST")
print("=" * 50)
print("Visit these URLs to verify deployment:")
print("1. https://conciousnessrevolution.io/screening.html")
print("   - Should show: 'Welcome to the Revolution'")
print("   - Should NOT show: 5 consciousness questions")
print("\n2. https://conciousnessrevolution.io/access.html")
print("   - Should show: Blue/cyan theme")
print("   - Should NOT show: Red police theme")
print("\n3. https://conciousnessrevolution.io/workspace-v3.html")
print("   - Enter PIN: 1234")
print("   - Should have cloud sync (Airtable)")
print("=" * 50)
