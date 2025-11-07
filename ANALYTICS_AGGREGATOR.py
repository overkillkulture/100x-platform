#!/usr/bin/env python3
"""
ANALYTICS AGGREGATOR
Processes raw analytics data and generates insights

Answers questions like:
- Is anybody in there?
- Did anybody build anything?
- How many hours of building?
- What was built?
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any
import statistics

class AnalyticsAggregator:
    def __init__(self, data_dir='visitor_data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def load_heartbeats(self, date=None):
        """Load heartbeat data for a specific date"""
        if date is None:
            date = datetime.now()

        date_str = date.strftime('%Y-%m-%d')
        heartbeat_file = self.data_dir / f"heartbeats_{date_str}.jsonl"

        if not heartbeat_file.exists():
            return []

        heartbeats = []
        with open(heartbeat_file, 'r') as f:
            for line in f:
                try:
                    heartbeats.append(json.loads(line.strip()))
                except:
                    pass

        return heartbeats

    def load_events(self, date=None):
        """Load event data for a specific date"""
        if date is None:
            date = datetime.now()

        date_str = date.strftime('%Y-%m-%d')
        events_file = self.data_dir / f"events_{date_str}.jsonl"

        if not events_file.exists():
            return []

        events = []
        with open(events_file, 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except:
                    pass

        return events

    def analyze_visitors(self, date=None):
        """Analyze visitor activity"""
        heartbeats = self.load_heartbeats(date)
        events = self.load_events(date)

        if not heartbeats:
            return {
                'total_visitors': 0,
                'message': 'No visitors today'
            }

        # Unique visitors
        visitors = set(h['pin'] for h in heartbeats if h['pin'] != 'anonymous')
        anonymous = sum(1 for h in heartbeats if h['pin'] == 'anonymous')

        # Session durations
        session_durations = {}
        for hb in heartbeats:
            pin = hb['pin']
            timestamp = datetime.fromisoformat(hb['timestamp'].replace('Z', ''))

            if pin not in session_durations:
                session_durations[pin] = {'start': timestamp, 'end': timestamp}
            else:
                if timestamp < session_durations[pin]['start']:
                    session_durations[pin]['start'] = timestamp
                if timestamp > session_durations[pin]['end']:
                    session_durations[pin]['end'] = timestamp

        # Calculate time spent per visitor
        time_spent = {}
        for pin, times in session_durations.items():
            duration = (times['end'] - times['start']).total_seconds() / 60  # minutes
            time_spent[pin] = duration

        # Device breakdown
        devices = Counter(h.get('device', {}).get('deviceType', 'unknown') for h in heartbeats)

        # Pages visited
        pages = Counter(h['page'] for h in heartbeats)

        return {
            'total_visitors': len(visitors),
            'anonymous_visitors': anonymous,
            'named_visitors': list(visitors),
            'total_time_spent_minutes': sum(time_spent.values()),
            'avg_time_per_visitor_minutes': statistics.mean(time_spent.values()) if time_spent else 0,
            'longest_session_minutes': max(time_spent.values()) if time_spent else 0,
            'devices': dict(devices),
            'top_pages': dict(pages.most_common(10)),
            'active_builders': [pin for pin, duration in time_spent.items() if duration > 30],  # 30+ minutes = active builder
        }

    def analyze_engagement(self, date=None):
        """Analyze engagement quality"""
        events = self.load_events(date)
        heartbeats = self.load_heartbeats(date)

        if not events:
            return {
                'total_events': 0,
                'message': 'No engagement events'
            }

        # Event breakdown
        event_types = Counter(e['type'] for e in events)

        # Click analysis
        clicks = [e for e in events if e['type'] == 'click']
        button_clicks = [e for e in events if e['type'] == 'button_click']
        link_clicks = [e for e in events if e['type'] == 'link_click']

        # Form analysis
        forms_started = len([e for e in events if e['type'] == 'form_start'])
        forms_submitted = len([e for e in events if e['type'] == 'form_submit'])
        forms_abandoned = len([e for e in events if e['type'] == 'form_abandon'])
        form_completion_rate = (forms_submitted / forms_started * 100) if forms_started > 0 else 0

        # Scroll analysis
        scroll_events = [e for e in events if e['type'] == 'scroll_milestone']
        depths_reached = Counter(e['data'].get('depth') for e in scroll_events)

        # Tool usage
        tools_used = [e for e in events if e['type'] == 'tool_used']
        tool_names = Counter(e['data'].get('tool') for e in tools_used)

        # Engagement scores from heartbeats
        engagement_scores = [h.get('engagementScore', 0) for h in heartbeats if h.get('engagementScore')]

        return {
            'total_events': len(events),
            'event_types': dict(event_types.most_common(20)),
            'clicks': {
                'total': len(clicks),
                'buttons': len(button_clicks),
                'links': len(link_clicks)
            },
            'forms': {
                'started': forms_started,
                'submitted': forms_submitted,
                'abandoned': forms_abandoned,
                'completion_rate': round(form_completion_rate, 2)
            },
            'scroll': {
                'milestone_events': len(scroll_events),
                'depths_reached': dict(depths_reached)
            },
            'tools': {
                'total_uses': len(tools_used),
                'tools_used': dict(tool_names.most_common(10))
            },
            'engagement_scores': {
                'average': round(statistics.mean(engagement_scores), 2) if engagement_scores else 0,
                'max': max(engagement_scores) if engagement_scores else 0,
                'min': min(engagement_scores) if engagement_scores else 0
            }
        }

    def analyze_building_activity(self, date=None):
        """Analyze what was built"""
        events = self.load_events(date)

        if not events:
            return {
                'built_anything': False,
                'message': 'No building activity detected'
            }

        # Building indicators
        forms_submitted = [e for e in events if e['type'] == 'form_submit']
        project_saves = [e for e in events if e['type'] == 'project_action' and e['data'].get('action') == 'save']
        project_exports = [e for e in events if e['type'] == 'project_action' and e['data'].get('action') == 'export']
        file_uploads = [e for e in events if e['type'] == 'file_upload']
        tools_used = [e for e in events if e['type'] == 'tool_used']

        # Calculate building time (time with tools/forms active)
        building_sessions = defaultdict(list)
        for event in events:
            if event['type'] in ['form_start', 'tool_used', 'field_typing']:
                pin = event['pin']
                timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', ''))
                building_sessions[pin].append(timestamp)

        building_time_per_user = {}
        for pin, timestamps in building_sessions.items():
            if timestamps:
                # Sort timestamps
                timestamps.sort()
                # Calculate total span (rough estimate of building time)
                total_time = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # hours
                building_time_per_user[pin] = total_time

        # Unique tools used per person
        tools_per_user = defaultdict(set)
        for event in tools_used:
            pin = event['pin']
            tool = event['data'].get('tool')
            if tool:
                tools_per_user[pin].add(tool)

        built_anything = (
            len(forms_submitted) > 0 or
            len(project_saves) > 0 or
            len(file_uploads) > 0 or
            sum(building_time_per_user.values()) > 0.5  # More than 30 minutes of building
        )

        return {
            'built_anything': built_anything,
            'forms_submitted': len(forms_submitted),
            'projects_saved': len(project_saves),
            'projects_exported': len(project_exports),
            'files_uploaded': len(file_uploads),
            'tools_used': len(set(e['data'].get('tool') for e in tools_used)),
            'total_building_hours': round(sum(building_time_per_user.values()), 2),
            'builders': [
                {
                    'pin': pin,
                    'hours': round(hours, 2),
                    'tools': list(tools_per_user.get(pin, []))
                }
                for pin, hours in building_time_per_user.items()
            ]
        }

    def generate_daily_report(self, date=None):
        """Generate comprehensive daily report"""
        if date is None:
            date = datetime.now()

        date_str = date.strftime('%Y-%m-%d')

        print(f"\n{'='*70}")
        print(f"📊 ANALYTICS REPORT: {date_str}")
        print(f"{'='*70}\n")

        # Visitor Analysis
        visitors = self.analyze_visitors(date)
        print("👥 VISITORS:")
        print(f"  Total: {visitors['total_visitors']} named + {visitors.get('anonymous_visitors', 0)} anonymous")
        print(f"  Total Time: {round(visitors['total_time_spent_minutes'], 1)} minutes ({round(visitors['total_time_spent_minutes']/60, 1)} hours)")
        print(f"  Avg Time/Visitor: {round(visitors['avg_time_per_visitor_minutes'], 1)} minutes")
        print(f"  Longest Session: {round(visitors['longest_session_minutes'], 1)} minutes")
        print(f"  Active Builders (30+ min): {len(visitors.get('active_builders', []))}")
        if visitors.get('named_visitors'):
            print(f"  Named Visitors: {', '.join(visitors['named_visitors'])}")

        # Engagement Analysis
        print("\n🎯 ENGAGEMENT:")
        engagement = self.analyze_engagement(date)
        print(f"  Total Events: {engagement['total_events']}")
        print(f"  Clicks: {engagement['clicks']['total']} (Buttons: {engagement['clicks']['buttons']}, Links: {engagement['clicks']['links']})")
        print(f"  Forms: {engagement['forms']['started']} started, {engagement['forms']['submitted']} submitted, {engagement['forms']['abandoned']} abandoned")
        print(f"  Form Completion Rate: {engagement['forms']['completion_rate']}%")
        print(f"  Tools Used: {engagement['tools']['total_uses']} times")
        print(f"  Avg Engagement Score: {engagement['engagement_scores']['average']}/100")

        # Building Analysis
        print("\n🔨 BUILDING ACTIVITY:")
        building = self.analyze_building_activity(date)
        print(f"  Built Anything: {'✅ YES' if building['built_anything'] else '❌ NO'}")
        print(f"  Forms Submitted: {building['forms_submitted']}")
        print(f"  Projects Saved: {building['projects_saved']}")
        print(f"  Projects Exported: {building['projects_exported']}")
        print(f"  Files Uploaded: {building['files_uploaded']}")
        print(f"  Total Building Time: {building['total_building_hours']} hours")

        if building.get('builders'):
            print(f"\n  👷 Builders:")
            for builder in building['builders']:
                print(f"    - {builder['pin']}: {builder['hours']} hours, {len(builder['tools'])} tools used")

        # Top Pages
        print("\n📄 TOP PAGES:")
        for page, hits in list(visitors.get('top_pages', {}).items())[:5]:
            print(f"  {page}: {hits} visits")

        # Device Breakdown
        print("\n💻 DEVICES:")
        for device, count in visitors.get('devices', {}).items():
            print(f"  {device}: {count}")

        print(f"\n{'='*70}\n")

        # Save report to file
        report_data = {
            'date': date_str,
            'generated_at': datetime.now().isoformat(),
            'visitors': visitors,
            'engagement': engagement,
            'building': building
        }

        report_file = self.data_dir / f"daily_report_{date_str}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"📝 Report saved to: {report_file}\n")

        return report_data

    def answer_commander_questions(self, date=None):
        """Answer the Commander's specific questions"""
        visitors = self.analyze_visitors(date)
        building = self.analyze_building_activity(date)

        print(f"\n{'='*70}")
        print("🎯 COMMANDER'S QUESTIONS ANSWERED:")
        print(f"{'='*70}\n")

        # Question 1: Is anybody in there?
        print("❓ Is anybody in there?")
        if visitors['total_visitors'] > 0:
            print(f"   ✅ YES - {visitors['total_visitors']} named visitors + {visitors.get('anonymous_visitors', 0)} anonymous")
            print(f"   Named: {', '.join(visitors['named_visitors']) if visitors['named_visitors'] else 'None'}")
        else:
            print("   ❌ NO - No visitors detected")

        # Question 2: Did anybody build anything?
        print("\n❓ Did anybody build anything?")
        if building['built_anything']:
            print(f"   ✅ YES - Building activity detected")
            print(f"   Forms Submitted: {building['forms_submitted']}")
            print(f"   Projects Saved: {building['projects_saved']}")
            print(f"   Files Uploaded: {building['files_uploaded']}")
        else:
            print("   ❌ NO - No building activity detected")

        # Question 3: How many hours of building?
        print("\n❓ How many hours of building?")
        print(f"   ⏱️  {building['total_building_hours']} hours total")
        if building.get('builders'):
            for builder in building['builders']:
                print(f"   - {builder['pin']}: {builder['hours']} hours")

        # Question 4: What was built?
        print("\n❓ What was built?")
        if building['built_anything']:
            print(f"   📊 Activity Summary:")
            print(f"   - {building['forms_submitted']} forms completed")
            print(f"   - {building['projects_saved']} projects saved")
            print(f"   - {building['projects_exported']} projects exported")
            print(f"   - {building['files_uploaded']} files uploaded")
            print(f"   - {building['tools_used']} different tools used")
        else:
            print("   ℹ️  Nothing was built yet")

        print(f"\n{'='*70}\n")


def main():
    """Run analytics aggregator"""
    import argparse

    parser = argparse.ArgumentParser(description='Analytics Aggregator')
    parser.add_argument('--date', type=str, help='Date to analyze (YYYY-MM-DD)', default=None)
    parser.add_argument('--questions', action='store_true', help='Answer Commander questions only')
    args = parser.parse_args()

    # Parse date if provided
    date = None
    if args.date:
        try:
            date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format: {args.date}. Use YYYY-MM-DD")
            return

    aggregator = AnalyticsAggregator()

    if args.questions:
        aggregator.answer_commander_questions(date)
    else:
        aggregator.generate_daily_report(date)


if __name__ == '__main__':
    main()
