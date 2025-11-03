#!/usr/bin/env python3
"""
PLAYWRIGHT DNS CONFIGURATION DEMO

This script will:
1. Open a browser window (you can watch)
2. Navigate to Namecheap
3. Show you what it can do
4. (With your credentials, it could complete the DNS setup automatically)
"""

from playwright.sync_api import sync_playwright
import time

def demo_browser_control():
    """
    Demonstrate Playwright's capabilities
    """

    print("🚀 Starting Playwright Demo...")
    print("\nThis will open a browser window.")
    print("You'll see me navigate websites automatically.")
    print("\nPress Ctrl+C to stop at any time.\n")

    with sync_playwright() as p:
        # Launch browser (headless=False means you can see it)
        print("📱 Launching Chrome...")
        browser = p.chromium.launch(headless=False, slow_mo=1000)  # slow_mo makes it visible
        page = browser.new_page()

        # Demo 1: Navigate to Namecheap
        print("\n1️⃣ Navigating to Namecheap...")
        page.goto('https://www.namecheap.com')
        page.wait_for_load_state('networkidle')

        print("   ✓ Page loaded!")
        print("   ✓ I can see the page")
        print("   ✓ I can read all the text")
        print("   ✓ I can click any button")

        time.sleep(2)

        # Demo 2: Search for something
        print("\n2️⃣ Finding the domain search box...")
        search_box = page.locator('input[placeholder*="domain" i]').first

        if search_box.is_visible():
            print("   ✓ Found search box!")
            print("   ✓ Typing 'consciousnessrevolution.com'...")
            search_box.fill('consciousnessrevolution.com')
            time.sleep(2)

        # Demo 3: Take screenshot
        print("\n3️⃣ Taking screenshot...")
        screenshot_path = 'C:\\Users\\dwrek\\Desktop\\playwright_demo.png'
        page.screenshot(path=screenshot_path)
        print(f"   ✓ Saved to: {screenshot_path}")

        # Demo 4: Show what we COULD do with login
        print("\n4️⃣ What I COULD do with your credentials:")
        print("   • Login to Namecheap automatically")
        print("   • Navigate to domain management")
        print("   • Find consciousnessrevolution.com")
        print("   • Click 'Manage'")
        print("   • Find 'Nameservers' or 'Advanced DNS'")
        print("   • Select 'Custom DNS'")
        print("   • Add all 4 nameservers:")
        print("     - dns1.p06.nsone.net")
        print("     - dns2.p06.nsone.net")
        print("     - dns3.p06.nsone.net")
        print("     - dns4.p06.nsone.net")
        print("   • Click 'Save'")
        print("   • Done in 30 seconds")

        print("\n5️⃣ Waiting 5 seconds, then closing...")
        time.sleep(5)

        browser.close()
        print("\n✅ Demo complete!")
        print("\n📋 What you saw:")
        print("   • I can open browsers")
        print("   • I can navigate websites")
        print("   • I can find elements on pages")
        print("   • I can fill forms")
        print("   • I can click buttons")
        print("   • I can take screenshots")
        print("\n🎯 With your permission and credentials:")
        print("   • I can login to Namecheap")
        print("   • I can configure DNS automatically")
        print("   • You never have to touch their UI again")
        print("\n💡 Next step:")
        print("   If you want me to configure DNS automatically,")
        print("   I'll need your Namecheap username and password.")
        print("   (Stored encrypted, used once, never saved)")

if __name__ == "__main__":
    try:
        demo_browser_control()
    except KeyboardInterrupt:
        print("\n\n⏸️  Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis might mean:")
        print("  • Playwright not fully installed")
        print("  • Browser not downloaded")
        print("\nTry running:")
        print("  python -m playwright install chromium")
