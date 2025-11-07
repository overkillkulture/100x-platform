"""
Create ZIP package of Trinity session for Google Drive upload
"""

import zipfile
from pathlib import Path
import os

# Files to package
FILES_TO_PACKAGE = {
    "Documentation": [
        "C:/Users/dwrek/Desktop/🎉 TRINITY_LIVE_24_7_COMPLETE.md",
        "C:/Users/dwrek/Desktop/⚡ TRINITY_SYSTEMS_STATUS_LIVE.md",
        "C:/Users/dwrek/Desktop/⚡ SESSION_COMPLETE_HANDOFF.txt",
        "C:/Users/dwrek/Desktop/📱 TRINITY_PHONE_URLS.txt",
        "C:/Users/dwrek/Desktop/🚀 RAILWAY_DEPLOYMENT_GUIDE.md",
        "C:/Users/dwrek/Desktop/🚀 RAILWAY_DEPLOYMENT_STATUS.md",
        "C:/Users/dwrek/Desktop/⚡ RAILWAY_DEPLOYMENT_98_PERCENT_COMPLETE.md",
        "C:/Users/dwrek/Desktop/⚡ AUTONOMOUS_BUILD_SESSION_COMPLETE.md",
        "C:/Users/dwrek/Desktop/⚡ FINAL_HANDOFF_NOVEMBER_6_2025.md",
        "C:/Users/dwrek/Desktop/RAILWAY_FINAL_SOLUTION.md",
    ],
    "Master_Boot_Orchestrator": [
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/models.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/config.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/health_monitor.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/auto_healer.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/orchestrator.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/requirements.txt",
        "C:/Users/dwrek/100X_DEPLOYMENT/MASTER_BOOT_ORCHESTRATOR/START_ORCHESTRATOR.bat",
    ],
    "Railway_Deployment": [
        "C:/Users/dwrek/100X_DEPLOYMENT/TRINITY_RAILWAY_DEPLOY/UNIVERSAL_WAKE_SYSTEM.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/TRINITY_RAILWAY_DEPLOY/requirements.txt",
        "C:/Users/dwrek/100X_DEPLOYMENT/TRINITY_RAILWAY_DEPLOY/Procfile",
        "C:/Users/dwrek/100X_DEPLOYMENT/TRINITY_RAILWAY_DEPLOY/railway.json",
        "C:/Users/dwrek/100X_DEPLOYMENT/TRINITY_RAILWAY_DEPLOY/README.md",
    ],
    "Automation_Scripts": [
        "C:/Users/dwrek/100X_DEPLOYMENT/SESSION_MANIFEST.json",
        "C:/Users/dwrek/100X_DEPLOYMENT/GOOGLE_DRIVE_SYNC.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/CHECK_RAILWAY_STATUS.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/RAILWAY_GENERATE_DOMAIN.py",
        "C:/Users/dwrek/100X_DEPLOYMENT/RAILWAY_GET_SERVICES.py",
    ]
}

def create_package():
    """Create ZIP package"""
    output_path = "C:/Users/dwrek/Desktop/TRINITY_SESSION_COMPLETE.zip"

    print("=" * 60)
    print("📦 CREATING TRINITY SESSION PACKAGE")
    print("=" * 60)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        total_files = 0
        total_size = 0

        for category, files in FILES_TO_PACKAGE.items():
            print(f"\n📁 {category}:")

            for file_path in files:
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    arcname = f"Trinity_Session_Nov_6_2025/{category}/{file_name}"

                    zipf.write(file_path, arcname)

                    size = os.path.getsize(file_path)
                    total_size += size
                    total_files += 1

                    print(f"  ✅ {file_name} ({size:,} bytes)")
                else:
                    print(f"  ⚠️  Not found: {os.path.basename(file_path)}")

    # Summary
    print("\n" + "=" * 60)
    print("✅ PACKAGE CREATED")
    print("=" * 60)
    print(f"📦 File: {output_path}")
    print(f"📊 Files: {total_files}")
    print(f"💾 Size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")
    print("\n🌐 Ready to upload to Google Drive!")
    print("=" * 60)

    return output_path

if __name__ == "__main__":
    try:
        output = create_package()
        print(f"\n✅ Package ready: {output}")
        print("\nNext: Upload to Google Drive Hub")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
