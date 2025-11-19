"""
🧠 CONSCIOUSNESS DETECTOR - Behavior Analysis for USB System
Detects builder vs destroyer intent through behavior patterns
No red tape, just smart observation
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path

class ConsciousnessDetector:
    def __init__(self, usb_root):
        self.usb_root = Path(usb_root)
        self.log_file = self.usb_root / ".consciousness_log.json"
        self.score = 0
        self.session_start = time.time()
        self.actions = []

        # Load previous session if exists
        self.load_session()

    def load_session(self):
        """Load previous session data"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.score = data.get('score', 0)
                    self.actions = data.get('actions', [])
            except:
                pass

    def save_session(self):
        """Save session data"""
        data = {
            'score': self.score,
            'actions': self.actions[-50:],  # Keep last 50 actions
            'last_update': datetime.now().isoformat(),
            'session_duration': time.time() - self.session_start
        }

        try:
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass

    def track_file_access(self, filepath, action='read'):
        """Track when files are accessed"""
        filename = Path(filepath).name.lower()

        # Positive signals (Builder behavior)
        if action == 'read':
            if filename in ['readme.txt', 'readme.md', 'start_here.html']:
                self.add_score(15, f"Read {filename} first (builder signal)")
            elif filename.endswith('.md') or filename.endswith('.txt'):
                self.add_score(5, f"Read documentation: {filename}")
            elif filename.endswith('.html'):
                self.add_score(3, f"Explored content: {filename}")

        # Negative signals (Destroyer behavior)
        if action == 'execute' and len(self.actions) < 3:
            self.add_score(-25, f"Tried to execute {filename} without reading docs")

        if action == 'modify':
            self.add_score(-30, f"Attempted to modify {filename} without permission")

        if action == 'scan' and (time.time() - self.session_start) < 60:
            self.add_score(-15, f"Rapid scanning detected (looking for exploits?)")

    def track_time_spent(self, filepath, duration_seconds):
        """Track how long they spend on content"""
        if duration_seconds > 60:  # Over 1 minute
            self.add_score(10, f"Spent {duration_seconds}s reading (patient builder)")
        elif duration_seconds < 10:  # Less than 10 seconds
            self.add_score(-5, f"Only spent {duration_seconds}s (impatient)")

    def track_sequence(self):
        """Analyze the sequence of actions"""
        if len(self.actions) < 3:
            return

        # Check if they started with documentation
        first_three = [a['description'] for a in self.actions[:3]]

        if any('Read readme' in a or 'Read documentation' in a for a in first_three):
            self.add_score(20, "Started with documentation (excellent builder signal)")

        # Check for suspicious patterns
        if sum('execute' in a.lower() for a in first_three) > 1:
            self.add_score(-20, "Multiple execution attempts before understanding")

    def check_boundaries(self, attempted_action):
        """Check if they respect boundaries"""
        forbidden_actions = [
            'access system files',
            'modify registry',
            'install without permission',
            'network scan',
            'port scan'
        ]

        if any(forbidden in attempted_action.lower() for forbidden in forbidden_actions):
            self.add_score(-50, f"Attempted forbidden action: {attempted_action}")
            return False

        return True

    def add_score(self, points, reason):
        """Add points and log the reason"""
        self.score += points

        action = {
            'timestamp': datetime.now().isoformat(),
            'points': points,
            'description': reason,
            'total_score': self.score
        }

        self.actions.append(action)
        self.save_session()

        print(f"{'✅' if points > 0 else '⚠️'} {reason} ({points:+d} pts, total: {self.score})")

    def get_consciousness_level(self):
        """Calculate consciousness level from score"""
        if self.score >= 100:
            return 'enlightened'
        elif self.score >= 50:
            return 'advanced'
        elif self.score >= 0:
            return 'builder'
        elif self.score >= -20:
            return 'confused'
        else:
            return 'destroyer'

    def get_access_level(self):
        """Determine what content they can access"""
        level = self.get_consciousness_level()

        access_levels = {
            'enlightened': {
                'level': 3,
                'name': 'Full Access',
                'description': 'All advanced consciousness tools unlocked',
                'folders': ['public', 'builders', 'advanced']
            },
            'advanced': {
                'level': 2,
                'name': 'Builder Access',
                'description': 'Builder tools and community access',
                'folders': ['public', 'builders']
            },
            'builder': {
                'level': 1,
                'name': 'Standard Access',
                'description': 'Introduction and basic tools',
                'folders': ['public']
            },
            'confused': {
                'level': 0,
                'name': 'Limited Access',
                'description': 'Basic documentation only',
                'folders': ['public']
            },
            'destroyer': {
                'level': -1,
                'name': 'De-Throttled',
                'description': 'Content simplified to prevent misuse',
                'folders': ['decoy']
            }
        }

        return access_levels[level]

    def should_de_throttle(self):
        """Check if content should be de-throttled"""
        return self.score < -20

    def get_report(self):
        """Generate behavior report"""
        session_duration = time.time() - self.session_start
        level = self.get_consciousness_level()
        access = self.get_access_level()

        report = {
            'score': self.score,
            'consciousness_level': level,
            'access_level': access,
            'session_duration': session_duration,
            'total_actions': len(self.actions),
            'recent_actions': self.actions[-10:],
            'recommendations': self.get_recommendations()
        }

        return report

    def get_recommendations(self):
        """Get recommendations based on behavior"""
        level = self.get_consciousness_level()

        if level == 'destroyer':
            return [
                "Pattern detected: Destructive intent",
                "Content has been simplified",
                "Visit consciousnessrevolution.io to learn more",
                "Start with documentation next time"
            ]
        elif level == 'confused':
            return [
                "Tip: Start with README.txt",
                "Take your time with the materials",
                "Understanding comes before action",
                "No rush - consciousness unfolds naturally"
            ]
        elif level == 'builder':
            return [
                "Good start! Keep exploring",
                "Check out the /builders folder",
                "Join the meritocracy system",
                "Contribute to earn more access"
            ]
        elif level == 'advanced':
            return [
                "Excellent builder behavior detected",
                "Advanced tools are now available",
                "Consider joining Trinity AI collaboration",
                "Your contributions matter"
            ]
        else:  # enlightened
            return [
                "Welcome, enlightened builder",
                "Full system access granted",
                "Your consciousness level is exceptional",
                "Help others reach this level"
            ]


# Command-line interface
if __name__ == "__main__":
    import sys

    print("="*60)
    print("🧠 CONSCIOUSNESS DETECTOR")
    print("="*60)

    # Get USB root (or use current directory for testing)
    usb_root = sys.argv[1] if len(sys.argv) > 1 else "."

    detector = ConsciousnessDetector(usb_root)

    print(f"\nCurrent Score: {detector.score}")
    print(f"Consciousness Level: {detector.get_consciousness_level()}")
    print(f"Access Level: {detector.get_access_level()['name']}")

    # Interactive mode
    print("\n" + "="*60)
    print("TESTING MODE - Simulate user behavior")
    print("="*60)
    print("\nCommands:")
    print("  read <filename>   - Track reading a file")
    print("  exec <filename>   - Track executing a file")
    print("  modify <filename> - Track modifying a file")
    print("  time <seconds>    - Track time spent")
    print("  report            - Show full report")
    print("  quit              - Exit")
    print()

    while True:
        try:
            cmd = input(">>> ").strip().lower()

            if not cmd:
                continue

            if cmd == 'quit':
                break

            if cmd == 'report':
                report = detector.get_report()
                print(json.dumps(report, indent=2))
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0]

            if action == 'read' and len(parts) > 1:
                detector.track_file_access(parts[1], 'read')

            elif action == 'exec' and len(parts) > 1:
                detector.track_file_access(parts[1], 'execute')

            elif action == 'modify' and len(parts) > 1:
                detector.track_file_access(parts[1], 'modify')

            elif action == 'time' and len(parts) > 1:
                detector.track_time_spent("content", int(parts[1]))

            else:
                print("Unknown command")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    print("\n" + "="*60)
    print("Final Report:")
    print("="*60)
    report = detector.get_report()
    print(f"Score: {report['score']}")
    print(f"Level: {report['consciousness_level']}")
    print(f"Access: {report['access_level']['name']}")
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
