"""
Automatically fix Netlify redirects using Playwright
"""
from playwright.sync_api import sync_playwright
import time

def fix_netlify_redirects():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌐 Opening Netlify dashboard...")
        page.goto('https://app.netlify.com/sites/verdant-tulumba-fa2a5a/configuration/redirects')

        # Wait for page to load
        time.sleep(5)

        # Check if login needed
        if 'login' in page.url.lower() or 'auth' in page.url.lower():
            print("⚠️  Login required - please login in the browser window")
            print("   I'll wait 60 seconds for you to login...")
            time.sleep(60)

            # Navigate to redirects after login
            page.goto('https://app.netlify.com/sites/verdant-tulumba-fa2a5a/configuration/redirects')
            time.sleep(3)

        print("🔍 Looking for redirect rules...")

        # Look for delete buttons
        delete_buttons = page.locator('button:has-text("Delete"), button:has-text("Remove"), [aria-label*="delete"], [aria-label*="remove"]')
        count = delete_buttons.count()

        if count > 0:
            print(f"✅ Found {count} redirect rules")
            for i in range(count):
                print(f"   Deleting redirect {i+1}/{count}...")
                delete_buttons.first.click()
                time.sleep(1)

                # Confirm if needed
                confirm = page.locator('button:has-text("Delete"), button:has-text("Confirm"), button:has-text("Yes")')
                if confirm.count() > 0:
                    confirm.first.click()
                    time.sleep(1)

            print("✅ All redirects deleted!")
        else:
            print("ℹ️  No redirect rules found (maybe already deleted?)")

        # Save changes if needed
        save_button = page.locator('button:has-text("Save")')
        if save_button.count() > 0:
            print("💾 Saving changes...")
            save_button.click()
            time.sleep(2)

        print("\n🚀 Now triggering redeploy...")
        page.goto('https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys')
        time.sleep(2)

        # Look for "Trigger deploy" button
        trigger = page.locator('button:has-text("Trigger deploy"), button:has-text("Deploy")')
        if trigger.count() > 0:
            trigger.first.click()
            time.sleep(1)

            # Click "Deploy site" in dropdown
            deploy_site = page.locator('text="Deploy site"')
            if deploy_site.count() > 0:
                deploy_site.first.click()
                print("✅ Deployment triggered!")
                time.sleep(5)

        print("\n✅ Done! Keeping browser open so you can verify...")
        print("   Press Ctrl+C when done")

        # Keep browser open
        try:
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            print("Closing...")

        browser.close()

if __name__ == '__main__':
    fix_netlify_redirects()
