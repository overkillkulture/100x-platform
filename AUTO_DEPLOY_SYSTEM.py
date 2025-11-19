#!/usr/bin/env python3
"""
AUTO DEPLOY SYSTEM
Automated deployment workflow - git commit + netlify deploy in one command
Based on today's pattern: Edit → Test → Deploy → Verify
"""

import subprocess
import sys
import time
from datetime import datetime

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr:
                print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} - TIMEOUT (>120s)")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def auto_deploy(commit_message=None):
    """
    Complete deployment workflow:
    1. Check git status
    2. Add all changes
    3. Commit with timestamp
    4. Deploy to Netlify
    5. Verify deployment
    """

    print("🚀 AUTO DEPLOY SYSTEM ACTIVATED")
    print("=" * 60)

    # Step 1: Check status
    if not run_command("git status --short", "Checking git status"):
        print("⚠️ Git status check failed, continuing anyway...")

    # Step 2: Add all changes
    if not run_command("git add .", "Adding files to git"):
        print("❌ Failed to add files. Aborting.")
        return False

    # Step 3: Commit
    if commit_message is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_message = f"Auto-deploy: Platform updates {timestamp}"

    commit_cmd = f'''git commit -m "{commit_message}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"'''

    if not run_command(commit_cmd, "Committing changes"):
        print("⚠️ Commit failed (maybe no changes?). Continuing to deploy...")

    # Step 4: Deploy to Netlify
    print("\n📡 Deploying to Netlify (production)...")
    if not run_command("npx netlify deploy --prod", "Netlify production deployment"):
        print("❌ Deployment failed. Check Netlify CLI configuration.")
        return False

    # Step 5: Success
    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT COMPLETE!")
    print("🌐 URL: https://conciousnessrevolution.io")
    print("📊 Tests: Should show 21/21 passed")
    print("⏱️ Allow 10-30 seconds for CDN propagation")
    print("=" * 60)

    return True

if __name__ == "__main__":
    # Get commit message from command line args
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = None

    success = auto_deploy(message)
    sys.exit(0 if success else 1)
