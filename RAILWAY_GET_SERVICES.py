"""
Get existing Railway services and complete deployment
"""

import requests
import json

RAILWAY_API = "https://backboard.railway.app/graphql/v2"
PROJECT_ID = "d46c9981-2f73-475b-b032-59975dd0fcd4"
ENVIRONMENT_ID = "a12dabfc-425b-42eb-80c0-6703e9f28bf3"
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
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Query to get all services in the project
query = """
query GetProject($id: String!) {
  project(id: $id) {
    id
    name
    services {
      edges {
        node {
          id
          name
          serviceInstances {
            edges {
              node {
                id
                domains {
                  serviceDomains {
                    domain
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

variables = {"id": PROJECT_ID}

print("🔍 Querying Railway project for existing services...")
result = graphql_request(query, variables)

if result:
    print("\n" + "=" * 60)
    print(json.dumps(result, indent=2))
    print("=" * 60)

    if "data" in result and result["data"].get("project"):
        project = result["data"]["project"]
        print(f"\n📦 Project: {project['name']}")

        services = project.get("services", {}).get("edges", [])
        print(f"📋 Found {len(services)} service(s)")

        for edge in services:
            service = edge["node"]
            print(f"\n   Service: {service['name']}")
            print(f"   ID: {service['id']}")

            instances = service.get("serviceInstances", {}).get("edges", [])
            for inst_edge in instances:
                inst = inst_edge["node"]
                domains = inst.get("domains", {}).get("serviceDomains", [])
                if domains:
                    for domain in domains:
                        print(f"   Domain: https://{domain['domain']}")
                else:
                    print(f"   No domains yet")
