"""
Test Araya User Tracking System
Simulates your daughter (Amelia, 10 years old) having a conversation with Araya
"""

import requests
import json
import time

ARAYA_API = 'http://localhost:6666'

def test_user_conversation(user_id, user_name, messages):
    """Simulate a user having a conversation with Araya"""
    print(f"\n{'='*60}")
    print(f"Testing conversation for: {user_name}")
    print(f"{'='*60}\n")

    for i, message in enumerate(messages, 1):
        print(f"\n[{i}] {user_name}: {message}")

        response = requests.post(f'{ARAYA_API}/chat', json={
            'message': message,
            'user_id': user_id,
            'user_name': user_name
        })

        data = response.json()
        print(f"[{i}] Araya: {data['response'][:200]}..." if len(data['response']) > 200 else f"[{i}] Araya: {data['response']}")

        if 'user_profile' in data:
            profile = data['user_profile']
            print(f"\n📊 Profile Update:")
            print(f"   Classification: {profile['classification']}")
            print(f"   Score: {profile['total_score']}")
            print(f"   Conversations: {profile['conversations_count']}")
            print(f"   Tokens: {profile['tokens_used']}")

        time.sleep(1)  # Brief pause between messages

def check_araya_status():
    """Check if Araya is running"""
    try:
        response = requests.get(f'{ARAYA_API}/status')
        data = response.json()
        print("\n✅ Araya Status:")
        print(f"   Mode: {data['mode']}")
        print(f"   Model: {data['model']}")
        print(f"   User Tracking: {data['user_tracking']['enabled']}")
        print(f"   Total Users: {data['user_tracking']['total_users']}")
        print(f"   Total Conversations: {data['user_tracking']['total_conversations']}")
        return True
    except Exception as e:
        print(f"\n❌ Araya not running: {e}")
        return False

def show_all_users():
    """Display all users in the system"""
    try:
        response = requests.get(f'{ARAYA_API}/users/all')
        data = response.json()

        print(f"\n{'='*60}")
        print(f"ALL USERS IN SYSTEM")
        print(f"{'='*60}\n")

        for user in data['users']:
            print(f"👤 {user['name']}")
            print(f"   ID: {user['user_id']}")
            print(f"   Classification: {user['classification']}")
            print(f"   Score: {user['total_score']}")
            print(f"   Builds: {user['builds_count']}")
            print(f"   Araya Chats: {user['araya_conversations_count']}")
            print(f"   Tokens: {user['tokens_used']}")
            print()
    except Exception as e:
        print(f"\n❌ Error fetching users: {e}")

if __name__ == '__main__':
    print("\n🌀 ARAYA USER TRACKING TEST 🌀")

    # Check if Araya is running
    if not check_araya_status():
        print("\n⚠️  Please start Araya first:")
        print("   cd C:/Users/dwrek/100X_DEPLOYMENT")
        print("   python ARAYA_WITH_USER_TRACKING.py")
        exit(1)

    # Test 1: Amelia (10 years old) - Should be classified as EMERGING_BUILDER
    amelia_messages = [
        "Hi Araya! I'm Amelia. Can you help me learn about building cool stuff?",
        "What is consciousness?",
        "How do I become a builder?",
        "This is really cool! Can you teach me more?"
    ]

    test_user_conversation('amelia_10yo', 'Amelia (10 years old)', amelia_messages)

    # Test 2: Another user asking questions
    test_messages = [
        "How do I get started with the platform?",
        "What can Araya do?"
    ]

    test_user_conversation('test_user', 'Test User', test_messages)

    # Show all users
    time.sleep(2)
    show_all_users()

    print("\n✅ Test Complete!")
    print("\n📊 View results at:")
    print("   Chat Interface: http://localhost:8003/araya-chat-with-profiles.html")
    print("   User Profiles: http://localhost:8003/USER_PROFILES_DASHBOARD.html")
    print("   Activity Dashboard: http://localhost:8003/ACTIVITY_DASHBOARD.html")
