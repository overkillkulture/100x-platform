"""
🎬 SIMPLE BUT POWERFUL VIDEO CONVERTER 🎬

Converts .webm to platform-ready MP4s with:
- Instagram (1:1 square)
- TikTok/Reels (9:16 vertical)
- Twitter/LinkedIn (16:9)
"""

from moviepy import VideoFileClip, AudioFileClip
from gtts import gTTS
import os

def convert_for_instagram_feed(input_file, output_file="instagram_feed.mp4"):
    """Convert to Instagram Feed format (1:1 square, 1080x1080)"""
    print("📱 Creating Instagram Feed video (1:1)...")

    clip = VideoFileClip(input_file)

    # Resize and crop to 1080x1080 square
    target_w, target_h = 1080, 1080

    # Scale to fill
    scale = max(target_w / clip.w, target_h / clip.h)
    clip = clip.with_effects([vfx.Resize(scale)])

    # Crop to square
    clip = clip.with_effects([vfx.Crop(
        x_center=clip.w/2,
        y_center=clip.h/2,
        width=target_w,
        height=target_h
    )])

    # Limit to 60 seconds
    if clip.duration > 60:
        clip = clip.with_subclip(0, 60)

    clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=30, bitrate='3000k')
    print(f"✅ Instagram Feed ready: {output_file}")
    return output_file


def convert_for_reels_tiktok(input_file, output_file="reels_tiktok.mp4", add_voice=True):
    """Convert to Instagram Reels/TikTok format (9:16 vertical)"""
    print("📱 Creating Reels/TikTok video (9:16)...")

    clip = VideoFileClip(input_file)

    # Resize and crop to 1080x1920 vertical
    target_w, target_h = 1080, 1920

    # Scale to fill
    scale = max(target_w / clip.w, target_h / clip.h)
    clip = clip.with_effects([vfx.Resize(scale)])

    # Crop to vertical
    clip = clip.with_effects([vfx.Crop(
        x_center=clip.w/2,
        y_center=clip.h/2,
        width=target_w,
        height=target_h
    )])

    # Limit to 90 seconds
    if clip.duration > 90:
        clip = clip.with_subclip(0, 90)

    # Add voice narration
    if add_voice:
        narration = """
        Welcome to the Consciousness Revolution.
        Seven sacred domains of consciousness-elevating tools.
        Education. Social. Music. Crypto. Games.
        One hundred twenty-seven modules.
        Fifty plus builders.
        Join today at consciousness revolution dot io.
        """

        print("🎤 Adding AI voice...")
        tts = gTTS(text=narration, lang='en', slow=False)
        tts.save("temp_voice.mp3")

        audio = AudioFileClip("temp_voice.mp3")
        clip = clip.with_audio(audio)

        os.remove("temp_voice.mp3")

    clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=30, bitrate='4000k')
    print(f"✅ Reels/TikTok ready: {output_file}")
    return output_file


def convert_for_twitter_linkedin(input_file, output_file="twitter_linkedin.mp4"):
    """Convert to Twitter/LinkedIn format (16:9, 1280x720)"""
    print("💼 Creating Twitter/LinkedIn video (16:9)...")

    clip = VideoFileClip(input_file)

    # Resize to 1280x720
    clip = clip.with_effects([vfx.Resize(height=720)])

    # Crop if needed
    if clip.w > 1280:
        clip = clip.with_effects([vfx.Crop(
            x_center=clip.w/2,
            width=1280,
            height=720
        )])

    clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=30, bitrate='2500k')
    print(f"✅ Twitter/LinkedIn ready: {output_file}")
    return output_file


def convert_all(input_file, output_dir="C:/Users/dwrek/SOCIAL_VIDEOS"):
    """Convert to all platforms at once!"""
    os.makedirs(output_dir, exist_ok=True)

    print("="*70)
    print("🚀 CONVERTING TO ALL PLATFORMS")
    print("="*70)
    print(f"Input: {input_file}\n")

    results = {}

    try:
        # Instagram Feed
        results['instagram'] = convert_for_instagram_feed(
            input_file,
            f"{output_dir}/instagram_feed.mp4"
        )
    except Exception as e:
        print(f"❌ Instagram failed: {e}")

    try:
        # Reels/TikTok with voice
        results['reels'] = convert_for_reels_tiktok(
            input_file,
            f"{output_dir}/reels_tiktok.mp4",
            add_voice=True
        )
    except Exception as e:
        print(f"❌ Reels/TikTok failed: {e}")

    try:
        # Twitter/LinkedIn
        results['twitter'] = convert_for_twitter_linkedin(
            input_file,
            f"{output_dir}/twitter_linkedin.mp4"
        )
    except Exception as e:
        print(f"❌ Twitter/LinkedIn failed: {e}")

    print("\n" + "="*70)
    print("✅ CONVERSION COMPLETE!")
    print("="*70)

    for platform, path in results.items():
        if path and os.path.exists(path):
            size_mb = os.path.getsize(path) / 1024 / 1024
            print(f"✅ {platform:15s} → {size_mb:5.1f} MB - {path}")

    print(f"\n📁 All videos in: {output_dir}")
    print("\n🚀 READY TO POST!")

    return results


if __name__ == "__main__":
    # Input video
    input_video = "C:/Users/dwrek/TUTORIAL_VIDEOS/7_DOMAINS_INSTAGRAM_DEMO.webm"

    # Convert to all platforms
    convert_all(input_video)

    print("\n" + "="*70)
    print("🎉 SOCIAL MEDIA PACKAGE READY!")
    print("="*70)
    print("\nYou have:")
    print("  📱 Instagram Feed (1:1 square, 1080x1080)")
    print("  📱 Reels/TikTok (9:16 vertical, 1080x1920) + AI VOICE")
    print("  💼 Twitter/LinkedIn (16:9, 1280x720)")
    print("\nAll optimized and ready to upload! 🚀")
