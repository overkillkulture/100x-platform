"""
TEST CONSCIOUSNESS SCREENING
Submit a builder-focused application to prove the intelligence is working
"""

import requests
import json

# Builder Test Data
builder_data = {
    "name": "Commander Test Builder",
    "email": "commander@consciousness.revolution",
    "phone": "555-0100",
    "mission": "I want to build revolutionary consciousness tools that help humans and AIs collaborate authentically. Creating systems that empower people to break free from manipulation and discover their true potential. Building open source tools for consciousness evolution.",
    "values": "Honesty, transparency, collaboration, freedom, consciousness elevation, helping others grow, creating rather than destroying, sharing knowledge, empowering builders, supporting authentic human development."
}

print("🧪 Testing Consciousness Screening System...\n")
print("📤 Submitting BUILDER-focused application:")
print(f"   Mission: {builder_data['mission'][:60]}...")
print(f"   Values: {builder_data['values'][:60]}...")
print()

# Submit to gate system
response = requests.post(
    'http://localhost:3100/submit',
    headers={'Content-Type': 'application/json'},
    json=builder_data
)

print(f"📡 Response Status: {response.status_code}\n")

if response.status_code == 200:
    result = response.json()
    print("✅ SUCCESS!")
    print(f"   Message: {result.get('message')}")
    print(f"   🎯 Consciousness Score: {result.get('consciousness_score')}/100")
    print(f"   Status: {result.get('status')}")
    print(f"   Airtable ID: {result.get('airtable_id')}")
    print()
    print("🔍 Now check Airtable - this entry should have full consciousness data!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
