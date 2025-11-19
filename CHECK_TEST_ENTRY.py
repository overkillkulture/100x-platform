"""
Check the specific test entry we just created
"""

import requests

AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

# Get the record we just created
record_id = "recj7vsxNC00fZthb"
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}/{record_id}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}"
}

print("🔍 Checking test entry by ID...\n")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    record = response.json()
    fields = record.get('fields', {})

    print("✅ FOUND THE TEST ENTRY!\n")
    print(f"📋 Name: {fields.get('Full Name', 'N/A')}")
    print(f"📧 Email: {fields.get('Email Address', 'N/A')}")
    print(f"📞 Phone: {fields.get('Phone Number', 'N/A')}")
    print(f"\n🎯 CONSCIOUSNESS DATA:")
    print(f"   Score: {fields.get('Consciousness Score', 'N/A')}/100")
    print(f"   Status: {fields.get('Status', 'N/A')}")
    print(f"\n📝 Mission: {fields.get('Mission', 'N/A')[:100]}...")
    print(f"📝 Values: {fields.get('Values', 'N/A')[:100]}...")

    if fields.get('Consciousness Score'):
        print("\n🎉 CONSCIOUSNESS SCREENING IS WORKING!")
    else:
        print("\n❌ Consciousness data missing")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
