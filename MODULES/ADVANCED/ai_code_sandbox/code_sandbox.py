#!/usr/bin/env python3
"""
AI CODE SANDBOX - Instant online code editor with Claude AI assistance
Compete with Replit, CodeSandbox, StackBlitz
"""

import os
import json
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import tempfile
import shutil

try:
    import anthropic
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages missing")
    print("   pip install anthropic python-dotenv docker flask flask-socketio")
    exit(1)

load_dotenv()


class Language:
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    CSHARP = "csharp"
    SWIFT = "swift"
    KOTLIN = "kotlin"


class ExecutionResult:
    """Result of code execution"""

    def __init__(self, output: str, error: str = "", execution_time: int = 0,
                 memory_used: float = 0, exit_code: int = 0):
        self.output = output
        self.error = error
        self.execution_time = execution_time  # milliseconds
        self.memory_used = memory_used  # MB
        self.exit_code = exit_code
        self.success = exit_code == 0

    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            'output': self.output,
            'error': self.error,
            'execution_time': self.execution_time,
            'memory_used': self.memory_used,
            'exit_code': self.exit_code,
            'success': self.success
        }


class SandboxProject:
    """Represents a code sandbox project"""

    def __init__(self, project_id: str, name: str, language: str, owner: str):
        self.id = project_id
        self.name = name
        self.language = language
        self.owner = owner
        self.created = datetime.now().isoformat()
        self.files = {}  # filename -> content
        self.collaborators = []
        self.is_public = False
        self.deployment_url = None

    def add_file(self, filename: str, content: str):
        """Add file to project"""
        self.files[filename] = content

    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'language': self.language,
            'owner': self.owner,
            'created': self.created,
            'files': self.files,
            'collaborators': self.collaborators,
            'is_public': self.is_public,
            'deployment_url': self.deployment_url
        }


class LanguageExecutor:
    """Execute code in different languages"""

    def __init__(self):
        self.executors = {
            Language.PYTHON: self._execute_python,
            Language.JAVASCRIPT: self._execute_javascript,
            Language.JAVA: self._execute_java,
            Language.CPP: self._execute_cpp,
            Language.GO: self._execute_go,
            Language.RUST: self._execute_rust,
            Language.RUBY: self._execute_ruby,
            Language.PHP: self._execute_php
        }

    def execute(self, language: str, code: str, timeout: int = 30) -> ExecutionResult:
        """Execute code in specified language"""
        print(f"\n🚀 Executing {language} code...")

        executor = self.executors.get(language)
        if not executor:
            return ExecutionResult(
                output="",
                error=f"Language {language} not supported",
                exit_code=1
            )

        try:
            return executor(code, timeout)
        except Exception as e:
            return ExecutionResult(
                output="",
                error=f"Execution error: {str(e)}",
                exit_code=1
            )

    def _execute_python(self, code: str, timeout: int) -> ExecutionResult:
        """Execute Python code"""
        import time

        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute
            start_time = time.time()

            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            execution_time = int((time.time() - start_time) * 1000)

            print(f"   ✅ Executed in {execution_time}ms")

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            # Cleanup
            Path(temp_file).unlink(missing_ok=True)

    def _execute_javascript(self, code: str, timeout: int) -> ExecutionResult:
        """Execute JavaScript code (Node.js)"""
        import time

        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()

            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            execution_time = int((time.time() - start_time) * 1000)

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            Path(temp_file).unlink(missing_ok=True)

    def _execute_cpp(self, code: str, timeout: int) -> ExecutionResult:
        """Execute C++ code"""
        import time

        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        source_file = Path(temp_dir) / "main.cpp"
        binary_file = Path(temp_dir) / "main"

        try:
            # Write source
            source_file.write_text(code)

            # Compile
            compile_result = subprocess.run(
                ['g++', str(source_file), '-o', str(binary_file), '-std=c++17'],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if compile_result.returncode != 0:
                return ExecutionResult(
                    output="",
                    error=f"Compilation error:\n{compile_result.stderr}",
                    exit_code=1
                )

            # Execute
            start_time = time.time()

            result = subprocess.run(
                [str(binary_file)],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            execution_time = int((time.time() - start_time) * 1000)

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _execute_java(self, code: str, timeout: int) -> ExecutionResult:
        """Execute Java code"""
        import time

        temp_dir = tempfile.mkdtemp()

        try:
            # Extract class name
            import re
            match = re.search(r'public\s+class\s+(\w+)', code)
            class_name = match.group(1) if match else 'Main'

            source_file = Path(temp_dir) / f"{class_name}.java"
            source_file.write_text(code)

            # Compile
            compile_result = subprocess.run(
                ['javac', str(source_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )

            if compile_result.returncode != 0:
                return ExecutionResult(
                    output="",
                    error=f"Compilation error:\n{compile_result.stderr}",
                    exit_code=1
                )

            # Execute
            start_time = time.time()

            result = subprocess.run(
                ['java', class_name],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )

            execution_time = int((time.time() - start_time) * 1000)

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _execute_go(self, code: str, timeout: int) -> ExecutionResult:
        """Execute Go code"""
        import time

        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()

            result = subprocess.run(
                ['go', 'run', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            execution_time = int((time.time() - start_time) * 1000)

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            Path(temp_file).unlink(missing_ok=True)

    def _execute_rust(self, code: str, timeout: int) -> ExecutionResult:
        """Execute Rust code"""
        # Simplified - in production would use rustc
        return ExecutionResult(
            output="",
            error="Rust execution requires rustc (coming soon)",
            exit_code=1
        )

    def _execute_ruby(self, code: str, timeout: int) -> ExecutionResult:
        """Execute Ruby code"""
        import time

        with tempfile.NamedTemporaryFile(mode='w', suffix='.rb', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()

            result = subprocess.run(
                ['ruby', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            execution_time = int((time.time() - start_time) * 1000)

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            Path(temp_file).unlink(missing_ok=True)

    def _execute_php(self, code: str, timeout: int) -> ExecutionResult:
        """Execute PHP code"""
        import time

        with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()

            result = subprocess.run(
                ['php', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            execution_time = int((time.time() - start_time) * 1000)

            return ExecutionResult(
                output=result.stdout,
                error=result.stderr,
                execution_time=execution_time,
                exit_code=result.returncode
            )

        finally:
            Path(temp_file).unlink(missing_ok=True)


class AICodeAssistant:
    """Claude AI-powered code assistant"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.claude = anthropic.Anthropic(api_key=api_key)

    def debug_code(self, code: str, error: str, language: str) -> str:
        """AI debugs code and suggests fix"""
        print(f"\n🤖 AI debugging {language} code...")

        prompt = f"""Debug this {language} code. It's producing this error:

ERROR:
{error}

CODE:
{code}

Provide:
1. Explanation of what's wrong
2. Fixed code
3. Why the fix works

Be concise and practical."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            suggestion = response.content[0].text
            print(f"   ✅ AI provided fix")

            return suggestion

        except Exception as e:
            print(f"   ❌ AI assist failed: {e}")
            return "AI assistance temporarily unavailable"

    def explain_code(self, code: str, language: str) -> str:
        """AI explains what code does"""
        print(f"\n📖 AI explaining code...")

        prompt = f"""Explain this {language} code in simple terms:

{code}

Explain:
1. What it does (in plain English)
2. How it works (step by step)
3. Any important concepts used

Keep it simple and beginner-friendly."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            explanation = response.content[0].text
            print(f"   ✅ AI explained code")

            return explanation

        except Exception as e:
            return f"Explanation failed: {e}"

    def optimize_code(self, code: str, language: str) -> str:
        """AI optimizes code for performance"""
        print(f"\n⚡ AI optimizing code...")

        prompt = f"""Optimize this {language} code for better performance:

{code}

Provide:
1. Optimized version
2. What you improved
3. Performance impact

Focus on practical optimizations."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            optimized = response.content[0].text
            print(f"   ✅ AI optimized code")

            return optimized

        except Exception as e:
            return f"Optimization failed: {e}"

    def generate_tests(self, code: str, language: str) -> str:
        """AI generates unit tests"""
        print(f"\n🧪 AI generating tests...")

        prompt = f"""Generate unit tests for this {language} code:

{code}

Provide:
1. Test cases covering normal cases
2. Edge cases
3. Error cases
4. Use appropriate testing framework

Make tests comprehensive but practical."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}]
            )

            tests = response.content[0].text
            print(f"   ✅ AI generated tests")

            return tests

        except Exception as e:
            return f"Test generation failed: {e}"


class CodeSandbox:
    """Main orchestrator for code sandbox platform"""

    def __init__(self):
        self.executor = LanguageExecutor()
        self.ai_assistant = AICodeAssistant()

        self.projects_dir = Path.home() / ".code_sandbox" / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        self.projects = {}  # project_id -> SandboxProject

    def create_project(self, name: str, language: str, owner: str,
                      template: str = "blank") -> SandboxProject:
        """Create new sandbox project"""
        print(f"\n📦 Creating project: {name}")

        project_id = hashlib.md5(f"{name}{owner}{datetime.now()}".encode()).hexdigest()[:12]

        project = SandboxProject(
            project_id=project_id,
            name=name,
            language=language,
            owner=owner
        )

        # Add template files
        if template == "blank":
            if language == Language.PYTHON:
                project.add_file("main.py", "print('Hello World')\n")
            elif language == Language.JAVASCRIPT:
                project.add_file("main.js", "console.log('Hello World');\n")
            elif language == Language.CPP:
                project.add_file("main.cpp", "#include <iostream>\nint main() {\n    std::cout << \"Hello World\" << std::endl;\n    return 0;\n}\n")

        # Save project
        self.projects[project_id] = project
        self._save_project(project)

        print(f"   ✅ Project created: {project_id}")

        return project

    def execute_code(self, project_id: str, filename: str = None,
                    code: str = None, timeout: int = 30) -> ExecutionResult:
        """Execute code from project"""
        project = self.projects.get(project_id)
        if not project:
            return ExecutionResult(output="", error="Project not found", exit_code=1)

        # Get code
        if code is None:
            if filename is None:
                filename = "main.py" if project.language == Language.PYTHON else "main.js"
            code = project.files.get(filename, "")

        # Execute
        result = self.executor.execute(project.language, code, timeout)

        return result

    def ai_help(self, code: str, language: str, request_type: str = "debug",
               error: str = "") -> str:
        """Get AI assistance"""
        if request_type == "debug":
            return self.ai_assistant.debug_code(code, error, language)
        elif request_type == "explain":
            return self.ai_assistant.explain_code(code, language)
        elif request_type == "optimize":
            return self.ai_assistant.optimize_code(code, language)
        elif request_type == "tests":
            return self.ai_assistant.generate_tests(code, language)
        else:
            return "Unknown request type"

    def _save_project(self, project: SandboxProject):
        """Save project to disk"""
        project_file = self.projects_dir / f"{project.id}.json"
        with open(project_file, 'w') as f:
            json.dump(project.to_dict(), f, indent=2)

    def list_projects(self, owner: str) -> List[SandboxProject]:
        """List user's projects"""
        return [p for p in self.projects.values() if p.owner == owner]


def main():
    """CLI interface"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='AI Code Sandbox')
    parser.add_argument('--language', default='python', help='Programming language')
    parser.add_argument('--code', help='Code to execute')
    parser.add_argument('--file', help='File to execute')
    parser.add_argument('--ai-help', choices=['debug', 'explain', 'optimize', 'tests'],
                       help='Get AI assistance')

    args = parser.parse_args()

    print("=" * 70)
    print("💻 AI CODE SANDBOX")
    print("=" * 70)

    sandbox = CodeSandbox()

    # Demo mode
    if not args.code and not args.file:
        print("\n🧪 DEMO MODE - Running sample code")

        # Create demo project
        project = sandbox.create_project(
            name="Demo Project",
            language=Language.PYTHON,
            owner="demo_user"
        )

        # Sample code
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"Fib({i}) = {fibonacci(i)}")
"""

        print("\n📝 Code:")
        print(code)

        # Execute
        result = sandbox.execute_code(project.id, code=code)

        print("\n📤 Output:")
        print(result.output)

        if result.error:
            print("\n❌ Error:")
            print(result.error)

            # Get AI help
            print("\n🤖 Getting AI help...")
            ai_help = sandbox.ai_help(code, Language.PYTHON, "debug", result.error)
            print(ai_help)

        print(f"\n⚡ Execution time: {result.execution_time}ms")

        # AI explain
        print("\n📖 AI Explanation:")
        explanation = sandbox.ai_help(code, Language.PYTHON, "explain")
        print(explanation)

    else:
        # Execute user code
        if args.file:
            code = Path(args.file).read_text()
        else:
            code = args.code

        # Create project
        project = sandbox.create_project(
            name="User Project",
            language=args.language,
            owner="user"
        )

        # Execute
        result = sandbox.execute_code(project.id, code=code)

        print("\n📤 Output:")
        print(result.output)

        if result.error:
            print("\n❌ Error:")
            print(result.error)

        # AI help if requested
        if args.ai_help:
            print(f"\n🤖 AI {args.ai_help.capitalize()}:")
            help_text = sandbox.ai_help(code, args.language, args.ai_help, result.error)
            print(help_text)

    print("\n" + "=" * 70)
    print("💡 Full platform at: https://conciousnesscode.dev")
    print("=" * 70)


if __name__ == "__main__":
    main()
