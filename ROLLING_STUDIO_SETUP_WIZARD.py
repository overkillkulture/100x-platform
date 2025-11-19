#!/usr/bin/env python3
"""
ROLLING STUDIO SETUP WIZARD
Makes deployment brain-dead simple. No PowerShell sword fighting.
"""

import os
import json
import sys
from pathlib import Path

class SetupWizard:
    """Interactive setup that does everything for you"""

    def __init__(self):
        self.config_file = Path("rolling_studio_config.json")
        self.config = {}

    def run(self):
        """Run the complete setup wizard"""

        print("\n" + "="*60)
        print("   ROLLING STUDIO SETUP WIZARD")
        print("="*60)
        print("\nThis wizard will set up your rolling studio in 5 minutes.")
        print("Answer a few questions and we'll handle the rest.\n")

        # Step 1: Choose mode
        mode = self.choose_mode()

        if mode == "test":
            self.setup_test_mode()
        elif mode == "live":
            self.setup_live_mode()
        elif mode == "skip":
            self.setup_skip_mode()

        # Save config
        self.save_config()

        print("\n" + "="*60)
        print("   SETUP COMPLETE!")
        print("="*60)
        print(f"\nConfiguration saved to: {self.config_file}")
        print("\nNext steps:")
        if mode == "test":
            print("  1. Run: DROP_VIDEO_HERE.bat")
            print("  2. Drop any video file when prompted")
            print("  3. Watch it process automatically")
        elif mode == "live":
            print("  1. Install 360° camera in vehicle")
            print("  2. Run: START_AUTO_POSTER.bat")
            print("  3. System posts automatically 24/7")
        else:
            print("  1. Read the book chapters")
            print("  2. Order hardware when ready")
            print("  3. Come back and run setup again")

        return 0

    def choose_mode(self):
        """Let user choose setup mode"""

        print("="*60)
        print("STEP 1: Choose Your Mode")
        print("="*60)
        print("\n1. TEST MODE - Try it with any video right now")
        print("   (No hardware needed, see how it works)")
        print("\n2. LIVE MODE - Full deployment with auto-posting")
        print("   (Requires social media API credentials)")
        print("\n3. SKIP FOR NOW - Just read the documentation")
        print("   (Come back when you're ready to deploy)")
        print()

        while True:
            choice = input("Choose [1/2/3]: ").strip()
            if choice == "1":
                return "test"
            elif choice == "2":
                return "live"
            elif choice == "3":
                return "skip"
            else:
                print("Please enter 1, 2, or 3")

    def setup_test_mode(self):
        """Set up for testing without credentials"""

        print("\n" + "="*60)
        print("TEST MODE SETUP")
        print("="*60)
        print("\nPerfect! Test mode lets you see the system work")
        print("without any API credentials or hardware.\n")

        self.config['mode'] = 'test'
        self.config['auto_post'] = False
        self.config['simulate'] = True

        print("✓ Test mode configured")
        print("✓ Simulation enabled")
        print("✓ No credentials needed")

        # Create helper batch file
        self.create_test_batch_file()

    def setup_live_mode(self):
        """Set up for live deployment"""

        print("\n" + "="*60)
        print("LIVE MODE SETUP")
        print("="*60)
        print("\nLive mode means content posts automatically to social media.")
        print("We'll need API credentials for the platforms you want to use.\n")

        print("Which platforms do you want to use?")
        print("(You can add more later)\n")

        platforms = {}

        # YouTube
        use_youtube = input("Use YouTube Shorts? [y/n]: ").strip().lower() == 'y'
        if use_youtube:
            platforms['youtube'] = self.get_youtube_credentials()

        # Instagram
        use_instagram = input("Use Instagram Reels? [y/n]: ").strip().lower() == 'y'
        if use_instagram:
            platforms['instagram'] = self.get_instagram_credentials()

        # TikTok
        use_tiktok = input("Use TikTok? [y/n]: ").strip().lower() == 'y'
        if use_tiktok:
            platforms['tiktok'] = self.get_tiktok_credentials()

        # Twitter
        use_twitter = input("Use Twitter/X? [y/n]: ").strip().lower() == 'y'
        if use_twitter:
            platforms['twitter'] = self.get_twitter_credentials()

        # LinkedIn
        use_linkedin = input("Use LinkedIn? [y/n]: ").strip().lower() == 'y'
        if use_linkedin:
            platforms['linkedin'] = self.get_linkedin_credentials()

        self.config['mode'] = 'live'
        self.config['auto_post'] = True
        self.config['simulate'] = False
        self.config['platforms'] = platforms

        print(f"\n✓ Live mode configured")
        print(f"✓ {len(platforms)} platform(s) enabled")
        print(f"✓ Auto-posting ready")

        # Create helper batch files
        self.create_live_batch_files()

    def setup_skip_mode(self):
        """Just save minimal config for later"""

        print("\n" + "="*60)
        print("DOCUMENTATION MODE")
        print("="*60)
        print("\nNo problem! Here's what to read:\n")
        print("  1. ROLLING_STUDIO_BOOK_CHAPTER_1.md - The opportunity")
        print("  2. ROLLING_STUDIO_BOOK_CHAPTER_2.md - The compound effect")
        print("  3. QUICK_START_ROLLING_STUDIO.md - 5-minute overview")
        print("  4. ROLLING_STUDIO_INTEGRATION_GUIDE.md - Complete setup")
        print("\nWhen you're ready to deploy, run this wizard again!")

        self.config['mode'] = 'skip'
        self.config['auto_post'] = False
        self.config['simulate'] = True

    def get_youtube_credentials(self):
        """Get YouTube API credentials"""
        print("\n--- YouTube Setup ---")
        print("Go to: https://console.cloud.google.com/apis/credentials")
        print("Create OAuth 2.0 credentials and download JSON file")

        creds_file = input("Path to credentials file (or 'skip'): ").strip()

        if creds_file.lower() == 'skip':
            print("⚠ YouTube skipped - will run in simulation mode")
            return {'enabled': False}

        if Path(creds_file).exists():
            print("✓ YouTube credentials found")
            return {'enabled': True, 'credentials_file': creds_file}
        else:
            print("⚠ File not found - will run in simulation mode")
            return {'enabled': False}

    def get_instagram_credentials(self):
        """Get Instagram API credentials"""
        print("\n--- Instagram Setup ---")
        print("Go to: https://developers.facebook.com/")
        print("Create app and get access token")

        token = input("Access token (or 'skip'): ").strip()

        if token.lower() == 'skip' or not token:
            print("⚠ Instagram skipped - will run in simulation mode")
            return {'enabled': False}

        # Save to environment variable
        os.environ['INSTAGRAM_ACCESS_TOKEN'] = token
        print("✓ Instagram token saved")
        return {'enabled': True, 'token': token}

    def get_tiktok_credentials(self):
        """Get TikTok API credentials"""
        print("\n--- TikTok Setup ---")
        print("Go to: https://developers.tiktok.com/")
        print("Create app and get access token")

        token = input("Access token (or 'skip'): ").strip()

        if token.lower() == 'skip' or not token:
            print("⚠ TikTok skipped - will run in simulation mode")
            return {'enabled': False}

        os.environ['TIKTOK_ACCESS_TOKEN'] = token
        print("✓ TikTok token saved")
        return {'enabled': True, 'token': token}

    def get_twitter_credentials(self):
        """Get Twitter API credentials"""
        print("\n--- Twitter/X Setup ---")
        print("Go to: https://developer.twitter.com/")
        print("Create app and get API keys")

        print("\nEnter your credentials (or 'skip' to skip):")
        api_key = input("  API Key: ").strip()

        if api_key.lower() == 'skip' or not api_key:
            print("⚠ Twitter skipped - will run in simulation mode")
            return {'enabled': False}

        api_secret = input("  API Secret: ").strip()
        access_token = input("  Access Token: ").strip()
        access_secret = input("  Access Secret: ").strip()

        # Save to environment variables
        os.environ['TWITTER_API_KEY'] = api_key
        os.environ['TWITTER_API_SECRET'] = api_secret
        os.environ['TWITTER_ACCESS_TOKEN'] = access_token
        os.environ['TWITTER_ACCESS_SECRET'] = access_secret

        print("✓ Twitter credentials saved")
        return {
            'enabled': True,
            'api_key': api_key,
            'api_secret': api_secret,
            'access_token': access_token,
            'access_secret': access_secret
        }

    def get_linkedin_credentials(self):
        """Get LinkedIn API credentials"""
        print("\n--- LinkedIn Setup ---")
        print("Go to: https://www.linkedin.com/developers/")
        print("Create app and get access token")

        token = input("Access token (or 'skip'): ").strip()

        if token.lower() == 'skip' or not token:
            print("⚠ LinkedIn skipped - will run in simulation mode")
            return {'enabled': False}

        os.environ['LINKEDIN_ACCESS_TOKEN'] = token
        print("✓ LinkedIn token saved")
        return {'enabled': True, 'token': token}

    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"\n✓ Configuration saved to {self.config_file}")

    def create_test_batch_file(self):
        """Create simple test batch file"""

        batch_content = """@echo off
echo.
echo ========================================
echo    ROLLING STUDIO TEST
echo ========================================
echo.
echo Drop a video file into this folder and rename it to:
echo    test_drive_footage.mp4
echo.
echo Then press any key to process it...
pause

if not exist "test_drive_footage.mp4" (
    echo ERROR: No test video found!
    echo Please add: test_drive_footage.mp4
    pause
    exit /b 1
)

echo.
echo Processing video...
python AI_ROLLING_STUDIO_PROCESSOR.py

echo.
echo ========================================
echo    PROCESSING COMPLETE
echo ========================================
echo.
echo Check results in: rolling_studio_output\\
echo.
pause
"""

        Path("DROP_VIDEO_HERE.bat").write_text(batch_content)
        print("✓ Created: DROP_VIDEO_HERE.bat")

    def create_live_batch_files(self):
        """Create batch files for live operation"""

        # Start auto-poster
        poster_content = """@echo off
echo.
echo ========================================
echo    ROLLING STUDIO AUTO-POSTER
echo ========================================
echo.
echo Starting 24/7 auto-posting system...
echo Press Ctrl+C to stop
echo.
python SOCIAL_MEDIA_AUTO_POSTER.py daemon
"""

        Path("START_AUTO_POSTER.bat").write_text(poster_content)
        print("✓ Created: START_AUTO_POSTER.bat")

        # Process new videos
        process_content = """@echo off
echo.
echo ========================================
echo    PROCESS NEW VIDEOS
echo ========================================
echo.
echo This will process any new videos in the watch folder
echo.
python AI_ROLLING_STUDIO_PROCESSOR.py
pause
"""

        Path("PROCESS_NEW_VIDEOS.bat").write_text(process_content)
        print("✓ Created: PROCESS_NEW_VIDEOS.bat")


if __name__ == "__main__":
    wizard = SetupWizard()
    sys.exit(wizard.run())
