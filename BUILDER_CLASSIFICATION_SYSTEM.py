"""
BUILDER vs WHINER CLASSIFICATION SYSTEM
Automatically classify users based on their behavior

Commander's vision: "Sheep herd them around and make them try out the interface
and make them have to fix it. That'll test them to see if they're a builder or a whiner."

This system:
1. Tracks user actions
2. Classifies as Builder or Whiner
3. Rewards builders, filters whiners
4. Auto-onboarding gauntlet
"""
import json
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# User data storage
USERS_DIR = Path('C:/Users/dwrek/100X_DEPLOYMENT/USER_PROFILES')
USERS_DIR.mkdir(exist_ok=True)

# Classification weights
BUILDER_ACTIONS = {
    'fixed_bug': 10,
    'built_feature': 15,
    'submitted_code': 12,
    'helped_other_user': 8,
    'completed_challenge': 10,
    'improved_interface': 15,
    'found_solution': 7,
    'asked_good_question': 5,
    'read_docs': 2,
    'explored_system': 3
}

WHINER_ACTIONS = {
    'complained': -5,
    'gave_up': -10,
    'blamed_system': -8,
    'demanded_help': -6,
    'ignored_instructions': -7,
    'spammed': -12,
    'trolled': -15,
    'asked_lazy_question': -3,
    'skipped_challenge': -8
}


class UserProfile:
    def __init__(self, user_id, name=None):
        self.user_id = user_id
        self.name = name or user_id
        self.joined_at = datetime.now().isoformat()
        self.builder_score = 0
        self.whiner_score = 0
        self.actions = []
        self.builds = []
        self.tokens_used = 0
        self.araya_conversations = []
        self.challenges_completed = []
        self.challenges_failed = []
        self.time_in_system = 0
        self.classification = 'UNKNOWN'

    def add_action(self, action_type, details=None):
        """Record an action and update scores"""
        action = {
            'type': action_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.actions.append(action)

        # Update scores
        if action_type in BUILDER_ACTIONS:
            self.builder_score += BUILDER_ACTIONS[action_type]
        elif action_type in WHINER_ACTIONS:
            self.whiner_score += WHINER_ACTIONS[action_type]

        # Reclassify
        self.classify()

        return action

    def classify(self):
        """Classify user as Builder, Whiner, or Unknown"""
        total_score = self.builder_score + self.whiner_score

        if total_score >= 30:
            self.classification = 'BUILDER'
        elif total_score <= -20:
            self.classification = 'WHINER'
        elif len(self.actions) > 10:
            # After 10 actions, lean toward classification
            if self.builder_score > abs(self.whiner_score):
                self.classification = 'EMERGING_BUILDER'
            else:
                self.classification = 'POTENTIAL_WHINER'
        else:
            self.classification = 'UNKNOWN'

        return self.classification

    def add_build(self, build_name, description):
        """Record something they built"""
        build = {
            'name': build_name,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        self.builds.append(build)
        self.add_action('built_feature', {'build': build_name})

    def add_araya_conversation(self, message, response):
        """Log Araya conversation"""
        conversation = {
            'user_message': message,
            'araya_response': response,
            'timestamp': datetime.now().isoformat()
        }
        self.araya_conversations.append(conversation)

        # Analyze if they're asking good questions or whining
        if any(word in message.lower() for word in ['how do i', 'can you help', 'what if']):
            self.add_action('asked_good_question')
        elif any(word in message.lower() for word in ['this sucks', 'doesnt work', 'broken', 'stupid']):
            self.add_action('complained')

    def use_tokens(self, count):
        """Track token usage"""
        self.tokens_used += count

    def complete_challenge(self, challenge_name):
        """Mark challenge as complete"""
        self.challenges_completed.append({
            'challenge': challenge_name,
            'timestamp': datetime.now().isoformat()
        })
        self.add_action('completed_challenge', {'challenge': challenge_name})

    def fail_challenge(self, challenge_name, reason):
        """Mark challenge as failed"""
        self.challenges_failed.append({
            'challenge': challenge_name,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        self.add_action('gave_up', {'challenge': challenge_name})

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'joined_at': self.joined_at,
            'builder_score': self.builder_score,
            'whiner_score': self.whiner_score,
            'total_score': self.builder_score + self.whiner_score,
            'classification': self.classification,
            'actions_count': len(self.actions),
            'builds_count': len(self.builds),
            'builds': self.builds,
            'tokens_used': self.tokens_used,
            'araya_conversations_count': len(self.araya_conversations),
            'araya_conversations': self.araya_conversations[-10:],  # Last 10
            'challenges_completed': self.challenges_completed,
            'challenges_failed': self.challenges_failed,
            'recent_actions': self.actions[-20:]  # Last 20 actions
        }

    def save(self):
        """Save profile to disk"""
        file_path = USERS_DIR / f'{self.user_id}.json'
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, user_id):
        """Load profile from disk"""
        file_path = USERS_DIR / f'{user_id}.json'
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)

            profile = cls(user_id, data.get('name'))
            profile.joined_at = data.get('joined_at')
            profile.builder_score = data.get('builder_score', 0)
            profile.whiner_score = data.get('whiner_score', 0)
            profile.actions = data.get('recent_actions', [])
            profile.builds = data.get('builds', [])
            profile.tokens_used = data.get('tokens_used', 0)
            profile.araya_conversations = data.get('araya_conversations', [])
            profile.challenges_completed = data.get('challenges_completed', [])
            profile.challenges_failed = data.get('challenges_failed', [])
            profile.classification = data.get('classification', 'UNKNOWN')

            return profile
        else:
            return cls(user_id)


def get_all_users():
    """Get all user profiles"""
    users = []
    for file_path in USERS_DIR.glob('*.json'):
        user_id = file_path.stem
        profile = UserProfile.load(user_id)
        users.append(profile.to_dict())

    # Sort by builder score
    users.sort(key=lambda x: x['total_score'], reverse=True)
    return users


def get_builders():
    """Get all classified builders"""
    all_users = get_all_users()
    return [u for u in all_users if u['classification'] in ['BUILDER', 'EMERGING_BUILDER']]


def get_whiners():
    """Get all classified whiners"""
    all_users = get_all_users()
    return [u for u in all_users if u['classification'] in ['WHINER', 'POTENTIAL_WHINER']]


def get_leaderboard(limit=20):
    """Get top builders"""
    all_users = get_all_users()
    return all_users[:limit]


# Example usage
if __name__ == '__main__':
    print("\n🏗️ BUILDER vs WHINER CLASSIFICATION SYSTEM 🏗️\n")

    # Create test user
    user = UserProfile('amelia_10yo', 'Amelia (10 years old)')

    # Simulate her actions
    print("Simulating Amelia's journey...\n")

    user.add_araya_conversation("Hi Araya, can you help me understand this?", "Of course! Let me explain...")
    print(f"Classification after question: {user.classification}")

    user.add_action('explored_system', {'page': 'dashboard'})
    user.add_action('read_docs', {'doc': 'getting_started'})
    print(f"Classification after exploring: {user.classification}")

    user.complete_challenge('onboarding_challenge_1')
    user.complete_challenge('fix_first_bug')
    print(f"Classification after challenges: {user.classification}")

    user.add_build('cool_dashboard', 'Built a dashboard for tracking stuff')
    print(f"Classification after building: {user.classification}")

    user.add_action('helped_other_user', {'helped': 'user_123'})
    print(f"Final classification: {user.classification}")

    print(f"\nFinal Scores:")
    print(f"  Builder Score: {user.builder_score}")
    print(f"  Whiner Score: {user.whiner_score}")
    print(f"  Total Score: {user.builder_score + user.whiner_score}")
    print(f"  Classification: {user.classification}")

    # Save profile
    user.save()
    print(f"\n✅ Profile saved to {USERS_DIR / f'{user.user_id}.json'}")

    # Show all users
    print(f"\n📊 All Users:")
    for user_data in get_all_users():
        print(f"  {user_data['name']}: {user_data['classification']} (Score: {user_data['total_score']})")
