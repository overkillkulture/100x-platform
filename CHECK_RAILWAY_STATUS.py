"""
Check Railway deployment status via API
"""

import requests
import json

RAILWAY_API = "https://backboard.railway.app/graphql/v2"
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
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Query service details including deployments
query = """
query GetService($id: String!) {
  service(id: $id) {
    id
    name
    deployments(first: 3) {
      edges {
        node {
          id
          status
          createdAt
          staticUrl
          url
        }
      }
    }
  }
}
"""

variables = {"id": SERVICE_ID}

print("🔍 Checking Railway deployment status...\n")
result = graphql_request(query, variables)

if result and "data" in result:
    service = result["data"]["service"]
    print(f"📦 Service: {service['name']}")
    print(f"   ID: {service['id']}")

    deployments = service.get("deployments", {}).get("edges", [])
    print(f"\n📋 Recent Deployments: {len(deployments)}")

    for edge in deployments:
        dep = edge["node"]
        print(f"\n   Deployment ID: {dep['id']}")
        print(f"   Status: {dep['status']}")
        print(f"   Created: {dep['createdAt']}")
        print(f"   URL: {dep.get('url', 'N/A')}")
        print(f"   Static URL: {dep.get('staticUrl', 'N/A')}")
else:
    print("❌ Failed to get service info")
    if result:
        print(json.dumps(result, indent=2))
