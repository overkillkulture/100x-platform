"""
Get the actual field names from Airtable table
"""
import requests
import json

# Real credentials
AIRTABLE_TOKEN = "patAbUog4LkER4Fbc.e2942db8dca37f951ad341e47796c5d23b268607341bb0603726e5ac006dee1a"
AIRTABLE_BASE_ID = "app7F75X1unyGjPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

print("🔍 Getting table schema from Airtable...\n")

# Get table schema
url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables/{AIRTABLE_TABLE_ID}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("✅ Got table schema!\n")
    print("📋 FIELD NAMES:")
    print("=" * 50)

    for field in data.get('fields', []):
        field_name = field.get('name')
        field_type = field.get('type')
        print(f"  • {field_name} ({field_type})")

    print("\n" + "=" * 50)
    print("\n💡 Use these EXACT names in the gate form!")

else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)
