import requests
import json

# Airtable API credentials
AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757"
AIRTABLE_BASE_ID = "app7F75X1uny6jPfd"

# Test connection by getting base info
def test_airtable_connection():
    """Test if we can talk to Airtable"""

    # Get base schema to see what tables exist
    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    print("🔌 Testing Airtable Connection...")
    print(f"📍 Base ID: {AIRTABLE_BASE_ID}\n")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("✅ CONNECTION SUCCESSFUL!\n")
            print("📊 Available Tables:")

            if 'tables' in data:
                for table in data['tables']:
                    print(f"\n  📋 {table['name']} (ID: {table['id']})")
                    if 'fields' in table:
                        print(f"     Fields: {', '.join([f['name'] for f in table['fields'][:5]])}...")
            else:
                print("  No tables found yet - base is empty")

            return True, data
        else:
            print(f"❌ CONNECTION FAILED: {response.status_code}")
            print(f"Response: {response.text}")
            return False, None

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, None

if __name__ == "__main__":
    success, data = test_airtable_connection()

    if success:
        print("\n🎯 READY TO BUILD GATE SYSTEM!")
        print("\n💡 Next Steps:")
        print("  1. Create 'Builder Applications' table in Airtable")
        print("  2. Add fields: Name, Email, Mission, Values, Status")
        print("  3. Connect to 100X registration form")
    else:
        print("\n⚠️ Fix connection before continuing")
