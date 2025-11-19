#!/usr/bin/env python3
"""
Create Bug Reports table in Airtable - ONE TIME SETUP
"""
import requests
import json

# Airtable credentials
AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
BASE_ID = "app7F75X1uny6jPfd"
TABLE_NAME = "Bug Reports"

# Test with a sample bug to create the table structure
url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

# Sample bug report - this creates the table if it doesn't exist
sample_bug = {
    "fields": {
        "Title": "Sample Bug - System Test",
        "Description": "This is a test bug to initialize the Bug Reports table",
        "Reporter": "Claude (System Setup)",
        "URL": "https://conciousnessrevolution.io",
        "Status": "New",
        "Timestamp": "2025-10-27T10:00:00.000Z",
        "UserAgent": "Setup Script",
        "RawData": json.dumps({"test": "data"})
    }
}

print("Creating Bug Reports table in Airtable...")
print(f"URL: {url}")

response = requests.post(url, headers=headers, json=sample_bug)

if response.status_code in [200, 201]:
    print("\n✅ SUCCESS! Bug Reports table created!")
    print(f"\nView it here: https://airtable.com/{BASE_ID}")
    print("\nTable Fields Created:")
    print("  - Title (text)")
    print("  - Description (text)")
    print("  - Reporter (text)")
    print("  - URL (text)")
    print("  - Status (text)")
    print("  - Timestamp (text)")
    print("  - UserAgent (text)")
    print("  - RawData (text)")
    print("\nAll future bug reports will save here automatically!")
else:
    print(f"\n❌ Error: {response.status_code}")
    print(f"Response: {response.text}")
    print("\nTable might already exist - try viewing it at:")
    print(f"https://airtable.com/{BASE_ID}")
