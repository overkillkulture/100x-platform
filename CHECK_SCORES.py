import requests

AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}?sort%5B0%5D%5Bfield%5D=Registration%20Date&sort%5B0%5D%5Bdirection%5D=desc"

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}"
}

print("🔍 Checking latest entries WITH consciousness scores...\n")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    records = data.get('records', [])

    print(f"📊 Latest 3 entries:\n")

    for i, record in enumerate(records[:3], 1):
        fields = record.get('fields', {})
        print(f"{i}. {fields.get('Full Name', 'No name')}")
        print(f"   Email: {fields.get('Email Address', 'N/A')}")
        print(f"   Mission: {fields.get('Mission', 'N/A')[:50]}...")
        print(f"   Values: {fields.get('Values', 'N/A')[:50]}...")
        print(f"   🎯 Consciousness Score: {fields.get('Consciousness Score', 'N/A')}/100")
        print(f"   Status: {fields.get('Status', 'N/A')}")
        print()
else:
    print(f"❌ Error: {response.status_code}")
