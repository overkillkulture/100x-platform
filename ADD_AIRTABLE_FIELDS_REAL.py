"""
Add Mission, Values, and Submitted fields to 100X Platform Users table
"""
import requests
import json

# Real credentials from session
AIRTABLE_TOKEN = "patAbUog4LkER4Fbc.e2942db8dca37f951ad341e47796c5d23b268607341bb0603726e5ac006dee1a"
AIRTABLE_BASE_ID = "app7F75X1unyGjPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

def add_fields():
    """Add Mission, Values, and Submitted fields"""

    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables/{AIRTABLE_TABLE_ID}/fields"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    fields_to_add = [
        {
            "name": "Mission",
            "type": "multilineText"
        },
        {
            "name": "Values",
            "type": "multilineText"
        },
        {
            "name": "Submitted",
            "type": "dateTime",
            "options": {
                "timeZone": "America/Chicago",
                "dateFormat": {
                    "name": "us"
                },
                "timeFormat": {
                    "name": "12hour"
                }
            }
        }
    ]

    print("🔧 Adding fields to Airtable...\n")

    for field in fields_to_add:
        try:
            response = requests.post(url, headers=headers, json=field)

            if response.status_code == 200:
                print(f"✅ Added field: {field['name']}")
            elif response.status_code == 422:
                print(f"⚠️  Field already exists: {field['name']}")
            else:
                print(f"❌ Failed to add {field['name']}: {response.status_code}")
                print(f"   {response.text}")
        except Exception as e:
            print(f"❌ Error adding {field['name']}: {str(e)}")

    print("\n🎯 Airtable fields updated!")
    print(f"\n📊 Your base: https://airtable.com/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}")

if __name__ == "__main__":
    add_fields()
