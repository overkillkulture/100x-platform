"""
🚀 ULTIMATE SOCIAL MEDIA POSTER
One command to post to ALL platforms!
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Import our modules
from LATE_API_WRAPPER import LateAPI
from YOUTUBE_UPLOADER import YouTubeUploader
from TWITTER_PLAYWRIGHT_POSTER import TwitterPoster
from INSTAGRAM_HELPER import InstagramHelper


class UltimateSocialPoster:
    """Post to all social media platforms with one command"""

    def __init__(self):
        """Initialize all platform integrations"""
        self.late_api = None
        self.youtube = None
        self.twitter = None
        self.instagram = InstagramHelper()

        # Try to initialize APIs
        self._init_apis()

    def _init_apis(self):
        """Initialize available APIs"""
        # Late API
        if os.getenv('LATE_API_KEY'):
            try:
                self.late_api = LateAPI()
                print("✅ Late API initialized (TikTok, LinkedIn, Facebook)")
            except:
                print("⚠️  Late API failed to initialize")

        # YouTube API
        if Path('youtube_client_secrets.json').exists():
            try:
                self.youtube = YouTubeUploader()
                print("✅ YouTube API initialized")
            except:
                print("⚠️  YouTube API failed to initialize")

        # Twitter
        if Path('./twitter_session').exists():
            try:
                self.twitter = TwitterPoster()
                print("✅ Twitter session ready")
            except:
                print("⚠️  Twitter session failed")

        # Instagram always available (semi-auto)
        print("✅ Instagram helper ready (semi-auto)")

    def post_to_all(
        self,
        video_path: str,
        caption: str,
        platforms: List[str] = None,
        youtube_title: str = None
    ) -> Dict:
        """Post to all specified platforms"""

        if platforms is None or 'all' in platforms:
            platforms = ['tiktok', 'linkedin', 'facebook', 'youtube', 'twitter', 'instagram']

        print("\n" + "="*70)
        print(f"🚀 POSTING TO {len(platforms)} PLATFORMS")
        print("="*70)

        results = {
            'timestamp': datetime.now().isoformat(),
            'video': video_path,
            'caption': caption,
            'platforms': {}
        }

        # Late API platforms (TikTok, LinkedIn, Facebook)
        late_platforms = [p for p in platforms if p in ['tiktok', 'linkedin', 'facebook']]
        if late_platforms and self.late_api:
            try:
                print(f"\n📱 Posting to Late platforms: {', '.join(late_platforms)}")
                late_result = self.late_api.post_to_all(video_path, caption)
                for platform in late_platforms:
                    results['platforms'][platform] = {
                        'status': 'success',
                        'post_id': late_result.get('id'),
                        'method': 'late_api'
                    }
                print(f"✅ Posted to {len(late_platforms)} platforms via Late API")
            except Exception as e:
                print(f"❌ Late API error: {e}")
                for platform in late_platforms:
                    results['platforms'][platform] = {'status': 'failed', 'error': str(e)}

        # YouTube
        if 'youtube' in platforms and self.youtube:
            try:
                print("\n🎬 Posting to YouTube...")
                yt_title = youtube_title or caption[:100]
                yt_result = self.youtube.upload_video(
                    video_path=video_path,
                    title=yt_title,
                    description=caption
                )
                results['platforms']['youtube'] = {
                    'status': 'success',
                    'url': yt_result['url'],
                    'video_id': yt_result['id'],
                    'method': 'youtube_api'
                }
                print(f"✅ Posted to YouTube: {yt_result['url']}")
            except Exception as e:
                print(f"❌ YouTube error: {e}")
                results['platforms']['youtube'] = {'status': 'failed', 'error': str(e)}

        # Twitter
        if 'twitter' in platforms and self.twitter:
            try:
                print("\n🐦 Posting to Twitter...")
                twitter_result = self.twitter.post_video(video_path, caption, headless=True)
                results['platforms']['twitter'] = {
                    'status': 'success',
                    'url': twitter_result['url'],
                    'method': 'playwright'
                }
                print(f"✅ Posted to Twitter: {twitter_result['url']}")
            except Exception as e:
                print(f"❌ Twitter error: {e}")
                results['platforms']['twitter'] = {'status': 'failed', 'error': str(e)}

        # Instagram (semi-auto)
        if 'instagram' in platforms:
            try:
                print("\n📱 Instagram helper (semi-automated)...")
                ig_result = self.instagram.prepare_for_instagram(video_path, caption)
                results['platforms']['instagram'] = {
                    'status': 'posted' if ig_result['posted'] else 'pending',
                    'transfer_path': ig_result['transfer_path'],
                    'method': 'semi_auto'
                }
            except Exception as e:
                print(f"❌ Instagram error: {e}")
                results['platforms']['instagram'] = {'status': 'failed', 'error': str(e)}

        # Save results
        results_file = f"posting_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        # Summary
        print("\n" + "="*70)
        print("📊 POSTING SUMMARY")
        print("="*70)

        success_count = sum(1 for p in results['platforms'].values() if p['status'] in ['success', 'posted'])
        print(f"\n✅ Successfully posted to {success_count}/{len(platforms)} platforms")

        for platform, result in results['platforms'].items():
            status_emoji = "✅" if result['status'] in ['success', 'posted'] else "❌"
            print(f"   {status_emoji} {platform.upper()}: {result['status']}")

        print(f"\n📄 Results saved: {results_file}")

        return results

    def post_with_different_videos(
        self,
        videos: Dict[str, str],
        caption: str
    ) -> Dict:
        """Post different video formats to different platforms"""

        print("\n🎬 POSTING WITH PLATFORM-SPECIFIC VIDEOS")

        results = {}

        # TikTok/Reels vertical video
        if 'reels' in videos and self.late_api:
            try:
                late_result = self.late_api.post_to_tiktok(videos['reels'], caption)
                results['tiktok'] = {'status': 'success', 'post_id': late_result.get('id')}
            except Exception as e:
                results['tiktok'] = {'status': 'failed', 'error': str(e)}

        # LinkedIn/Twitter widescreen video
        if 'widescreen' in videos:
            if self.late_api:
                try:
                    late_result = self.late_api.post_to_linkedin(videos['widescreen'], caption)
                    results['linkedin'] = {'status': 'success', 'post_id': late_result.get('id')}
                except Exception as e:
                    results['linkedin'] = {'status': 'failed', 'error': str(e)}

            if self.twitter:
                try:
                    twitter_result = self.twitter.post_video(videos['widescreen'], caption)
                    results['twitter'] = {'status': 'success', 'url': twitter_result['url']}
                except Exception as e:
                    results['twitter'] = {'status': 'failed', 'error': str(e)}

        # Instagram square video
        if 'square' in videos:
            try:
                ig_result = self.instagram.prepare_for_instagram(videos['square'], caption)
                results['instagram'] = {
                    'status': 'posted' if ig_result['posted'] else 'pending',
                    'transfer_path': ig_result['transfer_path']
                }
            except Exception as e:
                results['instagram'] = {'status': 'failed', 'error': str(e)}

        return results


def main():
    """CLI interface for ultimate social poster"""

    parser = argparse.ArgumentParser(
        description='🚀 Ultimate Social Media Poster - Post to all platforms with one command'
    )

    parser.add_argument('video', help='Path to video file')
    parser.add_argument('--caption', required=True, help='Caption/description for post')
    parser.add_argument('--platforms', nargs='+', default=['all'],
                       help='Platforms to post to (default: all)')
    parser.add_argument('--youtube-title', help='Custom YouTube title (default: caption)')
    parser.add_argument('--use-optimized', action='store_true',
                       help='Use platform-optimized videos from SOCIAL_VIDEOS folder')

    args = parser.parse_args()

    poster = UltimateSocialPoster()

    if args.use_optimized:
        # Use platform-specific videos
        videos = {
            'square': 'C:/Users/dwrek/SOCIAL_VIDEOS/instagram_feed.mp4',
            'reels': 'C:/Users/dwrek/SOCIAL_VIDEOS/reels_tiktok.mp4',
            'widescreen': 'C:/Users/dwrek/SOCIAL_VIDEOS/twitter_linkedin.mp4'
        }
        results = poster.post_with_different_videos(videos, args.caption)
    else:
        # Use single video for all platforms
        results = poster.post_to_all(
            video_path=args.video,
            caption=args.caption,
            platforms=args.platforms,
            youtube_title=args.youtube_title
        )

    print("\n✅ POSTING COMPLETE!")

    return results


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("\n🚀 ULTIMATE SOCIAL MEDIA POSTER")
        print("="*70)
        print("\nUsage:")
        print("  python ULTIMATE_SOCIAL_POSTER.py <video> --caption \"Your caption\"")
        print("\nExamples:")
        print("  # Post to all platforms:")
        print("  python ULTIMATE_SOCIAL_POSTER.py video.mp4 --caption \"Check this out!\"")
        print("\n  # Post to specific platforms:")
        print("  python ULTIMATE_SOCIAL_POSTER.py video.mp4 --caption \"...\" --platforms tiktok linkedin")
        print("\n  # Use platform-optimized videos:")
        print("  python ULTIMATE_SOCIAL_POSTER.py dummy.mp4 --caption \"...\" --use-optimized")
        print("\n")
    else:
        main()
