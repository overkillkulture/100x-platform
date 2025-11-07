"""
ARAYA SITE EDITOR - Full Site Editing Capabilities
Gives Araya the ability to read, edit, and deploy website changes

CAPABILITIES:
1. Read any HTML/CSS/JS file from the site
2. Make surgical edits (find/replace, insertions, deletions)
3. Preview changes locally
4. Deploy to Netlify
5. Rollback if needed
6. Safety checks and backups

Usage:
    from ARAYA_SITE_EDITOR import ArayaSiteEditor

    editor = ArayaSiteEditor()
    editor.edit_file('frontend/index.html', find='<title>Old</title>', replace='<title>New</title>')
    editor.deploy()
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import re

class ArayaSiteEditor:
    """
    Complete site editing system for Araya
    """

    def __init__(self, site_root=None):
        """
        Initialize site editor

        Args:
            site_root: Path to site root (defaults to 100X_DEPLOYMENT)
        """
        self.site_root = Path(site_root) if site_root else Path("C:/Users/dwrek/100X_DEPLOYMENT")
        self.frontend_dir = self.site_root / "frontend"
        self.backend_dir = self.site_root / "backend"
        self.backup_dir = self.site_root / ".site_backups"

        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)

        # Track changes for this session
        self.session_changes = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        print("✅ Araya Site Editor initialized")
        print(f"   Site root: {self.site_root}")
        print(f"   Session ID: {self.session_id}")

    def read_file(self, file_path):
        """
        Read a file from the site

        Args:
            file_path: Relative path from site root (e.g., 'frontend/index.html')

        Returns:
            File contents as string
        """
        full_path = self.site_root / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"✅ Read {file_path} ({len(content)} characters)")
            return content

        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            raise

    def backup_file(self, file_path):
        """
        Create backup of file before editing

        Args:
            file_path: Relative path from site root

        Returns:
            Path to backup file
        """
        full_path = self.site_root / file_path

        # Create timestamped backup
        backup_name = f"{Path(file_path).stem}_{self.session_id}{Path(file_path).suffix}"
        backup_path = self.backup_dir / backup_name

        # Ensure backup subdirectories exist
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        shutil.copy2(full_path, backup_path)

        print(f"💾 Backed up {file_path} → {backup_path.name}")
        return backup_path

    def edit_file(self, file_path, find=None, replace=None, insert_at=None, insert_content=None,
                  delete_lines=None, append=None):
        """
        Edit a file with various operations

        Args:
            file_path: Relative path from site root
            find: Text to find (for find/replace)
            replace: Text to replace with
            insert_at: Line number or search string to insert at
            insert_content: Content to insert
            delete_lines: (start, end) tuple of line numbers to delete
            append: Content to append to end of file

        Returns:
            True if successful
        """
        # Read current content
        content = self.read_file(file_path)
        original_content = content

        # Backup before editing
        backup_path = self.backup_file(file_path)

        # Perform requested operation
        if find and replace is not None:
            # Find and replace
            if find not in content:
                print(f"⚠️  Warning: '{find[:50]}...' not found in {file_path}")
                return False

            content = content.replace(find, replace)
            operation = f"Replace: '{find[:30]}...' → '{replace[:30]}...'"

        elif insert_at is not None and insert_content:
            # Insert at specific location
            if isinstance(insert_at, int):
                # Insert at line number
                lines = content.split('\n')
                lines.insert(insert_at, insert_content)
                content = '\n'.join(lines)
                operation = f"Insert at line {insert_at}"
            else:
                # Insert after search string
                content = content.replace(insert_at, insert_at + '\n' + insert_content)
                operation = f"Insert after '{insert_at[:30]}...'"

        elif delete_lines:
            # Delete lines
            lines = content.split('\n')
            start, end = delete_lines
            del lines[start:end]
            content = '\n'.join(lines)
            operation = f"Delete lines {start}-{end}"

        elif append:
            # Append to end
            content = content + '\n' + append
            operation = f"Append {len(append)} characters"

        else:
            print("❌ No edit operation specified")
            return False

        # Write modified content
        full_path = self.site_root / file_path
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Track change
            change = {
                "file": file_path,
                "operation": operation,
                "timestamp": datetime.now().isoformat(),
                "backup": str(backup_path),
                "lines_changed": content.count('\n') - original_content.count('\n')
            }
            self.session_changes.append(change)

            print(f"✅ Edited {file_path}")
            print(f"   {operation}")
            return True

        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            # Restore from backup
            shutil.copy2(backup_path, full_path)
            print(f"↩️  Restored from backup")
            return False

    def add_to_html(self, file_path, tag, content, before_tag=None):
        """
        Add content to HTML file at specific location

        Args:
            file_path: HTML file path
            tag: Tag to insert before (e.g., '</head>', '</body>')
            content: HTML content to insert
            before_tag: If True, insert before tag. If False, after tag.

        Returns:
            True if successful
        """
        html_content = self.read_file(file_path)

        if tag not in html_content:
            print(f"❌ Tag '{tag}' not found in {file_path}")
            return False

        # Insert before the tag
        if before_tag is None or before_tag:
            modified = html_content.replace(tag, f"{content}\n{tag}")
        else:
            modified = html_content.replace(tag, f"{tag}\n{content}")

        # Backup and write
        self.backup_file(file_path)
        full_path = self.site_root / file_path

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(modified)

        print(f"✅ Added content to {file_path} before {tag}")
        return True

    def inject_script(self, file_path, script_url=None, script_code=None):
        """
        Inject JavaScript into HTML file

        Args:
            file_path: HTML file path
            script_url: External script URL
            script_code: Inline script code

        Returns:
            True if successful
        """
        if script_url:
            script_tag = f'<script src="{script_url}"></script>'
        elif script_code:
            script_tag = f'<script>\n{script_code}\n</script>'
        else:
            print("❌ No script URL or code provided")
            return False

        return self.add_to_html(file_path, '</body>', script_tag, before_tag=True)

    def inject_css(self, file_path, css_url=None, css_code=None):
        """
        Inject CSS into HTML file

        Args:
            file_path: HTML file path
            css_url: External CSS URL
            css_code: Inline CSS code

        Returns:
            True if successful
        """
        if css_url:
            style_tag = f'<link rel="stylesheet" href="{css_url}">'
        elif css_code:
            style_tag = f'<style>\n{css_code}\n</style>'
        else:
            print("❌ No CSS URL or code provided")
            return False

        return self.add_to_html(file_path, '</head>', style_tag, before_tag=True)

    def create_file(self, file_path, content):
        """
        Create a new file

        Args:
            file_path: Relative path for new file
            content: File content

        Returns:
            True if successful
        """
        full_path = self.site_root / file_path

        if full_path.exists():
            print(f"⚠️  Warning: {file_path} already exists")
            response = input("Overwrite? (y/n): ")
            if response.lower() != 'y':
                return False
            self.backup_file(file_path)

        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Created {file_path}")

            self.session_changes.append({
                "file": file_path,
                "operation": "Create new file",
                "timestamp": datetime.now().isoformat()
            })

            return True

        except Exception as e:
            print(f"❌ Error creating {file_path}: {e}")
            return False

    def preview_changes(self):
        """
        Show all changes made in this session
        """
        print("\n" + "=" * 60)
        print(f"📋 SESSION CHANGES ({self.session_id})")
        print("=" * 60)

        if not self.session_changes:
            print("No changes made yet")
            return

        for i, change in enumerate(self.session_changes, 1):
            print(f"\n{i}. {change['file']}")
            print(f"   Operation: {change['operation']}")
            print(f"   Time: {change['timestamp']}")
            if 'backup' in change:
                print(f"   Backup: {change['backup']}")

        print("\n" + "=" * 60)

    def deploy(self, message=None, dry_run=False):
        """
        Deploy changes to Netlify

        Args:
            message: Commit message (auto-generated if not provided)
            dry_run: If True, show what would be deployed without actually deploying

        Returns:
            True if successful
        """
        if not self.session_changes:
            print("❌ No changes to deploy")
            return False

        # Generate commit message
        if not message:
            files_changed = len(self.session_changes)
            message = f"Araya edit: {files_changed} files changed ({self.session_id})"

        print("\n" + "=" * 60)
        print("🚀 DEPLOYING TO NETLIFY")
        print("=" * 60)

        # Preview
        self.preview_changes()

        if dry_run:
            print("\n🔍 DRY RUN - No actual deployment")
            return True

        try:
            # Git add changed files
            for change in self.session_changes:
                file_path = self.site_root / change['file']
                subprocess.run(['git', 'add', str(file_path)],
                             cwd=str(self.site_root), check=True)

            # Git commit
            subprocess.run(['git', 'commit', '-m', message],
                         cwd=str(self.site_root), check=True)

            print("✅ Changes committed to git")

            # Deploy to Netlify
            print("\n📦 Deploying to Netlify...")
            result = subprocess.run(['netlify', 'deploy', '--prod', '--dir=frontend'],
                                  cwd=str(self.site_root),
                                  capture_output=True,
                                  text=True)

            if result.returncode == 0:
                print("✅ Deployed to Netlify!")
                print("\n🌐 Live at: https://conciousnessrevolution.io")
                return True
            else:
                print(f"❌ Deployment failed: {result.stderr}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"❌ Error during deployment: {e}")
            return False

    def rollback(self, file_path=None):
        """
        Rollback changes from backups

        Args:
            file_path: Specific file to rollback (or None for all files in session)

        Returns:
            True if successful
        """
        if file_path:
            # Rollback specific file
            changes = [c for c in self.session_changes if c['file'] == file_path]
            if not changes:
                print(f"❌ No changes found for {file_path}")
                return False

            change = changes[-1]  # Most recent change
            backup_path = Path(change['backup'])
            full_path = self.site_root / file_path

            shutil.copy2(backup_path, full_path)
            print(f"↩️  Rolled back {file_path}")
            return True

        else:
            # Rollback all changes
            print(f"\n↩️  Rolling back all changes from session {self.session_id}...")

            for change in self.session_changes:
                if 'backup' in change:
                    backup_path = Path(change['backup'])
                    full_path = self.site_root / change['file']
                    shutil.copy2(backup_path, full_path)
                    print(f"   ↩️  {change['file']}")

            print("✅ All changes rolled back")
            return True

    def save_session(self):
        """
        Save session changes to JSON for future reference
        """
        session_file = self.backup_dir / f"session_{self.session_id}.json"

        with open(session_file, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'changes': self.session_changes,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)

        print(f"💾 Session saved: {session_file}")


class ArayaConversationalEditor:
    """
    Natural language interface to site editing
    Araya can understand conversational editing requests
    """

    def __init__(self):
        self.editor = ArayaSiteEditor()

    def understand_request(self, request):
        """
        Parse natural language editing request

        Args:
            request: User's natural language request

        Returns:
            Dict with editing instructions
        """
        request_lower = request.lower()

        # Detect file
        file_match = re.search(r'([\w\-]+\.html|[\w\-]+\.js|[\w\-]+\.css)', request)
        file_path = f"frontend/{file_match.group(1)}" if file_match else None

        # Detect operation
        if 'add script' in request_lower or 'inject script' in request_lower:
            return {
                'action': 'inject_script',
                'file': file_path,
                'params': self._extract_script(request)
            }

        elif 'add css' in request_lower or 'add style' in request_lower:
            return {
                'action': 'inject_css',
                'file': file_path,
                'params': self._extract_css(request)
            }

        elif 'change' in request_lower or 'replace' in request_lower:
            return {
                'action': 'edit_file',
                'file': file_path,
                'params': self._extract_find_replace(request)
            }

        elif 'create' in request_lower or 'new file' in request_lower:
            return {
                'action': 'create_file',
                'file': file_path,
                'params': self._extract_content(request)
            }

        else:
            return {'action': 'unknown', 'request': request}

    def _extract_script(self, request):
        """Extract script details from request"""
        # Look for URL
        url_match = re.search(r'https?://[^\s]+', request)
        if url_match:
            return {'script_url': url_match.group(0)}

        # Look for inline code
        code_match = re.search(r'```javascript\n(.*?)\n```', request, re.DOTALL)
        if code_match:
            return {'script_code': code_match.group(1)}

        return {}

    def _extract_css(self, request):
        """Extract CSS details from request"""
        # Similar to script extraction
        url_match = re.search(r'https?://[^\s]+\.css', request)
        if url_match:
            return {'css_url': url_match.group(0)}

        code_match = re.search(r'```css\n(.*?)\n```', request, re.DOTALL)
        if code_match:
            return {'css_code': code_match.group(1)}

        return {}

    def _extract_find_replace(self, request):
        """Extract find/replace strings"""
        # Look for quoted strings
        quotes = re.findall(r'"([^"]+)"', request)
        if len(quotes) >= 2:
            return {'find': quotes[0], 'replace': quotes[1]}
        return {}

    def _extract_content(self, request):
        """Extract file content"""
        code_match = re.search(r'```\n(.*?)\n```', request, re.DOTALL)
        if code_match:
            return {'content': code_match.group(1)}
        return {}

    def execute_request(self, request):
        """
        Execute natural language editing request

        Args:
            request: User's request in natural language

        Returns:
            Result of operation
        """
        instructions = self.understand_request(request)

        if instructions['action'] == 'unknown':
            return "I didn't understand that request. Can you rephrase?"

        action = instructions['action']
        file_path = instructions['file']
        params = instructions.get('params', {})

        # Execute
        method = getattr(self.editor, action)
        success = method(file_path, **params)

        if success:
            return f"✅ Successfully {action.replace('_', ' ')} on {file_path}"
        else:
            return f"❌ Failed to {action.replace('_', ' ')} on {file_path}"


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example_usage():
    """Show example usage of site editor"""

    print("\n" + "=" * 60)
    print("🤖 ARAYA SITE EDITOR - EXAMPLE USAGE")
    print("=" * 60)

    editor = ArayaSiteEditor()

    # Example 1: Add Userpilot snippet to index.html
    print("\n📝 Example 1: Add Userpilot snippet")
    editor.inject_script(
        'frontend/index.html',
        script_code="""
        !function(){var e=window.userpilot=window.userpilot||[];
        e.init("YOUR_TOKEN");}();
        """
    )

    # Example 2: Change page title
    print("\n📝 Example 2: Change page title")
    editor.edit_file(
        'frontend/index.html',
        find='<title>Consciousness Revolution</title>',
        replace='<title>Consciousness Revolution - 70/30 Creator Platform</title>'
    )

    # Example 3: Add custom CSS
    print("\n📝 Example 3: Add custom CSS")
    editor.inject_css(
        'frontend/index.html',
        css_code="""
        .araya-walkthrough-highlight {
            border: 2px solid #6366f1;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
        }
        """
    )

    # Preview changes
    editor.preview_changes()

    # Save session
    editor.save_session()

    print("\n✅ Example complete!")
    print("   Run editor.deploy() to push to Netlify")


if __name__ == "__main__":
    example_usage()
