"""
🎬 FULL SOCIAL MEDIA AUTOMATION WORKFLOW
Complete end-to-end: Create → Convert → Post → Track
ONE COMMAND TO RULE THEM ALL!
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path
import argparse

def run_command(cmd, description):
    """Run command with nice output"""
    print(f"\n{'='*70}")
    print(f"▶️  {description}")
    print(f"{'='*70}\n")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def full_automation_workflow(
    caption: str = None,
    platforms: list = None,
    skip_video_creation: bool = False
):
    """Complete workflow from video creation to posting"""

    print("\n" + "🎬"*35)
    print("     FULL SOCIAL MEDIA AUTOMATION WORKFLOW")
    print("🎬"*35 + "\n")

    workflow_start = time.time()
    results = {
        'started_at': datetime.now().isoformat(),
        'steps': {}
    }

    # Default caption
    if caption is None:
        caption = """🌌 The playground is OPEN 🌌

7 Sacred Domains of consciousness-elevating tools, education & community.

Click around. Explore. Discover.

127 automation modules | 50+ builders | AI guides

→ conciousnessrevolution.io

#ConsciousnessRevolution #100XBuilder #AI #BuildInPublic"""

    # Default platforms
    if platforms is None:
        platforms = ['all']

    # STEP 1: Create Demo Video (Optional)
    if not skip_video_creation:
        print("\n📹 STEP 1: Creating demo video...")
        video_created = run_command(
            'python CREATE_TUTORIAL_VIDEO.py',
            'Creating automated 7-domain tour video'
        )
        results['steps']['video_creation'] = {
            'success': video_created,
            'duration': '~2 minutes'
        }

        if not video_created:
            print("❌ Video creation failed! Stopping workflow.")
            return results

        time.sleep(2)  # Brief pause
    else:
        print("\n⏭️  STEP 1: Skipped (using existing video)")
        results['steps']['video_creation'] = {'skipped': True}

    # STEP 2: Convert to Platform Formats
    print("\n🎞️  STEP 2: Converting to platform-specific formats...")
    conversion_success = run_command(
        'python ACTUALLY_WORKING_CONVERTER.py',
        'Converting to Instagram, Reels, and Twitter formats'
    )
    results['steps']['format_conversion'] = {
        'success': conversion_success,
        'duration': '~5 minutes',
        'outputs': [
            'SOCIAL_VIDEOS/instagram_feed.mp4',
            'SOCIAL_VIDEOS/reels_tiktok.mp4',
            'SOCIAL_VIDEOS/twitter_linkedin.mp4'
        ]
    }

    if not conversion_success:
        print("❌ Conversion failed! Stopping workflow.")
        return results

    time.sleep(2)

    # STEP 3: Post to All Platforms
    print("\n🚀 STEP 3: Posting to all platforms...")

    platforms_str = ' '.join(platforms)
    posting_cmd = f'python ULTIMATE_SOCIAL_POSTER.py dummy.mp4 --caption "{caption}" --platforms {platforms_str} --use-optimized'

    posting_success = run_command(
        posting_cmd,
        f'Posting to platforms: {platforms_str}'
    )
    results['steps']['posting'] = {
        'success': posting_success,
        'platforms': platforms,
        'duration': '~2 minutes'
    }

    if not posting_success:
        print("⚠️  Posting had some issues, check output above")

    time.sleep(2)

    # STEP 4: Track Analytics (Optional)
    print("\n📊 STEP 4: Analytics tracking...")
    print("   Analytics dashboard available at: http://localhost:8888")
    print("   Run separately: python ANALYTICS_DASHBOARD.py")

    results['steps']['analytics'] = {
        'dashboard_url': 'http://localhost:8888',
        'note': 'Run ANALYTICS_DASHBOARD.py to start tracking'
    }

    # Calculate total time
    workflow_end = time.time()
    total_time = workflow_end - workflow_start
    results['completed_at'] = datetime.now().isoformat()
    results['total_duration_seconds'] = round(total_time, 2)
    results['total_duration_minutes'] = round(total_time / 60, 2)

    # Save workflow results
    results_file = f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Final summary
    print("\n" + "="*70)
    print("✅ FULL AUTOMATION WORKFLOW COMPLETE!")
    print("="*70)
    print(f"\n⏱️  Total Time: {results['total_duration_minutes']:.1f} minutes")
    print(f"\n📊 Results saved: {results_file}")

    print("\n📁 Generated Files:")
    print("   • TUTORIAL_VIDEOS/7_DOMAINS_INSTAGRAM_DEMO.webm")
    print("   • SOCIAL_VIDEOS/instagram_feed.mp4")
    print("   • SOCIAL_VIDEOS/reels_tiktok.mp4")
    print("   • SOCIAL_VIDEOS/twitter_linkedin.mp4")

    print("\n🎯 Next Steps:")
    print("   1. Check posting_results_*.json for status")
    print("   2. If Instagram pending, complete manual post (30 sec)")
    print("   3. Start analytics: python ANALYTICS_DASHBOARD.py")
    print("   4. Watch the engagement roll in! 📈")

    print("\n🚀 FROM ZERO TO POSTED EVERYWHERE IN <15 MINUTES!")

    return results


def quick_repost(caption: str = None):
    """Quick repost using existing videos"""
    print("\n🔄 QUICK REPOST MODE")
    print("Using existing videos from SOCIAL_VIDEOS folder\n")

    if caption is None:
        caption = input("Enter caption (or press ENTER for default): ").strip()

    if not caption:
        caption = "🌌 Check out the Consciousness Revolution platform!\n\n→ conciousnessrevolution.io"

    # Just post, skip video creation
    return full_automation_workflow(
        caption=caption,
        skip_video_creation=True
    )


def main():
    """CLI interface"""

    parser = argparse.ArgumentParser(
        description='🎬 Full Social Media Automation Workflow'
    )

    parser.add_argument('--caption', help='Custom caption for posts')
    parser.add_argument('--platforms', nargs='+', default=['all'],
                       help='Platforms to post to (default: all)')
    parser.add_argument('--skip-video', action='store_true',
                       help='Skip video creation, use existing')
    parser.add_argument('--quick', action='store_true',
                       help='Quick repost mode (skip video creation)')

    args = parser.parse_args()

    if args.quick:
        quick_repost(args.caption)
    else:
        full_automation_workflow(
            caption=args.caption,
            platforms=args.platforms,
            skip_video_creation=args.skip_video
        )


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        print("\n🎬 FULL SOCIAL MEDIA AUTOMATION")
        print("="*70)
        print("\nUsage:")
        print("  python FULL_SOCIAL_AUTOMATION.py [options]")
        print("\nOptions:")
        print("  --caption \"text\"       Custom caption for posts")
        print("  --platforms X Y        Post to specific platforms")
        print("  --skip-video           Use existing videos")
        print("  --quick                Quick repost mode")
        print("\nExamples:")
        print("  # Full automation (create → convert → post):")
        print("  python FULL_SOCIAL_AUTOMATION.py")
        print("\n  # Quick repost with existing videos:")
        print("  python FULL_SOCIAL_AUTOMATION.py --quick")
        print("\n  # Custom caption:")
        print('  python FULL_SOCIAL_AUTOMATION.py --caption "New update!"')
        print("\n  # Specific platforms:")
        print('  python FULL_SOCIAL_AUTOMATION.py --platforms tiktok linkedin youtube')
        print("\n")
        print("🚀 ONE COMMAND → POSTED EVERYWHERE IN <15 MINUTES!")
        print("\n")
    else:
        main()
