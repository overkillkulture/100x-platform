#!/usr/bin/env python3
"""
📱 SOCIAL MEDIA AUTO-POSTER
Automatically posts rolling studio content across all platforms

Reads posting_schedule.json and posts content at optimal times
Supports: YouTube, Instagram, TikTok, Twitter, LinkedIn

Commander records → AI processes → This posts → COMPLETE AUTOMATION
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import os
import sys

class SocialMediaAutoPoster:
    """Multi-platform content distribution system"""

    def __init__(self, schedule_file, output_dir):
        self.schedule_file = Path(schedule_file)
        self.output_dir = Path(output_dir)
        self.posted_log = self.output_dir / 'posted_content.json'

        # Load schedule
        with open(self.schedule_file) as f:
            self.schedule = json.load(f)

        # Load posted history
        if self.posted_log.exists():
            with open(self.posted_log) as f:
                self.posted_history = json.load(f)
        else:
            self.posted_history = []

        # Platform API clients (will be initialized when credentials available)
        self.platforms = {
            'youtube_shorts': None,
            'instagram_reels': None,
            'tiktok': None,
            'twitter': None,
            'linkedin': None
        }

    def initialize_platform_apis(self):
        """Initialize API clients for each platform"""

        # YouTube API
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials

            # Check for YouTube credentials
            creds_file = Path(os.getenv('YOUTUBE_CREDENTIALS', 'youtube_credentials.json'))
            if creds_file.exists():
                creds = Credentials.from_authorized_user_file(str(creds_file))
                self.platforms['youtube_shorts'] = build('youtube', 'v3', credentials=creds)
                print("✓ YouTube API initialized")
            else:
                print("⚠️  YouTube credentials not found (simulated mode)")
        except ImportError:
            print("⚠️  YouTube API not installed (pip install google-api-python-client)")

        # Instagram API
        try:
            import requests
            token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
            if token:
                self.platforms['instagram_reels'] = {
                    'token': token,
                    'api_url': 'https://graph.facebook.com/v18.0'
                }
                print("✓ Instagram API initialized")
            else:
                print("⚠️  Instagram token not found (simulated mode)")
        except Exception as e:
            print(f"⚠️  Instagram API error: {e}")

        # TikTok API
        try:
            token = os.getenv('TIKTOK_ACCESS_TOKEN')
            if token:
                self.platforms['tiktok'] = {
                    'token': token,
                    'api_url': 'https://open-api.tiktok.com'
                }
                print("✓ TikTok API initialized")
            else:
                print("⚠️  TikTok token not found (simulated mode)")
        except Exception as e:
            print(f"⚠️  TikTok API error: {e}")

        # Twitter/X API
        try:
            import tweepy
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_secret = os.getenv('TWITTER_ACCESS_SECRET')

            if all([api_key, api_secret, access_token, access_secret]):
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_secret)
                self.platforms['twitter'] = tweepy.API(auth)
                print("✓ Twitter API initialized")
            else:
                print("⚠️  Twitter credentials not found (simulated mode)")
        except ImportError:
            print("⚠️  Twitter API not installed (pip install tweepy)")

        # LinkedIn API
        try:
            token = os.getenv('LINKEDIN_ACCESS_TOKEN')
            if token:
                self.platforms['linkedin'] = {
                    'token': token,
                    'api_url': 'https://api.linkedin.com/v2'
                }
                print("✓ LinkedIn API initialized")
            else:
                print("⚠️  LinkedIn token not found (simulated mode)")
        except Exception as e:
            print(f"⚠️  LinkedIn API error: {e}")

    def post_to_youtube_shorts(self, content):
        """Upload video to YouTube Shorts"""

        video_file = self.output_dir / content['clip']

        if self.platforms['youtube_shorts']:
            # Real API upload
            try:
                request = self.platforms['youtube_shorts'].videos().insert(
                    part="snippet,status",
                    body={
                        'snippet': {
                            'title': content['title'],
                            'description': content['description'],
                            'tags': ['shorts', 'rollingstudio', 'consciousness'],
                            'categoryId': '22'  # People & Blogs
                        },
                        'status': {
                            'privacyStatus': 'public',
                            'selfDeclaredMadeForKids': False
                        }
                    },
                    media_body=str(video_file)
                )
                response = request.execute()
                return {
                    'success': True,
                    'platform': 'youtube_shorts',
                    'video_id': response['id'],
                    'url': f"https://youtube.com/shorts/{response['id']}"
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Simulated upload
            return {
                'success': True,
                'platform': 'youtube_shorts',
                'video_id': 'SIMULATED_ID',
                'url': f'https://youtube.com/shorts/SIMULATED_ID',
                'simulated': True
            }

    def post_to_instagram_reels(self, content):
        """Upload reel to Instagram"""

        video_file = self.output_dir / content['clip']

        if self.platforms['instagram_reels']:
            # Real API upload (multi-step process)
            try:
                import requests

                # Step 1: Initialize upload
                api = self.platforms['instagram_reels']
                init_url = f"{api['api_url']}/me/media"
                init_data = {
                    'media_type': 'REELS',
                    'video_url': str(video_file),  # Must be public URL
                    'caption': content['caption'],
                    'access_token': api['token']
                }
                init_response = requests.post(init_url, data=init_data)
                creation_id = init_response.json()['id']

                # Step 2: Publish
                publish_url = f"{api['api_url']}/me/media_publish"
                publish_data = {
                    'creation_id': creation_id,
                    'access_token': api['token']
                }
                publish_response = requests.post(publish_url, data=publish_data)

                return {
                    'success': True,
                    'platform': 'instagram_reels',
                    'media_id': publish_response.json()['id'],
                    'url': f"https://instagram.com/reel/{publish_response.json()['id']}"
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Simulated upload
            return {
                'success': True,
                'platform': 'instagram_reels',
                'media_id': 'SIMULATED_ID',
                'url': 'https://instagram.com/reel/SIMULATED_ID',
                'simulated': True
            }

    def post_to_tiktok(self, content):
        """Upload video to TikTok"""

        video_file = self.output_dir / content['clip']

        if self.platforms['tiktok']:
            # Real API upload
            try:
                import requests

                api = self.platforms['tiktok']
                url = f"{api['api_url']}/share/video/upload/"

                with open(video_file, 'rb') as f:
                    files = {'video': f}
                    data = {
                        'access_token': api['token'],
                        'caption': content['caption']
                    }
                    response = requests.post(url, files=files, data=data)

                result = response.json()
                return {
                    'success': result.get('error_code') == 0,
                    'platform': 'tiktok',
                    'share_id': result.get('share_id'),
                    'url': result.get('share_url')
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Simulated upload
            return {
                'success': True,
                'platform': 'tiktok',
                'share_id': 'SIMULATED_ID',
                'url': 'https://tiktok.com/@user/video/SIMULATED_ID',
                'simulated': True
            }

    def post_to_twitter(self, content):
        """Post video to Twitter/X"""

        video_file = self.output_dir / content['clip']

        if self.platforms['twitter']:
            # Real API upload
            try:
                # Upload media
                media = self.platforms['twitter'].media_upload(str(video_file))

                # Post tweet with media
                tweet = self.platforms['twitter'].update_status(
                    status=content['text'],
                    media_ids=[media.media_id]
                )

                return {
                    'success': True,
                    'platform': 'twitter',
                    'tweet_id': tweet.id,
                    'url': f"https://twitter.com/user/status/{tweet.id}"
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Simulated upload
            return {
                'success': True,
                'platform': 'twitter',
                'tweet_id': 'SIMULATED_ID',
                'url': 'https://twitter.com/user/status/SIMULATED_ID',
                'simulated': True
            }

    def post_to_linkedin(self, content):
        """Share video on LinkedIn"""

        video_file = self.output_dir / content['clip']

        if self.platforms['linkedin']:
            # Real API upload (complex multi-step)
            try:
                import requests

                api = self.platforms['linkedin']
                headers = {'Authorization': f"Bearer {api['token']}"}

                # Step 1: Register upload
                register_url = f"{api['api_url']}/assets?action=registerUpload"
                register_data = {
                    'registerUploadRequest': {
                        'recipes': ['urn:li:digitalmediaRecipe:feedshare-video'],
                        'owner': 'urn:li:person:PERSON_ID',  # Need user ID
                        'serviceRelationships': [{
                            'relationshipType': 'OWNER',
                            'identifier': 'urn:li:userGeneratedContent'
                        }]
                    }
                }
                register_response = requests.post(register_url, headers=headers, json=register_data)
                asset_id = register_response.json()['value']['asset']
                upload_url = register_response.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']

                # Step 2: Upload video
                with open(video_file, 'rb') as f:
                    requests.put(upload_url, data=f)

                # Step 3: Create share
                share_url = f"{api['api_url']}/ugcPosts"
                share_data = {
                    'author': 'urn:li:person:PERSON_ID',
                    'lifecycleState': 'PUBLISHED',
                    'specificContent': {
                        'com.linkedin.ugc.ShareContent': {
                            'shareCommentary': {'text': content['text']},
                            'shareMediaCategory': 'VIDEO',
                            'media': [{
                                'status': 'READY',
                                'media': asset_id
                            }]
                        }
                    },
                    'visibility': {'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'}
                }
                share_response = requests.post(share_url, headers=headers, json=share_data)

                return {
                    'success': True,
                    'platform': 'linkedin',
                    'post_id': share_response.json()['id'],
                    'url': f"https://linkedin.com/feed/update/{share_response.json()['id']}"
                }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Simulated upload
            return {
                'success': True,
                'platform': 'linkedin',
                'post_id': 'SIMULATED_ID',
                'url': 'https://linkedin.com/feed/update/SIMULATED_ID',
                'simulated': True
            }

    def post_content(self, scheduled_item):
        """Post content to appropriate platform"""

        platform = scheduled_item['platform']
        content = scheduled_item['content']

        print(f"\n📱 Posting to {platform}...")
        print(f"   Clip: {content['clip']}")

        # Route to appropriate platform handler
        if platform == 'youtube_shorts':
            result = self.post_to_youtube_shorts(content)
        elif platform == 'instagram_reels':
            result = self.post_to_instagram_reels(content)
        elif platform == 'tiktok':
            result = self.post_to_tiktok(content)
        elif platform == 'twitter':
            result = self.post_to_twitter(content)
        elif platform == 'linkedin':
            result = self.post_to_linkedin(content)
        else:
            result = {'success': False, 'error': f'Unknown platform: {platform}'}

        # Log result
        if result['success']:
            mode = ' (simulated)' if result.get('simulated') else ''
            print(f"   ✓ Posted{mode}: {result.get('url', 'N/A')}")

            # Save to posted history
            self.posted_history.append({
                'timestamp': datetime.now().isoformat(),
                'platform': platform,
                'clip': content['clip'],
                'result': result
            })

            # Update posted log
            with open(self.posted_log, 'w') as f:
                json.dump(self.posted_history, f, indent=2)
        else:
            print(f"   ✗ Failed: {result.get('error', 'Unknown error')}")

        return result

    def run_posting_scheduler(self, mode='once'):
        """Run posting scheduler

        Args:
            mode: 'once' (post due items now) or 'daemon' (run continuously)
        """

        print("=" * 60)
        print("📅 SOCIAL MEDIA AUTO-POSTER SCHEDULER")
        print("=" * 60)

        # Initialize platform APIs
        print("\n🔧 Initializing platform APIs...")
        self.initialize_platform_apis()

        if mode == 'once':
            # Post everything due now
            print(f"\n📋 Checking schedule for due posts...")

            current_time = datetime.now()
            posted_count = 0

            for item in self.schedule:
                # Check if already posted
                already_posted = any(
                    h['clip'] == item['content']['clip'] and h['platform'] == item['platform']
                    for h in self.posted_history
                )

                if already_posted:
                    continue

                # For demo, post first few items
                if posted_count < 5:  # Post first 5 items
                    result = self.post_content(item)
                    if result['success']:
                        posted_count += 1

            print(f"\n✅ Posted {posted_count} items")

        elif mode == 'daemon':
            # Run continuously, posting at scheduled times
            print("\n🔄 Running in daemon mode (Ctrl+C to stop)...")

            try:
                while True:
                    current_time = datetime.now()
                    current_hour = current_time.hour
                    current_day = (current_time - datetime.now().replace(hour=0, minute=0, second=0)).days

                    for item in self.schedule:
                        # Parse schedule time
                        schedule_day = int(item['post_day'].replace('Day ', ''))
                        schedule_hour = int(item['post_time'].split(':')[0])

                        # Check if it's time to post
                        if schedule_day == current_day + 1 and schedule_hour == current_hour:
                            # Check if already posted
                            already_posted = any(
                                h['clip'] == item['content']['clip'] and h['platform'] == item['platform']
                                for h in self.posted_history
                            )

                            if not already_posted:
                                self.post_content(item)

                    # Check every hour
                    print(f"⏰ {current_time.strftime('%H:%M')} - Waiting for next scheduled post...")
                    time.sleep(3600)  # Sleep 1 hour

            except KeyboardInterrupt:
                print("\n\n🛑 Scheduler stopped by user")


def main():
    """Run auto-poster"""

    # Default paths
    schedule_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/rolling_studio_output/posting_schedule.json")
    output_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/rolling_studio_output")

    # Check if schedule exists
    if not schedule_file.exists():
        print("❌ No posting schedule found!")
        print(f"   Expected: {schedule_file}")
        print("\n💡 Run AI_ROLLING_STUDIO_PROCESSOR.py first to generate schedule")
        sys.exit(1)

    # Create auto-poster
    poster = SocialMediaAutoPoster(schedule_file, output_dir)

    # Run scheduler (once mode for testing, daemon for production)
    mode = 'once'  # Change to 'daemon' for continuous operation
    poster.run_posting_scheduler(mode=mode)

    print("\n" + "=" * 60)
    print("✅ AUTO-POSTING COMPLETE")
    print("=" * 60)
    print(f"\nPosted items logged to: {poster.posted_log}")
    print("\n💡 Set mode='daemon' for continuous 24/7 posting")
    print("   python SOCIAL_MEDIA_AUTO_POSTER.py daemon\n")


if __name__ == "__main__":
    # Support command line argument for mode
    if len(sys.argv) > 1 and sys.argv[1] == 'daemon':
        mode = 'daemon'
    main()
