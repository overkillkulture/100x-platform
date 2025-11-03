"""
🎬 YOUTUBE AUTO-UPLOADER
Free YouTube API integration for automated video uploads
"""

import os
import pickle
from pathlib import Path
from typing import Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class YouTubeUploader:
    """YouTube API wrapper for automated video uploads"""

    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    def __init__(self, credentials_file: str = None):
        """Initialize YouTube uploader"""
        self.credentials_file = credentials_file or 'youtube_client_secrets.json'
        self.token_file = 'youtube_token.pickle'
        self.youtube = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds = None

        # Load saved credentials
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"\n⚠️  YouTube credentials file not found!")
                    print("\nTo set up:")
                    print("1. Go to: https://console.cloud.google.com/")
                    print("2. Create project → Enable YouTube Data API v3")
                    print("3. Create OAuth 2.0 credentials")
                    print("4. Download as 'youtube_client_secrets.json'")
                    return

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file,
                    self.SCOPES
                )
                creds = flow.run_local_server(port=8080)

            # Save credentials
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.youtube = build('youtube', 'v3', credentials=creds)
        print("✅ YouTube API authenticated")

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list = None,
        category_id: str = '22',  # People & Blogs
        privacy_status: str = 'public'
    ) -> Dict:
        """Upload video to YouTube"""

        if not self.youtube:
            raise Exception("YouTube API not authenticated")

        print(f"\n🎬 Uploading to YouTube: {title}")

        # Default tags
        if tags is None:
            tags = [
                'consciousness revolution',
                '100x builder',
                'automation',
                'AI',
                'web development'
            ]

        # Video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        # Upload video file
        media = MediaFileUpload(
            video_path,
            chunksize=1024*1024,  # 1MB chunks
            resumable=True
        )

        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        print("📤 Uploading...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"   Upload progress: {progress}%", end='\r')

        print("\n✅ Upload complete!")

        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"\n🔗 Video URL: {video_url}")

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'status': 'uploaded'
        }

    def upload_with_thumbnail(
        self,
        video_path: str,
        thumbnail_path: str,
        title: str,
        description: str,
        **kwargs
    ) -> Dict:
        """Upload video with custom thumbnail"""

        # Upload video first
        result = self.upload_video(video_path, title, description, **kwargs)

        # Upload thumbnail
        self.youtube.thumbnails().set(
            videoId=result['id'],
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()

        print("✅ Thumbnail uploaded")

        return result

    def get_video_analytics(self, video_id: str) -> Dict:
        """Get basic video statistics"""

        response = self.youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        if response['items']:
            stats = response['items'][0]['statistics']
            return {
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0))
            }

        return None


def test_youtube_uploader():
    """Test YouTube uploader with demo video"""
    try:
        uploader = YouTubeUploader()

        # Test video
        video_path = "C:/Users/dwrek/SOCIAL_VIDEOS/twitter_linkedin.mp4"

        title = "Consciousness Revolution - 7 Sacred Domains Platform Demo"

        description = """
        🌌 Welcome to the Consciousness Revolution!

        Explore 7 Sacred Domains of consciousness-elevating tools:
        • Education - Learn and grow
        • Social - Connect with builders
        • Music - Consciousness frequencies
        • Crypto - Financial freedom
        • Games - Interactive learning
        • And more!

        127 automation modules
        50+ active builders
        Zero coding required

        🔗 Try it now: https://conciousnessrevolution.io

        #ConsciousnessRevolution #100XBuilder #Automation #AI #WebDevelopment
        """

        tags = [
            'consciousness revolution',
            '100x builder',
            'automation',
            'AI tools',
            'web development',
            'no code',
            'builder tools',
            'productivity'
        ]

        # Upload
        result = uploader.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status='public'
        )

        print("\n" + "="*70)
        print("✅ YOUTUBE UPLOAD SUCCESSFUL!")
        print("="*70)
        print(f"\nVideo ID: {result['id']}")
        print(f"URL: {result['url']}")

        # Save result
        import json
        with open('youtube_upload_result.json', 'w') as f:
            json.dump(result, f, indent=2)

        return result

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nMake sure youtube_client_secrets.json is in the directory")
        return None


if __name__ == '__main__':
    print("🎬 YOUTUBE AUTO-UPLOADER TEST")
    print("="*70)

    # Check for credentials file
    if os.path.exists('youtube_client_secrets.json'):
        test_youtube_uploader()
    else:
        print("\n⚠️  YouTube credentials not set up yet!")
        print("\nSetup steps:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create new project: 'Consciousness Revolution'")
        print("3. Enable 'YouTube Data API v3'")
        print("4. Create OAuth 2.0 Client ID (Desktop app)")
        print("5. Download JSON and save as 'youtube_client_secrets.json'")
        print("\nThen run this script again!")
