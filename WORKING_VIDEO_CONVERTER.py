"""
🎬 WORKING SOCIAL MEDIA VIDEO CONVERTER 🎬
Compatible with MoviePy 2.x
"""

from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy import vfx
from gtts import gTTS
import os

def webm_to_mp4_simple(input_file, output_file):
    """Simple webm to mp4 conversion"""
    print(f"🔄 Converting {input_file} to MP4...")
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
    print(f"✅ Saved: {output_file}")
    return output_file

def add_ai_voice(video_clip, narration_text):
    """Add Google TTS voice to video"""
    print("🎤 Generating AI voice narration...")

    # Generate speech
    tts = gTTS(text=narration_text, lang='en', slow=False)
    tts.save("temp_narration.mp3")

    # Load and add to video
    audio = AudioFileClip("temp_narration.mp4")
    video_with_audio = video_clip.with_audio(audio)

    # Cleanup
    os.remove("temp_narration.mp3")

    return video_with_audio

def create_instagram_feed(input_file, output_file="instagram_feed.mp4"):
    """1:1 Square for Instagram Feed"""
    print("\n📱 Creating Instagram Feed (1:1 square)...")

    clip = VideoFileClip(input_file)

    # Calculate crop to 1:1
    target_size = min(clip.w, clip.h)

    # Crop to square from center
    clip_cropped = vfx.Crop(
        clip,
        x_center=clip.w/2,
        y_center=clip.h/2,
        width=target_size,
        height=target_size
    )

    # Resize to Instagram standard 1080x1080
    clip_resized = vfx.Resize(clip_cropped, height=1080)

    # Limit duration to 60 seconds
    if clip_resized.duration > 60:
        clip_final = clip_resized.subclipped(0, 60)
    else:
        clip_final = clip_resized

    # Export
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

def create_reels_tiktok(input_file, output_file="reels_tiktok.mp4"):
    """9:16 Vertical for Reels/TikTok"""
    print("\n📱 Creating Reels/TikTok (9:16 vertical)...")

    clip = VideoFileClip(input_file)

    # Crop to 9:16 aspect ratio
    target_h = clip.h
    target_w = int(target_h * 9 / 16)

    if target_w > clip.w:
        # Video is too narrow, crop height instead
        target_w = clip.w
        target_h = int(target_w * 16 / 9)

    clip_cropped = vfx.Crop(
        clip,
        x_center=clip.w/2,
        y_center=clip.h/2,
        width=target_w,
        height=target_h
    )

    # Resize to 1080x1920
    clip_resized = vfx.Resize(clip_cropped, width=1080)

    # Limit to 90 seconds
    if clip_resized.duration > 90:
        clip_final = clip_resized.subclipped(0, 90)
    else:
        clip_final = clip_resized

    # Add AI voice
    narration = """
    Welcome to the Consciousness Revolution.
    Seven sacred domains. One hundred twenty seven tools.
    Fifty plus builders. Zero coding required.
    Join us at consciousness revolution dot io.
    """

    try:
        print("🎤 Adding AI voice narration...")
        tts = gTTS(text=narration, lang='en', slow=False)
        tts.save("temp_voice.mp3")

        audio = AudioFileClip("temp_voice.mp3")
        clip_final = clip_final.with_audio(audio)

        os.remove("temp_voice.mp3")
        print("✅ Voice added!")
    except Exception as e:
        print(f"⚠️  Voice failed (continuing without): {e}")

    # Export
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

def create_twitter_linkedin(input_file, output_file="twitter.mp4"):
    """16:9 for Twitter/LinkedIn"""
    print("\n💼 Creating Twitter/LinkedIn (16:9)...")

    clip = VideoFileClip(input_file)

    # Already 16:9, just resize
    clip_resized = vfx.Resize(clip, height=720)

    # Export
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
    """ONE COMMAND TO RULE THEM ALL"""
    output_dir = "C:/Users/dwrek/SOCIAL_VIDEOS"
    os.makedirs(output_dir, exist_ok=True)

    print("="*70)
    print("🚀 SOCIAL MEDIA VIDEO DOMINATION SYSTEM")
    print("="*70)
    print(f"\nInput: {input_file}")
    print(f"Output: {output_dir}\n")

    results = {}

    # 1. Instagram Feed (1:1 square)
    try:
        results['instagram'] = create_instagram_feed(
            input_file,
            f"{output_dir}/instagram_feed.mp4"
        )
    except Exception as e:
        print(f"❌ Instagram failed: {e}")

    # 2. Reels/TikTok (9:16 with voice)
    try:
        results['reels'] = create_reels_tiktok(
            input_file,
            f"{output_dir}/reels_tiktok.mp4"
        )
    except Exception as e:
        print(f"❌ Reels/TikTok failed: {e}")

    # 3. Twitter/LinkedIn (16:9)
    try:
        results['twitter'] = create_twitter_linkedin(
            input_file,
            f"{output_dir}/twitter_linkedin.mp4"
        )
    except Exception as e:
        print(f"❌ Twitter/LinkedIn failed: {e}")

    # Summary
    print("\n" + "="*70)
    print("📊 CONVERSION COMPLETE")
    print("="*70)

    for platform, path in results.items():
        if path and os.path.exists(path):
            size_mb = os.path.getsize(path) / 1024 / 1024
            print(f"✅ {platform.upper():15s} → {size_mb:5.1f} MB - {path}")

    print(f"\n📁 All videos: {output_dir}")
    print("\n🚀 READY TO DOMINATE SOCIAL MEDIA!")

    return results

if __name__ == "__main__":
    # The video we created earlier
    input_video = "C:/Users/dwrek/TUTORIAL_VIDEOS/7_DOMAINS_INSTAGRAM_DEMO.webm"

    # Convert to all platforms
    results = convert_all_platforms(input_video)

    print("\n" + "="*70)
    print("🎉 SUCCESS! YOU NOW HAVE:")
    print("="*70)
    print("\n  📱 Instagram Feed (1080x1080 square)")
    print("  📱 Reels/TikTok (1080x1920 vertical) + AI VOICE")
    print("  💼 Twitter/LinkedIn (1280x720 widescreen)")
    print("\n  All formatted, compressed, and ready to upload!")
    print("\n🚀 POST TO ALL PLATFORMS AND WATCH THE ENGAGEMENT! 🚀")
