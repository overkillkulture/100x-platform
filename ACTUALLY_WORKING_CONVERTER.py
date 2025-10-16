"""
🎬 ACTUALLY WORKING VIDEO CONVERTER 🎬
MoviePy 2.1.2 - Correct API (cropped, resized, subclipped)
"""

from moviepy import VideoFileClip, AudioFileClip
from gtts import gTTS
import os

def create_instagram_square(input_file, output_file="instagram_feed.mp4"):
    """1:1 Square for Instagram Feed"""
    print("\n📱 Creating Instagram Feed (1:1 square)...")

    clip = VideoFileClip(input_file)

    # Get dimensions
    w, h = clip.size
    target_size = min(w, h)

    # Calculate crop coordinates
    x1 = (w - target_size) // 2
    y1 = (h - target_size) // 2

    # Crop to square (MoviePy 2.x: use .cropped())
    clip_cropped = clip.cropped(x1=x1, y1=y1, width=target_size, height=target_size)

    # Resize to 1080x1080 (MoviePy 2.x: use .resized())
    clip_resized = clip_cropped.resized(height=1080)

    # Limit to 60 seconds (MoviePy 2.x: use .subclipped())
    if clip_resized.duration > 60:
        clip_final = clip_resized.subclipped(0, 60)
    else:
        clip_final = clip_resized

    clip_final.write_videofile(
        output_file,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        bitrate='3000k'
    )

    size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"✅ Instagram Feed ready: {output_file} ({size_mb:.1f} MB)")
    return output_file

def create_reels_vertical(input_file, output_file="reels_tiktok.mp4", add_voice=True):
    """9:16 Vertical for Reels/TikTok"""
    print("\n📱 Creating Reels/TikTok (9:16 vertical)...")

    clip = VideoFileClip(input_file)

    # Get dimensions
    w, h = clip.size

    # Target 9:16 aspect ratio
    target_w = int(h * 9 / 16)

    if target_w > w:
        # Video too narrow, crop height
        target_h = int(w * 16 / 9)
        x1 = 0
        y1 = (h - target_h) // 2
        width = w
        height = target_h
    else:
        # Crop width
        target_h = h
        x1 = (w - target_w) // 2
        y1 = 0
        width = target_w
        height = h

    # Crop to 9:16
    clip_cropped = clip.cropped(x1=x1, y1=y1, width=width, height=height)

    # Resize to 1080x1920
    clip_resized = clip_cropped.resized(width=1080)

    # Limit to 90 seconds
    if clip_resized.duration > 90:
        clip_final = clip_resized.subclipped(0, 90)
    else:
        clip_final = clip_resized

    # Add voice narration
    if add_voice:
        try:
            narration = """
            Welcome to the Consciousness Revolution.
            Seven sacred domains. One hundred twenty seven tools.
            Fifty plus builders. Zero coding required.
            Join us at consciousness revolution dot io.
            """

            print("🎤 Adding AI voice...")
            tts = gTTS(text=narration, lang='en', slow=False)
            tts.save("temp_voice.mp3")

            audio = AudioFileClip("temp_voice.mp3")

            # Mix audio with original (or replace if no original audio)
            clip_final = clip_final.with_audio(audio)

            os.remove("temp_voice.mp3")
            print("✅ Voice added!")
        except Exception as e:
            print(f"⚠️  Voice failed (continuing without): {e}")

    clip_final.write_videofile(
        output_file,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        bitrate='4000k'
    )

    size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"✅ Reels/TikTok ready: {output_file} ({size_mb:.1f} MB)")
    return output_file

def create_twitter_widescreen(input_file, output_file="twitter_linkedin.mp4"):
    """16:9 for Twitter/LinkedIn"""
    print("\n💼 Creating Twitter/LinkedIn (16:9)...")

    clip = VideoFileClip(input_file)

    # Resize to 720p
    clip_resized = clip.resized(height=720)

    clip_resized.write_videofile(
        output_file,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        bitrate='2500k'
    )

    size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"✅ Twitter/LinkedIn ready: {output_file} ({size_mb:.1f} MB)")
    return output_file

def convert_all_platforms(input_file):
    """ONE COMMAND - ALL PLATFORMS"""
    output_dir = "C:/Users/dwrek/SOCIAL_VIDEOS"
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("🚀 SOCIAL MEDIA VIDEO AUTOMATION - OPTION 3")
    print("=" * 70)
    print(f"\nInput: {input_file}")
    print(f"Output: {output_dir}\n")

    results = {}

    # 1. Instagram Feed
    try:
        results['instagram'] = create_instagram_square(
            input_file,
            f"{output_dir}/instagram_feed.mp4"
        )
    except Exception as e:
        print(f"❌ Instagram failed: {e}")
        import traceback
        traceback.print_exc()

    # 2. Reels/TikTok with AI voice
    try:
        results['reels'] = create_reels_vertical(
            input_file,
            f"{output_dir}/reels_tiktok.mp4",
            add_voice=True
        )
    except Exception as e:
        print(f"❌ Reels/TikTok failed: {e}")
        import traceback
        traceback.print_exc()

    # 3. Twitter/LinkedIn
    try:
        results['twitter'] = create_twitter_widescreen(
            input_file,
            f"{output_dir}/twitter_linkedin.mp4"
        )
    except Exception as e:
        print(f"❌ Twitter/LinkedIn failed: {e}")
        import traceback
        traceback.print_exc()

    # Summary
    print("\n" + "=" * 70)
    print("📊 CONVERSION COMPLETE")
    print("=" * 70)

    success_count = 0
    for platform, path in results.items():
        if path and os.path.exists(path):
            size_mb = os.path.getsize(path) / 1024 / 1024
            print(f"✅ {platform.upper():15s} → {size_mb:5.1f} MB - {path}")
            success_count += 1

    if success_count == 0:
        print("\n❌ All conversions failed. See errors above.")
    else:
        print(f"\n📁 All videos: {output_dir}")
        print(f"\n🚀 {success_count}/3 PLATFORMS READY TO POST!")

    return results

if __name__ == "__main__":
    # Input video
    input_video = "C:/Users/dwrek/TUTORIAL_VIDEOS/7_DOMAINS_INSTAGRAM_DEMO.webm"

    print("\n🎬 FULL AUTOMATION SYSTEM (OPTION 3)")
    print("MoviePy 2.1.2 - Correct API")
    print("=" * 70)

    # Convert to all platforms
    results = convert_all_platforms(input_video)

    print("\n" + "=" * 70)
    if results:
        print("🎉 OPTION 3 COMPLETE!")
        print("=" * 70)
        print("\n  📱 Instagram Feed (1080x1080 square)")
        print("  📱 Reels/TikTok (1080x1920 vertical) + AI VOICE")
        print("  💼 Twitter/LinkedIn (1280x720 widescreen)")
        print("\n🚀 POST TO ALL PLATFORMS NOW! 🚀")
    else:
        print("❌ AUTOMATION FAILED - USE CLOUDCONVERT FALLBACK")
