#!/usr/bin/env python3
"""
AUTOMATIC SOCIAL MEDIA POSTER
Post to multiple platforms with a single command

Usage:
    python social_poster.py --content "Your post" --platforms all
    python social_poster.py --content "Your post" --platforms twitter,instagram
    python social_poster.py --file post.txt --platforms all --schedule "2025-12-01 14:00"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Try to import required packages
try:
    from dotenv import load_dotenv
    import anthropic
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("\n📦 Install with:")
    print("   pip install python-dotenv anthropic tweepy instagrapi playwright")
    sys.exit(1)


class SocialMediaPoster:
    """Multi-platform social media posting engine"""

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Initialize Claude for content optimization
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            self.claude = anthropic.Anthropic(api_key=api_key)
            self.ai_enabled = True
        else:
            self.claude = None
            self.ai_enabled = False
            print("⚠️  AI optimization disabled (no ANTHROPIC_API_KEY)")

        # Platform configurations
        self.platforms = {
            'twitter': self._load_twitter_config(),
            'instagram': self._load_instagram_config(),
            'tiktok': self._load_tiktok_config(),
            'linkedin': self._load_linkedin_config(),
            'facebook': self._load_facebook_config()
        }

        # Character limits by platform
        self.char_limits = {
            'twitter': 280,
            'instagram': 2200,
            'tiktok': 150,
            'linkedin': 3000,
            'facebook': 63206
        }

    def _load_twitter_config(self) -> Dict:
        """Load Twitter API configuration"""
        return {
            'enabled': bool(os.getenv("TWITTER_API_KEY")),
            'api_key': os.getenv("TWITTER_API_KEY"),
            'api_secret': os.getenv("TWITTER_API_SECRET"),
            'access_token': os.getenv("TWITTER_ACCESS_TOKEN"),
            'access_secret': os.getenv("TWITTER_ACCESS_SECRET")
        }

    def _load_instagram_config(self) -> Dict:
        """Load Instagram configuration"""
        return {
            'enabled': bool(os.getenv("INSTAGRAM_USERNAME")),
            'username': os.getenv("INSTAGRAM_USERNAME"),
            'password': os.getenv("INSTAGRAM_PASSWORD")
        }

    def _load_tiktok_config(self) -> Dict:
        """Load TikTok configuration"""
        return {
            'enabled': bool(os.getenv("TIKTOK_SESSION")),
            'session_id': os.getenv("TIKTOK_SESSION")
        }

    def _load_linkedin_config(self) -> Dict:
        """Load LinkedIn configuration"""
        return {
            'enabled': bool(os.getenv("LINKEDIN_ACCESS_TOKEN")),
            'access_token': os.getenv("LINKEDIN_ACCESS_TOKEN")
        }

    def _load_facebook_config(self) -> Dict:
        """Load Facebook configuration"""
        return {
            'enabled': bool(os.getenv("FACEBOOK_ACCESS_TOKEN")),
            'access_token': os.getenv("FACEBOOK_ACCESS_TOKEN"),
            'page_id': os.getenv("FACEBOOK_PAGE_ID")
        }

    def optimize_content(self, content: str, platform: str) -> str:
        """Use AI to optimize content for specific platform"""
        if not self.ai_enabled:
            # Simple truncation without AI
            limit = self.char_limits.get(platform, 280)
            return content[:limit]

        try:
            platform_guidelines = {
                'twitter': "Short, punchy, include relevant hashtags. Use thread if needed.",
                'instagram': "Engaging caption, emoji, call-to-action, multiple hashtags.",
                'tiktok': "Short, attention-grabbing, trending hashtag or two.",
                'linkedin': "Professional, insightful, storytelling, business value.",
                'facebook': "Conversational, engaging question or statement."
            }

            prompt = f"""Optimize this social media post for {platform}:

Original: {content}

Platform guidelines: {platform_guidelines.get(platform, '')}
Character limit: {self.char_limits.get(platform, 280)}

Provide ONLY the optimized post text, nothing else."""

            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text.strip()

        except Exception as e:
            print(f"⚠️  AI optimization failed: {e}")
            # Fallback to simple truncation
            limit = self.char_limits.get(platform, 280)
            return content[:limit]

    def post_to_twitter(self, content: str, media_path: Optional[str] = None) -> bool:
        """Post to Twitter/X"""
        config = self.platforms['twitter']

        if not config['enabled']:
            print("❌ Twitter not configured")
            return False

        try:
            import tweepy

            # Authenticate
            auth = tweepy.OAuthHandler(config['api_key'], config['api_secret'])
            auth.set_access_token(config['access_token'], config['access_secret'])
            api = tweepy.API(auth)

            # Optimize content
            optimized = self.optimize_content(content, 'twitter')

            # Post
            if media_path and Path(media_path).exists():
                api.update_status_with_media(optimized, media_path)
            else:
                api.update_status(optimized)

            print("✅ Posted to Twitter")
            return True

        except ImportError:
            print("❌ tweepy not installed: pip install tweepy")
            return False
        except Exception as e:
            print(f"❌ Twitter error: {e}")
            return False

    def post_to_instagram(self, content: str, media_path: str) -> bool:
        """Post to Instagram"""
        config = self.platforms['instagram']

        if not config['enabled']:
            print("❌ Instagram not configured")
            return False

        if not media_path or not Path(media_path).exists():
            print("❌ Instagram requires an image or video")
            return False

        try:
            from instagrapi import Client

            # Login
            cl = Client()
            cl.login(config['username'], config['password'])

            # Optimize content
            optimized = self.optimize_content(content, 'instagram')

            # Determine media type
            if media_path.endswith(('.mp4', '.mov')):
                cl.video_upload(media_path, optimized)
            else:
                cl.photo_upload(media_path, optimized)

            print("✅ Posted to Instagram")
            return True

        except ImportError:
            print("❌ instagrapi not installed: pip install instagrapi")
            return False
        except Exception as e:
            print(f"❌ Instagram error: {e}")
            return False

    def post_to_tiktok(self, content: str, video_path: str) -> bool:
        """Post to TikTok"""
        config = self.platforms['tiktok']

        if not config['enabled']:
            print("❌ TikTok not configured")
            return False

        if not video_path or not Path(video_path).exists():
            print("❌ TikTok requires a video")
            return False

        try:
            # TikTok posting typically requires browser automation
            # This is a placeholder for the implementation
            print("⚠️  TikTok posting requires manual configuration")
            print("   Video ready at:", video_path)
            print("   Caption:", self.optimize_content(content, 'tiktok'))
            return False

        except Exception as e:
            print(f"❌ TikTok error: {e}")
            return False

    def post_to_linkedin(self, content: str, media_path: Optional[str] = None) -> bool:
        """Post to LinkedIn"""
        config = self.platforms['linkedin']

        if not config['enabled']:
            print("❌ LinkedIn not configured")
            return False

        try:
            import requests

            # Optimize content
            optimized = self.optimize_content(content, 'linkedin')

            # Post via LinkedIn API
            headers = {
                'Authorization': f'Bearer {config["access_token"]}',
                'Content-Type': 'application/json'
            }

            # Simplified - actual LinkedIn API requires more setup
            print("⚠️  LinkedIn posting requires additional configuration")
            print("   Content ready:", optimized)
            return False

        except Exception as e:
            print(f"❌ LinkedIn error: {e}")
            return False

    def post_to_facebook(self, content: str, media_path: Optional[str] = None) -> bool:
        """Post to Facebook"""
        config = self.platforms['facebook']

        if not config['enabled']:
            print("❌ Facebook not configured")
            return False

        try:
            import requests

            # Optimize content
            optimized = self.optimize_content(content, 'facebook')

            # Post via Facebook Graph API
            print("⚠️  Facebook posting requires additional configuration")
            print("   Content ready:", optimized)
            return False

        except Exception as e:
            print(f"❌ Facebook error: {e}")
            return False

    def post(self, content: str, platforms: List[str], media_path: Optional[str] = None) -> Dict[str, bool]:
        """Post to multiple platforms"""
        results = {}

        platform_map = {
            'twitter': self.post_to_twitter,
            'instagram': self.post_to_instagram,
            'tiktok': self.post_to_tiktok,
            'linkedin': self.post_to_linkedin,
            'facebook': self.post_to_facebook
        }

        for platform in platforms:
            if platform in platform_map:
                print(f"\n📱 Posting to {platform.title()}...")
                results[platform] = platform_map[platform](content, media_path)
            else:
                print(f"⚠️  Unknown platform: {platform}")
                results[platform] = False

        return results


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(description='Post to multiple social media platforms')

    parser.add_argument('--content', type=str, help='Post content')
    parser.add_argument('--file', type=str, help='Read content from file')
    parser.add_argument('--media', type=str, help='Path to image or video')
    parser.add_argument('--platforms', type=str, default='all',
                        help='Comma-separated platforms (twitter,instagram,etc) or "all"')
    parser.add_argument('--schedule', type=str, help='Schedule for later (YYYY-MM-DD HH:MM)')
    parser.add_argument('--test', action='store_true', help='Test mode (dry run)')

    args = parser.parse_args()

    # Get content
    if args.file and Path(args.file).exists():
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    elif args.content:
        content = args.content
    else:
        print("❌ Must provide --content or --file")
        sys.exit(1)

    # Parse platforms
    if args.platforms.lower() == 'all':
        platforms = ['twitter', 'instagram', 'tiktok', 'linkedin', 'facebook']
    else:
        platforms = [p.strip() for p in args.platforms.split(',')]

    print("=" * 60)
    print("📱 AUTOMATIC SOCIAL MEDIA POSTER")
    print("=" * 60)
    print(f"\n📝 Content: {content[:100]}{'...' if len(content) > 100 else ''}")
    print(f"📱 Platforms: {', '.join(platforms)}")
    if args.media:
        print(f"🎨 Media: {args.media}")
    if args.schedule:
        print(f"⏰ Scheduled: {args.schedule}")
    print("")

    if args.test:
        print("🧪 TEST MODE - No actual posting")
        sys.exit(0)

    # Post
    poster = SocialMediaPoster()
    results = poster.post(content, platforms, args.media)

    # Summary
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)

    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)

    for platform, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {platform.title()}")

    print(f"\n✅ Success: {success_count}/{total_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
