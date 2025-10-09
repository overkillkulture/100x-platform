"""
Update index.html with real Airtable credentials
"""

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old config
old_config = """        // Airtable configuration
        const AIRTABLE_CONFIG = {
            baseId: 'appD0L28VPIzkSDQk',
            tableName: '100X_BUILDERS',
            apiKey: 'patD67BUwx3cRMAEH.b5d8c4f8a1f9c0b2e3d4a5f6c7b8d9e0a1b2c3d4e5f6a7b8'
        };"""

new_config = """        // Airtable configuration - REAL CREDENTIALS
        const AIRTABLE_CONFIG = {
            baseId: 'app7F75X1unyGjPfd',
            tableName: 'tblnf4KNaOfbU5FgK',
            apiKey: 'patAbUog4LkER4Fbc.e2942db8dca37f951ad341e47796c5d23b268607341bb0603726e5ac006dee1a'
        };"""

# Replace
if old_config in content:
    content = content.replace(old_config, new_config)
    print("✅ Updated Airtable config")
else:
    print("❌ Old config not found - checking if already updated...")
    if 'app7F75X1unyGjPfd' in content:
        print("✅ Already has real credentials!")
    else:
        print("⚠️  Config format changed - manual edit needed")

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎯 Credentials updated in index.html")
