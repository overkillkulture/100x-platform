"""
INTERACTIVE CREDENTIAL UPDATER
Updates the gate with real Airtable credentials
"""

import re

print("\n" + "="*60)
print("🔐 AIRTABLE CREDENTIAL UPDATER")
print("="*60)

print("\nI'll ask for each credential, then update the gate automatically.")
print("Press Enter to skip and keep current value.\n")

# Get current values from index.html
try:
    with open('C:/Users/dwrek/100X_DEPLOYMENT/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extract current values
    base_id_match = re.search(r"baseId:\s*['\"]([^'\"]+)['\"]", html_content)
    table_name_match = re.search(r"tableName:\s*['\"]([^'\"]+)['\"]", html_content)
    api_key_match = re.search(r"apiKey:\s*['\"]([^'\"]+)['\"]", html_content)

    current_base_id = base_id_match.group(1) if base_id_match else "NOT FOUND"
    current_table_name = table_name_match.group(1) if table_name_match else "NOT FOUND"
    current_api_key = api_key_match.group(1) if api_key_match else "NOT FOUND"

except Exception as e:
    print(f"⚠️  Warning: Could not read current values: {e}")
    current_base_id = ""
    current_table_name = ""
    current_api_key = ""

print(f"Current Base ID: {current_base_id}")
print(f"Current Table Name: {current_table_name}")
print(f"Current API Key: {current_api_key[:20]}..." if len(current_api_key) > 20 else current_api_key)

# Get new values
print("\n" + "="*60)
print("ENTER NEW VALUES (or press Enter to keep current)")
print("="*60)

new_base_id = input(f"\nBase ID (starts with 'app'): ").strip()
if not new_base_id:
    new_base_id = current_base_id
    print(f"  → Keeping: {new_base_id}")

new_table_name = input(f"\nTable Name: ").strip()
if not new_table_name:
    new_table_name = current_table_name
    print(f"  → Keeping: {new_table_name}")

new_api_key = input(f"\nPersonal Access Token (starts with 'pat'): ").strip()
if not new_api_key:
    new_api_key = current_api_key
    print(f"  → Keeping: {new_api_key[:20]}...")

# Validate
print("\n" + "="*60)
print("VALIDATING...")
print("="*60)

errors = []

if not new_base_id.startswith('app'):
    errors.append("⚠️  Base ID should start with 'app'")

if not new_api_key.startswith('pat'):
    errors.append("⚠️  API Key should start with 'pat'")

if not new_table_name:
    errors.append("⚠️  Table Name cannot be empty")

if errors:
    print("\n❌ VALIDATION ERRORS:")
    for error in errors:
        print(f"   {error}")
    print("\nPlease run again with correct values.")
    exit(1)

print("✅ Validation passed!")

# Update HTML file
print("\n" + "="*60)
print("UPDATING GATE...")
print("="*60)

try:
    # Read current HTML
    with open('C:/Users/dwrek/100X_DEPLOYMENT/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace values
    html_content = re.sub(
        r"baseId:\s*['\"]([^'\"]+)['\"]",
        f"baseId: '{new_base_id}'",
        html_content
    )

    html_content = re.sub(
        r"tableName:\s*['\"]([^'\"]+)['\"]",
        f"tableName: '{new_table_name}'",
        html_content
    )

    html_content = re.sub(
        r"apiKey:\s*['\"]([^'\"]+)['\"]",
        f"apiKey: '{new_api_key}'",
        html_content
    )

    # Write updated HTML
    with open('C:/Users/dwrek/100X_DEPLOYMENT/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("\n✅ Gate updated successfully!")
    print("\n" + "="*60)
    print("📋 NEXT STEPS")
    print("="*60)
    print("\n1. Test the connection:")
    print("   python DIAGNOSE_AIRTABLE.py")
    print("\n2. Deploy the updated gate:")
    print("   netlify deploy --prod --dir=. --site=ba8f1795-1517-42ee-aa47-c1f5fa71b736")
    print("\n3. Test with browser:")
    print("   Visit the deployed site and submit test data")
    print("\n" + "="*60)

except Exception as e:
    print(f"\n❌ ERROR: Could not update gate: {e}")
    exit(1)
