import requests

AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}"
}

print("🔍 Checking Airtable Users table...\n")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    records = data.get('records', [])

    print(f"✅ Found {len(records)} total records in Users table\n")

    if records:
        print("📋 Recent entries:")
        for i, record in enumerate(records[-5:], 1):  # Show last 5
            fields = record.get('fields', {})
            print(f"\n{i}. {fields.get('Full Name', 'No name')}")
            print(f"   Email: {fields.get('Email Address', 'No email')}")
            print(f"   Phone: {fields.get('Phone Number', 'No phone')}")
            print(f"   ID: {record.get('id')}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
