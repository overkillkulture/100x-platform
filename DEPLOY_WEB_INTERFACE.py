"""
Deploy using Netlify WEB interface with Playwright automation
Clicks through EVERYTHING automatically
"""

from playwright.sync_api import sync_playwright
import time
import os

def deploy_via_web():
    print("🚀 DEPLOYING VIA NETLIFY WEB INTERFACE")
    print("=" * 60)
    print()

    folder_path = r"C:\Users\dwrek\100X_DEPLOYMENT"

    with sync_playwright() as p:
        # Launch visible browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: Check if logged in
            print("Step 1: Opening Netlify...")
            page.goto('https://app.netlify.com/')
            time.sleep(3)

            # Step 2: Go to Sites
            print("Step 2: Going to Sites page...")
            try:
                page.click('text=Sites', timeout=5000)
                time.sleep(2)
            except:
                print("Already on sites page or different layout")

            # Step 3: Click "Add new site"
            print("Step 3: Clicking 'Add new site'...")
            try:
                # Try different selectors
                selectors = [
                    'text=Add new site',
                    'button:has-text("Add new site")',
                    '[data-testid="add-site-button"]',
                    'text=Import an existing project',
                    'text=Deploy manually'
                ]

                clicked = False
                for selector in selectors:
                    try:
                        page.click(selector, timeout=2000)
                        clicked = True
                        print(f"✅ Clicked: {selector}")
                        break
                    except:
                        continue

                if not clicked:
                    print("⚠️ Could not find 'Add new site' button")
                    print("Taking screenshot...")
                    page.screenshot(path='netlify_page.png')
                    print("Screenshot saved: netlify_page.png")

                time.sleep(2)

            except Exception as e:
                print(f"Error clicking button: {e}")

            # Step 4: Click "Deploy manually"
            print("Step 4: Looking for 'Deploy manually' option...")
            try:
                selectors_deploy = [
                    'text=Deploy manually',
                    'button:has-text("Deploy manually")',
                    'text=Drag and drop',
                    '[href*="drop"]'
                ]

                for selector in selectors_deploy:
                    try:
                        page.click(selector, timeout=2000)
                        print(f"✅ Clicked: {selector}")
                        break
                    except:
                        continue

                time.sleep(2)
            except Exception as e:
                print(f"Deploy manually not found: {e}")

            # Check current URL
            current_url = page.url
            print(f"Current URL: {current_url}")

            # If we're on the drop page
            if 'drop' in current_url.lower() or 'deploy' in current_url.lower():
                print()
                print("✅ We're on the deploy page!")
                print()
                print("🎯 ACTION REQUIRED:")
                print(f"   Drag folder: {folder_path}")
                print("   Into the browser window now!")
                print()
                print("   Watching for deployment URL...")
                print()

                # Wait for deployment
                max_wait = 180  # 3 minutes
                start_time = time.time()

                while time.time() - start_time < max_wait:
                    try:
                        # Look for .netlify.app URL
                        url_pattern = page.query_selector('text=/https?:\\/\\/.+\\.netlify\\.app/')
                        if url_pattern:
                            url_text = url_pattern.inner_text()
                            print()
                            print("🎉 DEPLOYMENT SUCCESSFUL!")
                            print(f"   URL: {url_text}")
                            print()

                            # Try to configure custom domain
                            print("Attempting to configure custom domain...")
                            configure_custom_domain(page, url_text)

                            return url_text
                    except:
                        pass

                    # Progress indicator every 10 seconds
                    elapsed = int(time.time() - start_time)
                    if elapsed % 10 == 0 and elapsed > 0:
                        print(f"⏳ Still watching... ({elapsed}s)")

                    time.sleep(1)

                print()
                print("⏰ Timeout waiting for deployment")
                print("   You may need to drag the folder manually")

            else:
                print()
                print("❌ Not on deploy page")
                print(f"   Current URL: {current_url}")
                print()
                print("Taking screenshot to help debug...")
                page.screenshot(path='current_page.png')
                print("Screenshot saved: current_page.png")

        except Exception as e:
            print(f"❌ Error: {e}")
            page.screenshot(path='error_screenshot.png')

        finally:
            print()
            print("Press Enter to close browser...")
            try:
                input()
            except:
                pass
            browser.close()


def configure_custom_domain(page, site_url):
    """Try to configure custom domain"""
    try:
        # Extract site name
        site_name = site_url.replace('https://', '').replace('.netlify.app', '').split('/')[0]

        print(f"Site name: {site_name}")
        print("Navigating to domain settings...")

        # Go to domain settings
        settings_url = f"https://app.netlify.com/sites/{site_name}/settings/domain"
        page.goto(settings_url)
        time.sleep(3)

        # Click "Add custom domain"
        page.click('text=Add custom domain', timeout=10000)
        time.sleep(2)

        # Enter domain
        page.fill('input[type="text"]', 'conciousnessco.com')
        time.sleep(1)

        # Click Verify
        page.click('text=Verify')
        time.sleep(3)

        # Click Add domain
        page.click('text=Add domain')
        time.sleep(2)

        print("✅ Custom domain configured!")

    except Exception as e:
        print(f"⚠️ Could not auto-configure domain: {e}")
        print("You can do this manually in Netlify dashboard")


if __name__ == '__main__':
    deploy_via_web()
