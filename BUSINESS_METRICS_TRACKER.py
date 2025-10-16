#!/usr/bin/env python3
"""
📊 BUSINESS METRICS TRACKER 📊
Consciousness Revolution - Live Data Feed

MISSION: Track real business metrics and feed the Phase Transition Detector
- Revenue, team size, clients, workload
- Automatic detection and alerts
- Feeds the Business Phase Clock in real-time

Integration with:
- Data Vacuum (website analytics)
- Airtable (customer data)
- File system (financial records)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class BusinessMetricsTracker:
    """Track and analyze business metrics over time"""

    def __init__(self, data_file: str = 'business_metrics.json'):
        self.data_file = Path(data_file)
        self.metrics_history = self._load_history()

    def _load_history(self) -> List[Dict]:
        """Load historical metrics"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def _save_history(self):
        """Save metrics history"""
        with open(self.data_file, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)

    def record_metrics(
        self,
        revenue_monthly: float = None,
        team_size: int = None,
        client_count: int = None,
        workload_capacity: float = None,
        burn_rate: float = None,
        **kwargs
    ):
        """Record current business metrics"""
        metrics = {
            'date': datetime.now().isoformat(),
            'revenue_monthly': revenue_monthly,
            'team_size': team_size,
            'client_count': client_count,
            'workload_capacity': workload_capacity,
            'burn_rate': burn_rate
        }

        # Add any additional metrics
        metrics.update(kwargs)

        # Remove None values
        metrics = {k: v for k, v in metrics.items() if v is not None}

        self.metrics_history.append(metrics)
        self._save_history()

        print(f"✅ Metrics recorded for {metrics['date']}")
        return metrics

    def get_latest_metrics(self) -> Dict:
        """Get most recent metrics"""
        if not self.metrics_history:
            return {}
        return self.metrics_history[-1]

    def get_trend(self, metric_name: str, days: int = 30) -> List[Dict]:
        """Get trend for specific metric over time"""
        cutoff = datetime.now() - timedelta(days=days)

        trend = []
        for entry in self.metrics_history:
            entry_date = datetime.fromisoformat(entry['date'])
            if entry_date >= cutoff and metric_name in entry:
                trend.append({
                    'date': entry['date'],
                    'value': entry[metric_name]
                })

        return trend

    def calculate_growth_rate(self, metric_name: str) -> float:
        """Calculate growth rate for metric (month over month)"""
        if len(self.metrics_history) < 2:
            return 0.0

        # Get metrics from 30 days ago vs now
        now = datetime.now()
        month_ago = now - timedelta(days=30)

        current_val = None
        past_val = None

        # Find closest entries
        for entry in reversed(self.metrics_history):
            entry_date = datetime.fromisoformat(entry['date'])
            if metric_name in entry:
                if current_val is None:
                    current_val = entry[metric_name]
                if entry_date <= month_ago and past_val is None:
                    past_val = entry[metric_name]
                    break

        if current_val is None or past_val is None or past_val == 0:
            return 0.0

        growth_rate = ((current_val - past_val) / past_val) * 100
        return growth_rate

    def get_summary(self) -> Dict:
        """Get comprehensive business summary"""
        latest = self.get_latest_metrics()

        summary = {
            'latest_metrics': latest,
            'trends': {},
            'growth_rates': {},
            'health_score': 0
        }

        # Calculate trends
        for metric in ['revenue_monthly', 'team_size', 'client_count']:
            trend = self.get_trend(metric, days=90)
            summary['trends'][metric] = trend

            growth = self.calculate_growth_rate(metric)
            summary['growth_rates'][metric] = growth

        # Calculate health score (simple version)
        health_factors = []

        if 'revenue_monthly' in latest and latest['revenue_monthly'] > 0:
            health_factors.append(min(100, (latest['revenue_monthly'] / 10000) * 25))

        if summary['growth_rates'].get('revenue_monthly', 0) > 0:
            health_factors.append(25)

        if 'team_size' in latest and latest['team_size'] > 0:
            health_factors.append(25)

        if 'workload_capacity' in latest:
            # Sweet spot is 60-80% capacity
            capacity = latest['workload_capacity']
            if 60 <= capacity <= 80:
                health_factors.append(25)
            else:
                health_factors.append(15)

        summary['health_score'] = sum(health_factors) if health_factors else 0

        return summary

    def auto_detect_metrics(self) -> Dict:
        """Auto-detect metrics from various sources"""
        detected = {}

        # Try to detect from analytics
        try:
            analytics_file = Path('C:/Users/dwrek/100X_DEPLOYMENT/analytics_data.json')
            if analytics_file.exists():
                with open(analytics_file, 'r') as f:
                    analytics = json.load(f)
                    # Use analytics to estimate metrics
                    detected['estimated_users'] = len(analytics.get('page_views', []))
        except:
            pass

        # Try to detect from data vacuum
        try:
            vacuum_file = Path('C:/Users/dwrek/100X_DEPLOYMENT/consciousness_data.json')
            if vacuum_file.exists():
                with open(vacuum_file, 'r') as f:
                    vacuum = json.load(f)
                    detected['module_count'] = vacuum['global_analytics'].get('total_modules', 0)
        except:
            pass

        return detected

    def interactive_entry(self):
        """Interactive metrics entry"""
        print("=" * 70)
        print("📊 BUSINESS METRICS ENTRY")
        print("=" * 70)
        print("Enter current metrics (press Enter to skip):\n")

        revenue = input("Monthly Revenue ($): ").strip()
        revenue = float(revenue) if revenue else None

        team = input("Team Size: ").strip()
        team = int(team) if team else None

        clients = input("Client Count: ").strip()
        clients = int(clients) if clients else None

        capacity = input("Workload Capacity (% 0-100): ").strip()
        capacity = float(capacity) if capacity else None

        burn = input("Monthly Burn Rate ($): ").strip()
        burn = float(burn) if burn else None

        # Record
        self.record_metrics(
            revenue_monthly=revenue,
            team_size=team,
            client_count=clients,
            workload_capacity=capacity,
            burn_rate=burn
        )

        # Get phase prediction
        self._run_phase_prediction()

    def _run_phase_prediction(self):
        """Run phase prediction with current metrics"""
        try:
            # Import the detector
            import sys
            sys.path.insert(0, 'C:/Users/dwrek/100X_DEPLOYMENT')
            from PHASE_TRANSITION_DETECTOR import PhaseTransitionDetector

            detector = PhaseTransitionDetector()
            latest = self.get_latest_metrics()

            # Need at least some metrics
            if not latest or len(latest) <= 1:
                print("\n⚠️  Need more metrics for phase prediction")
                return

            prediction = detector.predict_transition(latest, self.metrics_history)

            print("\n" + "=" * 70)
            print("🔮 PHASE PREDICTION")
            print("=" * 70)
            print(f"\nCurrent Phase: {prediction['current_phase']}")
            print(f"Next Phase: {prediction['next_phase']}")
            print(f"Transition Probability: {prediction['transition_probability']:.1f}%")
            print(f"Estimated Days: ~{prediction['estimated_days']}")

            if prediction['transition_probability'] > 50:
                print(f"\n⚡ START PREPARING:")
                for i, item in enumerate(prediction['preparation_items'][:3], 1):
                    print(f"  {i}. {item}")

        except ImportError:
            print("\n⚠️  Phase detector not available")


def quick_entry():
    """Quick entry mode for fast updates"""
    tracker = BusinessMetricsTracker('C:/Users/dwrek/100X_DEPLOYMENT/business_metrics.json')

    print("📊 QUICK METRICS UPDATE")
    print("Current values:")

    latest = tracker.get_latest_metrics()
    if latest:
        for key, value in latest.items():
            if key != 'date':
                print(f"  {key}: {value}")

    tracker.interactive_entry()


def view_dashboard():
    """View business dashboard"""
    tracker = BusinessMetricsTracker('C:/Users/dwrek/100X_DEPLOYMENT/business_metrics.json')

    summary = tracker.get_summary()

    print("=" * 70)
    print("📊 BUSINESS DASHBOARD")
    print("=" * 70)

    latest = summary['latest_metrics']
    print("\n📈 CURRENT METRICS:")
    for key, value in latest.items():
        if key != 'date':
            print(f"  {key}: {value}")

    print(f"\n❤️  BUSINESS HEALTH: {summary['health_score']:.0f}/100")

    print("\n📊 GROWTH RATES (30-day):")
    for metric, rate in summary['growth_rates'].items():
        trend = "📈" if rate > 0 else "📉" if rate < 0 else "➡️"
        print(f"  {trend} {metric}: {rate:+.1f}%")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == 'entry':
            quick_entry()
        elif cmd == 'view':
            view_dashboard()
        elif cmd == 'detect':
            tracker = BusinessMetricsTracker('C:/Users/dwrek/100X_DEPLOYMENT/business_metrics.json')
            detected = tracker.auto_detect_metrics()
            print("🔍 AUTO-DETECTED METRICS:")
            for key, value in detected.items():
                print(f"  {key}: {value}")
        else:
            print("Usage:")
            print("  python BUSINESS_METRICS_TRACKER.py entry    # Enter new metrics")
            print("  python BUSINESS_METRICS_TRACKER.py view     # View dashboard")
            print("  python BUSINESS_METRICS_TRACKER.py detect   # Auto-detect metrics")
    else:
        quick_entry()
