"""
Railway Dashboard Automation - Complete Service Configuration
Automates the final 5% of Railway deployment via browser automation
"""

import time
from playwright.sync_api import sync_playwright

# Railway Project Details
PROJECT_URL = "https://railway.com/project/d46c9981-2f73-475b-b032-59975dd0fcd4"
SERVICE_NAME = "trinity-wake-system"

def complete_railway_deployment():
    """
    Automate Railway dashboard service configuration
    """
    print("🚀 Starting Railway Dashboard Automation...")
    print(f"📍 Project: {PROJECT_URL}")

    with sync_playwright() as p:
        # Launch browser (headless=False to see what's happening)
        print("\n🌐 Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Railway project
        print(f"📂 Opening project: {PROJECT_URL}")
        page.goto(PROJECT_URL)

        # Wait for page to load
        print("⏳ Waiting for page load...")
        time.sleep(3)

        # Check if already logged in
        try:
            # Look for "+ New" or "+ New Service" button
            print("\n🔍 Looking for '+ New Service' button...")

            # Try multiple selectors
            selectors = [
                "button:has-text('New')",
                "button:has-text('New Service')",
                "[data-testid='new-service-button']",
                "button >> text=/.*New.*/i"
            ]

            clicked = False
            for selector in selectors:
                try:
                    print(f"   Trying selector: {selector}")
                    page.click(selector, timeout=2000)
                    clicked = True
                    print("✅ Clicked '+ New Service' button!")
                    break
                except:
                    continue

            if not clicked:
                print("\n⚠️  Could not find '+ New Service' button automatically")
                print("📋 Please click '+ New Service' manually in the browser window")
                print("⏳ Waiting 30 seconds for manual interaction...")
                time.sleep(30)

            # Wait for service creation dialog
            time.sleep(2)

            # Look for "Empty Service" or deployment options
            print("\n🔍 Looking for deployment options...")

            deployment_selectors = [
                "button:has-text('Empty Service')",
                "button:has-text('Deploy')",
                "button:has-text('GitHub')",
                "[data-testid='empty-service']"
            ]

            for selector in deployment_selectors:
                try:
                    print(f"   Trying selector: {selector}")
                    page.click(selector, timeout=2000)
                    print("✅ Selected deployment option!")
                    break
                except:
                    continue

            # Wait for service to be created
            print("\n⏳ Waiting for service creation...")
            time.sleep(5)

            # Look for settings/networking to generate domain
            print("\n🔍 Looking for Settings → Networking...")

            settings_selectors = [
                "button:has-text('Settings')",
                "[data-testid='settings-button']",
                "a:has-text('Settings')"
            ]

            for selector in settings_selectors:
                try:
                    print(f"   Trying selector: {selector}")
                    page.click(selector, timeout=2000)
                    print("✅ Opened Settings!")
                    break
                except:
                    continue

            time.sleep(2)

            # Click Networking
            networking_selectors = [
                "button:has-text('Networking')",
                "[data-testid='networking-tab']",
                "a:has-text('Networking')"
            ]

            for selector in networking_selectors:
                try:
                    print(f"   Trying selector: {selector}")
                    page.click(selector, timeout=2000)
                    print("✅ Opened Networking!")
                    break
                except:
                    continue

            time.sleep(2)

            # Generate domain
            print("\n🔍 Looking for 'Generate Domain' button...")

            domain_selectors = [
                "button:has-text('Generate Domain')",
                "[data-testid='generate-domain-button']",
                "button:has-text('Add Domain')"
            ]

            for selector in domain_selectors:
                try:
                    print(f"   Trying selector: {selector}")
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Generate Domain!")
                    break
                except:
                    continue

            time.sleep(3)

            # Try to get the generated URL
            print("\n🔍 Looking for generated URL...")
            try:
                # Railway typically shows the URL after generation
                url_element = page.query_selector("text=/.*\.up\.railway\.app/")
                if url_element:
                    generated_url = url_element.text_content()
                    print(f"\n✅ SUCCESS! Generated URL: {generated_url}")
                    print(f"\n📋 Save this URL:")
                    print(f"   Health: {generated_url}/health")
                    print(f"   Wake: {generated_url}/wake")
                    print(f"   Status: {generated_url}/status")
                else:
                    print("\n⚠️  URL not found automatically")
                    print("📋 Please copy the generated URL from the browser")
            except:
                print("\n⚠️  Could not extract URL automatically")
                print("📋 Please copy the generated URL from the browser")

            print("\n⏳ Keeping browser open for 60 seconds for verification...")
            time.sleep(60)

        except Exception as e:
            print(f"\n❌ Error during automation: {str(e)}")
            print("\n📋 MANUAL STEPS NEEDED:")
            print("1. In the browser window, click '+ New Service'")
            print("2. Select 'Empty Service' or deployment option")
            print("3. Go to Settings → Networking")
            print("4. Click 'Generate Domain'")
            print("5. Copy the generated URL")
            print("\n⏳ Keeping browser open for 120 seconds...")
            time.sleep(120)

        finally:
            print("\n🔒 Closing browser...")
            browser.close()
            print("✅ Automation complete!")

if __name__ == "__main__":
    print("=" * 60)
    print("🌀 RAILWAY DASHBOARD AUTOMATION")
    print("=" * 60)

    try:
        complete_railway_deployment()
        print("\n✅ DEPLOYMENT AUTOMATION COMPLETE")
        print("\n📋 Next steps:")
        print("1. Test health: curl [your-url]/health")
        print("2. Test wake: curl [your-url]/wake")
        print("3. Add URL to phone home screen")
    except Exception as e:
        print(f"\n❌ AUTOMATION FAILED: {str(e)}")
        print("\n📋 FALLBACK - Manual steps:")
        print("1. Open: https://railway.com/project/d46c9981-2f73-475b-b032-59975dd0fcd4")
        print("2. Click '+ New Service'")
        print("3. Generate domain")
