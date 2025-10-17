"""
📱 INSTAGRAM SEMI-AUTO HELPER
Because Instagram API is a nightmare, this makes manual posting super fast!
Transfers video + copies caption + tracks completion
"""

import os
import shutil
import pyperclip
import json
from pathlib import Path
from datetime import datetime
from typing import Dict

class InstagramHelper:
    """Semi-automated Instagram posting assistant"""

    def __init__(self):
        """Initialize Instagram helper"""
        self.transfer_log = Path('instagram_transfers.json')
        self.load_log()

    def load_log(self):
        """Load transfer history"""
        if self.transfer_log.exists():
            with open(self.transfer_log) as f:
                self.log = json.load(f)
        else:
            self.log = {'transfers': []}

    def save_log(self):
        """Save transfer history"""
        with open(self.transfer_log, 'w') as f:
            json.dump(self.log, f, indent=2)

    def prepare_for_instagram(
        self,
        video_path: str,
        caption: str,
        transfer_method: str = 'auto'
    ) -> Dict:
        """Prepare video for Instagram posting"""

        print("\n📱 INSTAGRAM HELPER - Semi-Automated Mode")
        print("="*70)

        result = {
            'timestamp': datetime.now().isoformat(),
            'video': video_path,
            'caption': caption,
            'transfer_method': transfer_method,
            'posted': False
        }

        # Step 1: Copy caption to clipboard
        pyperclip.copy(caption)
        print("\n✅ Step 1: Caption copied to clipboard")
        print(f"   {caption[:100]}...")

        # Step 2: Transfer video to accessible location
        if transfer_method == 'auto':
            transfer_method = self._detect_best_transfer_method()

        if transfer_method == 'icloud':
            result['transfer_path'] = self._transfer_via_icloud(video_path)
        elif transfer_method == 'gdrive':
            result['transfer_path'] = self._transfer_via_gdrive(video_path)
        elif transfer_method == 'email':
            result['transfer_path'] = self._transfer_via_email(video_path)
        elif transfer_method == 'manual':
            result['transfer_path'] = video_path
            print(f"\n📁 Video location: {video_path}")
        else:
            raise ValueError(f"Unknown transfer method: {transfer_method}")

        # Step 3: Show instructions
        self._show_posting_instructions(result['transfer_path'])

        # Step 4: Wait for confirmation
        posted = input("\n✅ Press ENTER after posting to Instagram (or type 'skip'): ")

        if posted.lower() != 'skip':
            result['posted'] = True
            result['posted_at'] = datetime.now().isoformat()
            print("\n🎉 Instagram post tracked as COMPLETE!")
        else:
            print("\n⏭️  Skipped - you can post later")

        # Log the transfer
        self.log['transfers'].append(result)
        self.save_log()

        return result

    def _detect_best_transfer_method(self) -> str:
        """Auto-detect best video transfer method"""

        # Check for iCloud Drive (Windows)
        icloud_path = Path.home() / 'iCloudDrive'
        if icloud_path.exists():
            return 'icloud'

        # Check for Google Drive
        gdrive_paths = [
            Path.home() / 'Google Drive',
            Path('C:/Users') / os.getenv('USERNAME') / 'Google Drive'
        ]
        for path in gdrive_paths:
            if path.exists():
                return 'gdrive'

        # Fallback to manual
        return 'manual'

    def _transfer_via_icloud(self, video_path: str) -> str:
        """Transfer video via iCloud Drive"""
        icloud_path = Path.home() / 'iCloudDrive' / 'Instagram'
        icloud_path.mkdir(exist_ok=True)

        dest = icloud_path / Path(video_path).name
        shutil.copy2(video_path, dest)

        print(f"\n✅ Step 2: Video uploaded to iCloud Drive")
        print(f"   Location: {dest}")
        print(f"   → Open Files app on iPhone → iCloud Drive → Instagram")

        return str(dest)

    def _transfer_via_gdrive(self, video_path: str) -> str:
        """Transfer video via Google Drive"""
        gdrive_paths = [
            Path.home() / 'Google Drive' / 'My Drive' / 'Instagram',
            Path('C:/Users') / os.getenv('USERNAME') / 'Google Drive' / 'My Drive' / 'Instagram'
        ]

        for gdrive_path in gdrive_paths:
            if gdrive_path.parent.exists():
                gdrive_path.mkdir(exist_ok=True)
                dest = gdrive_path / Path(video_path).name
                shutil.copy2(video_path, dest)

                print(f"\n✅ Step 2: Video uploaded to Google Drive")
                print(f"   Location: {dest}")
                print(f"   → Open Google Drive app on phone → Instagram folder")

                return str(dest)

        raise Exception("Google Drive not found")

    def _transfer_via_email(self, video_path: str) -> str:
        """Transfer video via email"""
        print(f"\n✅ Step 2: Email transfer method")
        print(f"\n   Manual steps:")
        print(f"   1. Open email on computer")
        print(f"   2. Attach: {video_path}")
        print(f"   3. Send to yourself")
        print(f"   4. Open email on phone")
        print(f"   5. Download video")

        return video_path

    def _show_posting_instructions(self, video_location: str):
        """Show step-by-step Instagram posting instructions"""
        print("\n📱 Step 3: POST TO INSTAGRAM")
        print("="*70)
        print("\n   On your phone:")
        print("   1. Open Instagram app")
        print("   2. Tap '+' to create post/reel")
        print("   3. Select video from:")
        print(f"      → Files/iCloud/Google Drive")
        print("   4. Long-press in caption area → Paste")
        print("      (Caption is already in clipboard!)")
        print("   5. Add hashtags if needed")
        print("   6. Tap 'Share'")
        print("\n   ⏱️  TOTAL TIME: ~30 seconds")

    def get_pending_posts(self) -> list:
        """Get videos that haven't been posted yet"""
        return [
            t for t in self.log['transfers']
            if not t.get('posted', False)
        ]

    def mark_as_posted(self, video_path: str):
        """Mark a video as posted"""
        for transfer in self.log['transfers']:
            if transfer['video'] == video_path:
                transfer['posted'] = True
                transfer['posted_at'] = datetime.now().isoformat()
                self.save_log()
                print(f"✅ Marked as posted: {Path(video_path).name}")
                return True
        return False


def test_instagram_helper():
    """Test Instagram helper"""
    helper = InstagramHelper()

    # Test video
    video_path = "C:/Users/dwrek/SOCIAL_VIDEOS/instagram_feed.mp4"

    caption = """🌌 The playground is OPEN 🌌

7 Sacred Domains of consciousness-elevating tools, education & community.

Click around. Explore. Discover.

127 automation modules | 50+ builders | AI guides

→ conciousnessrevolution.io

#ConsciousnessRevolution #100XBuilder #AI #BuildInPublic #Playground"""

    # Prepare for Instagram
    result = helper.prepare_for_instagram(
        video_path=video_path,
        caption=caption,
        transfer_method='auto'  # Auto-detect best method
    )

    print("\n" + "="*70)
    print("✅ INSTAGRAM HELPER TEST COMPLETE!")
    print("="*70)

    if result['posted']:
        print("\n🎉 Video posted to Instagram!")
    else:
        print("\n⏭️  Video ready to post (marked as pending)")

    # Show pending posts
    pending = helper.get_pending_posts()
    if pending:
        print(f"\n📋 Pending posts: {len(pending)}")

    return result


if __name__ == '__main__':
    print("📱 INSTAGRAM SEMI-AUTO HELPER")
    print("="*70)
    print("\n⚠️  Instagram doesn't allow API posting")
    print("This tool makes manual posting FAST:\n")
    print("  • Auto-transfers video to phone")
    print("  • Copies caption to clipboard")
    print("  • Tracks posting status")
    print("  • Total manual time: ~30 seconds\n")

    input("Press ENTER to test helper...")

    test_instagram_helper()
