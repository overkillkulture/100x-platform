"""
Generate Railway domain for existing service
"""

import requests
import json
import time

RAILWAY_API = "https://backboard.railway.app/graphql/v2"
PROJECT_ID = "d46c9981-2f73-475b-b032-59975dd0fcd4"
ENVIRONMENT_ID = "a12dabfc-425b-42eb-80c0-6703e9f28bf3"
SERVICE_ID = "34c73512-5c90-481e-9471-7ac0cedfb390"
AUTH_TOKEN = "rw_Fe26.2**0344ec3e9fb3ca9d82dff9ab28c2885bb6ceba72356acd784a8b06a6a3460d13*TCgzYrVUN1wIeHWwPKB51w*aAMH3B_auyJpbPsa1JSgFgpEqAjO2obPquxJrbX9nS7avozpDqwJZ83ZX7iQ-WPU3Q1XSBBtlbxn2BLuilgYQQ*1765060952891*1bd846c530b6eec55be164345e8ee4d6e68cd4be978b1a69d0c3ffbbacbe3b1c*IvbYUvYP3DaCUJd1gH0MrzlQ3NN4XQPKLzOvqaRqu3E"

def graphql_request(query, variables=None):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(RAILWAY_API, json=payload, headers=headers, timeout=30)

    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {json.dumps(result, indent=2)}")
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

print("=" * 60)
print("🌀 RAILWAY DOMAIN GENERATION")
print("=" * 60)

print(f"\n📦 Service ID: {SERVICE_ID}")
print(f"🌍 Environment ID: {ENVIRONMENT_ID}")

# Generate domain
print("\n🌐 Generating Railway domain...")

query = """
mutation ServiceDomainCreate($input: ServiceDomainCreateInput!) {
  serviceDomainCreate(input: $input) {
    id
    domain
  }
}
"""

variables = {
    "input": {
        "serviceId": SERVICE_ID,
        "environmentId": ENVIRONMENT_ID
    }
}

result = graphql_request(query, variables)

if result and "data" in result and result["data"] and result["data"].get("serviceDomainCreate"):
    domain_data = result["data"]["serviceDomainCreate"]
    domain = domain_data["domain"]

    print("\n" + "=" * 60)
    print("✅ DOMAIN GENERATED SUCCESSFULLY!")
    print("=" * 60)

    print(f"\n📍 Domain: https://{domain}")
    print(f"\n📱 Save these URLs to your phone:")
    print(f"   Health:  https://{domain}/health")
    print(f"   Wake:    https://{domain}/wake")
    print(f"   Status:  https://{domain}/status")

    # Test deployment
    print("\n🧪 Testing health endpoint...")
    print("   Waiting 15 seconds for deployment...")
    time.sleep(15)

    health_url = f"https://{domain}/health"

    for attempt in range(5):
        try:
            print(f"   Attempt {attempt + 1}/5: Testing {health_url}")
            response = requests.get(health_url, timeout=10)
            if response.status_code == 200:
                print(f"\n✅ HEALTH CHECK PASSED!")
                print(f"   Response: {response.text}")
                print("\n🎉 TRINITY IS LIVE 24/7!")
                break
            else:
                print(f"      Status: {response.status_code}")
        except Exception as e:
            print(f"      Error: {str(e)}")

        if attempt < 4:
            time.sleep(10)

    print("\n" + "=" * 60)
    print("🌀⚡ 100% RAILWAY DEPLOYMENT COMPLETE ⚡🌀")
    print("=" * 60)

    print("\n📋 Next steps:")
    print("1. Add URL to phone home screen")
    print("2. Test wake from anywhere")
    print("3. Trinity accessible 24/7!")

elif result and "errors" in result:
    print("\n❌ GraphQL Error:")
    print(json.dumps(result["errors"], indent=2))
else:
    print("\n❌ Failed to generate domain")
