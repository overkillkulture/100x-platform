"""
Test the gate submission to verify Airtable integration works
"""
import requests
import json
from datetime import datetime

# Real credentials
AIRTABLE_TOKEN = "patAbUog4LkER4Fbc.e2942db8dca37f951ad341e47796c5d23b268607341bb0603726e5ac006dee1a"
AIRTABLE_BASE_ID = "app7F75X1unyGjPfd"
AIRTABLE_TABLE_ID = "tblnf4KNaOfbU5FgK"

# Test data - matching the form fields
test_data = {
    "fields": {
        "Name": "Claude Test User",
        "Email": "claude-test@consciousnessrevolution.io",
        "Phone": "+1 (555) 123-4567",
        "Mission": "Testing the 100X gate to ensure Airtable integration works properly",
        "Values": "Quality, automation, consciousness elevation",
        "Submitted": datetime.utcnow().isoformat()
    }
}

print("🧪 Testing gate submission...")
print(f"\n📊 Base: {AIRTABLE_BASE_ID}")
print(f"📊 Table: {AIRTABLE_TABLE_ID}\n")

# Submit to Airtable
url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, headers=headers, json=test_data)

    if response.status_code == 200:
        print("✅ SUCCESS! Gate submission worked!")
        record = response.json()
        print(f"\n📝 Created record ID: {record.get('id')}")
        print(f"\n📋 Record data:")
        print(json.dumps(record.get('fields', {}), indent=2))
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(f"\n{response.text}")

        # Try to parse error for helpful info
        try:
            error_data = response.json()
            if 'error' in error_data:
                print(f"\n⚠️  Error type: {error_data['error'].get('type')}")
                print(f"⚠️  Message: {error_data['error'].get('message')}")
        except:
            pass

except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "="*50)
print("If you see field name errors, we need to update the form to match Airtable field names")
