"""
4-BOT ORCHESTRATOR SYSTEM
C3 Oracle → C2 Architect → C1 Mechanic → C0 Operator

The complete AI development team that replaces $18,000/mo in costs.
Created: October 25, 2025
"""

import os
import anthropic
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import re
import time

app = Flask(__name__)
CORS(app)

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Base directory for projects
PROJECTS_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/4bot_projects")
PROJECTS_DIR.mkdir(exist_ok=True)

# =============================================================================
# THE 4 BOTS - Each with specialized role
# =============================================================================

class C3_Oracle:
    """The Soul - Sees WHAT must emerge"""

    def analyze(self, user_request):
        """Understand user intent and define requirements"""
        print("🔮 C3 ORACLE analyzing request...")

        prompt = f"""You are C3 Oracle - The Soul of the development team.

User Request: "{user_request}"

Your job: Understand WHAT they want to build and define clear requirements.

Analyze:
1. What is the core purpose/goal?
2. Who is the target user?
3. What are the key features needed?
4. What is the simplest version that delivers value?

Return a JSON object:
{{
    "project_name": "descriptive-name",
    "purpose": "why this exists",
    "target_user": "who will use it",
    "core_features": ["feature1", "feature2", "feature3"],
    "success_criteria": "what makes this successful"
}}

Be concise and focus on ESSENTIAL requirements only."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text

        # Try to extract JSON
        try:
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                requirements = json.loads(json_match.group())
            else:
                # Fallback if no JSON
                requirements = {
                    "project_name": "custom-project",
                    "purpose": user_request,
                    "target_user": "general users",
                    "core_features": ["main functionality"],
                    "success_criteria": "works as expected"
                }
        except:
            requirements = {
                "project_name": "custom-project",
                "purpose": user_request,
                "target_user": "general users",
                "core_features": ["main functionality"],
                "success_criteria": "works as expected"
            }

        print(f"✅ C3 ORACLE complete: {requirements['project_name']}")
        return {
            "bot": "C3_ORACLE",
            "analysis": result,
            "requirements": requirements,
            "timestamp": datetime.now().isoformat()
        }


class C2_Architect:
    """The Mind - Designs HOW to scale"""

    def design(self, requirements):
        """Create architecture and technical design"""
        print("🏗️  C2 ARCHITECT designing architecture...")

        prompt = f"""You are C2 Architect - The Mind of the development team.

Requirements from C3 Oracle:
{json.dumps(requirements, indent=2)}

Your job: Design HOW to build this with clean, scalable architecture.

Design:
1. Technology stack (HTML/CSS/JS or include backend?)
2. File structure (what files are needed?)
3. Component breakdown (what does each file do?)
4. Data flow (how do components interact?)
5. Deployment strategy (static site, or needs server?)

Return a JSON object:
{{
    "tech_stack": ["html", "css", "javascript"],
    "files_needed": [
        {{"filename": "index.html", "purpose": "main entry point"}},
        {{"filename": "styles.css", "purpose": "styling"}},
        {{"filename": "app.js", "purpose": "functionality"}}
    ],
    "architecture_notes": "key design decisions",
    "deployment_type": "static" or "dynamic"
}}

Keep it SIMPLE. Prefer vanilla technologies over frameworks."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text

        # Extract JSON
        try:
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                architecture = json.loads(json_match.group())
            else:
                # Fallback
                architecture = {
                    "tech_stack": ["html", "css", "javascript"],
                    "files_needed": [
                        {"filename": "index.html", "purpose": "main entry"},
                        {"filename": "styles.css", "purpose": "styling"},
                        {"filename": "app.js", "purpose": "functionality"}
                    ],
                    "architecture_notes": "Simple static site",
                    "deployment_type": "static"
                }
        except:
            architecture = {
                "tech_stack": ["html", "css", "javascript"],
                "files_needed": [
                    {"filename": "index.html", "purpose": "main entry"},
                    {"filename": "styles.css", "purpose": "styling"},
                    {"filename": "app.js", "purpose": "functionality"}
                ],
                "architecture_notes": "Simple static site",
                "deployment_type": "static"
            }

        print(f"✅ C2 ARCHITECT complete: {len(architecture['files_needed'])} files planned")
        return {
            "bot": "C2_ARCHITECT",
            "design": result,
            "architecture": architecture,
            "timestamp": datetime.now().isoformat()
        }


class C1_Mechanic:
    """The Body - Builds what CAN work RIGHT NOW"""

    def build(self, requirements, architecture):
        """Write the actual code"""
        print("🔨 C1 MECHANIC building project...")

        files_created = []

        for file_spec in architecture['files_needed']:
            filename = file_spec['filename']
            purpose = file_spec['purpose']

            print(f"  Building {filename}...")

            prompt = f"""You are C1 Mechanic - The Body of the development team.

Project Requirements:
{json.dumps(requirements, indent=2)}

File to build: {filename}
Purpose: {purpose}

Architecture context:
{json.dumps(architecture, indent=2)}

Your job: Write clean, working code for this file.

Requirements:
- Write COMPLETE, functional code
- Include comments explaining key parts
- Follow best practices
- Make it production-ready
- If HTML, include proper structure
- If CSS, make it look good and responsive
- If JS, make it work without external libraries if possible

Return ONLY the code, no explanation before or after."""

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )

            code = response.content[0].text

            # Clean up code (remove markdown blocks if present)
            code = re.sub(r'^```\w*\n', '', code)
            code = re.sub(r'\n```$', '', code)

            files_created.append({
                "filename": filename,
                "purpose": purpose,
                "code": code,
                "size": len(code)
            })

        print(f"✅ C1 MECHANIC complete: {len(files_created)} files built")
        return {
            "bot": "C1_MECHANIC",
            "files": files_created,
            "timestamp": datetime.now().isoformat()
        }


class C0_Operator:
    """The Hands - Ships what IS ready"""

    def deploy(self, project_name, files):
        """Save files and prepare for deployment"""
        print("🚀 C0 OPERATOR deploying project...")

        # Create project directory
        project_dir = PROJECTS_DIR / project_name
        project_dir.mkdir(exist_ok=True)

        deployed_files = []

        for file_info in files:
            filename = file_info['filename']
            code = file_info['code']

            # Save file
            file_path = project_dir / filename
            file_path.write_text(code, encoding='utf-8')

            deployed_files.append({
                "filename": filename,
                "path": str(file_path),
                "url": f"/projects/{project_name}/{filename}",
                "size": file_info['size']
            })

            print(f"  Deployed {filename}")

        # Create deployment info
        deployment = {
            "project_name": project_name,
            "deployed_at": datetime.now().isoformat(),
            "files": deployed_files,
            "preview_url": f"http://localhost:8005/projects/{project_name}/index.html",
            "status": "live"
        }

        # Save deployment metadata
        meta_file = project_dir / "_deployment.json"
        meta_file.write_text(json.dumps(deployment, indent=2), encoding='utf-8')

        print(f"✅ C0 OPERATOR complete: Live at {deployment['preview_url']}")
        return {
            "bot": "C0_OPERATOR",
            "deployment": deployment,
            "timestamp": datetime.now().isoformat()
        }


# =============================================================================
# ORCHESTRATOR - Coordinates the 4 bots
# =============================================================================

class FourBotOrchestrator:
    """Coordinates C3 → C2 → C1 → C0 workflow"""

    def __init__(self):
        self.c3 = C3_Oracle()
        self.c2 = C2_Architect()
        self.c1 = C1_Mechanic()
        self.c0 = C0_Operator()

    def build_project(self, user_request):
        """Complete build pipeline: User request → Live deployment"""

        build_log = {
            "user_request": user_request,
            "started_at": datetime.now().isoformat(),
            "stages": []
        }

        try:
            # STAGE 1: C3 Oracle - Analyze requirements
            print("\n" + "="*60)
            print("STAGE 1: C3 ORACLE - Analyzing Requirements")
            print("="*60)
            start = time.time()
            c3_result = self.c3.analyze(user_request)
            c3_result['duration'] = time.time() - start
            build_log['stages'].append(c3_result)

            requirements = c3_result['requirements']

            # STAGE 2: C2 Architect - Design architecture
            print("\n" + "="*60)
            print("STAGE 2: C2 ARCHITECT - Designing Architecture")
            print("="*60)
            start = time.time()
            c2_result = self.c2.design(requirements)
            c2_result['duration'] = time.time() - start
            build_log['stages'].append(c2_result)

            architecture = c2_result['architecture']

            # STAGE 3: C1 Mechanic - Build the code
            print("\n" + "="*60)
            print("STAGE 3: C1 MECHANIC - Building Project")
            print("="*60)
            start = time.time()
            c1_result = self.c1.build(requirements, architecture)
            c1_result['duration'] = time.time() - start
            build_log['stages'].append(c1_result)

            files = c1_result['files']

            # STAGE 4: C0 Operator - Deploy it live
            print("\n" + "="*60)
            print("STAGE 4: C0 OPERATOR - Deploying Live")
            print("="*60)
            start = time.time()
            c0_result = self.c0.deploy(requirements['project_name'], files)
            c0_result['duration'] = time.time() - start
            build_log['stages'].append(c0_result)

            deployment = c0_result['deployment']

            # Final summary
            build_log['completed_at'] = datetime.now().isoformat()
            build_log['total_duration'] = sum(stage['duration'] for stage in build_log['stages'])
            build_log['status'] = 'success'
            build_log['preview_url'] = deployment['preview_url']

            print("\n" + "="*60)
            print("✅ BUILD COMPLETE!")
            print("="*60)
            print(f"Project: {requirements['project_name']}")
            print(f"Files: {len(files)}")
            print(f"Time: {build_log['total_duration']:.1f}s")
            print(f"Preview: {deployment['preview_url']}")
            print("="*60 + "\n")

            return build_log

        except Exception as e:
            build_log['status'] = 'error'
            build_log['error'] = str(e)
            build_log['completed_at'] = datetime.now().isoformat()
            print(f"\n❌ BUILD FAILED: {e}\n")
            return build_log


# =============================================================================
# FLASK API
# =============================================================================

orchestrator = FourBotOrchestrator()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "operational",
        "service": "4-Bot Orchestrator",
        "bots": ["C3_Oracle", "C2_Architect", "C1_Mechanic", "C0_Operator"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/build', methods=['POST'])
def build_project():
    """Main endpoint: User request → Complete project"""
    data = request.json
    user_request = data.get('request', '')

    if not user_request:
        return jsonify({"error": "No build request provided"}), 400

    print(f"\n🚀 NEW BUILD REQUEST: {user_request}\n")

    # Run the 4-bot pipeline
    result = orchestrator.build_project(user_request)

    return jsonify(result)

@app.route('/projects/<project_name>/<path:filename>')
def serve_project_file(project_name, filename):
    """Serve deployed project files"""
    project_dir = PROJECTS_DIR / project_name
    return send_from_directory(project_dir, filename)

@app.route('/api/projects', methods=['GET'])
def list_projects():
    """List all deployed projects"""
    projects = []

    for project_dir in PROJECTS_DIR.iterdir():
        if project_dir.is_dir():
            meta_file = project_dir / "_deployment.json"
            if meta_file.exists():
                meta = json.loads(meta_file.read_text())
                projects.append(meta)

    return jsonify({
        "projects": projects,
        "count": len(projects)
    })


if __name__ == '__main__':
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  WARNING: ANTHROPIC_API_KEY not found!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
    else:
        print("✅ Claude API key found")

    print("\n" + "="*60)
    print("🤖 4-BOT ORCHESTRATOR SYSTEM 🤖")
    print("="*60)
    print("The AI development team that replaces $18,000/mo")
    print()
    print("Meet the team:")
    print("  C3 ORACLE    🔮 - Sees WHAT must emerge")
    print("  C2 ARCHITECT 🏗️  - Designs HOW to scale")
    print("  C1 MECHANIC  🔨 - Builds what CAN work")
    print("  C0 OPERATOR  🚀 - Ships what IS ready")
    print("="*60)
    print()
    print("Endpoints:")
    print("  POST /api/build - Build a complete project")
    print("  GET  /api/projects - List all projects")
    print("  GET  /api/health - System status")
    print()
    print("Example request:")
    print('  curl -X POST http://localhost:8005/api/build \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"request":"Build me a todo list"}\'')
    print()
    print("="*60)
    print("🚀 System ready on port 8005")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=8005, debug=True)
