"""
SIMPLE AIRTABLE DIAGNOSTIC
Find out why submission is failing
"""

import requests
import json

# Current credentials from the HTML
AIRTABLE_CONFIG = {
    'baseId': 'appD0L28VPIzkSDQk',
    'tableName': '100X_BUILDERS',
    'apiKey': 'patD67BUwx3cRMAEH.b5d8c4f8a1f9c0b2e3d4a5f6c7b8d9e0a1b2c3d4e5f6a7b8'
}

print("\n" + "="*60)
print("🔍 DIAGNOSING AIRTABLE CONNECTION")
print("="*60)

print(f"\nBase ID: {AIRTABLE_CONFIG['baseId']}")
print(f"Table Name: {AIRTABLE_CONFIG['tableName']}")
print(f"API Key: {AIRTABLE_CONFIG['apiKey'][:20]}...")

# Test 1: Can we reach Airtable API?
print("\n📡 TEST 1: Checking Airtable API connection...")

url = f"https://api.airtable.com/v0/{AIRTABLE_CONFIG['baseId']}/{AIRTABLE_CONFIG['tableName']}"
headers = {
    'Authorization': f"Bearer {AIRTABLE_CONFIG['apiKey']}",
    'Content-Type': 'application/json'
}

# Try to list records (GET request)
try:
    print("   Attempting GET request to list records...")
    response = requests.get(url, headers=headers)

    print(f"\n   Status Code: {response.status_code}")
    print(f"   Response: {response.text[:200]}...")

    if response.status_code == 401:
        print("\n❌ PROBLEM FOUND: Authentication failed")
        print("   The API key is invalid or expired")
        print("\n🔧 FIX NEEDED:")
        print("   1. Go to Airtable.com")
        print("   2. Open your base")
        print("   3. Click 'Help' > 'API Documentation'")
        print("   4. Get the correct Base ID")
        print("   5. Create a new Personal Access Token")

    elif response.status_code == 404:
        print("\n❌ PROBLEM FOUND: Base or table not found")
        print("   Either the Base ID or Table Name is wrong")
        print("\n🔧 FIX NEEDED:")
        print("   1. Verify Base ID in Airtable")
        print("   2. Check table name (case-sensitive!)")

    elif response.status_code == 200:
        print("\n✅ CONNECTION WORKS!")
        print("   Airtable is reachable with current credentials")

        # Test 2: Can we POST a record?
        print("\n📡 TEST 2: Attempting to create a test record...")

        test_data = {
            'fields': {
                'Name': 'Test Submission',
                'Email': 'test@example.com',
                'Phone': '+1 555 123 4567',
                'Mission': 'Testing the gate',
                'Values': 'Truth and testing'
            }
        }

        response = requests.post(url, headers=headers, json=test_data)

        print(f"\n   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:500]}")

        if response.status_code == 200:
            print("\n✅ POST WORKS! Gate should be functional")
        else:
            print("\n❌ POST FAILED")
            print(f"   Error: {response.json().get('error', {})}")

    else:
        print(f"\n❌ UNEXPECTED STATUS: {response.status_code}")
        print(f"   Response: {response.text}")

except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {e}")
    print("\n🔧 POSSIBLE FIXES:")
    print("   1. Check internet connection")
    print("   2. Verify Airtable credentials")
    print("   3. Check if Airtable is down")

print("\n" + "="*60)
print("📋 NEXT STEPS:")
print("="*60)
print("If authentication failed:")
print("  → Get real Airtable credentials")
print("  → Update index.html with correct values")
print("\nIf everything works:")
print("  → Check browser console for CORS errors")
print("  → May need Airtable API proxy")
print("="*60 + "\n")
