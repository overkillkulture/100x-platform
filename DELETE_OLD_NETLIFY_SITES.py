"""
DELETE OLD NETLIFY SITES AUTOMATICALLY
Keeps only verdant-tulumba-fa2a5a
"""

from playwright.sync_api import sync_playwright
import time

def delete_old_sites():
    print("🗑️ DELETING OLD NETLIFY SITES...")
    print()

    # Sites to DELETE
    sites_to_delete = [
        "100x-consciousness-gate",
        "profound-travesseiro-adeab4",
        "conciousnessco.com",
        "fantastic-twilight-28b317",
        "wonderful-sorbet-b49c22"
    ]

    # Site to KEEP
    keep_site = "verdant-tulumba-fa2a5a"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Go to Netlify
            print("Step 1: Opening Netlify...")
            page.goto('https://app.netlify.com/')
            time.sleep(3)

            # Should already be logged in
            print("Step 2: Going to sites list...")
            page.goto('https://app.netlify.com/teams/overkor-tek/sites')
            time.sleep(2)

            print()
            print(f"Sites to delete: {len(sites_to_delete)}")
            print(f"Site to keep: {keep_site}")
            print()

            deleted_count = 0

            for site_name in sites_to_delete:
                print(f"Looking for: {site_name}...")

                try:
                    # Try to find and click the site
                    site_link = page.query_selector(f'text="{site_name}"')

                    if site_link:
                        print(f"  Found {site_name}!")
                        site_link.click()
                        time.sleep(2)

                        # Look for Site settings
                        try:
                            settings_link = page.query_selector('text="Site settings"')
                            if settings_link:
                                settings_link.click()
                                time.sleep(2)

                                # Scroll to bottom for delete button
                                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                                time.sleep(1)

                                # Look for Delete site button
                                delete_button = page.query_selector('text=/Delete site/i')
                                if delete_button:
                                    print(f"  Clicking delete for {site_name}...")
                                    delete_button.click()
                                    time.sleep(1)

                                    # Confirm deletion (might ask for site name)
                                    # Try to type site name if input appears
                                    confirm_input = page.query_selector('input[type="text"]')
                                    if confirm_input:
                                        confirm_input.fill(site_name)
                                        time.sleep(0.5)

                                    # Click final delete/confirm button
                                    final_confirm = page.query_selector('button:has-text("Delete")')
                                    if final_confirm:
                                        final_confirm.click()
                                        time.sleep(2)
                                        print(f"  ✅ DELETED: {site_name}")
                                        deleted_count += 1

                                    # Go back to sites list
                                    page.goto('https://app.netlify.com/teams/overkor-tek/sites')
                                    time.sleep(2)

                        except Exception as e:
                            print(f"  ⚠️ Couldn't delete {site_name}: {e}")
                            page.goto('https://app.netlify.com/teams/overkor-tek/sites')
                            time.sleep(2)
                    else:
                        print(f"  ⚠️ Couldn't find {site_name}")

                except Exception as e:
                    print(f"  ❌ Error with {site_name}: {e}")

            print()
            print("=" * 60)
            print(f"✅ DELETED {deleted_count} old sites!")
            print(f"✅ KEPT: {keep_site}")
            print("=" * 60)
            print()
            print("Keeping browser open so you can verify...")
            print("Press Enter to close...")
            input()

        except Exception as e:
            print(f"❌ Error: {e}")
            print("Keeping browser open...")
            input()

        finally:
            browser.close()

if __name__ == '__main__':
    delete_old_sites()
