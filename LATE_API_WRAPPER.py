"""
🚀 LATE API WRAPPER - Multi-Platform Social Media Posting
Supports: TikTok, LinkedIn, Facebook, Threads, Instagram (limited)
"""

import requests
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

class LateAPI:
    """Late API wrapper for social media automation"""

    def __init__(self, api_key: str = None):
        """Initialize Late API client"""
        self.api_key = api_key or os.getenv('LATE_API_KEY')
        if not self.api_key:
            raise ValueError("Late API key not found. Set LATE_API_KEY environment variable.")

        self.base_url = "https://api.getlate.dev/v1"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def upload_media(self, file_path: str) -> str:
        """Upload media file to Late and get URL"""
        print(f"📤 Uploading media: {file_path}")

        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f'{self.base_url}/media',
                headers={'Authorization': f'Bearer {self.api_key}'},
                files=files
            )

        if response.status_code == 200:
            media_url = response.json()['url']
            print(f"✅ Media uploaded: {media_url}")
            return media_url
        else:
            raise Exception(f"Upload failed: {response.text}")

    def create_post(
        self,
        platforms: List[str],
        media_url: str,
        caption: str,
        schedule_time: Optional[str] = None
    ) -> Dict:
        """Create post on specified platforms"""

        print(f"\n📱 Posting to: {', '.join(platforms)}")

        payload = {
            'platforms': platforms,
            'mediaUrl': media_url,
            'caption': caption
        }

        if schedule_time:
            payload['scheduledAt'] = schedule_time

        response = requests.post(
            f'{self.base_url}/posts',
            headers=self.headers,
            json=payload
        )

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Posted successfully!")
            return result
        else:
            raise Exception(f"Post failed: {response.text}")

    def post_to_tiktok(self, video_path: str, caption: str) -> Dict:
        """Post video to TikTok"""
        print("\n🎵 Posting to TikTok...")
        media_url = self.upload_media(video_path)
        return self.create_post(['tiktok'], media_url, caption)

    def post_to_linkedin(self, video_path: str, caption: str) -> Dict:
        """Post video to LinkedIn"""
        print("\n💼 Posting to LinkedIn...")
        media_url = self.upload_media(video_path)
        return self.create_post(['linkedin'], media_url, caption)

    def post_to_facebook(self, video_path: str, caption: str) -> Dict:
        """Post video to Facebook"""
        print("\n👥 Posting to Facebook...")
        media_url = self.upload_media(video_path)
        return self.create_post(['facebook'], media_url, caption)

    def post_to_threads(self, video_path: str, caption: str) -> Dict:
        """Post video to Threads"""
        print("\n🧵 Posting to Threads...")
        media_url = self.upload_media(video_path)
        return self.create_post(['threads'], media_url, caption)

    def post_to_all(self, video_path: str, caption: str) -> Dict:
        """Post to all supported platforms"""
        print("\n🚀 POSTING TO ALL LATE PLATFORMS...")
        media_url = self.upload_media(video_path)
        platforms = ['tiktok', 'linkedin', 'facebook', 'threads']
        return self.create_post(platforms, media_url, caption)

    def get_post_analytics(self, post_id: str) -> Dict:
        """Get analytics for a specific post"""
        response = requests.get(
            f'{self.base_url}/posts/{post_id}/analytics',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Analytics fetch failed: {response.text}")

    def get_all_posts(self, limit: int = 10) -> List[Dict]:
        """Get recent posts"""
        response = requests.get(
            f'{self.base_url}/posts?limit={limit}',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['posts']
        else:
            raise Exception(f"Failed to fetch posts: {response.text}")


def test_late_api():
    """Test Late API with sample video"""
    try:
        late = LateAPI()

        # Test with demo video
        video_path = "C:/Users/dwrek/SOCIAL_VIDEOS/reels_tiktok.mp4"
        caption = """
        🌌 The playground is OPEN 🌌

        7 Sacred Domains of consciousness-elevating tools.
        127 automation modules | 50+ builders

        → conciousnessrevolution.io

        #ConsciousnessRevolution #100XBuilder #AI
        """

        # Post to all platforms
        result = late.post_to_all(video_path, caption)

        print("\n" + "="*70)
        print("✅ LATE API TEST SUCCESSFUL!")
        print("="*70)
        print(f"\nPost ID: {result.get('id')}")
        print(f"Platforms: {result.get('platforms')}")
        print(f"Status: {result.get('status')}")

        # Save result
        with open('late_api_test_result.json', 'w') as f:
            json.dump(result, f, indent=2)

        return result

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n⚠️  Make sure LATE_API_KEY is set in environment variables")
        return None


if __name__ == '__main__':
    print("🚀 LATE API WRAPPER TEST")
    print("="*70)

    # Check if API key exists
    if os.getenv('LATE_API_KEY'):
        test_late_api()
    else:
        print("\n⚠️  LATE_API_KEY not found!")
        print("\nTo set it up:")
        print("1. Get API key from Late dashboard")
        print("2. Run: setx LATE_API_KEY \"your_key_here\"")
        print("3. Restart terminal and run this script again")
