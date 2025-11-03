"""
🐦 TWITTER AUTO-POSTER (Playwright Browser Automation)
FREE alternative to expensive Twitter API
"""

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
from typing import Dict, Optional

class TwitterPoster:
    """Automated Twitter posting via browser automation"""

    def __init__(self, session_dir: str = './twitter_session'):
        """Initialize Twitter poster with saved session"""
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)

    def login_first_time(self, username: str, password: str):
        """One-time login to save session"""
        print("🔐 Logging into Twitter (one-time setup)...")

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_dir),
                headless=False
            )

            page = browser.new_page()
            page.goto('https://twitter.com/login')

            # Enter username
            page.wait_for_selector('input[autocomplete="username"]', timeout=10000)
            page.fill('input[autocomplete="username"]', username)
            page.click('button:has-text("Next")')

            # Enter password
            page.wait_for_selector('input[name="password"]', timeout=10000)
            page.fill('input[name="password"]', password)
            page.click('button[data-testid="LoginForm_Login_Button"]')

            # Wait for home page
            page.wait_for_url('https://twitter.com/home', timeout=30000)

            print("✅ Login successful! Session saved.")
            browser.close()

    def post_video(
        self,
        video_path: str,
        caption: str,
        headless: bool = True
    ) -> Dict:
        """Post video to Twitter using saved session"""

        print(f"\n🐦 Posting to Twitter...")
        print(f"   Video: {Path(video_path).name}")
        print(f"   Caption: {caption[:50]}...")

        with sync_playwright() as p:
            # Use saved session
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_dir),
                headless=headless
            )

            page = browser.new_page()

            try:
                # Go to compose tweet
                page.goto('https://twitter.com/compose/tweet')
                time.sleep(2)

                # Check if logged in
                if 'login' in page.url.lower():
                    raise Exception("Not logged in! Run login_first_time() first")

                # Wait for compose box
                page.wait_for_selector('div[role="textbox"]', timeout=10000)

                # Add caption text
                page.fill('div[role="textbox"]', caption)
                print("   ✅ Caption added")

                # Upload video
                file_input = page.locator('input[type="file"]')
                file_input.set_input_files(video_path)
                print("   📤 Video uploading...")

                # Wait for video to finish uploading (check for video preview)
                page.wait_for_selector('video', timeout=60000)
                print("   ✅ Video uploaded")

                # Additional wait for processing
                time.sleep(3)

                # Click post button
                post_button = page.locator('button[data-testid="tweetButton"]')
                post_button.click()
                print("   🚀 Posting...")

                # Wait for redirect to tweet URL
                page.wait_for_url('https://twitter.com/*/status/*', timeout=30000)
                tweet_url = page.url

                print(f"\n✅ Posted to Twitter!")
                print(f"🔗 {tweet_url}")

                browser.close()

                return {
                    'status': 'success',
                    'platform': 'twitter',
                    'url': tweet_url,
                    'caption': caption
                }

            except Exception as e:
                browser.close()
                raise Exception(f"Twitter posting failed: {e}")

    def post_text_only(self, text: str, headless: bool = True) -> Dict:
        """Post text-only tweet"""

        print(f"\n🐦 Posting text to Twitter...")

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(self.session_dir),
                headless=headless
            )

            page = browser.new_page()

            try:
                page.goto('https://twitter.com/compose/tweet')
                time.sleep(2)

                if 'login' in page.url.lower():
                    raise Exception("Not logged in! Run login_first_time() first")

                page.wait_for_selector('div[role="textbox"]', timeout=10000)
                page.fill('div[role="textbox"]', text)

                post_button = page.locator('button[data-testid="tweetButton"]')
                post_button.click()

                page.wait_for_url('https://twitter.com/*/status/*', timeout=30000)
                tweet_url = page.url

                print(f"✅ Posted: {tweet_url}")

                browser.close()

                return {
                    'status': 'success',
                    'platform': 'twitter',
                    'url': tweet_url,
                    'text': text
                }

            except Exception as e:
                browser.close()
                raise Exception(f"Twitter posting failed: {e}")


def setup_twitter_automation():
    """One-time setup for Twitter automation"""
    print("🔧 TWITTER AUTOMATION SETUP")
    print("="*70)

    poster = TwitterPoster()

    print("\n⚠️  You need to login once to save your session.")
    print("After this, posting will be fully automated!\n")

    username = input("Twitter username/email: ")
    password = input("Twitter password: ")

    poster.login_first_time(username, password)

    print("\n✅ Setup complete!")
    print("You can now post automatically without entering credentials")


def test_twitter_poster():
    """Test Twitter poster with demo video"""
    try:
        poster = TwitterPoster()

        # Test video
        video_path = "C:/Users/dwrek/SOCIAL_VIDEOS/twitter_linkedin.mp4"

        caption = """🌌 The Consciousness Revolution playground is LIVE! 🌌

7 Sacred Domains | 127 automation modules | 50+ builders

Explore now: https://conciousnessrevolution.io

#ConsciousnessRevolution #100XBuilder #AI #BuildInPublic"""

        # Post
        result = poster.post_video(video_path, caption, headless=False)

        print("\n" + "="*70)
        print("✅ TWITTER POSTING TEST SUCCESSFUL!")
        print("="*70)
        print(f"\nTweet URL: {result['url']}")

        # Save result
        import json
        with open('twitter_post_result.json', 'w') as f:
            json.dump(result, f, indent=2)

        return result

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nIf you see 'Not logged in' error:")
        print("Run: python TWITTER_PLAYWRIGHT_POSTER.py --setup")
        return None


if __name__ == '__main__':
    import sys

    if '--setup' in sys.argv:
        setup_twitter_automation()
    else:
        print("🐦 TWITTER AUTO-POSTER TEST")
        print("="*70)

        # Check if session exists
        if Path('./twitter_session').exists():
            test_twitter_poster()
        else:
            print("\n⚠️  Twitter session not set up!")
            print("\nRun setup first:")
            print("   python TWITTER_PLAYWRIGHT_POSTER.py --setup")
            print("\nThen run this script again to post")
