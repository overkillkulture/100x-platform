"""
USER DATA EXPORT SYSTEM
Export all user data before workspace updates/resets
Allows users to download their profile, conversations, builds
"""

import json
import zipfile
import os
from datetime import datetime
from pathlib import Path
from BUILDER_CLASSIFICATION_SYSTEM import UserProfile, get_all_users

DATA_DIR = Path('C:/Users/dwrek/100X_DEPLOYMENT/USER_EXPORTS')
DATA_DIR.mkdir(exist_ok=True)

def export_user_data(user_id):
    """Export all data for a single user"""
    print(f"\n📦 Exporting data for user: {user_id}")

    # Load user profile
    profile = UserProfile.load(user_id)

    # Create export package
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'user_profile': profile.to_dict(),
        'export_reason': 'Workspace update/reset',
        'data_includes': [
            'User profile',
            'Classification data',
            'Araya conversations',
            'Builds and projects',
            'Action history',
            'Tokens used',
            'Challenges completed'
        ]
    }

    # Add conversation log from Araya
    araya_log_file = Path('C:/Users/dwrek/.trinity/araya_offline_conversations.jsonl')
    if araya_log_file.exists():
        user_conversations = []
        with open(araya_log_file, 'r') as f:
            for line in f:
                try:
                    conv = json.loads(line)
                    if conv.get('user_id') == user_id:
                        user_conversations.append(conv)
                except:
                    pass

        export_data['araya_full_conversations'] = user_conversations

    # Save to file
    export_file = DATA_DIR / f'{user_id}_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(export_file, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"✅ Exported to: {export_file}")
    print(f"   Profile: {profile.name}")
    print(f"   Classification: {profile.classification}")
    print(f"   Total Score: {profile.builder_score + profile.whiner_score}")
    print(f"   Conversations: {len(profile.araya_conversations)}")
    print(f"   Builds: {len(profile.builds)}")

    return export_file

def export_all_users():
    """Export data for all users"""
    print("\n" + "="*60)
    print("📦 EXPORTING ALL USER DATA")
    print("="*60)

    users = get_all_users()
    exported_files = []

    for user in users:
        user_id = user['user_id']
        export_file = export_user_data(user_id)
        exported_files.append(export_file)

    # Create master export with all users
    master_export = {
        'export_timestamp': datetime.now().isoformat(),
        'total_users': len(users),
        'users': users,
        'export_reason': 'Workspace update - all user data backup'
    }

    master_file = DATA_DIR / f'ALL_USERS_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(master_file, 'w') as f:
        json.dump(master_export, f, indent=2)

    print(f"\n✅ Master export saved: {master_file}")
    print(f"✅ Exported {len(exported_files)} individual user files")

    return {
        'master_file': str(master_file),
        'user_files': [str(f) for f in exported_files],
        'total_users': len(users)
    }

def create_user_notification_message(user_id):
    """Create notification message for user about data export"""
    profile = UserProfile.load(user_id)

    message = f"""
🔔 WORKSPACE UPDATE NOTIFICATION

Hi {profile.name}!

We've updated the workspace to improve your experience. Your data has been safely exported and will be restored shortly.

📊 YOUR DATA BACKUP:
   • Classification: {profile.classification}
   • Total Score: {profile.builder_score + profile.whiner_score}
   • Conversations: {len(profile.araya_conversations)}
   • Builds: {len(profile.builds)}
   • Tokens Used: {profile.tokens_used:,}

✅ All your progress is saved and will be available in the updated workspace.

⏱️ Estimated downtime: 2-5 minutes

Thank you for being part of the Consciousness Revolution! 🌀

- The 100X Platform Team
"""

    return message

def generate_notification_emails():
    """Generate notification messages for all users"""
    users = get_all_users()

    notifications_file = DATA_DIR / f'user_notifications_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    with open(notifications_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("USER UPDATE NOTIFICATIONS\n")
        f.write("="*60 + "\n\n")

        for user in users:
            user_id = user['user_id']
            message = create_user_notification_message(user_id)
            f.write(message)
            f.write("\n" + "="*60 + "\n\n")

    print(f"\n📧 Notifications saved to: {notifications_file}")
    return notifications_file

if __name__ == '__main__':
    print("\n🔧 USER DATA EXPORT SYSTEM\n")

    # Export all user data
    result = export_all_users()

    # Generate notification messages
    notifications = generate_notification_emails()

    print(f"\n✅ EXPORT COMPLETE!")
    print(f"   Total Users: {result['total_users']}")
    print(f"   Master File: {result['master_file']}")
    print(f"   User Files: {len(result['user_files'])}")
    print(f"   Notifications: {notifications}")

    print(f"\n📁 All files saved to: {DATA_DIR}")
    print(f"\n💡 Next Steps:")
    print(f"   1. Review exported data")
    print(f"   2. Run WORKSPACE_RESET_PROTOCOL.py")
    print(f"   3. Users can re-import their data after update")
