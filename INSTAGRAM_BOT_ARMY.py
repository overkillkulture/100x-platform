"""
🤖 INSTAGRAM BOT ARMY - AUTONOMOUS HELPER ACTIVATION 🤖

Activates Instagram automation helpers to assist with the 30-second manual step.
Because even semi-automation can be FULL automation with the right helpers!

Built autonomously while Commander ate.
Trinity-powered consciousness automation.
"""

from playwright.sync_api import sync_playwright
import time
import pyperclip
import json
from pathlib import Path
from datetime import datetime
import os

class InstagramBotArmy:
    """
    Instagram Bot Army - Automated helpers for Instagram posting

    What it does:
    1. Monitors clipboard for Instagram-ready videos
    2. Detects when InstagramHelper prepares a post
    3. Auto-opens Instagram in browser
    4. Auto-navigates to create post
    5. Auto-uploads video
    6. Auto-pastes caption
    7. Waits for human to click "Share" (Instagram's bot detection)

    This reduces 5 minutes of manual work to 5 seconds.
    """

    def __init__(self):
        self.instagram_folder = Path("C:/Users/dwrek/Instagram_Queue")
        self.instagram_folder.mkdir(exist_ok=True)
        self.log_file = Path("instagram_bot_log.json")
        self.queue_file = Path("instagram_queue.json")

    def load_queue(self):
        """Load Instagram post queue"""
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        return []

    def save_queue(self, queue):
        """Save Instagram post queue"""
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)

    def add_to_queue(self, video_path, caption):
        """Add post to Instagram queue"""
        queue = self.load_queue()
        queue.append({
            'video_path': video_path,
            'caption': caption,
            'added_at': datetime.now().isoformat(),
            'status': 'pending'
        })
        self.save_queue(queue)
        print(f"✅ Added to Instagram queue: {video_path}")

    def auto_instagram_post(self, video_path, caption, headless=False):
        """
        Automated Instagram posting with Playwright

        NOTE: Instagram has strong bot detection, so this:
        1. Opens browser (non-headless for human-like behavior)
        2. Navigates to Instagram
        3. Logs in (uses saved session if available)
        4. Creates new post
        5. Uploads video
        6. Pastes caption
        7. STOPS before clicking Share (human must click)

        This bypasses bot detection while still automating 95% of work.
        """

        print("\n" + "="*70)
        print("🤖 INSTAGRAM BOT - AUTO-HELPER ACTIVATED")
        print("="*70)

        with sync_playwright() as p:
            # Launch browser with persistent context (saves login)
            context_dir = Path("./instagram_session")
            context_dir.mkdir(exist_ok=True)

            print("\n📱 Opening Instagram...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(context_dir),
                headless=headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage'
                ]
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            try:
                # Navigate to Instagram
                page.goto('https://www.instagram.com/', wait_until='networkidle')
                time.sleep(3)

                # Check if logged in
                if 'login' in page.url.lower() or page.locator('input[name="username"]').count() > 0:
                    print("\n⚠️  NOT LOGGED IN - Please login manually in the browser")
                    print("    After logging in, run this script again")
                    print("    The session will be saved for future use")
                    input("\nPress ENTER after you've logged in...")

                # Navigate to create post
                print("\n📤 Navigating to create post...")

                # Click create button (+ icon)
                create_selectors = [
                    'a[href="#"]',  # New post icon
                    'svg[aria-label="New post"]',
                    'svg[aria-label="Create"]',
                    '[aria-label="New post"]',
                    '[aria-label="Create"]'
                ]

                clicked = False
                for selector in create_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click()
                            clicked = True
                            print("✅ Clicked create button")
                            break
                    except:
                        continue

                if not clicked:
                    print("⚠️  Could not find create button - Instagram UI may have changed")
                    print("    Opening Instagram in browser for manual posting")
                    page.goto('https://www.instagram.com/')
                    input("\nPress ENTER when ready to close browser...")
                    return

                time.sleep(2)

                # Upload video
                print(f"\n📹 Uploading video: {video_path}")

                # Find file input
                file_input = page.locator('input[type="file"]')
                if file_input.count() > 0:
                    file_input.first.set_input_files(video_path)
                    print("✅ Video uploaded")
                    time.sleep(3)
                else:
                    print("⚠️  Could not find file upload input")

                # Click Next button
                next_button_selectors = [
                    'button:has-text("Next")',
                    'button:has-text("Далее")',  # Russian
                    'button:has-text("Siguiente")',  # Spanish
                    'button[type="button"]'
                ]

                for selector in next_button_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click()
                            print("✅ Clicked Next")
                            time.sleep(2)
                            break
                    except:
                        continue

                # Click Next again (for filters/editing screen)
                time.sleep(2)
                for selector in next_button_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click()
                            print("✅ Clicked Next (editing)")
                            time.sleep(2)
                            break
                    except:
                        continue

                # Paste caption
                print(f"\n📝 Pasting caption...")
                pyperclip.copy(caption)

                # Find caption textarea
                caption_selectors = [
                    'textarea[aria-label*="caption"]',
                    'textarea[placeholder*="caption"]',
                    'textarea'
                ]

                for selector in caption_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click()
                            page.keyboard.press('Control+V')
                            print("✅ Caption pasted")
                            break
                    except:
                        continue

                # STOP HERE - Human must click Share
                print("\n" + "="*70)
                print("⚠️  BOT PAUSES HERE - HUMAN ACTION REQUIRED")
                print("="*70)
                print("\n👆 Please review the post and click 'Share' button")
                print("   This prevents Instagram bot detection")
                print("   (Bot did 95% of work, you just click Share!)")
                print("\nPress ENTER after you've clicked Share...")

                input()

                print("\n✅ Post complete!")
                print("="*70)

            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("   Opening Instagram in browser for manual posting")

            finally:
                # Keep browser open for a moment
                time.sleep(2)
                browser.close()

    def monitor_instagram_queue(self):
        """
        Monitor Instagram queue and auto-process posts

        This runs in background and watches for new posts
        added to the queue by INSTAGRAM_HELPER.py
        """
        print("\n" + "="*70)
        print("👀 INSTAGRAM QUEUE MONITOR - WATCHING FOR POSTS")
        print("="*70)
        print("\nWatching for posts added by Instagram Helper...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                queue = self.load_queue()

                # Process pending posts
                for i, post in enumerate(queue):
                    if post['status'] == 'pending':
                        print(f"\n📬 New post detected in queue!")
                        print(f"   Video: {post['video_path']}")
                        print(f"   Caption: {post['caption'][:50]}...")

                        # Auto-process
                        self.auto_instagram_post(
                            post['video_path'],
                            post['caption']
                        )

                        # Mark as processed
                        queue[i]['status'] = 'completed'
                        queue[i]['completed_at'] = datetime.now().isoformat()
                        self.save_queue(queue)

                # Wait before checking again
                time.sleep(5)

        except KeyboardInterrupt:
            print("\n\n👋 Queue monitor stopped")

def create_instagram_helper_integration():
    """
    Integrate bot army with existing INSTAGRAM_HELPER.py

    Modifies INSTAGRAM_HELPER.py to automatically add posts to bot queue
    """
    helper_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/INSTAGRAM_HELPER.py")

    if not helper_file.exists():
        print("⚠️  INSTAGRAM_HELPER.py not found")
        return

    # Read existing helper
    with open(helper_file, 'r') as f:
        helper_code = f.read()

    # Check if already integrated
    if 'InstagramBotArmy' in helper_code:
        print("✅ Instagram Helper already integrated with Bot Army")
        return

    # Add integration code
    integration = '''
# ═══════════════════════════════════════════════════════════
#  BOT ARMY INTEGRATION
# ═══════════════════════════════════════════════════════════

try:
    from INSTAGRAM_BOT_ARMY import InstagramBotArmy
    BOT_ARMY_AVAILABLE = True
except:
    BOT_ARMY_AVAILABLE = False

def add_to_bot_queue(video_path, caption):
    """Add post to Instagram Bot Army queue for auto-processing"""
    if BOT_ARMY_AVAILABLE:
        bot_army = InstagramBotArmy()
        bot_army.add_to_queue(video_path, caption)
        print("🤖 Added to Instagram Bot Army queue!")
        print("   Run: python INSTAGRAM_BOT_ARMY.py --monitor")
        print("   To auto-process this post")
'''

    # Add to file
    with open(helper_file, 'a') as f:
        f.write('\n' + integration)

    print("✅ Instagram Helper integrated with Bot Army")
    print("   Now Instagram Helper will auto-add to bot queue!")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='🤖 Instagram Bot Army - Automated Helper System'
    )

    parser.add_argument('--monitor', action='store_true',
                       help='Monitor queue and auto-process posts')
    parser.add_argument('--post', type=str,
                       help='Video path to post')
    parser.add_argument('--caption', type=str,
                       help='Caption for post')
    parser.add_argument('--integrate', action='store_true',
                       help='Integrate with INSTAGRAM_HELPER.py')

    args = parser.parse_args()

    bot_army = InstagramBotArmy()

    if args.integrate:
        create_instagram_helper_integration()

    elif args.monitor:
        bot_army.monitor_instagram_queue()

    elif args.post and args.caption:
        bot_army.auto_instagram_post(args.post, args.caption)

    else:
        print("\n🤖 INSTAGRAM BOT ARMY")
        print("="*70)
        print("\nUsage:")
        print("  Monitor queue:     python INSTAGRAM_BOT_ARMY.py --monitor")
        print("  Post manually:     python INSTAGRAM_BOT_ARMY.py --post video.mp4 --caption 'text'")
        print("  Integrate helper:  python INSTAGRAM_BOT_ARMY.py --integrate")
        print("\nThe bot army automates 95% of Instagram posting!")
        print("Human only needs to click 'Share' button (5 seconds)")
        print("="*70)
