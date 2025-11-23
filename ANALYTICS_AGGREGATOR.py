#!/usr/bin/env python3
"""
ANALYTICS AGGREGATOR
Processes raw analytics events into actionable insights
Generates daily/weekly/monthly reports
Detects patterns and anomalies
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import statistics

class AnalyticsAggregator:
    def __init__(self, data_dir='visitor_data/analytics'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_events_for_date(self, date_str):
        """Load all events for a specific date"""
        events_file = self.data_dir / f"events_{date_str}.jsonl"

        if not events_file.exists():
            return []

        events = []
        with open(events_file, 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return events

    def load_events_for_period(self, start_date, end_date):
        """Load all events for a date range"""
        all_events = []
        current_date = start_date

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            all_events.extend(self.load_events_for_date(date_str))
            current_date += timedelta(days=1)

        return all_events

    def aggregate_daily(self, date_str):
        """Generate daily summary report"""
        events = self.load_events_for_date(date_str)

        if not events:
            return {
                'date': date_str,
                'summary': 'No data',
                'total_events': 0
            }

        # Extract metrics
        sessions = set(e.get('sessionId') for e in events if e.get('sessionId'))
        visitors = set(e.get('pin') for e in events if e.get('pin'))
        pages = set(e.get('page') for e in events if e.get('page'))

        event_types = Counter(e.get('eventType') for e in events)
        pages_visited = Counter(e.get('page') for e in events if e.get('eventType') == 'page_enter')

        # Calculate session metrics
        session_events = defaultdict(list)
        for event in events:
            sid = event.get('sessionId')
            if sid:
                session_events[sid].append(event)

        session_durations = []
        session_actions = []
        session_quality_scores = []

        for sid, session_evts in session_events.items():
            if len(session_evts) > 1:
                # Approximate duration based on number of events
                session_durations.append(len(session_evts) * 10)  # ~10 seconds per event

            # Count actions (clicks, scrolls, etc.)
            actions = [e for e in session_evts if e.get('eventType') in ['click', 'scroll', 'form_submit', 'tool_used']]
            session_actions.append(len(actions))

            # Get quality score if available
            quality_events = [e for e in session_evts if e.get('eventType') == 'page_exit']
            for qe in quality_events:
                score = qe.get('eventData', {}).get('qualityScore')
                if score is not None:
                    session_quality_scores.append(score)

        # Form analytics
        form_starts = [e for e in events if e.get('eventType') == 'form_start']
        form_submits = [e for e in events if e.get('eventType') == 'form_submit']
        form_abandons = [e for e in events if e.get('eventType') == 'form_abandon']

        # Engagement metrics
        clicks = [e for e in events if e.get('eventType') == 'click']
        scrolls = [e for e in events if e.get('eventType') == 'scroll']

        # Building activity
        tool_uses = [e for e in events if e.get('eventType') == 'tool_used']
        project_saves = [e for e in events if e.get('eventType') == 'project_save']

        summary = {
            'date': date_str,
            'overview': {
                'total_events': len(events),
                'unique_visitors': len(visitors),
                'unique_sessions': len(sessions),
                'unique_pages': len(pages)
            },
            'traffic': {
                'page_views': event_types.get('page_enter', 0),
                'avg_pages_per_session': event_types.get('page_enter', 0) / len(sessions) if sessions else 0,
                'top_pages': dict(pages_visited.most_common(10))
            },
            'engagement': {
                'total_clicks': len(clicks),
                'total_scrolls': len(scrolls),
                'avg_clicks_per_session': len(clicks) / len(sessions) if sessions else 0,
                'avg_session_duration_seconds': statistics.mean(session_durations) if session_durations else 0,
                'avg_session_actions': statistics.mean(session_actions) if session_actions else 0,
                'avg_quality_score': statistics.mean(session_quality_scores) if session_quality_scores else 0
            },
            'forms': {
                'starts': len(form_starts),
                'submits': len(form_submits),
                'abandons': len(form_abandons),
                'completion_rate': (len(form_submits) / len(form_starts) * 100) if form_starts else 0
            },
            'building': {
                'tool_uses': len(tool_uses),
                'project_saves': len(project_saves),
                'builders_active': len(set(e.get('sessionId') for e in tool_uses if e.get('sessionId')))
            },
            'conversion': {
                'visitors': len(visitors),
                'started_building': len(set(e.get('sessionId') for e in form_starts if e.get('sessionId'))),
                'completed_projects': len(set(e.get('sessionId') for e in form_submits if e.get('sessionId'))),
                'conversion_rate': (len(form_submits) / len(visitors) * 100) if visitors else 0
            },
            'hourly_distribution': self._calculate_hourly_distribution(events)
        }

        return summary

    def _calculate_hourly_distribution(self, events):
        """Calculate event distribution by hour of day"""
        hourly = defaultdict(int)

        for event in events:
            try:
                timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                hour = timestamp.hour
                hourly[hour] += 1
            except (KeyError, ValueError):
                continue

        return dict(sorted(hourly.items()))

    def detect_patterns(self, events):
        """Detect common user journeys and patterns"""
        # Group events by session
        session_paths = defaultdict(list)

        for event in events:
            sid = event.get('sessionId')
            if sid and event.get('eventType') == 'page_enter':
                page = event.get('page', '/')
                session_paths[sid].append(page)

        # Find common paths
        path_counter = Counter()

        for sid, path in session_paths.items():
            if len(path) > 1:
                # Create path string
                path_str = ' → '.join(path[:5])  # First 5 pages
                path_counter[path_str] += 1

        return {
            'total_unique_paths': len(session_paths),
            'common_journeys': dict(path_counter.most_common(10)),
            'single_page_sessions': sum(1 for path in session_paths.values() if len(path) == 1),
            'multi_page_sessions': sum(1 for path in session_paths.values() if len(path) > 1)
        }

    def detect_anomalies(self, daily_summary, historical_summaries):
        """Detect unusual patterns compared to historical data"""
        anomalies = []

        if not historical_summaries:
            return anomalies

        # Calculate historical averages
        historical_visitors = [s['overview']['unique_visitors'] for s in historical_summaries]
        historical_sessions = [s['overview']['unique_sessions'] for s in historical_summaries]
        historical_events = [s['overview']['total_events'] for s in historical_summaries]

        if historical_visitors:
            avg_visitors = statistics.mean(historical_visitors)
            std_visitors = statistics.stdev(historical_visitors) if len(historical_visitors) > 1 else 0

            current_visitors = daily_summary['overview']['unique_visitors']

            # Check for anomalies (2 standard deviations from mean)
            if std_visitors > 0:
                if current_visitors > avg_visitors + (2 * std_visitors):
                    anomalies.append({
                        'type': 'traffic_spike',
                        'metric': 'unique_visitors',
                        'current': current_visitors,
                        'average': avg_visitors,
                        'deviation': (current_visitors - avg_visitors) / std_visitors
                    })
                elif current_visitors < avg_visitors - (2 * std_visitors):
                    anomalies.append({
                        'type': 'traffic_drop',
                        'metric': 'unique_visitors',
                        'current': current_visitors,
                        'average': avg_visitors,
                        'deviation': (current_visitors - avg_visitors) / std_visitors
                    })

        return anomalies

    def generate_daily_report(self, date_str):
        """Generate complete daily report"""
        summary = self.aggregate_daily(date_str)
        events = self.load_events_for_date(date_str)

        if not events:
            return summary

        patterns = self.detect_patterns(events)

        # Load last 7 days for anomaly detection
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        historical = []

        for i in range(1, 8):
            past_date = (date_obj - timedelta(days=i)).strftime('%Y-%m-%d')
            past_summary = self.aggregate_daily(past_date)
            if past_summary.get('overview', {}).get('total_events', 0) > 0:
                historical.append(past_summary)

        anomalies = self.detect_anomalies(summary, historical)

        report = {
            **summary,
            'patterns': patterns,
            'anomalies': anomalies,
            'generated_at': datetime.now().isoformat()
        }

        # Save report
        report_file = self.data_dir / f"daily_report_{date_str}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Generated daily report: {date_str}")
        return report

    def generate_weekly_report(self, end_date_str):
        """Generate weekly report (last 7 days)"""
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=6)

        events = self.load_events_for_period(start_date, end_date)

        # Aggregate across week
        visitors = set(e.get('pin') for e in events if e.get('pin'))
        sessions = set(e.get('sessionId') for e in events if e.get('sessionId'))

        daily_visitors = defaultdict(set)
        for event in events:
            if event.get('pin') and event.get('timestamp'):
                event_date = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00')).date()
                daily_visitors[event_date].add(event.get('pin'))

        report = {
            'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date_str}",
            'total_visitors': len(visitors),
            'total_sessions': len(sessions),
            'total_events': len(events),
            'daily_active_users': {str(date): len(pins) for date, pins in daily_visitors.items()},
            'avg_daily_visitors': len(visitors) / 7,
            'retention': self._calculate_retention(daily_visitors),
            'generated_at': datetime.now().isoformat()
        }

        # Save report
        report_file = self.data_dir / f"weekly_report_{end_date_str}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def _calculate_retention(self, daily_visitors):
        """Calculate day-over-day retention"""
        dates = sorted(daily_visitors.keys())

        if len(dates) < 2:
            return {}

        retention = {}
        for i in range(len(dates) - 1):
            day1 = dates[i]
            day2 = dates[i + 1]

            returning = daily_visitors[day1] & daily_visitors[day2]
            retention[f"{day1} to {day2}"] = {
                'day1_visitors': len(daily_visitors[day1]),
                'returning_next_day': len(returning),
                'retention_rate': (len(returning) / len(daily_visitors[day1]) * 100) if daily_visitors[day1] else 0
            }

        return retention


def main():
    """Generate reports for today"""
    aggregator = AnalyticsAggregator()

    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    print("=" * 60)
    print("📊 ANALYTICS AGGREGATOR")
    print("=" * 60)

    # Generate today's report
    print(f"\n[*] Generating daily report for {today}...")
    today_report = aggregator.generate_daily_report(today)

    print(f"\n[*] Summary for {today}:")
    print(f"  - Unique Visitors: {today_report['overview']['unique_visitors']}")
    print(f"  - Sessions: {today_report['overview']['unique_sessions']}")
    print(f"  - Total Events: {today_report['overview']['total_events']}")
    print(f"  - Avg Quality Score: {today_report['engagement']['avg_quality_score']:.1f}/100")

    # Generate weekly report
    print(f"\n[*] Generating weekly report...")
    weekly_report = aggregator.generate_weekly_report(today)

    print(f"\n[*] Weekly Summary:")
    print(f"  - Total Visitors: {weekly_report['total_visitors']}")
    print(f"  - Avg Daily Visitors: {weekly_report['avg_daily_visitors']:.1f}")

    print("\n[OK] Analytics aggregation complete!")


if __name__ == '__main__':
    main()
