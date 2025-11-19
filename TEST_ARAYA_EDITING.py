"""
Test Araya's file editing abilities
"""
import requests
import json
import os
from datetime import datetime

print("🔍 TESTING ARAYA'S EDITING ABILITIES\n")
print("="*60)

# Test 1: Check if Araya is running
print("\n1️⃣ Testing: Is Araya online?")
try:
    response = requests.get('http://localhost:6666/health', timeout=5)
    print(f"✅ Araya is ONLINE: {response.json()}")
except Exception as e:
    print(f"❌ Araya is OFFLINE: {e}")
    exit(1)

# Test 2: Check file editing endpoint
print("\n2️⃣ Testing: File editing endpoint exists?")
try:
    # Create a test file
    test_file = 'C:/Users/dwrek/100X_DEPLOYMENT/ARAYA_TEST_FILE.txt'
    with open(test_file, 'w') as f:
        f.write("This is a test file.\nAraya will edit this line.\nEnd of file.")

    print(f"✅ Test file created: {test_file}")

    # Try to edit it via Araya's API
    response = requests.post('http://localhost:6666/api/edit-file', json={
        'file_path': test_file,
        'find_text': 'Araya will edit this line.',
        'replace_text': 'Araya HAS EDITED this line! ✅'
    }, timeout=10)

    result = response.json()
    print(f"✅ Edit endpoint response: {json.dumps(result, indent=2)}")

    # Verify the edit worked
    with open(test_file, 'r') as f:
        content = f.read()

    if '✅' in content:
        print("✅ FILE EDIT SUCCESSFUL! Araya can edit files!")
    else:
        print("❌ FILE EDIT FAILED! Content not changed")

    print(f"\nFile content after edit:\n{content}")

except Exception as e:
    print(f"❌ File editing test FAILED: {e}")

# Test 3: Check if chat can trigger file edits
print("\n3️⃣ Testing: Can chat trigger file edits?")
try:
    response = requests.post('http://localhost:6666/chat', json={
        'message': 'Edit the test file and change "test" to "WORKING"',
        'user_id': 'test_commander',
        'auto_execute': True
    }, timeout=30)

    result = response.json()
    print(f"Chat response: {result.get('response', '')[:200]}...")

    if result.get('auto_execute'):
        print(f"✅ Auto-execute detected: {result['auto_execute']}")
    else:
        print("⚠️ Auto-execute NOT triggered")

except Exception as e:
    print(f"❌ Chat test FAILED: {e}")

# Test 4: Check memory persistence
print("\n4️⃣ Testing: Memory persistence?")
try:
    # Send two messages
    msg1 = requests.post('http://localhost:6666/chat', json={
        'message': 'My name is TestUser and I like pizza',
        'user_id': 'memory_test',
    }).json()

    msg2 = requests.post('http://localhost:6666/chat', json={
        'message': 'What is my name?',
        'user_id': 'memory_test',
    }).json()

    if 'TestUser' in msg2['response'] or 'remember' in msg2['response'].lower():
        print("✅ Memory is WORKING! Araya remembers context")
    else:
        print("⚠️ Memory might not be working properly")
        print(f"Response: {msg2['response']}")

except Exception as e:
    print(f"❌ Memory test FAILED: {e}")

# Test 5: Check user tracking
print("\n5️⃣ Testing: User tracking?")
try:
    response = requests.get('http://localhost:6666/users/all')
    users = response.json()
    print(f"✅ Total users tracked: {len(users.get('users', []))}")
    print(f"Sample users: {[u['user_id'] for u in users.get('users', [])[:3]]}")
except Exception as e:
    print(f"❌ User tracking test FAILED: {e}")

print("\n" + "="*60)
print("🎯 TEST COMPLETE!")
