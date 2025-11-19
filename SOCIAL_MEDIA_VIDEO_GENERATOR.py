"""
🎬 ULTIMATE SOCIAL MEDIA VIDEO GENERATOR 🎬

One command creates perfect videos for ANY platform:
- Instagram Feed (1:1 square)
- Instagram Reels (9:16 vertical)
- TikTok (9:16 vertical)
- LinkedIn (16:9 professional)
- Twitter/X (16:9)
- YouTube Shorts (9:16)

With:
- Text overlays
- AI voice narration
- Perfect compression
- Platform-specific formatting
"""

from moviepy import *
from gtts import gTTS
import os
from pathlib import Path

class SocialMediaVideoGenerator:

    PLATFORM_SPECS = {
        'instagram_feed': {
            'aspect_ratio': '1:1',
            'width': 1080,
            'height': 1080,
            'max_duration': 60,
            'max_size_mb': 30,
            'format': 'mp4'
        },
        'instagram_reels': {
            'aspect_ratio': '9:16',
            'width': 1080,
            'height': 1920,
            'max_duration': 90,
            'max_size_mb': 50,
            'format': 'mp4'
        },
        'tiktok': {
            'aspect_ratio': '9:16',
            'width': 1080,
            'height': 1920,
            'max_duration': 180,
            'max_size_mb': 72,
            'format': 'mp4'
        },
        'linkedin': {
            'aspect_ratio': '16:9',
            'width': 1920,
            'height': 1080,
            'max_duration': 600,
            'max_size_mb': 200,
            'format': 'mp4'
        },
        'twitter': {
            'aspect_ratio': '16:9',
            'width': 1280,
            'height': 720,
            'max_duration': 140,
            'max_size_mb': 512,
            'format': 'mp4'
        },
        'youtube_shorts': {
            'aspect_ratio': '9:16',
            'width': 1080,
            'height': 1920,
            'max_duration': 60,
            'max_size_mb': 256,
            'format': 'mp4'
        }
    }

    def __init__(self, input_video):
        self.input_video = input_video
        self.base_clip = VideoFileClip(input_video)
        print(f"✅ Loaded video: {input_video}")
        print(f"   Duration: {self.base_clip.duration:.1f}s")
        print(f"   Size: {self.base_clip.size}")

    def add_text_overlays(self, scenes):
        """Add text overlays at specific timestamps"""
        clips = [self.base_clip]

        for start, end, text in scenes:
            txt = TextClip(
                text=text,
                font_size=70,
                color='white',
                font='C:/Windows/Fonts/arialbd.ttf',  # Arial Bold from Windows fonts
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(self.base_clip.w - 100, None)
            )
            txt = txt.with_position(('center', 100)).with_start(start).with_end(end)
            clips.append(txt)

        return CompositeVideoClip(clips)

    def add_voice_narration(self, video_clip, narration_text, voice='en'):
        """Add AI-generated voice narration"""
        print("🎤 Generating voice narration...")

        # Generate speech
        tts = gTTS(text=narration_text, lang=voice, slow=False)
        audio_path = "temp_narration.mp3"
        tts.save(audio_path)

        # Load audio
        audio = AudioFileClip(audio_path)

        # Set audio to video
        video_with_audio = video_clip.set_audio(audio)

        # Clean up
        os.remove(audio_path)

        return video_with_audio

    def format_for_platform(self, video_clip, platform):
        """Resize and crop for specific platform"""
        specs = self.PLATFORM_SPECS[platform]
        target_w = specs['width']
        target_h = specs['height']

        print(f"📐 Formatting for {platform} ({specs['aspect_ratio']})...")

        # Calculate scaling
        scale_w = target_w / video_clip.w
        scale_h = target_h / video_clip.h
        scale = max(scale_w, scale_h)

        # Resize
        resized = video_clip.resize(scale)

        # Crop to exact dimensions
        if resized.w > target_w or resized.h > target_h:
            x_center = resized.w / 2
            y_center = resized.h / 2

            formatted = resized.crop(
                x_center=x_center,
                y_center=y_center,
                width=target_w,
                height=target_h
            )
        else:
            formatted = resized

        # Trim duration if needed
        max_duration = specs['max_duration']
        if formatted.duration > max_duration:
            formatted = formatted.subclip(0, max_duration)

        return formatted

    def export(self, video_clip, output_path, platform):
        """Export with optimal settings for platform"""
        specs = self.PLATFORM_SPECS[platform]

        # Calculate bitrate for target file size
        target_size_mb = specs['max_size_mb'] * 0.8  # Use 80% of max
        target_size_bytes = target_size_mb * 1024 * 1024
        duration = video_clip.duration
        bitrate = int((target_size_bytes * 8) / duration)  # bits per second

        print(f"💾 Exporting {platform} video...")
        print(f"   Target size: {target_size_mb:.1f} MB")
        print(f"   Bitrate: {bitrate/1000:.0f} kbps")

        video_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30,
            bitrate=f"{bitrate}",
            preset='medium',
            threads=4
        )

        # Check actual file size
        actual_size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"✅ Exported: {output_path}")
        print(f"   Actual size: {actual_size_mb:.1f} MB")

        return output_path

    def create_for_platform(self, platform, scenes, narration=None, output_dir="SOCIAL_VIDEOS"):
        """Complete pipeline for one platform"""
        print(f"\n{'='*60}")
        print(f"🎬 CREATING {platform.upper()} VIDEO")
        print(f"{'='*60}\n")

        # Start with base clip
        video = self.base_clip.copy()

        # Add text overlays
        if scenes:
            print("📝 Adding text overlays...")
            video = self.add_text_overlays(scenes)

        # Add voice narration
        if narration:
            video = self.add_voice_narration(video, narration)

        # Format for platform
        video = self.format_for_platform(video, platform)

        # Export
        Path(output_dir).mkdir(exist_ok=True)
        output_path = f"{output_dir}/{platform}_ready.mp4"
        self.export(video, output_path, platform)

        return output_path


def generate_all_platforms(input_video, output_dir="C:/Users/dwrek/SOCIAL_VIDEOS"):
    """
    ONE COMMAND TO GENERATE ALL PLATFORM VIDEOS!
    """

    print("="*70)
    print("🚀 SOCIAL MEDIA VIDEO GENERATOR - FULL AUTOMATION MODE 🚀")
    print("="*70)

    # Text overlays for 7 domains video
    scenes = [
        (0, 10, "🌌 100X BUILDER PLATFORM"),
        (10, 22, "✨ SEVEN SACRED DOMAINS"),
        (22, 34, "📚 EDUCATION DOMAIN"),
        (34, 46, "💬 SOCIAL DOMAIN"),
        (46, 58, "🎵 MUSIC DOMAIN"),
        (58, 70, "₿ CRYPTO DOMAIN"),
        (70, 82, "🎮 GAMES DOMAIN"),
        (82, 90, "🚀 EXPLORE NOW")
    ]

    # Voice narration script
    narration = """
    Welcome to the Consciousness Revolution.
    A platform with seven sacred domains of consciousness-elevating tools.
    Education. Social. Music. Crypto. Games. And more.
    One hundred twenty-seven automation modules.
    Fifty plus active builders.
    Zero coding required.
    Join the revolution today at consciousness revolution dot io.
    """

    # Initialize generator
    generator = SocialMediaVideoGenerator(input_video)

    # Generate for each platform
    platforms_to_generate = [
        'instagram_feed',     # 1:1 square
        'instagram_reels',    # 9:16 vertical
        'tiktok',            # 9:16 vertical
        'linkedin',          # 16:9 professional
        'twitter',           # 16:9
        'youtube_shorts'     # 9:16 vertical
    ]

    results = {}

    for platform in platforms_to_generate:
        try:
            output_path = generator.create_for_platform(
                platform=platform,
                scenes=scenes,
                narration=narration if platform in ['instagram_reels', 'tiktok', 'youtube_shorts'] else None,
                output_dir=output_dir
            )
            results[platform] = output_path
            print(f"✅ {platform}: SUCCESS")
        except Exception as e:
            print(f"❌ {platform}: FAILED - {e}")
            results[platform] = None

    # Summary
    print("\n" + "="*70)
    print("📊 GENERATION COMPLETE - SUMMARY")
    print("="*70)

    for platform, path in results.items():
        if path:
            size_mb = os.path.getsize(path) / 1024 / 1024
            print(f"✅ {platform:20s} → {size_mb:5.1f} MB - {path}")
        else:
            print(f"❌ {platform:20s} → FAILED")

    print(f"\n📁 All videos saved to: {output_dir}")
    print("\n🚀 READY TO POST TO ALL PLATFORMS!")

    return results


if __name__ == "__main__":
    # Input video
    input_video = "C:/Users/dwrek/TUTORIAL_VIDEOS/7_DOMAINS_INSTAGRAM_DEMO.webm"

    # Output directory
    output_dir = "C:/Users/dwrek/SOCIAL_VIDEOS"

    # GENERATE EVERYTHING!
    results = generate_all_platforms(input_video, output_dir)

    print("\n" + "="*70)
    print("🎉 SOCIAL MEDIA DOMINATION PACKAGE READY! 🎉")
    print("="*70)
    print("\nYou now have:")
    print("  📱 Instagram Feed video (1:1)")
    print("  📱 Instagram Reels video (9:16) + voice")
    print("  📱 TikTok video (9:16) + voice")
    print("  💼 LinkedIn video (16:9)")
    print("  🐦 Twitter video (16:9)")
    print("  📺 YouTube Shorts (9:16) + voice")
    print("\nAll formatted, compressed, and ready to upload!")
    print("\n🚀 POST EVERYWHERE. DOMINATE SOCIAL MEDIA. 🚀")
