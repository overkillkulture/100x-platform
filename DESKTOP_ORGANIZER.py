#!/usr/bin/env python3
"""
DESKTOP ORGANIZER
Automatically categorizes and organizes your desktop into clean folders

WHAT IT DOES:
- Scans desktop for all files
- Categorizes them intelligently
- Creates organized folder structure
- Moves files to appropriate folders
- Generates beautiful index HTML to find everything

CATEGORIES:
- 🧠 Consciousness Systems
- 🤖 Automation & Bots
- 📊 Analytics & Dashboards
- 🔐 Security & Passwords
- 💰 Business & Financial
- 📚 Documentation
- 🎨 Designs & Interfaces
- 🛠️ Tools & Scripts
- 🎯 Strategy & Planning
- 🎵 Music & Media
- 🔧 System & Config
- 📦 Archive (everything else)
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class DesktopOrganizer:
    def __init__(self):
        self.desktop = Path("C:/Users/dwrek/Desktop")
        self.organized_folder = self.desktop / "_ORGANIZED"

        # File categories
        self.categories = {
            "🧠 Consciousness Systems": {
                "keywords": ["consciousness", "overkore", "awakening", "manifestation", "trinity", "quantum"],
                "extensions": []
            },
            "🤖 Automation & Bots": {
                "keywords": ["bot", "automation", "autonomous", "puppet", "auto_", "script"],
                "extensions": [".py", ".bat", ".ps1"]
            },
            "📊 Analytics & Dashboards": {
                "keywords": ["dashboard", "analytics", "heatmap", "metrics", "cockpit"],
                "extensions": []
            },
            "🔐 Security & Passwords": {
                "keywords": ["password", "credential", "auth", "login", "key", "private", "secret", "attack", "defense"],
                "extensions": [".json", ".txt", ".1pux"]
            },
            "💰 Business & Financial": {
                "keywords": ["banking", "payment", "money", "financial", "stripe", "revenue"],
                "extensions": [".xlsx"]
            },
            "📚 Documentation": {
                "keywords": ["guide", "manual", "checklist", "handbook", "README", "strategy", "plan"],
                "extensions": [".md", ".txt"]
            },
            "🎨 Designs & Interfaces": {
                "keywords": ["design", "interface", "ui", "visualization", "visualizer", "platform"],
                "extensions": [".html", ".css"]
            },
            "🛠️ Tools & Scripts": {
                "keywords": ["tool", "utility", "system", "scanner", "extractor", "builder"],
                "extensions": [".py", ".js"]
            },
            "🎯 Strategy & Planning": {
                "keywords": ["strategy", "blueprint", "architecture", "roadmap", "vision", "master"],
                "extensions": [".md"]
            },
            "🎵 Music & Media": {
                "keywords": ["music", "video", "song", "distribution", "instagram", "social"],
                "extensions": [".mp3", ".mp4", ".png", ".jpg"]
            },
            "🔧 System & Config": {
                "keywords": ["config", "setting", "launch", "start", "run", "deploy"],
                "extensions": [".bat", ".lnk", ".ini", ".json"]
            }
        }

    def categorize_file(self, filename):
        """Determine which category a file belongs to"""
        filename_lower = filename.lower()

        # Check each category
        for category, rules in self.categories.items():
            # Check keywords
            for keyword in rules["keywords"]:
                if keyword.lower() in filename_lower:
                    return category

            # Check extensions
            for ext in rules["extensions"]:
                if filename_lower.endswith(ext):
                    return category

        # Default category
        return "📦 Archive"

    def organize(self, dry_run=True):
        """Organize desktop files"""
        print("🗂️  DESKTOP ORGANIZER\n")

        # Get all files on desktop
        files = [f for f in self.desktop.iterdir() if f.is_file()]
        folders = [f for f in self.desktop.iterdir() if f.is_dir() and f.name != "_ORGANIZED"]

        print(f"Found {len(files)} files and {len(folders)} folders\n")

        # Categorize files
        categorized = {}
        for file in files:
            category = self.categorize_file(file.name)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(file)

        # Show what would happen
        print("📋 ORGANIZATION PLAN:\n")
        for category, items in sorted(categorized.items()):
            print(f"{category} ({len(items)} items)")
            for item in sorted(items)[:5]:  # Show first 5
                print(f"  • {item.name}")
            if len(items) > 5:
                print(f"  ... and {len(items) - 5} more")
            print()

        if dry_run:
            print("🔍 DRY RUN - No files moved")
            print("\nRun with --execute to actually move files")
            return categorized

        # Actually organize
        print("📦 ORGANIZING FILES...\n")

        # Create organized folder structure
        self.organized_folder.mkdir(exist_ok=True)

        for category in categorized.keys():
            category_folder = self.organized_folder / category
            category_folder.mkdir(exist_ok=True)

        # Move files
        moved = 0
        for category, items in categorized.items():
            category_folder = self.organized_folder / category
            for item in items:
                try:
                    dest = category_folder / item.name
                    shutil.move(str(item), str(dest))
                    print(f"✅ Moved: {item.name} → {category}")
                    moved += 1
                except Exception as e:
                    print(f"❌ Error moving {item.name}: {e}")

        print(f"\n✅ Organized {moved} files!")

        # Create index
        self.create_index(categorized)

        return categorized

    def create_index(self, categorized):
        """Create beautiful HTML index of all organized files"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Desktop - Organized</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .search-box {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .category {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .category-header {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ddd;
        }
        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 10px;
        }
        .file-item {
            background: white;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .file-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateX(5px);
        }
        .file-icon {
            font-size: 1.5em;
        }
        .file-name {
            flex: 1;
            font-size: 0.9em;
            color: #333;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .timestamp {
            text-align: center;
            color: #999;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗂️ Desktop - Organized</h1>
        <p class="subtitle">Everything in its place, everything findable</p>

        <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search for any file...">

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_files}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_categories}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">100%</div>
                <div class="stat-label">Organized</div>
            </div>
        </div>

        <div id="categories">
            {categories_html}
        </div>

        <div class="timestamp">
            Organized: {timestamp}
        </div>
    </div>

    <script>
        // Search functionality
        const searchBox = document.getElementById('searchBox');
        searchBox.addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const fileItems = document.querySelectorAll('.file-item');

            fileItems.forEach(item => {{
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {{
                    item.style.display = 'flex';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }});

        // File click handling
        document.querySelectorAll('.file-item').forEach(item => {{
            item.addEventListener('click', () => {{
                const path = item.dataset.path;
                window.open(path, '_blank');
            }});
        }});
    </script>
</body>
</html>"""

        # Generate categories HTML
        categories_html = ""
        total_files = 0

        for category, items in sorted(categorized.items()):
            total_files += len(items)

            files_html = ""
            for item in sorted(items):
                icon = self.get_icon(item.suffix)
                file_path = str(self.organized_folder / category / item.name)
                files_html += f'''
                <div class="file-item" data-path="{file_path}">
                    <span class="file-icon">{icon}</span>
                    <span class="file-name">{item.name}</span>
                </div>'''

            categories_html += f'''
            <div class="category">
                <div class="category-header">{category} <span style="color: #999;">({len(items)})</span></div>
                <div class="file-grid">
                    {files_html}
                </div>
            </div>'''

        # Fill in template
        html = html.format(
            total_files=total_files,
            total_categories=len(categorized),
            categories_html=categories_html,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Save index
        index_path = self.organized_folder / "INDEX.html"
        index_path.write_text(html, encoding='utf-8')

        print(f"\n📖 Created index: {index_path}")

    def get_icon(self, extension):
        """Get emoji icon for file type"""
        icons = {
            '.html': '🌐',
            '.py': '🐍',
            '.js': '📜',
            '.md': '📄',
            '.txt': '📝',
            '.json': '🗂️',
            '.bat': '⚙️',
            '.ps1': '💻',
            '.xlsx': '📊',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.lnk': '🔗',
        }
        return icons.get(extension.lower(), '📄')

def main():
    import sys

    organizer = DesktopOrganizer()

    # Check for --execute flag
    execute = '--execute' in sys.argv or '-e' in sys.argv

    if execute:
        print("⚠️  EXECUTE MODE - Files will be moved!\n")
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return

    categorized = organizer.organize(dry_run=not execute)

    if execute:
        print("\n✅ DESKTOP ORGANIZED!")
        print("\n📖 Open INDEX.html to browse all files")
        print(f"   Location: {organizer.organized_folder / 'INDEX.html'}")

if __name__ == '__main__':
    main()
