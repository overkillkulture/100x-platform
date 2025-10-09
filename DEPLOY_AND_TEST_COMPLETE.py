"""
COMPLETE DEPLOYMENT AND TESTING SYSTEM
Square-by-square verification following Commander's painter methodology
"""

import subprocess
import time
import requests
import re
from playwright.sync_api import sync_playwright

print("\n" + "="*70)
print("🎯 COMPLETE GATE DEPLOYMENT AND TESTING SYSTEM")
print("   Following painter's square-by-square methodology")
print("="*70)

# SQUARE 1: Verify Airtable credentials
print("\n" + "="*70)
print("SQUARE 1: VERIFYING AIRTABLE CREDENTIALS")
print("="*70)

# Read credentials from index.html
with open('C:/Users/dwrek/100X_DEPLOYMENT/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

base_id_match = re.search(r"baseId:\s*['\"]([^'\"]+)['\"]", html_content)
table_name_match = re.search(r"tableName:\s*['\"]([^'\"]+)['\"]", html_content)
api_key_match = re.search(r"apiKey:\s*['\"]([^'\"]+)['\"]", html_content)

base_id = base_id_match.group(1) if base_id_match else None
table_name = table_name_match.group(1) if table_name_match else None
api_key = api_key_match.group(1) if api_key_match else None

print(f"\n  Base ID: {base_id}")
print(f"  Table Name: {table_name}")
print(f"  API Key: {api_key[:20]}..." if api_key and len(api_key) > 20 else "MISSING")

# Test Airtable connection
print("\n  🔍 Testing Airtable connection...")
url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
headers = {
    'Authorization': f"Bearer {api_key}",
    'Content-Type': 'application/json'
}

try:
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        print("  ✅ SQUARE 1 PASSED: Airtable credentials valid")
        square1_passed = True
    elif response.status_code == 401:
        print("  ❌ SQUARE 1 FAILED: Authentication failed")
        print("\n  🔧 Run this to update credentials:")
        print("     python UPDATE_GATE_CREDENTIALS.py")
        exit(1)
    else:
        print(f"  ❌ SQUARE 1 FAILED: Status {response.status_code}")
        print(f"     {response.text}")
        exit(1)

except Exception as e:
    print(f"  ❌ SQUARE 1 FAILED: {e}")
    exit(1)

# SQUARE 2: Deploy to Netlify
print("\n" + "="*70)
print("SQUARE 2: DEPLOYING TO NETLIFY")
print("="*70)

print("\n  📤 Deploying to production...")

try:
    result = subprocess.run(
        ['netlify', 'deploy', '--prod', '--dir=.', '--site=ba8f1795-1517-42ee-aa47-c1f5fa71b736'],
        cwd='C:/Users/dwrek/100X_DEPLOYMENT',
        capture_output=True,
        text=True,
        timeout=120
    )

    if 'Deploy is live' in result.stdout:
        print("  ✅ SQUARE 2 PASSED: Deployed successfully")

        # Extract deploy URL
        deploy_url_match = re.search(r'https://[^\s]+--verdant-tulumba-fa2a5a\.netlify\.app', result.stdout)
        deploy_url = deploy_url_match.group(0) if deploy_url_match else None

        print(f"\n  📍 Unique Deploy URL: {deploy_url}")
        square2_passed = True
    else:
        print("  ❌ SQUARE 2 FAILED: Deployment failed")
        print(result.stdout)
        print(result.stderr)
        exit(1)

except Exception as e:
    print(f"  ❌ SQUARE 2 FAILED: {e}")
    exit(1)

# SQUARE 3: Verify deployment loads
print("\n" + "="*70)
print("SQUARE 3: VERIFYING DEPLOYED SITE LOADS")
print("="*70)

print("\n  ⏳ Waiting 5 seconds for CDN propagation...")
time.sleep(5)

print(f"  🌐 Fetching {deploy_url}...")

try:
    response = requests.get(deploy_url, timeout=30)

    if response.status_code == 200 and '100X' in response.text:
        print("  ✅ SQUARE 3 PASSED: Site loads correctly")
        square3_passed = True
    else:
        print(f"  ❌ SQUARE 3 FAILED: Status {response.status_code}")
        exit(1)

except Exception as e:
    print(f"  ❌ SQUARE 3 FAILED: {e}")
    exit(1)

# SQUARE 4: Test form interaction
print("\n" + "="*70)
print("SQUARE 4: TESTING FORM INTERACTION")
print("="*70)

print("\n  🤖 Launching Playwright browser automation...")

with sync_playwright() as p:
    try:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"  📍 Loading {deploy_url}...")
        page.goto(deploy_url, timeout=30000)
        time.sleep(2)

        print("  ⌨️  Typing in form fields...")
        page.fill('input#name', 'Test Builder')
        page.fill('input#email', 'test@consciousnessrevolution.io')
        page.fill('input#phone', '+1 555 123 4567')
        page.fill('textarea#mission', 'Testing the 100X Gate automation')
        page.fill('textarea#values', 'Truth, autonomy, verification')

        print("  ✅ SQUARE 4 PASSED: All fields interactive")
        square4_passed = True

        browser.close()

    except Exception as e:
        print(f"  ❌ SQUARE 4 FAILED: {e}")
        try:
            browser.close()
        except:
            pass
        exit(1)

# SQUARE 5: Test form submission
print("\n" + "="*70)
print("SQUARE 5: TESTING FORM SUBMISSION TO AIRTABLE")
print("="*70)

print("\n  🤖 Launching browser to test submission...")

with sync_playwright() as p:
    try:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Track network responses
        airtable_responses = []

        def handle_response(response):
            if 'airtable' in response.url.lower():
                airtable_responses.append({
                    'url': response.url,
                    'status': response.status,
                    'ok': response.ok
                })

        page.on('response', handle_response)

        page.goto(deploy_url, timeout=30000)
        time.sleep(2)

        # Fill form
        page.fill('input#name', 'Automated Test Submission')
        page.fill('input#email', 'autotest@consciousnessrevolution.io')
        page.fill('input#phone', '+1 555 999 9999')
        page.fill('textarea#mission', 'Automated testing of gate submission')
        page.fill('textarea#values', 'Automation, verification, truth')

        # Click submit
        print("  🖱️  Clicking submit button...")
        page.click('button#submitBtn')

        # Wait for response
        print("  ⏳ Waiting for Airtable response...")
        time.sleep(5)

        # Check status message
        status_message = page.locator('#statusMessage')

        if status_message.is_visible():
            message_class = status_message.get_attribute('class')
            message_text = status_message.inner_text()

            if 'success' in message_class:
                print(f"  ✅ SQUARE 5 PASSED: {message_text}")
                square5_passed = True
            else:
                print(f"  ❌ SQUARE 5 FAILED: {message_text}")
                print(f"\n  Network responses: {airtable_responses}")
                square5_passed = False
        else:
            print("  ❌ SQUARE 5 FAILED: No status message appeared")
            square5_passed = False

        browser.close()

    except Exception as e:
        print(f"  ❌ SQUARE 5 FAILED: {e}")
        try:
            browser.close()
        except:
            pass
        square5_passed = False

# FINAL REPORT
print("\n" + "="*70)
print("📊 FINAL VERIFICATION REPORT")
print("="*70)

results = [
    ("Square 1", "Airtable Credentials", square1_passed),
    ("Square 2", "Netlify Deployment", square2_passed),
    ("Square 3", "Site Loading", square3_passed),
    ("Square 4", "Form Interaction", square4_passed),
    ("Square 5", "Airtable Submission", square5_passed)
]

all_passed = all(result[2] for result in results)

for name, desc, passed in results:
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"\n  {name}: {desc}")
    print(f"    Status: {status}")

print("\n" + "="*70)

if all_passed:
    print("🎉 ALL SQUARES COMPLETE - GATE IS FULLY FUNCTIONAL")
    print("="*70)
    print(f"\n🌐 Live URL: https://conciousnessrevolution.io")
    print(f"📍 Test URL: {deploy_url}")
    print("\n✅ Gate is ready to accept builders")
else:
    print("⚠️  SOME SQUARES FAILED - GATE NEEDS ATTENTION")
    print("="*70)
    print("\nReview failures above and fix issues before deployment.")

print("\n")
