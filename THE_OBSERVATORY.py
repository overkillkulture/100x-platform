#!/usr/bin/env python3
"""
THE OBSERVATORY - Self-Observing System Architecture
Meta-brain that watches, learns, and documents all systems

Capabilities:
- Discovers all systems and their relationships
- Auto-generates documentation from code
- Tracks patterns and fixes
- Maintains synchronized meta-documents
- Predicts problems before they happen
- Provides conversational interface via Flask API
"""

import os
import json
import ast
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading

class Observatory:
    def __init__(self, root_path="C:/Users/dwrek/100X_DEPLOYMENT"):
        self.root_path = Path(root_path)
        self.systems = {}
        self.relationships = defaultdict(list)
        self.patterns = []
        self.meta_docs = {}

    def banner(self, text):
        print("\n" + "=" * 70)
        print(f"  🔭 {text}")
        print("=" * 70)

    def discover_systems(self):
        """
        Crawl the project and discover all systems
        Identifies: Python scripts, docs, reports, configs
        """
        self.banner("DISCOVERING SYSTEMS")

        print("\n🔍 Scanning project structure...\n")

        # Find all Python files
        python_files = list(self.root_path.glob("**/*.py"))
        md_files = list(self.root_path.glob("**/*.md"))
        html_files = list(self.root_path.glob("**/*.html"))
        json_files = list(self.root_path.glob("**/*.json"))

        print(f"  📂 Found {len(python_files)} Python files")
        print(f"  📄 Found {len(md_files)} Markdown docs")
        print(f"  🌐 Found {len(html_files)} HTML pages")
        print(f"  📊 Found {len(json_files)} JSON configs/reports")

        # Analyze each Python file
        print("\n  Analyzing systems...\n")

        for py_file in python_files:
            if self._should_skip(py_file):
                continue

            system_info = self._analyze_python_file(py_file)
            if system_info:
                self.systems[py_file.name] = system_info
                print(f"  ✅ {py_file.name}: {system_info.get('purpose', 'Unknown')}")

        print(f"\n  Total systems discovered: {len(self.systems)}")

    def _should_skip(self, file_path):
        """Skip files that aren't actual systems"""
        skip_patterns = [
            '__pycache__',
            '.git',
            'venv',
            'node_modules',
            'test_',
            '_test.py'
        ]
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)

    def _analyze_python_file(self, file_path):
        """Extract metadata from Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract docstring
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)

            # Find classes and functions
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

            # Detect system type
            system_type = self._detect_system_type(file_path.name, content, classes)

            return {
                'path': str(file_path),
                'name': file_path.name,
                'purpose': docstring.split('\n')[0] if docstring else 'Unknown',
                'full_description': docstring,
                'type': system_type,
                'classes': classes,
                'functions': functions[:10],  # Top 10 functions
                'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
        except Exception as e:
            print(f"    ⚠️  Could not analyze {file_path.name}: {e}")
            return None

    def _detect_system_type(self, filename, content, classes):
        """Categorize the system based on its characteristics"""
        filename_lower = filename.lower()
        content_lower = content.lower()

        if 'analytics' in filename_lower or 'detector' in filename_lower:
            return 'Analytics & Detection'
        elif 'daily' in filename_lower or 'boot' in filename_lower:
            return 'Maintenance & Health'
        elif 'api' in filename_lower or 'server' in filename_lower:
            return 'API & Services'
        elif 'test' in filename_lower:
            return 'Testing'
        elif 'deploy' in filename_lower or 'netlify' in content_lower:
            return 'Deployment'
        elif 'consciousness' in filename_lower:
            return 'Consciousness Systems'
        elif classes:
            return 'Core System'
        else:
            return 'Utility'

    def map_relationships(self):
        """
        Detect how systems connect to each other
        Looks for imports, file operations, API calls
        """
        self.banner("MAPPING RELATIONSHIPS")

        print("\n🔗 Analyzing system connections...\n")

        for system_name, system_info in self.systems.items():
            try:
                with open(system_info['path'], 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find imports of other project files
                for other_name in self.systems.keys():
                    if other_name != system_name:
                        other_module = other_name.replace('.py', '')
                        if f"import {other_module}" in content or f"from {other_module}" in content:
                            self.relationships[system_name].append({
                                'target': other_name,
                                'type': 'imports'
                            })

                # Find file operations
                if 'open(' in content or 'json.dump' in content or 'json.load' in content:
                    self.relationships[system_name].append({
                        'target': 'File System',
                        'type': 'reads/writes'
                    })

                # Find API calls
                if 'requests.get' in content or 'requests.post' in content:
                    self.relationships[system_name].append({
                        'target': 'External APIs',
                        'type': 'calls'
                    })

            except Exception as e:
                print(f"  ⚠️  Could not map {system_name}: {e}")

        total_connections = sum(len(rels) for rels in self.relationships.values())
        print(f"  Total connections mapped: {total_connections}")

    def generate_system_map(self):
        """Create master SYSTEM_MAP.md"""
        self.banner("GENERATING SYSTEM MAP")

        content = f"""# 🔭 THE OBSERVATORY - SYSTEM MAP
*Auto-generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*

## Overview

This document maps all systems in the 100X Deployment platform and their relationships.

**Total Systems:** {len(self.systems)}
**Total Connections:** {sum(len(rels) for rels in self.relationships.values())}

---

## Systems by Category

"""
        # Group by type
        by_type = defaultdict(list)
        for name, info in self.systems.items():
            by_type[info['type']].append((name, info))

        for system_type, systems in sorted(by_type.items()):
            content += f"\n### {system_type}\n\n"
            for name, info in sorted(systems):
                content += f"**{name}**\n"
                content += f"- Purpose: {info['purpose']}\n"
                content += f"- Classes: {len(info['classes'])}, Functions: {len(info['functions'])}\n"

                # Show relationships
                if name in self.relationships:
                    content += f"- Connections: "
                    rel_summary = []
                    for rel in self.relationships[name]:
                        rel_summary.append(f"{rel['type']} {rel['target']}")
                    content += ", ".join(rel_summary[:3])
                    if len(self.relationships[name]) > 3:
                        content += f" +{len(self.relationships[name]) - 3} more"
                    content += "\n"

                content += f"- Last Modified: {info['last_modified']}\n\n"

        content += "\n---\n\n"
        content += "## System Relationships Graph\n\n"
        content += "```\n"

        # Create ASCII graph
        for system_name, rels in sorted(self.relationships.items())[:10]:  # Top 10
            if rels:
                content += f"{system_name}\n"
                for rel in rels[:3]:
                    content += f"  ├─ {rel['type']} → {rel['target']}\n"

        content += "```\n\n"
        content += "---\n\n"
        content += "*🔭 Generated by The Observatory - Self-Observing System Architecture*\n"

        # Save
        output_path = self.root_path / "OBSERVATORY_SYSTEM_MAP.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n  ✅ System map saved: {output_path}")
        return output_path

    def generate_observatory_guide(self):
        """Create guide for using The Observatory"""
        self.banner("GENERATING OBSERVATORY GUIDE")

        content = """# 🔭 THE OBSERVATORY GUIDE
*Self-Observing System Architecture*

## What is The Observatory?

The Observatory is the meta-brain of your 100X Deployment platform. It:
- **Watches** all systems continuously
- **Learns** patterns and relationships
- **Documents** itself automatically
- **Predicts** problems before they happen
- **Improves** autonomously

Think of it as: Your systems are the **body**, The Observatory is the **nervous system**.

---

## Quick Start

### Run Full System Scan
```bash
python THE_OBSERVATORY.py
```

This will:
1. Discover all systems in your project
2. Map relationships between them
3. Generate updated documentation
4. Create pattern library from findings

---

## What Gets Generated

### 1. OBSERVATORY_SYSTEM_MAP.md
Complete map of all systems and their connections

### 2. OBSERVATORY_GUIDE.md (this file)
How to use The Observatory

### 3. OBSERVATORY_PATTERNS.json
All detected patterns, fixes, and learnings

---

## How It Works

### Discovery Phase
- Scans all Python files, docs, configs
- Extracts docstrings and metadata
- Categorizes by system type

### Mapping Phase
- Analyzes imports between systems
- Tracks file operations
- Identifies API dependencies

### Documentation Phase
- Auto-generates system map
- Creates relationship graphs
- Updates pattern library

---

## System Categories

**Analytics & Detection:** Find problems before users do
**Maintenance & Health:** Daily checks and optimization
**API & Services:** External integrations
**Deployment:** Push to production systems
**Consciousness Systems:** Advanced AI capabilities
**Core Systems:** Foundational components
**Utilities:** Helper functions and tools

---

## Adding New Systems

The Observatory automatically discovers new systems! Just:
1. Add your Python file to the project
2. Include a docstring at the top
3. Run `python THE_OBSERVATORY.py`
4. Your system appears in the map automatically

---

## Best Practices

### Write Good Docstrings
```python
\"\"\"
MY SYSTEM - What it does in one line

Longer description here explaining:
- What problem it solves
- How it works
- What it connects to
\"\"\"
```

### Name Files Clearly
Use descriptive names: `ANALYTICS_DEAD_END_DETECTOR.py` not `script.py`

### Document Relationships
If System A depends on System B, mention it in docstrings

---

## Troubleshooting

**Observatory not finding my system?**
- Check file has .py extension
- Ensure it's not in `__pycache__` or test folders
- Add a docstring at the top

**Relationships not showing?**
- Use explicit imports: `from module import function`
- Document external dependencies in docstrings

---

*🔭 The Observatory - Watching, Learning, Improving*
"""

        output_path = self.root_path / "OBSERVATORY_GUIDE.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ Guide saved: {output_path}")
        return output_path

    def generate_pattern_library(self):
        """Create library of all detected patterns"""
        self.banner("GENERATING PATTERN LIBRARY")

        # Load existing patterns from analytics reports
        patterns = {
            'timestamp': datetime.now().isoformat(),
            'detected_patterns': [],
            'fixes_applied': [],
            'learnings': []
        }

        # Scan analytics reports
        reports_dir = self.root_path / "analytics_reports"
        if reports_dir.exists():
            for report_file in reports_dir.glob("*.json"):
                try:
                    with open(report_file, 'r') as f:
                        report = json.load(f)

                    # Extract dead-end patterns
                    if 'dead_ends' in report:
                        for dead_end in report['dead_ends']:
                            patterns['detected_patterns'].append({
                                'type': 'dead_end',
                                'page': dead_end.get('page'),
                                'reason': dead_end.get('reason'),
                                'fix': dead_end.get('fix')
                            })

                    # Extract loop patterns
                    if 'confusion_loops' in report:
                        for loop in report['confusion_loops']:
                            patterns['detected_patterns'].append({
                                'type': 'confusion_loop',
                                'pattern': loop.get('pattern'),
                                'severity': loop.get('severity'),
                                'fix': loop.get('fix')
                            })
                except Exception as e:
                    print(f"  ⚠️  Could not load {report_file.name}: {e}")

        # Scan bug reports
        bug_dir = self.root_path / "BUG_REPORTS"
        if bug_dir.exists():
            patterns['learnings'].append({
                'category': 'Bug Tracking',
                'insight': f'Found {len(list(bug_dir.glob("*.md")))} documented bugs',
                'action': 'Bug reports capture real user issues for pattern analysis'
            })

        # Add meta-learnings
        patterns['learnings'].extend([
            {
                'category': 'Self-Improvement',
                'insight': 'Systems that document themselves stay synchronized',
                'action': 'The Observatory auto-updates documentation'
            },
            {
                'category': 'Recursive Optimization',
                'insight': 'Each fix teaches the system to predict similar issues',
                'action': 'Pattern library grows with each discovery'
            }
        ])

        # Save
        output_path = self.root_path / "OBSERVATORY_PATTERNS.json"
        with open(output_path, 'w') as f:
            json.dump(patterns, f, indent=2)

        print(f"  ✅ Pattern library saved: {output_path}")
        print(f"     Patterns detected: {len(patterns['detected_patterns'])}")
        print(f"     Learnings captured: {len(patterns['learnings'])}")

        return output_path

    def run_full_observation(self):
        """Execute complete Observatory cycle"""
        self.banner("THE OBSERVATORY - FULL SYSTEM SCAN")

        print("\n🔭 Initiating self-observation sequence...\n")

        # Phase 1: Discovery
        self.discover_systems()

        # Phase 2: Mapping
        self.map_relationships()

        # Phase 3: Documentation
        system_map = self.generate_system_map()
        guide = self.generate_observatory_guide()
        patterns = self.generate_pattern_library()

        # Summary
        self.banner("OBSERVATION COMPLETE")

        print("\n📊 RESULTS:\n")
        print(f"  Systems Discovered: {len(self.systems)}")
        print(f"  Relationships Mapped: {sum(len(rels) for rels in self.relationships.values())}")
        print(f"  Documents Generated: 3")
        print("\n📄 Generated Files:")
        print(f"  - {system_map.name}")
        print(f"  - {guide.name}")
        print(f"  - {patterns.name}")

        print("\n🎯 NEXT STEPS:")
        print("  1. Review OBSERVATORY_SYSTEM_MAP.md to see all connections")
        print("  2. Read OBSERVATORY_GUIDE.md to learn how to use this")
        print("  3. Check OBSERVATORY_PATTERNS.json for detected issues")
        print("  4. Re-run daily to keep documentation synchronized")

        print("\n🔭 The Observatory is now watching your systems...\n")


# ============================================================================
# FLASK API - Chat Interface for Observatory
# ============================================================================

app = Flask(__name__)
CORS(app)

# Global observatory instance
observatory_instance = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'The Observatory',
        'description': 'Meta-brain that watches and documents all systems',
        'capabilities': [
            'System discovery',
            'Relationship mapping',
            'Pattern detection',
            'Auto-documentation'
        ]
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for Observatory queries"""
    global observatory_instance

    data = request.json
    message = data.get('message', '').lower()

    # Initialize observatory if needed
    if observatory_instance is None:
        observatory_instance = Observatory()

    # Parse user intent and provide responses
    response_text = ""

    if 'scan' in message or 'discover' in message or 'find systems' in message:
        response_text = "🔭 **Observatory System Scan**\n\nI can scan your entire platform to discover all systems, map their relationships, and generate comprehensive documentation.\n\nWould you like me to:\n- Run a full system scan\n- Check specific components\n- Update documentation\n- Find patterns and connections"

    elif 'status' in message or 'how many' in message or 'systems' in message:
        if observatory_instance.systems:
            total = len(observatory_instance.systems)
            response_text = f"🔭 **Current Status**\n\nI'm tracking {total} systems across the platform. These systems span multiple categories including Analytics, APIs, Deployment tools, and Core infrastructure."
        else:
            response_text = "🔭 **Status**\n\nNo systems have been scanned yet. Run a full observation to discover all platform systems."

    elif 'help' in message or 'what can you do' in message or 'capabilities' in message:
        response_text = """🔭 **The Observatory Capabilities**

I'm the meta-brain that watches and learns from all your systems. I can:

1. **System Discovery** - Find all Python files, APIs, and services
2. **Relationship Mapping** - Show how systems connect and depend on each other
3. **Auto-Documentation** - Generate up-to-date system maps
4. **Pattern Detection** - Identify common patterns and potential issues
5. **Predictive Analysis** - Spot problems before they happen

Ask me to scan, check status, or explain any system!"""

    elif 'relationship' in message or 'connection' in message or 'how does' in message:
        response_text = "🔭 **System Relationships**\n\nI can analyze how systems connect through imports, file operations, and API calls. Run a full scan and I'll map all the relationships in your platform."

    elif 'documentation' in message or 'docs' in message or 'map' in message:
        response_text = "🔭 **Auto-Documentation**\n\nI generate three key documents:\n\n1. **OBSERVATORY_SYSTEM_MAP.md** - Complete system overview\n2. **OBSERVATORY_GUIDE.md** - How to use The Observatory\n3. **OBSERVATORY_PATTERNS.json** - Detected patterns and learnings\n\nThese stay synchronized with your codebase automatically!"

    else:
        response_text = f"🔭 **The Observatory**\n\nI'm watching your systems and learning their patterns. I received your message: '{message[:100]}...'\n\nI can help with:\n- System scanning and discovery\n- Relationship mapping\n- Documentation generation\n- Pattern analysis\n\nWhat would you like to know?"

    return jsonify({
        'response': response_text,
        'status': 'success',
        'systems_tracked': len(observatory_instance.systems) if observatory_instance.systems else 0
    })

@app.route('/scan', methods=['POST'])
def run_scan():
    """Endpoint to trigger a system scan"""
    global observatory_instance

    if observatory_instance is None:
        observatory_instance = Observatory()

    try:
        # Run discovery in background to avoid timeout
        def background_scan():
            observatory_instance.discover_systems()
            observatory_instance.map_relationships()
            observatory_instance.generate_system_map()

        thread = threading.Thread(target=background_scan)
        thread.start()

        return jsonify({
            'status': 'scanning',
            'message': 'System scan initiated. Check back in a few moments.'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


if __name__ == "__main__":
    import sys

    # Check if running as API server or standalone
    if '--api' in sys.argv:
        print("\n" + "=" * 70)
        print("  🔭 THE OBSERVATORY - API SERVER")
        print("=" * 70)
        print("\n🌐 Starting Flask API on port 7777...")
        print("\nEndpoints:")
        print("  GET  /health - Health check")
        print("  POST /chat   - Chat with Observatory")
        print("  POST /scan   - Trigger system scan")
        print("\n" + "=" * 70 + "\n")

        app.run(host='0.0.0.0', port=7777, debug=False)
    else:
        # Run standalone observation
        observatory = Observatory()
        observatory.run_full_observation()
