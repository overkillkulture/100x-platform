#!/usr/bin/env python3
import requests
import json

# Test GitHub token
TOKEN = "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"
REPO = "overkillkulture/consciousness-bugs"

url = f"https://api.github.com/repos/{REPO}/issues"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

data = {
    "title": "TEST: Token verification",
    "body": "This is a test issue to verify the GitHub token works. If you can see this, the token is working!"
}

print(f"Testing token by creating issue at: {url}")
response = requests.post(url, headers=headers, json=data)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    print("\n✅ SUCCESS! Token works!")
    print(f"View issue at: {response.json()['html_url']}")
else:
    print("\n❌ FAILED! Token doesn't work or repo has issues disabled")
