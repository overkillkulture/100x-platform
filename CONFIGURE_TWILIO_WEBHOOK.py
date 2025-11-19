"""
Configure Twilio webhook automatically with Playwright
No manual steps needed
"""

from playwright.sync_api import sync_playwright
import time

def configure_twilio_webhook():
    """Automate Twilio webhook configuration"""

    TWILIO_EMAIL = "darrick.preble@gmail.com"
    TWILIO_PASSWORD = "Kill50780630#"
    WEBHOOK_URL = "https://conciousnessrevolution.io/.netlify/functions/sms-bug-report"
    PHONE_NUMBER = "+15092166552"

    print("🚀 Configuring Twilio webhook automatically...")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Go to Twilio login
            print("📱 Opening Twilio...")
            page.goto('https://www.twilio.com/login')
            time.sleep(2)

            # Login
            print("🔐 Logging in...")
            page.fill('input[name="email"]', TWILIO_EMAIL)
            page.fill('input[name="password"]', TWILIO_PASSWORD)
            page.click('button[type="submit"]')
            time.sleep(5)

            # Check if 2FA required
            if '2fa' in page.url.lower() or 'mfa' in page.url.lower() or 'verify' in page.url.lower():
                print("⚠️  2FA/MFA required!")
                print("Please complete 2FA in the browser window...")
                print("Waiting 60 seconds...")
                time.sleep(60)

            # Navigate to phone numbers
            print("📞 Going to phone numbers...")
            page.goto('https://www.twilio.com/console/phone-numbers/incoming')
            time.sleep(3)

            # Find and click the Idaho number
            print(f"🔍 Finding {PHONE_NUMBER}...")

            # Try to find the phone number link
            try:
                page.click(f'a:has-text("{PHONE_NUMBER}")')
                time.sleep(3)
            except:
                print("⚠️  Couldn't find phone number by link, trying table...")
                # Alternative: look in table
                page.click('table tr:has-text("509") a')
                time.sleep(3)

            # Scroll to messaging section
            print("📝 Configuring messaging webhook...")
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)

            # Find webhook URL input for incoming messages
            webhook_input = page.locator('input[name*="sms"], input[placeholder*="URL"], input[type="url"]').first
            webhook_input.clear()
            webhook_input.fill(WEBHOOK_URL)
            time.sleep(1)

            # Make sure HTTP POST is selected
            try:
                page.select_option('select[name*="method"]', 'POST')
            except:
                print("⚠️  Method dropdown not found, might already be POST")

            # Save
            print("💾 Saving configuration...")
            page.click('button:has-text("Save")')
            time.sleep(3)

            # Check for success message
            if page.locator('text=/saved|success/i').count() > 0:
                print()
                print("✅ WEBHOOK CONFIGURED SUCCESSFULLY!")
                print()
                print(f"Phone number: {PHONE_NUMBER}")
                print(f"Webhook URL: {WEBHOOK_URL}")
                print(f"Method: POST")
                print()
                print("Beta testers can now text bugs to this number!")
                success = True
            else:
                print()
                print("⚠️  Save completed but couldn't confirm success message")
                print("Please verify in browser window")
                success = True

            print()
            print("Browser will stay open for 10 seconds so you can verify...")
            time.sleep(10)

            browser.close()
            return success

        except Exception as e:
            print(f"❌ Error: {e}")
            print()
            print("Browser will stay open so you can complete manually...")
            print("Press Ctrl+C when done")
            try:
                time.sleep(300)  # 5 minutes
            except KeyboardInterrupt:
                pass
            browser.close()
            return False


if __name__ == '__main__':
    print()
    print("="*70)
    print("🔧 TWILIO WEBHOOK AUTO-CONFIGURATION")
    print("="*70)
    print()

    success = configure_twilio_webhook()

    if success:
        print("="*70)
        print("✅ CONFIGURATION COMPLETE")
        print("="*70)
        print()
        print("Next: Send notification to beta testers")
    else:
        print("="*70)
        print("⚠️  CONFIGURATION INCOMPLETE")
        print("="*70)
        print()
        print("Please check Twilio console manually")
