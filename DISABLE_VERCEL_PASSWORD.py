"""
Disable Vercel Password Protection via Playwright
"""
from playwright.sync_api import sync_playwright
import time

def disable_vercel_password():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("🔓 Opening Vercel Deployment Protection page...")
        
        # Navigate to the deployment protection page
        page.goto('https://vercel.com/overkillkultures-projects/consciousness-revolution/settings/deployment-protection')
        
        # Wait for page to load
        time.sleep(3)
        
        print("📜 Scrolling down to find password protection toggle...")
        
        # Scroll down the page to reveal password protection settings
        for i in range(5):
            page.keyboard.press('PageDown')
            time.sleep(0.5)
        
        # Take screenshot to see what we have
        page.screenshot(path='C:/Users/dwrek/vercel_page.png')
        print("📸 Screenshot saved to C:/Users/dwrek/vercel_page.png")
        
        # Look for password protection toggle or checkbox
        # Common patterns: "Password Protection", "Vercel Authentication", toggle switches
        
        # Try to find and click password protection toggle
        try:
            # Look for "Password Protection" text and associated toggle
            password_section = page.locator('text=Password Protection').first
            if password_section.is_visible():
                print("✅ Found 'Password Protection' section")
                
                # Find the toggle/checkbox near it
                # Vercel typically uses a switch or checkbox
                toggle = page.locator('input[type="checkbox"]').first
                if toggle.is_checked():
                    print("🔓 Password protection is ON - clicking to disable...")
                    toggle.click()
                    time.sleep(1)
                    print("✅ Password protection disabled!")
                else:
                    print("✅ Password protection already OFF")
            else:
                print("⚠️ Could not find Password Protection section")
                
        except Exception as e:
            print(f"⚠️ Error finding toggle: {e}")
            print("📸 Check the screenshot to see what's on the page")
        
        # Look for Save button if needed
        try:
            save_button = page.locator('button:has-text("Save")').first
            if save_button.is_visible():
                print("💾 Clicking Save button...")
                save_button.click()
                time.sleep(2)
                print("✅ Settings saved!")
        except:
            print("ℹ️ No Save button found (settings may auto-save)")
        
        # Final screenshot
        page.screenshot(path='C:/Users/dwrek/vercel_page_after.png')
        print("📸 Final screenshot saved")
        
        print("⏸️ Keeping browser open for 10 seconds so you can verify...")
        time.sleep(10)
        
        browser.close()
        print("✅ Done!")

if __name__ == '__main__':
    disable_vercel_password()
