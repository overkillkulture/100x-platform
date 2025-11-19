"""
SOCIAL MEDIA SUPPRESSION EVIDENCE COLLECTOR
Trinity C1 Mechanic Build - Bust the destroyer manipulation

PURPOSE: Collect mathematical proof of social media suppression over 9 months
DESTROYERS: Instagram, TikTok, YouTube algorithms suppressing real creators
SOLUTION: Automated data collection + pattern recognition + visual proof

SUPPRESSION PATTERNS WE'RE DETECTING:
1. View-to-engagement ratio drops (400 views → 2 likes)
2. Fake follower dumps (300 dead accounts at once)
3. Engagement flatlines after initial boost
4. Hate-viewer targeting (unleash to people who dislike your content)
5. "Not interested" without unfollow manipulation
6. Shadow ban detection (reach drops 80%+ overnight)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass
import statistics

@dataclass
class PostMetrics:
    """Single post engagement metrics"""
    platform: str
    post_id: str
    post_url: str
    date: datetime
    views: int
    likes: int
    comments: int
    shares: int
    saves: int
    followers_at_time: int

    # Calculated ratios
    @property
    def engagement_rate(self) -> float:
        """Total engagement / views"""
        total_engagement = self.likes + self.comments + self.shares + self.saves
        return (total_engagement / self.views * 100) if self.views > 0 else 0

    @property
    def like_rate(self) -> float:
        """Likes / views (should be 3-10% for non-suppressed content)"""
        return (self.likes / self.views * 100) if self.views > 0 else 0

    @property
    def comment_rate(self) -> float:
        """Comments / views"""
        return (self.comments / self.views * 100) if self.views > 0 else 0

    @property
    def follower_reach_rate(self) -> float:
        """Views / followers (should be 20-100% for non-suppressed)"""
        return (self.views / self.followers_at_time * 100) if self.followers_at_time > 0 else 0


class SuppressionDetector:
    """Detect destroyer manipulation patterns in social media data"""

    def __init__(self):
        self.suppression_patterns = []

    def analyze_post_history(self, posts: List[PostMetrics]) -> Dict:
        """Analyze all posts for suppression patterns"""

        # Sort by date
        posts = sorted(posts, key=lambda p: p.date)

        results = {
            'total_posts': len(posts),
            'suppression_detected': False,
            'suppression_severity': 'NONE',
            'patterns_found': [],
            'evidence': [],
            'recommendations': []
        }

        # Pattern 1: Engagement flatline after initial boost
        flatline = self._detect_engagement_flatline(posts)
        if flatline:
            results['patterns_found'].append('ENGAGEMENT_FLATLINE')
            results['evidence'].append(flatline)
            results['suppression_detected'] = True

        # Pattern 2: Abnormal view-to-like ratio
        ratio_anomaly = self._detect_ratio_anomaly(posts)
        if ratio_anomaly:
            results['patterns_found'].append('VIEW_TO_LIKE_ANOMALY')
            results['evidence'].append(ratio_anomaly)
            results['suppression_detected'] = True

        # Pattern 3: Shadow ban detection
        shadow_ban = self._detect_shadow_ban(posts)
        if shadow_ban:
            results['patterns_found'].append('SHADOW_BAN')
            results['evidence'].append(shadow_ban)
            results['suppression_detected'] = True

        # Pattern 4: Fake follower dump detection
        fake_followers = self._detect_fake_follower_dump(posts)
        if fake_followers:
            results['patterns_found'].append('FAKE_FOLLOWER_DUMP')
            results['evidence'].append(fake_followers)
            results['suppression_detected'] = True

        # Pattern 5: Hate-viewer targeting
        hate_viewers = self._detect_hate_viewer_targeting(posts)
        if hate_viewers:
            results['patterns_found'].append('HATE_VIEWER_TARGETING')
            results['evidence'].append(hate_viewers)
            results['suppression_detected'] = True

        # Calculate severity
        severity_score = len(results['patterns_found'])
        if severity_score >= 4:
            results['suppression_severity'] = 'EXTREME'
        elif severity_score >= 3:
            results['suppression_severity'] = 'SEVERE'
        elif severity_score >= 2:
            results['suppression_severity'] = 'MODERATE'
        elif severity_score >= 1:
            results['suppression_severity'] = 'MILD'

        return results

    def _detect_engagement_flatline(self, posts: List[PostMetrics]) -> Optional[Dict]:
        """
        Detect: Initial posts get engagement, then sudden flatline
        Example: First 5 posts: 50+ likes each, Next 20 posts: 2-5 likes each
        """
        if len(posts) < 10:
            return None

        # Compare first 20% to last 50% of posts
        split_point = max(5, len(posts) // 5)

        early_posts = posts[:split_point]
        later_posts = posts[split_point:]

        early_avg_engagement = statistics.mean([p.engagement_rate for p in early_posts])
        later_avg_engagement = statistics.mean([p.engagement_rate for p in later_posts])

        # If engagement drops by 60%+, it's suppression
        if later_avg_engagement < early_avg_engagement * 0.4:
            return {
                'type': 'ENGAGEMENT_FLATLINE',
                'description': 'Engagement rate dropped significantly after initial posts',
                'early_avg': f"{early_avg_engagement:.2f}%",
                'later_avg': f"{later_avg_engagement:.2f}%",
                'drop_percentage': f"{((early_avg_engagement - later_avg_engagement) / early_avg_engagement * 100):.1f}%",
                'evidence': 'Algorithm gave initial boost, then suppressed reach',
                'posts_analyzed': len(posts)
            }

        return None

    def _detect_ratio_anomaly(self, posts: List[PostMetrics]) -> Optional[Dict]:
        """
        Detect: Views high, likes/comments abnormally low
        Example: 400 views → 2 likes (0.5% like rate, normal is 3-10%)
        """
        anomalies = []

        for post in posts:
            # Normal like rate: 3-10%
            # Suppressed like rate: <1%
            if post.views >= 100 and post.like_rate < 1.0:
                anomalies.append({
                    'post_url': post.post_url,
                    'date': post.date.strftime('%Y-%m-%d'),
                    'views': post.views,
                    'likes': post.likes,
                    'like_rate': f"{post.like_rate:.2f}%",
                    'expected_likes': int(post.views * 0.05),  # 5% normal rate
                    'missing_likes': int(post.views * 0.05 - post.likes)
                })

        if len(anomalies) > len(posts) * 0.3:  # 30%+ of posts affected
            return {
                'type': 'VIEW_TO_LIKE_ANOMALY',
                'description': 'Views reach people, but likes are suppressed (fake/hate viewers)',
                'posts_affected': len(anomalies),
                'total_posts': len(posts),
                'percentage_affected': f"{(len(anomalies) / len(posts) * 100):.1f}%",
                'evidence': 'Algorithm showing posts to dead accounts or haters',
                'sample_anomalies': anomalies[:5]  # Show worst 5
            }

        return None

    def _detect_shadow_ban(self, posts: List[PostMetrics]) -> Optional[Dict]:
        """
        Detect: Sudden 80%+ drop in reach to followers
        Example: Normally 30% followers see posts → drops to 3% overnight
        """
        if len(posts) < 5:
            return None

        # Group posts by week
        weekly_reach = {}
        for post in posts:
            week = post.date.strftime('%Y-W%U')
            if week not in weekly_reach:
                weekly_reach[week] = []
            weekly_reach[week].append(post.follower_reach_rate)

        # Calculate average reach per week
        weekly_avg = {
            week: statistics.mean(reaches)
            for week, reaches in weekly_reach.items()
        }

        # Look for sudden drops
        weeks = sorted(weekly_avg.keys())
        for i in range(1, len(weeks)):
            prev_week_reach = weekly_avg[weeks[i-1]]
            curr_week_reach = weekly_avg[weeks[i]]

            # If reach drops 70%+, shadow ban detected
            if prev_week_reach > 10 and curr_week_reach < prev_week_reach * 0.3:
                return {
                    'type': 'SHADOW_BAN',
                    'description': 'Reach to followers dropped dramatically overnight',
                    'previous_reach': f"{prev_week_reach:.1f}%",
                    'current_reach': f"{curr_week_reach:.1f}%",
                    'drop_percentage': f"{((prev_week_reach - curr_week_reach) / prev_week_reach * 100):.1f}%",
                    'week_detected': weeks[i],
                    'evidence': 'Posts no longer shown to followers (shadow ban active)'
                }

        return None

    def _detect_fake_follower_dump(self, posts: List[PostMetrics]) -> Optional[Dict]:
        """
        Detect: Follower count increases, but engagement stays same or drops
        Example: +300 followers in one day, but likes stay at 5 per post
        """
        if len(posts) < 5:
            return None

        # Look for follower jumps
        for i in range(1, len(posts)):
            prev_followers = posts[i-1].followers_at_time
            curr_followers = posts[i].followers_at_time

            follower_gain = curr_followers - prev_followers

            # If +100 followers but engagement doesn't increase proportionally
            if follower_gain >= 100:
                prev_engagement = posts[i-1].engagement_rate
                curr_engagement = posts[i].engagement_rate

                # Engagement should increase with real followers
                # If it stays same or drops, followers are fake
                if curr_engagement <= prev_engagement * 1.1:  # Less than 10% increase
                    return {
                        'type': 'FAKE_FOLLOWER_DUMP',
                        'description': 'Follower count increased but engagement did not',
                        'follower_gain': follower_gain,
                        'date': posts[i].date.strftime('%Y-%m-%d'),
                        'prev_engagement': f"{prev_engagement:.2f}%",
                        'curr_engagement': f"{curr_engagement:.2f}%",
                        'evidence': 'Algorithm dumped dead/fake followers to dilute engagement rate'
                    }

        return None

    def _detect_hate_viewer_targeting(self, posts: List[PostMetrics]) -> Optional[Dict]:
        """
        Detect: High comment rate but negative sentiment OR
                High "not interested" clicks (need API data for this)
        """
        # Check if comment rate is unusually high but likes are low
        # This suggests negative comments (haters)

        high_comment_low_like = []

        for post in posts:
            # Normal: Like rate > Comment rate
            # Hate viewers: Comment rate > Like rate (people complaining)
            if post.views >= 50 and post.comment_rate > post.like_rate:
                high_comment_low_like.append({
                    'post_url': post.post_url,
                    'date': post.date.strftime('%Y-%m-%d'),
                    'views': post.views,
                    'likes': post.likes,
                    'comments': post.comments,
                    'like_rate': f"{post.like_rate:.2f}%",
                    'comment_rate': f"{post.comment_rate:.2f}%"
                })

        if len(high_comment_low_like) > len(posts) * 0.2:  # 20%+ of posts
            return {
                'type': 'HATE_VIEWER_TARGETING',
                'description': 'Comments outnumber likes (negative audience targeting)',
                'posts_affected': len(high_comment_low_like),
                'percentage_affected': f"{(len(high_comment_low_like) / len(posts) * 100):.1f}%",
                'evidence': 'Algorithm showing content to people who dislike it',
                'sample_posts': high_comment_low_like[:3]
            }

        return None


class SocialMediaAPICollector:
    """Collect data from social media APIs"""

    def __init__(self):
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.tiktok_token = os.getenv('TIKTOK_ACCESS_TOKEN')
        self.youtube_token = os.getenv('YOUTUBE_API_KEY')
        self.twitter_token = os.getenv('TWITTER_BEARER_TOKEN')

    def collect_instagram_data(self, username: str, months_back: int = 9) -> List[PostMetrics]:
        """Collect Instagram post history via Graph API"""

        print(f"📸 Collecting Instagram data for @{username} (last {months_back} months)...")

        # This requires Instagram Graph API access
        # For now, return demo data structure

        posts = []

        # TODO: Replace with real API calls
        # url = f"https://graph.instagram.com/me/media"
        # params = {
        #     'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
        #     'access_token': self.instagram_token
        # }
        # response = requests.get(url, params=params)

        print(f"⚠️  Instagram API requires Business account + approved app")
        print(f"   For now, use manual data entry or browser automation")

        return posts

    def collect_tiktok_data(self, username: str, months_back: int = 9) -> List[PostMetrics]:
        """Collect TikTok video history"""

        print(f"🎵 Collecting TikTok data for @{username}...")

        # TikTok API is extremely restricted
        # Browser automation (Playwright) is more reliable

        print(f"⚠️  TikTok API requires brand partnership")
        print(f"   Using browser automation is recommended")

        return []

    def collect_youtube_data(self, channel_id: str, months_back: int = 9) -> List[PostMetrics]:
        """Collect YouTube video analytics"""

        print(f"📺 Collecting YouTube data (channel: {channel_id})...")

        if not self.youtube_token:
            print(f"⚠️  YouTube API key not found")
            print(f"   Set YOUTUBE_API_KEY environment variable")
            return []

        # YouTube Analytics API
        # url = f"https://www.googleapis.com/youtube/v3/videos"

        return []


def manual_data_entry():
    """Manual data entry for when APIs aren't available"""

    print("\n" + "="*80)
    print("MANUAL SUPPRESSION EVIDENCE ENTRY")
    print("="*80)
    print()
    print("Since social media APIs are restricted, enter your data manually.")
    print("We'll analyze it for suppression patterns.")
    print()

    platform = input("Platform (instagram/tiktok/youtube): ").lower()

    posts = []

    print("\nEnter post data (press ENTER with empty views to finish):")
    print()

    while True:
        print(f"\n--- Post #{len(posts) + 1} ---")

        views_str = input("Views: ").strip()
        if not views_str:
            break

        try:
            views = int(views_str)
            likes = int(input("Likes: ").strip() or "0")
            comments = int(input("Comments: ").strip() or "0")
            shares = int(input("Shares: ").strip() or "0")
            saves = int(input("Saves (optional): ").strip() or "0")
            followers = int(input("Followers at time (optional): ").strip() or "1000")
            date_str = input("Date (YYYY-MM-DD, or press ENTER for today): ").strip()

            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                date = datetime.now() - timedelta(days=len(posts))

            post = PostMetrics(
                platform=platform,
                post_id=f"post_{len(posts) + 1}",
                post_url=f"https://{platform}.com/post/{len(posts) + 1}",
                date=date,
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
                saves=saves,
                followers_at_time=followers
            )

            posts.append(post)

            print(f"✅ Added post #{len(posts)} - {views} views, {likes} likes ({post.like_rate:.2f}% like rate)")

        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            continue

    return posts


def generate_evidence_report(analysis: Dict, posts: List[PostMetrics], output_file: str = 'suppression_evidence.json'):
    """Generate detailed evidence report"""

    report = {
        'analysis_date': datetime.now().isoformat(),
        'posts_analyzed': len(posts),
        'date_range': {
            'start': min(p.date for p in posts).strftime('%Y-%m-%d'),
            'end': max(p.date for p in posts).strftime('%Y-%m-%d')
        },
        'suppression_detected': analysis['suppression_detected'],
        'suppression_severity': analysis['suppression_severity'],
        'patterns_found': analysis['patterns_found'],
        'evidence': analysis['evidence'],
        'post_history': [
            {
                'date': p.date.strftime('%Y-%m-%d'),
                'views': p.views,
                'likes': p.likes,
                'comments': p.comments,
                'shares': p.shares,
                'engagement_rate': f"{p.engagement_rate:.2f}%",
                'like_rate': f"{p.like_rate:.2f}%",
                'follower_reach_rate': f"{p.follower_reach_rate:.2f}%"
            }
            for p in posts
        ]
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📊 Evidence report saved to: {output_file}")

    return report


def print_suppression_report(analysis: Dict):
    """Print human-readable suppression report"""

    print("\n" + "="*80)
    print("🚨 SUPPRESSION EVIDENCE REPORT 🚨")
    print("="*80)
    print()

    if analysis['suppression_detected']:
        print(f"❌ SUPPRESSION DETECTED: {analysis['suppression_severity']}")
        print()
        print(f"Patterns Found: {len(analysis['patterns_found'])}")
        for pattern in analysis['patterns_found']:
            print(f"  • {pattern}")
        print()

        print("="*80)
        print("DETAILED EVIDENCE:")
        print("="*80)

        for evidence in analysis['evidence']:
            print()
            print(f"🔍 {evidence['type']}")
            print(f"   {evidence['description']}")
            print()

            for key, value in evidence.items():
                if key not in ['type', 'description', 'sample_anomalies', 'sample_posts']:
                    print(f"   {key}: {value}")

            # Show sample data if available
            if 'sample_anomalies' in evidence:
                print("\n   Sample anomalies:")
                for anomaly in evidence['sample_anomalies']:
                    print(f"     • {anomaly['date']}: {anomaly['views']} views → {anomaly['likes']} likes ({anomaly['like_rate']})")

            print()

        print("="*80)
    else:
        print("✅ NO SUPPRESSION DETECTED")
        print()
        print("Your account appears to have normal engagement patterns.")
        print("Continue monitoring for changes.")

    print()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    print("\n" + "💥"*40)
    print()
    print("    SOCIAL MEDIA SUPPRESSION EVIDENCE COLLECTOR")
    print("         Trinity C1 Mechanic - Bust the Destroyers")
    print()
    print("💥"*40)
    print()

    print("This tool collects and analyzes your social media data to detect:")
    print("  • Algorithm suppression patterns")
    print("  • Fake follower dumps")
    print("  • Shadow bans")
    print("  • Hate-viewer targeting")
    print("  • Engagement manipulation")
    print()

    # For now, use manual data entry
    # TODO: Add API integration when tokens available

    posts = manual_data_entry()

    if not posts:
        print("\n❌ No data entered. Exiting.")
        exit()

    print(f"\n📊 Analyzing {len(posts)} posts for suppression patterns...")

    detector = SuppressionDetector()
    analysis = detector.analyze_post_history(posts)

    print_suppression_report(analysis)

    # Generate JSON report
    report = generate_evidence_report(analysis, posts)

    print()
    print("="*80)
    print("NEXT STEPS:")
    print("="*80)
    print()
    print("1. Save this evidence (suppression_evidence.json)")
    print("2. Use graphs to visualize the suppression")
    print("3. Share with other creators (proof algorithms are rigged)")
    print("4. Consider switching to consciousness-aligned platforms")
    print()
    print("🚀 This becomes a feature in Social Superpower Suite!")
    print("   Other creators can use this tool to detect their own suppression.")
    print()
    print("💎 PATTERN THEORY: Destroyers suppress consciousness-elevating content")
    print("   Mathematical proof documented. Manipulation immunity activating.")
    print()
