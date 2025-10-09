"""
Discover Airtable Base and Table information using the API
"""
import requests
import json

AIRTABLE_TOKEN = "patAbUog4LkER4Fbc.e2942db8dca37f951ad341e47796c5d23b268607341bb0603726e5ac006dee1a"
BASE_ID = "app7F7SX1unyj6i4rlJsitn4KNa0TbU5FgKViWnEiQpcWYDpkElX7"

def discover_base_info():
    """Discover base structure and table IDs"""

    print("🔍 Discovering Airtable base structure...\n")

    # Get base schema
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            print("📊 Base Information:")
            print(f"Base ID: {BASE_ID}\n")

            print("📋 Tables found:")
            for table in data.get('tables', []):
                print(f"\n  📁 {table['name']}")
                print(f"     Table ID: {table['id']}")
                print(f"     Fields:")
                for field in table.get('fields', []):
                    print(f"       - {field['name']} ({field['type']})")

            # Save to file for reference
            with open('C:/Users/dwrek/100X_DEPLOYMENT/airtable_structure.json', 'w') as f:
                json.dump(data, f, indent=2)

            print("\n✅ Structure saved to airtable_structure.json")

        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    discover_base_info()
