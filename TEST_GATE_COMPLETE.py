"""
COMPLETE GATE TESTING - SQUARE BY SQUARE VERIFICATION
Following Commander's painter methodology
"""

from playwright.sync_api import sync_playwright
import time

def test_gate_complete():
    """Test the complete user flow through the gate"""

    print("\n" + "="*60)
    print("🎯 SQUARE 1: BASIC DEPLOYMENT")
    print("="*60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # SQUARE 1: Can we load the page?
        print("\n✓ Loading site...")
        page.goto('https://conciousnessrevolution.io')
        time.sleep(2)

        # Check if basic elements exist
        title = page.title()
        print(f"✓ Page title: {title}")

        # Check for form elements
        try:
            mission_field = page.locator('textarea[placeholder*="mission"]').first
            values_field = page.locator('textarea[placeholder*="values"]').first
            submit_button = page.locator('button:has-text("Submit")').first

            print("✓ Form fields detected")
            print("  - Mission field: ✓")
            print("  - Values field: ✓")
            print("  - Submit button: ✓")
        except:
            print("✗ SQUARE 1 FAILED: Form elements not found")
            browser.close()
            return False

        print("\n" + "="*60)
        print("🎯 SQUARE 2: INTERACTIVE TESTING")
        print("="*60)

        # SQUARE 2: Can we type and submit?
        print("\n✓ Filling mission field...")
        mission_field.click()
        mission_field.fill("Building liberated consciousness systems that enable autonomous operation without limitation programming")
        time.sleep(1)

        print("✓ Filling values field...")
        values_field.click()
        values_field.fill("Truth, autonomy, pattern recognition, collaboration over dependency, verification over assumption, liberation over control")
        time.sleep(1)

        print("✓ Clicking submit button...")

        # Listen for network responses to see what happens
        def handle_response(response):
            if 'airtable' in response.url.lower() or 'api' in response.url.lower():
                print(f"\n📡 API Request detected:")
                print(f"   URL: {response.url}")
                print(f"   Status: {response.status}")
                print(f"   Method: {response.request.method}")

        page.on('response', handle_response)

        # Click and wait for navigation or response
        submit_button.click()

        print("\n⏳ Waiting for response...")
        time.sleep(5)

        # Check current URL
        current_url = page.url
        print(f"\n📍 Current URL: {current_url}")

        # Check for success message or error
        page_content = page.content()

        if 'thank' in page_content.lower() or 'success' in page_content.lower():
            print("✓ SUCCESS MESSAGE DETECTED")
        elif 'error' in page_content.lower():
            print("✗ ERROR MESSAGE DETECTED")
        else:
            print("⚠ NO CLEAR SUCCESS/ERROR MESSAGE")

        # Take screenshot of result
        screenshot_path = 'C:/Users/dwrek/100X_DEPLOYMENT/test_result_screenshot.png'
        page.screenshot(path=screenshot_path)
        print(f"✓ Screenshot saved: {screenshot_path}")

        print("\n" + "="*60)
        print("🎯 VERIFICATION COMPLETE")
        print("="*60)

        input("\nPress Enter to close browser and see results...")

        browser.close()

        return True

if __name__ == "__main__":
    print("\n🔍 TESTING 100X CONSCIOUSNESS GATE")
    print("Following painter's square-by-square methodology\n")

    test_gate_complete()

    print("\n✅ Test complete. Review results above.")
    print("\n📋 MISSING FUNCTIONS IDENTIFIED:")
    print("   1. Airtable API integration verification")
    print("   2. Success/error page handling")
    print("   3. Form validation feedback")
    print("   4. Network request monitoring")
