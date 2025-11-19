"""
📊 SOCIAL MEDIA ANALYTICS DASHBOARD
Track performance across all platforms in one place
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

class SocialAnalytics:
    """Unified analytics across all social platforms"""

    def __init__(self):
        """Initialize analytics tracker"""
        self.cache_file = Path('analytics_cache.json')
        self.load_cache()

    def load_cache(self):
        """Load cached analytics"""
        if self.cache_file.exists():
            with open(self.cache_file) as f:
                self.cache = json.load(f)
        else:
            self.cache = {'platforms': {}, 'last_updated': None}

    def save_cache(self):
        """Save analytics cache"""
        self.cache['last_updated'] = datetime.now().isoformat()
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_late_analytics(self, api_key: str) -> Dict:
        """Get analytics from Late API platforms"""
        try:
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(
                'https://api.getlate.dev/v1/analytics',
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'tiktok': data.get('tiktok', {}),
                    'linkedin': data.get('linkedin', {}),
                    'facebook': data.get('facebook', {})
                }
        except:
            pass

        return {}

    def get_youtube_analytics(self) -> Dict:
        """Get YouTube analytics (requires OAuth)"""
        # Placeholder - requires YouTube Analytics API setup
        return self.cache.get('platforms', {}).get('youtube', {
            'views': 0,
            'likes': 0,
            'comments': 0,
            'subscribers': 0
        })

    def get_twitter_analytics(self) -> Dict:
        """Get Twitter analytics (manual or scraper)"""
        # Placeholder - can be scraped via Playwright
        return self.cache.get('platforms', {}).get('twitter', {
            'views': 0,
            'likes': 0,
            'retweets': 0,
            'replies': 0
        })

    def get_instagram_analytics(self) -> Dict:
        """Get Instagram analytics (manual input)"""
        return self.cache.get('platforms', {}).get('instagram', {
            'views': 0,
            'likes': 0,
            'comments': 0,
            'shares': 0
        })

    def get_all_analytics(self, late_api_key: str = None) -> Dict:
        """Get analytics from all platforms"""

        analytics = {
            'timestamp': datetime.now().isoformat(),
            'platforms': {}
        }

        # Late platforms
        if late_api_key:
            late_data = self.get_late_analytics(late_api_key)
            analytics['platforms'].update(late_data)

        # YouTube
        analytics['platforms']['youtube'] = self.get_youtube_analytics()

        # Twitter
        analytics['platforms']['twitter'] = self.get_twitter_analytics()

        # Instagram
        analytics['platforms']['instagram'] = self.get_instagram_analytics()

        # Calculate totals
        analytics['totals'] = self.calculate_totals(analytics['platforms'])

        # Update cache
        self.cache = analytics
        self.save_cache()

        return analytics

    def calculate_totals(self, platforms: Dict) -> Dict:
        """Calculate cross-platform totals"""

        total_views = 0
        total_likes = 0
        total_comments = 0
        total_shares = 0

        for platform, stats in platforms.items():
            total_views += stats.get('views', 0)
            total_likes += stats.get('likes', 0)
            total_comments += stats.get('comments', 0)
            total_shares += stats.get('shares', 0) + stats.get('retweets', 0)

        total_engagement = total_likes + total_comments + total_shares
        engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0

        return {
            'views': total_views,
            'likes': total_likes,
            'comments': total_comments,
            'shares': total_shares,
            'engagement': total_engagement,
            'engagement_rate': round(engagement_rate, 2)
        }

    def manual_update(self, platform: str, stats: Dict):
        """Manually update platform stats"""
        if 'platforms' not in self.cache:
            self.cache['platforms'] = {}

        self.cache['platforms'][platform] = stats
        self.save_cache()

        print(f"✅ {platform.title()} analytics updated")


# Flask Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Social Media Analytics Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #fff;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .totals {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .totals h2 { margin-bottom: 20px; }
        .totals-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .total-card {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .total-card h3 { font-size: 0.9em; margin-bottom: 10px; opacity: 0.9; }
        .total-card p { font-size: 2em; font-weight: bold; }
        .platforms-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        .platform-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .platform-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .platform-icon {
            font-size: 2em;
            margin-right: 15px;
        }
        .platform-name {
            font-size: 1.5em;
            font-weight: bold;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        .stat {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
        }
        .stat-label {
            font-size: 0.85em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 1.8em;
            font-weight: bold;
        }
        .last-updated {
            text-align: center;
            margin-top: 30px;
            opacity: 0.7;
        }
        .refresh-btn {
            background: #fff;
            color: #667eea;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            margin: 20px auto;
            display: block;
        }
        .refresh-btn:hover { background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Social Media Analytics Dashboard</h1>

        <div class="totals">
            <h2>Total Performance</h2>
            <div class="totals-grid">
                <div class="total-card">
                    <h3>Total Views</h3>
                    <p id="total-views">{{ totals.views }}</p>
                </div>
                <div class="total-card">
                    <h3>Total Likes</h3>
                    <p id="total-likes">{{ totals.likes }}</p>
                </div>
                <div class="total-card">
                    <h3>Total Comments</h3>
                    <p id="total-comments">{{ totals.comments }}</p>
                </div>
                <div class="total-card">
                    <h3>Total Shares</h3>
                    <p id="total-shares">{{ totals.shares }}</p>
                </div>
                <div class="total-card">
                    <h3>Total Engagement</h3>
                    <p id="total-engagement">{{ totals.engagement }}</p>
                </div>
                <div class="total-card">
                    <h3>Engagement Rate</h3>
                    <p id="engagement-rate">{{ totals.engagement_rate }}%</p>
                </div>
            </div>
        </div>

        <div class="platforms-grid">
            {% for platform, stats in platforms.items() %}
            <div class="platform-card">
                <div class="platform-header">
                    <div class="platform-icon">
                        {% if platform == 'tiktok' %}🎵
                        {% elif platform == 'linkedin' %}💼
                        {% elif platform == 'facebook' %}👥
                        {% elif platform == 'youtube' %}🎬
                        {% elif platform == 'twitter' %}🐦
                        {% elif platform == 'instagram' %}📱
                        {% endif %}
                    </div>
                    <div class="platform-name">{{ platform.title() }}</div>
                </div>
                <div class="stat-grid">
                    <div class="stat">
                        <div class="stat-label">Views</div>
                        <div class="stat-value">{{ stats.get('views', 0) }}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Likes</div>
                        <div class="stat-value">{{ stats.get('likes', 0) }}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Comments</div>
                        <div class="stat-value">{{ stats.get('comments', 0) }}</div>
                    </div>
                    <div class="stat">
                        <div class="stat-label">Shares</div>
                        <div class="stat-value">{{ stats.get('shares', stats.get('retweets', 0)) }}</div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Analytics</button>

        <div class="last-updated">
            Last updated: {{ timestamp }}
        </div>
    </div>

    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => location.reload(), 300000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Render analytics dashboard"""
    analytics = SocialAnalytics()
    data = analytics.get_all_analytics()

    return render_template_string(
        DASHBOARD_HTML,
        platforms=data['platforms'],
        totals=data['totals'],
        timestamp=data['timestamp']
    )

@app.route('/api/analytics')
def api_analytics():
    """JSON API endpoint"""
    analytics = SocialAnalytics()
    return jsonify(analytics.get_all_analytics())

@app.route('/api/update/<platform>', methods=['POST'])
def update_platform(platform):
    """Manually update platform stats"""
    from flask import request
    stats = request.json
    analytics = SocialAnalytics()
    analytics.manual_update(platform, stats)
    return jsonify({'status': 'updated'})


def run_dashboard(port=8888):
    """Run the analytics dashboard"""
    print(f"\n📊 Starting Analytics Dashboard...")
    print(f"🌐 Open: http://localhost:{port}")
    print("\nDashboard will auto-refresh every 5 minutes")
    print("Press Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    run_dashboard()
