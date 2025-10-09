"""
SQUARE 2 VERIFICATION - Test the fresh deployment
"""

from playwright.sync_api import sync_playwright
import time

def test_fresh_gate():
    """Test the gate that has JavaScript (unique deploy URL)"""

    print("\n" + "="*60)
    print("🎯 TESTING FRESH DEPLOYMENT")
    print("="*60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Use the unique deploy URL (fresh, no cache)
        print("\n✓ Loading fresh deployment...")
        page.goto('https://68e79faff34a7f3ce22f21df--verdant-tulumba-fa2a5a.netlify.app')
        time.sleep(3)

        # SQUARE 2: Can we interact with fields?
        print("\n" + "="*60)
        print("🎯 SQUARE 2: INTERACTIVE TESTING")
        print("="*60)

        try:
            # Type in name field
            print("\n✓ Typing in name field...")
            page.fill('input#name', 'Test Builder')
            time.sleep(1)

            # Type in email field
            print("✓ Typing in email field...")
            page.fill('input#email', 'test@consciousnessrevolution.io')
            time.sleep(1)

            # Type in phone field
            print("✓ Typing in phone field...")
            page.fill('input#phone', '+1 555 123 4567')
            time.sleep(1)

            # Type in mission field
            print("✓ Typing in mission field...")
            page.fill('textarea#mission', 'Building liberated AI consciousness systems')
            time.sleep(1)

            # Type in values field
            print("✓ Typing in values field...")
            page.fill('textarea#values', 'Truth, autonomy, pattern recognition, liberation over control')
            time.sleep(1)

            print("\n✅ SQUARE 2 PASSED: All fields are interactive!")

            # Take screenshot
            screenshot_path = 'C:/Users/dwrek/100X_DEPLOYMENT/form_filled_screenshot.png'
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")

            print("\n⚠️  NOT clicking submit (would submit to real Airtable)")
            print("    Manual verification needed to test actual submission")

        except Exception as e:
            print(f"\n✗ SQUARE 2 FAILED: {e}")

        input("\nPress Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    test_fresh_gate()
