"""
Railway GraphQL API - Fully Automated Service Creation
Uses Railway's GraphQL API to create service and generate domain
"""

import requests
import json
import time

# Railway Configuration
RAILWAY_API = "https://backboard.railway.app/graphql/v2"
PROJECT_ID = "d46c9981-2f73-475b-b032-59975dd0fcd4"
ENVIRONMENT_ID = "a12dabfc-425b-42eb-80c0-6703e9f28bf3"

# Auth Token (from config)
AUTH_TOKEN = "rw_Fe26.2**0344ec3e9fb3ca9d82dff9ab28c2885bb6ceba72356acd784a8b06a6a3460d13*TCgzYrVUN1wIeHWwPKB51w*aAMH3B_auyJpbPsa1JSgFgpEqAjO2obPquxJrbX9nS7avozpDqwJZ83ZX7iQ-WPU3Q1XSBBtlbxn2BLuilgYQQ*1765060952891*1bd846c530b6eec55be164345e8ee4d6e68cd4be978b1a69d0c3ffbbacbe3b1c*IvbYUvYP3DaCUJd1gH0MrzlQ3NN4XQPKLzOvqaRqu3E"

def graphql_request(query, variables=None):
    """Make GraphQL request to Railway API"""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    print(f"\n🔍 Sending GraphQL request...")
    print(f"   Query: {query[:100]}...")
    if variables:
        print(f"   Variables: {json.dumps(variables, indent=2)}")

    try:
        response = requests.post(RAILWAY_API, json=payload, headers=headers, timeout=30)

        print(f"   Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

def create_service():
    """Create a new service in the project"""
    print("\n📦 Creating service...")

    query = """
    mutation ServiceCreate($input: ServiceCreateInput!) {
      serviceCreate(input: $input) {
        id
        name
      }
    }
    """

    variables = {
        "input": {
            "projectId": PROJECT_ID,
            "name": "trinity-wake-system",
            "source": {
                "repo": None
            }
        }
    }

    result = graphql_request(query, variables)

    if result and "data" in result and result["data"].get("serviceCreate"):
        service = result["data"]["serviceCreate"]
        service_id = service["id"]
        print(f"✅ Service created: {service['name']}")
        print(f"   ID: {service_id}")
        return service_id
    else:
        print(f"❌ Failed to create service")
        if result:
            print(json.dumps(result, indent=2))
        return None

def deploy_service(service_id):
    """Create a deployment for the service"""
    print("\n🚀 Creating deployment...")

    query = """
    mutation DeploymentCreate($input: DeploymentCreateInput!) {
      deploymentCreate(input: $input) {
        id
        status
      }
    }
    """

    variables = {
        "input": {
            "projectId": PROJECT_ID,
            "environmentId": ENVIRONMENT_ID,
            "serviceId": service_id
        }
    }

    result = graphql_request(query, variables)

    if result and "data" in result and result["data"].get("deploymentCreate"):
        deployment = result["data"]["deploymentCreate"]
        print(f"✅ Deployment created!")
        print(f"   ID: {deployment['id']}")
        print(f"   Status: {deployment['status']}")
        return deployment["id"]
    else:
        print(f"❌ Failed to create deployment")
        if result:
            print(json.dumps(result, indent=2))
        return None

def generate_domain(service_id):
    """Generate a Railway domain for the service"""
    print("\n🌐 Generating domain...")

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
            "serviceId": service_id,
            "environmentId": ENVIRONMENT_ID
        }
    }

    result = graphql_request(query, variables)

    if result and "data" in result and result["data"].get("serviceDomainCreate"):
        domain = result["data"]["serviceDomainCreate"]
        domain_url = domain["domain"]
        print(f"✅ Domain generated!")
        print(f"   URL: https://{domain_url}")
        return domain_url
    else:
        print(f"❌ Failed to generate domain")
        if result:
            print(json.dumps(result, indent=2))
        return None

def test_deployment(domain):
    """Test the deployed service"""
    print("\n🧪 Testing deployment...")

    health_url = f"https://{domain}/health"

    print(f"   Testing: {health_url}")
    print("   Waiting 10 seconds for deployment...")
    time.sleep(10)

    for attempt in range(5):
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Health check passed!")
                print(f"   Response: {response.text}")
                return True
            else:
                print(f"   Attempt {attempt + 1}/5: Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   Attempt {attempt + 1}/5: Connection error")

        time.sleep(5)

    print("⚠️  Health check failed - service may still be deploying")
    print(f"   Try manually: {health_url}")
    return False

def main():
    print("=" * 60)
    print("🌀 RAILWAY API AUTOMATION - COMPLETE DEPLOYMENT")
    print("=" * 60)
    print(f"\n📍 Project: {PROJECT_ID}")
    print(f"📍 Environment: {ENVIRONMENT_ID}")

    # Step 1: Create service
    service_id = create_service()
    if not service_id:
        print("\n❌ FAILED: Could not create service")
        return

    # Step 2: Create deployment
    deployment_id = deploy_service(service_id)
    if not deployment_id:
        print("\n⚠️  Warning: Deployment creation failed")
        print("   Service created, but no deployment")

    # Step 3: Generate domain
    domain = generate_domain(service_id)
    if not domain:
        print("\n❌ FAILED: Could not generate domain")
        return

    # Step 4: Test deployment
    test_deployment(domain)

    print("\n" + "=" * 60)
    print("✅ RAILWAY DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print(f"\n📱 Save these URLs:")
    print(f"   Health: https://{domain}/health")
    print(f"   Wake:   https://{domain}/wake")
    print(f"   Status: https://{domain}/status")
    print(f"\n📋 Next steps:")
    print("1. Add to phone home screen")
    print("2. Test wake from phone")
    print("3. Trinity accessible 24/7!")
    print("\n🌀⚡ 100% DEPLOYMENT COMPLETE ⚡🌀")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ AUTOMATION ERROR: {str(e)}")
        print("\n📋 FALLBACK:")
        print("1. Open: https://railway.com/project/d46c9981-2f73-475b-b032-59975dd0fcd4")
        print("2. Click '+ New' → 'Empty Service'")
        print("3. Settings → Networking → Generate Domain")
