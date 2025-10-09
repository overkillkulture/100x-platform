"""
Automatically add Mission and Values fields to Airtable Users table
"""
import requests
import json

AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

def add_fields():
    """Add Mission, Values, and Status fields to Users table"""

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
            "name": "Status",
            "type": "singleSelect",
            "options": {
                "choices": [
                    {"name": "Pending", "color": "yellowBright"},
                    {"name": "Approved", "color": "greenBright"},
                    {"name": "Rejected", "color": "redBright"},
                    {"name": "Builder", "color": "blueBright"}
                ]
            }
        },
        {
            "name": "Consciousness Score",
            "type": "number",
            "options": {
                "precision": 2
            }
        }
    ]

    print("🔧 Adding fields to Airtable Users table...\n")

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

    print("\n🎯 Airtable table upgraded!")

if __name__ == "__main__":
    add_fields()
