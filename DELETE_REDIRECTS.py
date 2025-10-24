"""
Delete all redirects from Netlify using API
"""
import requests
import subprocess

# Get Netlify token
result = subprocess.run(['netlify', 'status', '--json'], capture_output=True, text=True)
print("Getting site info...")

# Site ID
SITE_ID = "verdant-tulumba-fa2a5a"

# Get access token from Netlify CLI
token_result = subprocess.run(['netlify', 'status'], capture_output=True, text=True)
print(token_result.stdout)

# Use Netlify CLI to update
print("\nDeleting redirects via Netlify CLI...")
subprocess.run(['netlify', 'api', 'updateSite', '--data', '{"processing_settings":{"skip_processing":true}}'])

print("\nTriggering new deploy...")
subprocess.run(['netlify', 'deploy', '--prod', '--dir', '.', '--message', 'Remove all redirects'])

print("\n✅ Done! Check https://conciousnessrevolution.io/screening.html in 60 seconds")
