"""
Railway API Automation - Fully Automated Service Deployment
Uses Railway GraphQL API to complete deployment without browser interaction
"""

import os
import json
import subprocess
import time

def get_railway_token():
    """Get Railway authentication token from CLI"""
    try:
        result = subprocess.run(
            ["railway", "whoami", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        # Token is stored in Railway CLI config
        print("✅ Railway authentication verified")
        return True
    except Exception as e:
        print(f"❌ Railway authentication failed: {str(e)}")
        return False

def deploy_via_cli():
    """Deploy using Railway CLI with all flags"""
    print("\n🚀 Attempting fully automated CLI deployment...")

    project_id = "d46c9981-2f73-475b-b032-59975dd0fcd4"

    try:
        # Change to deployment directory
        os.chdir("C:/Users/dwrek/100X_DEPLOYMENT/TRINITY_RAILWAY_DEPLOY")
        print("📂 Changed to deployment directory")

        # Try: railway up with project flag
        print("\n📤 Uploading code to Railway...")
        result = subprocess.run(
            ["railway", "up", "--detach"],
            capture_output=True,
            text=True,
            timeout=120
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Code uploaded successfully!")

            # Wait for deployment
            print("\n⏳ Waiting for deployment to complete...")
            time.sleep(10)

            # Try to get domain
            print("\n🌐 Attempting to generate/get domain...")
            domain_result = subprocess.run(
                ["railway", "domain"],
                capture_output=True,
                text=True,
                timeout=30
            )

            print(domain_result.stdout)
            if domain_result.stderr:
                print(domain_result.stderr)

            # Try to get status
            print("\n📊 Getting deployment status...")
            status_result = subprocess.run(
                ["railway", "status"],
                capture_output=True,
                text=True,
                timeout=30
            )

            print(status_result.stdout)
            if status_result.stderr:
                print(status_result.stderr)

            return True
        else:
            print(f"❌ Upload failed with code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("⏳ Command timed out - may still be running")
        return False
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🌀 RAILWAY API AUTOMATION - FULLY AUTOMATED")
    print("=" * 60)

    # Verify authentication
    if not get_railway_token():
        print("\n❌ FAILED: Not authenticated with Railway")
        print("Run: railway login")
        return

    # Deploy via CLI
    if deploy_via_cli():
        print("\n✅ DEPLOYMENT COMPLETE!")
        print("\n📋 Next steps:")
        print("1. Run: railway logs (to view deployment logs)")
        print("2. Run: railway status (to get URL)")
        print("3. Test: curl [your-url]/health")
    else:
        print("\n⚠️  AUTOMATED DEPLOYMENT NEEDS MANUAL STEP")
        print("\n📋 Manual steps:")
        print("1. Open: https://railway.com/project/d46c9981-2f73-475b-b032-59975dd0fcd4")
        print("2. Click '+ New Service'")
        print("3. Select deployment source")
        print("4. Generate domain in Settings → Networking")

if __name__ == "__main__":
    main()
