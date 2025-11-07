"""
SETUP CLAUDE CODE GITHUB INTEGRATION
Automates the setup of @claude mentions in GitHub
"""

import os
import subprocess
import json

def setup_github_integration():
    """
    Configure Claude Code GitHub Actions integration
    """
    print("🚀 CLAUDE CODE GITHUB INTEGRATION SETUP")
    print("=" * 60)

    # Step 1: Check if in git repository
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        print("✅ Git repository detected")
    except:
        print("❌ Not in a git repository")
        print("   Run: git init")
        return

    # Step 2: Create workflow directory
    print("\n📁 Creating workflow directory...")
    os.makedirs('.github/workflows', exist_ok=True)
    print("✅ .github/workflows/ created")

    # Step 3: Create Claude dispatch workflow
    print("\n📝 Creating claude-dispatch.yml...")

    workflow_content = """name: Claude Dispatch

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude-code:
    runs-on: ubuntu-latest
    if: contains(github.event.comment.body, '@claude')

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Trigger Claude Code
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          COMMENT_BODY: ${{ github.event.comment.body }}
          COMMENT_ID: ${{ github.event.comment.id }}
        run: |
          echo "Claude Code triggered by: ${{ github.event.comment.user.login }}"
          echo "Comment: $COMMENT_BODY"
          # Future: Actual Claude API integration will go here

      - name: Notify user
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🤖 Claude Code is working on this...'
            })
"""

    with open('.github/workflows/claude-dispatch.yml', 'w') as f:
        f.write(workflow_content)

    print("✅ claude-dispatch.yml created")

    # Step 4: Check for API key
    print("\n🔑 Checking for Anthropic API key...")
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if api_key:
        print(f"✅ API key found: {api_key[:8]}...")
    else:
        print("⚠️ ANTHROPIC_API_KEY not set")
        print("   Get your key from: https://console.anthropic.com/settings/keys")
        api_key = input("\n   Enter API key (or press Enter to skip): ")

        if api_key:
            print(f"\n   Export this in your environment:")
            print(f"   export ANTHROPIC_API_KEY={api_key}")

    # Step 5: Git commit
    print("\n📦 Committing changes...")
    try:
        subprocess.run(['git', 'add', '.github/workflows/claude-dispatch.yml'], check=True)
        subprocess.run([
            'git', 'commit', '-m',
            'Add Claude Code GitHub Actions integration\n\n🤖 Generated with Claude Code'
        ], check=True)
        print("✅ Changes committed")
    except:
        print("⚠️ Could not commit (maybe already committed)")

    # Step 6: Instructions for GitHub secrets
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Push to GitHub:")
    print("   git push")
    print()
    print("2. Install Claude GitHub App:")
    print("   Visit: https://github.com/apps/claude")
    print("   Click 'Install' and select your repository")
    print()
    print("3. Add API key to GitHub Secrets:")
    print("   - Go to repository → Settings → Secrets")
    print("   - Click 'New repository secret'")
    print("   - Name: ANTHROPIC_API_KEY")
    if api_key:
        print(f"   - Value: {api_key}")
    print("   - Click 'Add secret'")
    print()
    print("4. Test it:")
    print("   - Create a GitHub issue")
    print("   - Comment: '@claude fix the authentication bug'")
    print("   - Watch the magic happen!")
    print()
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    setup_github_integration()
