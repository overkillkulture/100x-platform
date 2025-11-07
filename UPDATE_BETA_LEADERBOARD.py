"""
BETA LEADERBOARD UPDATER
Autonomous system to track beta tester progress
"""

import json
import os
from datetime import datetime
from pathlib import Path

TRACKER_FILE = Path("C:/Users/dwrek/100X_DEPLOYMENT/BETA_TESTER_DEDICATION_TRACKER.json")

class BetaLeaderboardUpdater:
    def __init__(self):
        """Initialize updater"""
        self.tracker_data = self.load_tracker()

    def load_tracker(self):
        """Load tracker JSON"""
        with open(TRACKER_FILE) as f:
            return json.load(f)

    def save_tracker(self):
        """Save updated tracker"""
        with open(TRACKER_FILE, 'w') as f:
            json.dump(self.tracker_data, f, indent=2)
        print(f"✅ Tracker updated: {TRACKER_FILE}")

    def calculate_total_points(self, tester):
        """Calculate total points for a tester"""
        tasks = tester['tasks']
        total = 0

        # Task 1: Bugs (20 points)
        total += tasks['task_1_bugs']['points_earned']

        # Task 2: Feature (10 points)
        total += tasks['task_2_feature']['points_earned']

        # Task 3: Confusion (15 points)
        total += tasks['task_3_confusion']['points_earned']

        # Task 4: Deep test (25 points)
        total += tasks['task_4_deep_test']['points_earned']

        # Task 5: Referral (30 points bonus)
        total += tasks['task_5_referral']['points_earned']

        # Early bird bonus (10 points)
        total += tasks['early_bird_bonus']['points_earned']

        return total

    def assign_tier(self, points):
        """Assign tier based on points"""
        if points >= 70:
            return ("INSIDER", "🥇")
        elif points >= 40:
            return ("ACTIVE", "🥈")
        elif points >= 10:
            return ("CASUAL", "🥉")
        else:
            return ("INACTIVE", "⛔")

    def mark_bug_submitted(self, pin, bug_id):
        """Mark a bug as submitted for a tester"""
        for tester in self.tracker_data['beta_testers']:
            if tester['pin'] == pin:
                bugs = tester['tasks']['task_1_bugs']

                # Add bug ID
                if bug_id not in bugs['bug_ids']:
                    bugs['bug_ids'].append(bug_id)
                    bugs['bugs_submitted'] = len(bugs['bug_ids'])

                # Check if completed (need 3 bugs)
                if bugs['bugs_submitted'] >= bugs['bugs_required']:
                    bugs['completed'] = True
                    bugs['points_earned'] = bugs['points_possible']
                    print(f"🐛 PIN {pin}: Task 1 COMPLETE ({bugs['bugs_submitted']} bugs)")
                else:
                    print(f"🐛 PIN {pin}: Bug #{bugs['bugs_submitted']} submitted ({bugs['bugs_required'] - bugs['bugs_submitted']} more needed)")

                # Recalculate total points
                tester['total_points'] = self.calculate_total_points(tester)
                tester['tier'], tester['tier_badge'] = self.assign_tier(tester['total_points'])

                return True

        print(f"⚠️  PIN {pin} not found")
        return False

    def mark_feature_requested(self, pin, feature_text):
        """Mark feature request as submitted"""
        for tester in self.tracker_data['beta_testers']:
            if tester['pin'] == pin:
                feature = tester['tasks']['task_2_feature']

                if not feature['completed']:
                    feature['completed'] = True
                    feature['points_earned'] = feature['points_possible']
                    feature['feature_request'] = feature_text
                    print(f"💡 PIN {pin}: Task 2 COMPLETE (feature requested)")

                    # Recalculate total points
                    tester['total_points'] = self.calculate_total_points(tester)
                    tester['tier'], tester['tier_badge'] = self.assign_tier(tester['total_points'])

                    return True
                else:
                    print(f"⚠️  PIN {pin}: Task 2 already complete")
                    return False

        print(f"⚠️  PIN {pin} not found")
        return False

    def mark_confusion_reported(self, pin, confusion_text):
        """Mark confusion report as submitted"""
        for tester in self.tracker_data['beta_testers']:
            if tester['pin'] == pin:
                confusion = tester['tasks']['task_3_confusion']

                if not confusion['completed']:
                    confusion['completed'] = True
                    confusion['points_earned'] = confusion['points_possible']
                    confusion['confusion_report'] = confusion_text
                    print(f"🤔 PIN {pin}: Task 3 COMPLETE (confusion reported)")

                    # Recalculate total points
                    tester['total_points'] = self.calculate_total_points(tester)
                    tester['tier'], tester['tier_badge'] = self.assign_tier(tester['total_points'])

                    return True
                else:
                    print(f"⚠️  PIN {pin}: Task 3 already complete")
                    return False

        print(f"⚠️  PIN {pin} not found")
        return False

    def mark_deep_test_completed(self, pin, system_tested, report_text):
        """Mark deep test as completed"""
        for tester in self.tracker_data['beta_testers']:
            if tester['pin'] == pin:
                deep_test = tester['tasks']['task_4_deep_test']

                if not deep_test['completed']:
                    deep_test['completed'] = True
                    deep_test['points_earned'] = deep_test['points_possible']
                    deep_test['system_tested'] = system_tested
                    deep_test['report'] = report_text
                    print(f"🔬 PIN {pin}: Task 4 COMPLETE (tested {system_tested})")

                    # Recalculate total points
                    tester['total_points'] = self.calculate_total_points(tester)
                    tester['tier'], tester['tier_badge'] = self.assign_tier(tester['total_points'])

                    return True
                else:
                    print(f"⚠️  PIN {pin}: Task 4 already complete")
                    return False

        print(f"⚠️  PIN {pin} not found")
        return False

    def mark_referral(self, pin, referral_name, referral_email):
        """Mark referral as made"""
        for tester in self.tracker_data['beta_testers']:
            if tester['pin'] == pin:
                referral = tester['tasks']['task_5_referral']

                if not referral['completed']:
                    referral['completed'] = True
                    referral['points_earned'] = referral['points_possible']
                    referral['referral_name'] = referral_name
                    referral['referral_email'] = referral_email
                    print(f"👥 PIN {pin}: Task 5 COMPLETE (referred {referral_name})")

                    # Recalculate total points
                    tester['total_points'] = self.calculate_total_points(tester)
                    tester['tier'], tester['tier_badge'] = self.assign_tier(tester['total_points'])

                    return True
                else:
                    print(f"⚠️  PIN {pin}: Task 5 already complete")
                    return False

        print(f"⚠️  PIN {pin} not found")
        return False

    def check_early_bird_bonus(self):
        """Check if testers qualify for early bird bonus (complete all by Nov 8)"""
        early_bird_deadline = datetime(2025, 11, 8, 23, 59, 59)
        now = datetime.now()

        if now > early_bird_deadline:
            print("⏰ Early bird deadline passed")
            return

        for tester in self.tracker_data['beta_testers']:
            tasks = tester['tasks']

            # Check if all 5 main tasks complete
            all_complete = (
                tasks['task_1_bugs']['completed'] and
                tasks['task_2_feature']['completed'] and
                tasks['task_3_confusion']['completed'] and
                tasks['task_4_deep_test']['completed']
            )

            if all_complete and not tasks['early_bird_bonus']['completed']:
                tasks['early_bird_bonus']['completed'] = True
                tasks['early_bird_bonus']['points_earned'] = tasks['early_bird_bonus']['points_possible']

                # Recalculate total points
                tester['total_points'] = self.calculate_total_points(tester)
                tester['tier'], tester['tier_badge'] = self.assign_tier(tester['total_points'])

                print(f"🎉 PIN {tester['pin']}: EARLY BIRD BONUS (+10 points)!")

    def log_update(self, action, note):
        """Log an update to tracker"""
        self.tracker_data['update_log'].append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'note': note
        })

    def show_leaderboard(self):
        """Display current leaderboard"""
        print("\n" + "="*70)
        print("🏆 BETA TESTER LEADERBOARD")
        print("="*70)

        # Sort by points
        sorted_testers = sorted(
            self.tracker_data['beta_testers'],
            key=lambda t: t['total_points'],
            reverse=True
        )

        print(f"\n{'Rank':<6} {'PIN':<8} {'Points':<8} {'Tier':<12} {'Tasks':<8}")
        print("-" * 70)

        for i, tester in enumerate(sorted_testers):
            rank = i + 1
            pin = tester['pin']
            points = tester['total_points']
            tier = f"{tester['tier_badge']} {tester['tier']}"

            # Count completed tasks
            completed = sum([
                1 for task in tester['tasks'].values()
                if isinstance(task, dict) and task.get('completed', False)
            ])
            tasks_display = f"{completed}/5"

            print(f"#{rank:<5} {pin:<8} {points:<8} {tier:<12} {tasks_display:<8}")

        print("="*70)

        # Show tier distribution
        insider = sum(1 for t in sorted_testers if t['total_points'] >= 70)
        active = sum(1 for t in sorted_testers if 40 <= t['total_points'] < 70)
        casual = sum(1 for t in sorted_testers if 10 <= t['total_points'] < 40)
        inactive = sum(1 for t in sorted_testers if t['total_points'] < 10)

        print(f"\n📊 TIER DISTRIBUTION:")
        print(f"   🥇 INSIDER:  {insider} testers")
        print(f"   🥈 ACTIVE:   {active} testers")
        print(f"   🥉 CASUAL:   {casual} testers")
        print(f"   ⛔ INACTIVE: {inactive} testers")
        print()


def interactive_menu():
    """Interactive menu for updating leaderboard"""
    updater = BetaLeaderboardUpdater()

    while True:
        print("\n" + "="*70)
        print("📊 BETA LEADERBOARD UPDATER")
        print("="*70)
        print("\n1. Mark bug submitted")
        print("2. Mark feature requested")
        print("3. Mark confusion reported")
        print("4. Mark deep test completed")
        print("5. Mark referral made")
        print("6. Check early bird bonus")
        print("7. Show current leaderboard")
        print("8. Save and exit")
        print()

        choice = input("Enter choice (1-8): ").strip()

        if choice == '1':
            pin = int(input("Enter PIN: "))
            bug_id = input("Enter bug ID (e.g., #123): ")
            updater.mark_bug_submitted(pin, bug_id)

        elif choice == '2':
            pin = int(input("Enter PIN: "))
            feature = input("Enter feature request: ")
            updater.mark_feature_requested(pin, feature)

        elif choice == '3':
            pin = int(input("Enter PIN: "))
            confusion = input("Enter confusion report: ")
            updater.mark_confusion_reported(pin, confusion)

        elif choice == '4':
            pin = int(input("Enter PIN: "))
            system = input("Enter system tested: ")
            report = input("Enter report summary: ")
            updater.mark_deep_test_completed(pin, system, report)

        elif choice == '5':
            pin = int(input("Enter PIN: "))
            name = input("Enter referral name: ")
            email = input("Enter referral email: ")
            updater.mark_referral(pin, name, email)

        elif choice == '6':
            updater.check_early_bird_bonus()

        elif choice == '7':
            updater.show_leaderboard()

        elif choice == '8':
            updater.save_tracker()
            print("\n✅ Leaderboard updated and saved!")
            print(f"📁 File: {TRACKER_FILE}")
            print(f"🌐 View leaderboard: C:/Users/dwrek/100X_DEPLOYMENT/beta-leaderboard.html")
            break

        else:
            print("❌ Invalid choice")


if __name__ == '__main__':
    print("\n🏆 BETA TESTER LEADERBOARD UPDATER")
    print("="*70)
    print()

    interactive_menu()
