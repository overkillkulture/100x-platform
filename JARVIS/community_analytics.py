"""
JARVIS Community Analytics System
For: Josh (Community Builder - Node #2)
Purpose: Generate comprehensive community metrics and insights

Dependencies:
- anthropic (Claude AI for analysis)
- python-dotenv (environment variables)
- matplotlib (charts - optional)
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

class CommunityAnalytics:
    def __init__(self):
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')

        # Initialize Claude client
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            print("⚠️  No ANTHROPIC_API_KEY found - AI analysis limited")
            self.claude = None

        # Data directories
        self.data_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/JARVIS/data")
        self.reports_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/JARVIS/reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def collect_weekly_data(self):
        """
        Collect data from all JARVIS systems for the past week
        """
        print("📊 Collecting weekly data...")

        data = {
            'period': {
                'start': (datetime.now() - timedelta(days=7)).isoformat(),
                'end': datetime.now().isoformat()
            },
            'emails': self.collect_email_data(),
            'social': self.collect_social_data(),
            'onboarding': self.collect_onboarding_data(),
            'collected_at': datetime.now().isoformat()
        }

        return data

    def collect_email_data(self):
        """Collect email metrics from community_responder data"""
        email_dir = self.data_dir
        email_files = list(email_dir.glob('emails_*.json'))

        if not email_files:
            return {'total': 0, 'processed': 0, 'types': {}}

        # Get recent emails (last 7 days)
        recent_emails = []
        cutoff = datetime.now() - timedelta(days=7)

        for file in email_files:
            # Check file modification time
            if datetime.fromtimestamp(file.stat().st_mtime) > cutoff:
                with open(file) as f:
                    emails = json.load(f)
                    recent_emails.extend(emails)

        # Count by type
        types = {}
        for email in recent_emails:
            subject = email.get('subject', '').lower()
            if any(word in subject for word in ['join', 'signup', 'new']):
                types['welcome'] = types.get('welcome', 0) + 1
            elif '?' in subject:
                types['question'] = types.get('question', 0) + 1
            elif any(word in subject for word in ['help', 'issue', 'problem']):
                types['support'] = types.get('support', 0) + 1
            else:
                types['other'] = types.get('other', 0) + 1

        return {
            'total': len(recent_emails),
            'processed': len(recent_emails),  # Assuming all are processed
            'types': types
        }

    def collect_social_data(self):
        """Collect social media metrics"""
        social_dir = self.data_dir / 'social'

        if not social_dir.exists():
            return {'platforms': {}, 'engagement': 0}

        # Collect from social monitor data
        urgent_files = list(social_dir.glob('urgent_*.json'))

        total_issues = 0
        urgent_issues = 0

        for file in urgent_files:
            with open(file) as f:
                issues = json.load(f)
                total_issues += len(issues)
                urgent_issues += sum(1 for i in issues if i.get('urgency_score', 0) >= 80)

        return {
            'platforms': {
                'discord': 'monitored',
                'twitter': 'monitored'
            },
            'total_issues': total_issues,
            'urgent_issues': urgent_issues,
            'engagement': 'manual_review_needed'
        }

    def collect_onboarding_data(self):
        """Collect builder onboarding metrics"""
        builders_dir = self.data_dir / 'builders'

        if not builders_dir.exists():
            return {'total_builders': 0, 'completion_rate': 0}

        onboarding_files = list(builders_dir.glob('onboarding_*.json'))

        total_builders = len(onboarding_files)
        total_steps = 0
        completed_steps = 0

        for file in onboarding_files:
            with open(file) as f:
                record = json.load(f)
                steps = record.get('steps', {})
                total_steps += len(steps)
                completed_steps += sum(1 for v in steps.values() if v)

        completion_rate = (completed_steps / total_steps * 100) if total_steps > 0 else 0

        return {
            'total_builders': total_builders,
            'completion_rate': completion_rate,
            'avg_steps_completed': completed_steps / total_builders if total_builders > 0 else 0
        }

    def generate_weekly_report(self):
        """
        Generate comprehensive weekly community report
        """
        print("\n" + "="*70)
        print("📊 WEEKLY COMMUNITY ANALYTICS REPORT")
        print("="*70)

        # Collect data
        data = self.collect_weekly_data()

        # Report header
        start_date = datetime.fromisoformat(data['period']['start']).strftime('%Y-%m-%d')
        end_date = datetime.fromisoformat(data['period']['end']).strftime('%Y-%m-%d')

        print(f"\n📅 Period: {start_date} to {end_date}")
        print(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Email metrics
        print("\n📧 EMAIL ACTIVITY:")
        print("-"*70)
        emails = data['emails']
        print(f"  Total Emails: {emails['total']}")
        print(f"  Processed: {emails['processed']}")
        print(f"\n  By Type:")
        for email_type, count in emails.get('types', {}).items():
            print(f"    {email_type.title()}: {count}")

        # Social media metrics
        print("\n🌐 SOCIAL MEDIA:")
        print("-"*70)
        social = data['social']
        print(f"  Platforms Monitored: {len(social['platforms'])}")
        for platform, status in social['platforms'].items():
            print(f"    {platform.title()}: {status}")
        print(f"  Total Issues Tracked: {social.get('total_issues', 0)}")
        print(f"  Urgent Issues: {social.get('urgent_issues', 0)}")

        # Onboarding metrics
        print("\n👥 BUILDER ONBOARDING:")
        print("-"*70)
        onboarding = data['onboarding']
        print(f"  New Builders: {onboarding['total_builders']}")
        print(f"  Completion Rate: {onboarding['completion_rate']:.1f}%")
        print(f"  Avg Steps Completed: {onboarding.get('avg_steps_completed', 0):.1f}")

        # Overall health score
        health_score = self.calculate_health_score(data)
        print("\n💚 COMMUNITY HEALTH SCORE:")
        print("-"*70)
        print(f"  Overall: {health_score}/100")
        print(f"  Status: {self.get_health_status(health_score)}")

        # Key insights
        print("\n💡 KEY INSIGHTS:")
        print("-"*70)
        insights = self.generate_insights(data)
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. {insight}")

        # Recommendations
        print("\n🎯 RECOMMENDED ACTIONS:")
        print("-"*70)
        recommendations = self.generate_recommendations(data)
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")

        # Top contributors (placeholder)
        print("\n⭐ TOP CONTRIBUTORS:")
        print("-"*70)
        print("  [Manual identification needed]")
        print("  💡 Track: Most helpful responses, most active in Discord")

        print("\n" + "="*70)

        # Save report
        self.save_report(data)

        # Generate AI summary if available
        if self.claude:
            print("\n🤖 Generating AI Summary...")
            summary = self.generate_ai_summary(data)
            print("\n📝 AI SUMMARY:")
            print("-"*70)
            print(summary)
            print("-"*70)

        return data

    def calculate_health_score(self, data):
        """
        Calculate overall community health score (0-100)
        """
        score = 50  # Base score

        # Email responsiveness (+20 if processing emails)
        if data['emails']['total'] > 0:
            score += 15

        # Onboarding effectiveness (+20 for high completion)
        completion = data['onboarding'].get('completion_rate', 0)
        score += int(completion * 0.2)

        # Active monitoring (+10)
        if len(data['social']['platforms']) > 0:
            score += 10

        # Deduct for urgent issues (-5 per urgent issue)
        urgent = data['social'].get('urgent_issues', 0)
        score -= (urgent * 5)

        # Cap at 0-100
        return max(0, min(100, score))

    def get_health_status(self, score):
        """Convert health score to status"""
        if score >= 80:
            return "🟢 Excellent"
        elif score >= 60:
            return "🟡 Good"
        elif score >= 40:
            return "🟠 Fair"
        else:
            return "🔴 Needs Attention"

    def generate_insights(self, data):
        """Generate key insights from data"""
        insights = []

        # Email insights
        email_total = data['emails']['total']
        if email_total > 20:
            insights.append(f"High email volume ({email_total}) - consider automation or help")
        elif email_total < 5:
            insights.append("Low email volume - growth opportunity or awareness issue?")

        # Onboarding insights
        completion = data['onboarding'].get('completion_rate', 0)
        if completion < 50:
            insights.append(f"Low onboarding completion ({completion:.0f}%) - simplify process")
        elif completion > 80:
            insights.append(f"Excellent onboarding completion ({completion:.0f}%) - system working well!")

        # Social insights
        urgent = data['social'].get('urgent_issues', 0)
        if urgent > 0:
            insights.append(f"{urgent} urgent issues - immediate attention needed")

        # Default insight
        if not insights:
            insights.append("Community metrics look stable - maintain current pace")

        return insights

    def generate_recommendations(self, data):
        """Generate action recommendations"""
        recommendations = []

        # Based on email volume
        if data['emails']['total'] > 15:
            recommendations.append("Scale email responses - create more templates or hire help")

        # Based on onboarding
        if data['onboarding']['total_builders'] > 0:
            completion = data['onboarding'].get('completion_rate', 0)
            if completion < 70:
                recommendations.append("Improve onboarding flow - identify where builders drop off")
            else:
                recommendations.append("Excellent onboarding - document process for scaling")

        # Based on social activity
        if data['social'].get('urgent_issues', 0) > 0:
            recommendations.append("Address urgent community issues immediately")

        # Growth recommendations
        if data['onboarding']['total_builders'] < 5:
            recommendations.append("Increase builder acquisition - social media push or partnerships")

        # Default recommendation
        if not recommendations:
            recommendations.append("Continue current operations - metrics are healthy")

        return recommendations

    def generate_ai_summary(self, data):
        """Use Claude to generate executive summary"""
        if not self.claude:
            return "AI summary unavailable - ANTHROPIC_API_KEY not set"

        try:
            prompt = f"""You are Josh's AI assistant analyzing community metrics. Generate a brief executive summary (3-4 sentences) of this week's community activity:

DATA:
- Emails: {data['emails']['total']} total, types: {data['emails']['types']}
- Social: {data['social'].get('total_issues', 0)} issues tracked, {data['social'].get('urgent_issues', 0)} urgent
- Onboarding: {data['onboarding']['total_builders']} new builders, {data['onboarding'].get('completion_rate', 0):.0f}% completion

Focus on: Overall health, biggest wins, areas needing attention, and one actionable next step.

Keep it concise, positive, and actionable."""

            message = self.claude.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            return f"AI summary generation failed: {e}"

    def save_report(self, data):
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = self.reports_dir / f"weekly_report_{timestamp}.json"

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n💾 Report saved to: {file_path}")

    def generate_growth_chart(self, weeks=4):
        """
        Generate growth chart for past N weeks
        (Placeholder - requires matplotlib)
        """
        print("\n📈 GROWTH TRENDS (Past 4 Weeks):")
        print("-"*70)

        # Find all weekly reports
        reports = sorted(self.reports_dir.glob('weekly_report_*.json'))[-weeks:]

        if not reports:
            print("  ⚠️  Not enough historical data")
            return

        print("  Week  | Emails | Builders | Health")
        print("  " + "-"*40)

        for i, report_file in enumerate(reports, 1):
            with open(report_file) as f:
                report_data = json.load(f)

            emails = report_data['emails']['total']
            builders = report_data['onboarding']['total_builders']
            health = self.calculate_health_score(report_data)

            print(f"  {i:2d}    | {emails:6d} | {builders:8d} | {health:3d}/100")

        print("-"*70)

    def compare_weeks(self, current_week_data, previous_week_data):
        """Compare this week vs last week"""
        print("\n📊 WEEK-OVER-WEEK COMPARISON:")
        print("-"*70)

        # Email comparison
        current_emails = current_week_data['emails']['total']
        previous_emails = previous_week_data['emails']['total']
        email_change = ((current_emails - previous_emails) / previous_emails * 100) if previous_emails > 0 else 0

        print(f"  Emails: {current_emails} (vs {previous_emails}) ", end="")
        print(f"{'📈' if email_change > 0 else '📉'} {email_change:+.0f}%")

        # Builder comparison
        current_builders = current_week_data['onboarding']['total_builders']
        previous_builders = previous_week_data['onboarding']['total_builders']
        builder_change = ((current_builders - previous_builders) / previous_builders * 100) if previous_builders > 0 else 0

        print(f"  Builders: {current_builders} (vs {previous_builders}) ", end="")
        print(f"{'📈' if builder_change > 0 else '📉'} {builder_change:+.0f}%")

        print("-"*70)


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='JARVIS Community Analytics')
    parser.add_argument('--weekly-report', action='store_true', help='Generate weekly community report')
    parser.add_argument('--growth-chart', action='store_true', help='Show 4-week growth trends')
    parser.add_argument('--health-check', action='store_true', help='Quick community health check')

    args = parser.parse_args()

    analytics = CommunityAnalytics()

    if args.weekly_report:
        analytics.generate_weekly_report()

    elif args.growth_chart:
        analytics.generate_growth_chart()

    elif args.health_check:
        data = analytics.collect_weekly_data()
        health = analytics.calculate_health_score(data)
        status = analytics.get_health_status(health)

        print(f"\n💚 Community Health: {health}/100 - {status}")
        print(f"📧 Emails this week: {data['emails']['total']}")
        print(f"👥 New builders: {data['onboarding']['total_builders']}")
        print(f"🚨 Urgent issues: {data['social'].get('urgent_issues', 0)}\n")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
