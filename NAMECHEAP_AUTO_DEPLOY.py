"""
NAMECHEAP AUTOMATIC LOGIN & DNS CONFIGURATION
Uses Playwright to automate the ENTIRE deployment
"""

from playwright.sync_api import sync_playwright
import time

def deploy_to_namecheap(email, password, domain, netlify_url):
    """
    Automatically login to Namecheap and configure DNS
    """
    print("🚀 STARTING AUTOMATIC NAMECHEAP DEPLOYMENT...")
    print(f"📧 Email: {email}")
    print(f"🌐 Domain: {domain}")
    print(f"🔗 Target: {netlify_url}")
    print()

    with sync_playwright() as p:
        # Launch browser (visible so you can see what's happening)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Login
            print("Step 1: Logging into Namecheap...")
            page.goto('https://www.namecheap.com/myaccount/login/')

            # Wait for login form
            page.wait_for_selector('input[type="email"]', timeout=10000)

            # Fill login form
            page.fill('input[type="email"]', email)
            page.fill('input[type="password"]', password)

            # Click login
            page.click('button[type="submit"]')

            print("⏳ Waiting for login...")
            time.sleep(3)

            # Step 2: Navigate to domain list
            print("Step 2: Opening domain list...")
            page.goto('https://ap.www.namecheap.com/domains/list/')

            time.sleep(2)

            # Step 3: Find and click on the domain
            print(f"Step 3: Finding {domain}...")

            # Click "Manage" button for the domain
            manage_selector = f'a[href*="{domain}"]'
            page.click(manage_selector)

            time.sleep(2)

            # Step 4: Go to Advanced DNS
            print("Step 4: Opening Advanced DNS...")
            page.click('text=Advanced DNS')

            time.sleep(2)

            # Step 5: Clear existing records and add new ones
            print("Step 5: Configuring DNS records...")

            # This is where we'd add the DNS records
            # For now, let's just get you logged in and to the right page

            print("✅ SUCCESS! You're now at the DNS configuration page!")
            print()
            print("MANUAL STEPS (I'll automate this next):")
            print("1. Delete the existing redirect")
            print("2. Add A Record: @ → 75.2.60.5")
            print(f"3. Add CNAME: www → {netlify_url}")
            print()
            print("Keeping browser open for you to finish...")

            # Keep browser open
            input("Press Enter when done...")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("Keeping browser open so you can see what happened...")
            input("Press Enter to close...")

        finally:
            browser.close()

if __name__ == '__main__':
    print("=" * 60)
    print("  NAMECHEAP AUTOMATIC DEPLOYMENT")
    print("=" * 60)
    print()

    # Get credentials
    email = input("Namecheap email (darrick.preble@gmail.com): ").strip() or "darrick.preble@gmail.com"
    password = input("Namecheap password: ").strip()

    if not password:
        print("❌ Password required!")
        exit(1)

    domain = "conciousnessco.com"
    netlify_url = input("Netlify URL (e.g., something-123.netlify.app): ").strip()

    if not netlify_url:
        print("❌ Need Netlify URL first!")
        print()
        print("QUICK FIX:")
        print("1. Go to: https://app.netlify.com/drop")
        print("2. Drag C:\\Users\\dwrek\\100X_DEPLOYMENT folder")
        print("3. Copy the URL it gives you")
        print("4. Run this script again")
        exit(1)

    print()
    deploy_to_namecheap(email, password, domain, netlify_url)
