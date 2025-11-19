#!/usr/bin/env python3
"""
Test Araya's Actual Capabilities
Let's find out what she can really do vs what we think she can do
"""

import os
import json
import subprocess
from datetime import datetime

class ArayaCapabilityTester:
    def __init__(self):
        self.results = {
            "test_date": datetime.now().isoformat(),
            "capabilities": {},
            "recommendations": []
        }

        print("="*70)
        print("🤖 ARAYA CAPABILITY TESTING")
        print("="*70)
        print("Testing what Araya can actually do...")
        print()

    def test_file_access(self):
        """Can Araya read/write files?"""
        print("📁 TEST 1: File Access")

        test_file = "C:/Users/dwrek/100X_DEPLOYMENT/ARAYA_TEST_FILE.txt"

        try:
            # Write test
            with open(test_file, 'w') as f:
                f.write("Araya was here!")

            # Read test
            with open(test_file, 'r') as f:
                content = f.read()

            # Cleanup
            os.remove(test_file)

            self.results["capabilities"]["file_access"] = {
                "status": "✅ WORKING",
                "read": True,
                "write": True,
                "notes": "Can read and write local files"
            }
            print("   ✅ Can read/write files")

        except Exception as e:
            self.results["capabilities"]["file_access"] = {
                "status": "❌ FAILED",
                "error": str(e)
            }
            print(f"   ❌ Failed: {e}")
        print()

    def test_api_access(self):
        """Does Araya have API keys?"""
        print("🔑 TEST 2: API Access")

        apis_tested = {}

        # Check Claude API
        claude_key = os.environ.get("ANTHROPIC_API_KEY")
        if claude_key:
            apis_tested["claude"] = "✅ Key found"
            print("   ✅ Claude API key available")
        else:
            apis_tested["claude"] = "❌ No key"
            print("   ❌ No Claude API key")

        # Check other APIs
        for api_name, env_var in [
            ("OpenAI", "OPENAI_API_KEY"),
            ("Groq", "GROQ_API_KEY"),
            ("DeepSeek", "DEEPSEEK_API_KEY")
        ]:
            if os.environ.get(env_var):
                apis_tested[api_name.lower()] = "✅ Key found"
                print(f"   ✅ {api_name} API key available")
            else:
                apis_tested[api_name.lower()] = "❌ No key"

        self.results["capabilities"]["api_access"] = apis_tested
        print()

    def test_knowledge_base(self):
        """Can Araya access her knowledge base?"""
        print("📚 TEST 3: Knowledge Base Access")

        kb_file = "C:/Users/dwrek/100X_DEPLOYMENT/ARAYA_KNOWLEDGE_BASE.json"

        try:
            with open(kb_file, 'r') as f:
                kb_data = json.load(f)

            # Check key sections
            sections = ["platform_context", "visitor_types", "available_downloads"]
            found_sections = [s for s in sections if s in kb_data]

            self.results["capabilities"]["knowledge_base"] = {
                "status": "✅ WORKING",
                "file": kb_file,
                "sections_found": found_sections,
                "notes": f"Found {len(found_sections)}/{len(sections)} expected sections"
            }

            print(f"   ✅ Knowledge base accessible")
            print(f"   📊 Sections: {', '.join(found_sections)}")

        except Exception as e:
            self.results["capabilities"]["knowledge_base"] = {
                "status": "❌ FAILED",
                "error": str(e)
            }
            print(f"   ❌ Failed: {e}")
        print()

    def test_command_execution(self):
        """Can Araya run commands?"""
        print("⚙️  TEST 4: Command Execution")

        try:
            # Test simple command
            result = subprocess.run(
                ['echo', 'Araya test'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                self.results["capabilities"]["command_execution"] = {
                    "status": "✅ WORKING",
                    "notes": "Can execute system commands"
                }
                print("   ✅ Can execute commands")
            else:
                self.results["capabilities"]["command_execution"] = {
                    "status": "⚠️  LIMITED",
                    "notes": "Command execution may be restricted"
                }
                print("   ⚠️  Command execution limited")

        except Exception as e:
            self.results["capabilities"]["command_execution"] = {
                "status": "❌ FAILED",
                "error": str(e)
            }
            print(f"   ❌ Failed: {e}")
        print()

    def test_network_access(self):
        """Can Araya access the network?"""
        print("🌐 TEST 5: Network Access")

        try:
            import urllib.request

            # Try to reach a simple endpoint
            response = urllib.request.urlopen('https://www.google.com', timeout=5)

            if response.status == 200:
                self.results["capabilities"]["network_access"] = {
                    "status": "✅ WORKING",
                    "notes": "Can access external networks"
                }
                print("   ✅ Network access working")
            else:
                self.results["capabilities"]["network_access"] = {
                    "status": "⚠️  LIMITED",
                    "notes": f"Got status code: {response.status}"
                }
                print(f"   ⚠️  Limited (status: {response.status})")

        except Exception as e:
            self.results["capabilities"]["network_access"] = {
                "status": "❌ FAILED",
                "error": str(e)
            }
            print(f"   ❌ Failed: {e}")
        print()

    def test_python_libraries(self):
        """What Python libraries are available?"""
        print("📦 TEST 6: Available Python Libraries")

        required_libs = [
            "flask", "anthropic", "openai", "sounddevice",
            "numpy", "requests", "psutil"
        ]

        available = {}

        for lib in required_libs:
            try:
                __import__(lib)
                available[lib] = "✅ Installed"
                print(f"   ✅ {lib}")
            except ImportError:
                available[lib] = "❌ Missing"
                print(f"   ❌ {lib} not installed")

        self.results["capabilities"]["python_libraries"] = available
        print()

    def generate_recommendations(self):
        """Based on tests, what should Araya be able to do?"""
        print("="*70)
        print("💡 RECOMMENDATIONS")
        print("="*70)

        caps = self.results["capabilities"]

        # Check file access
        if caps.get("file_access", {}).get("status") == "✅ WORKING":
            self.results["recommendations"].append({
                "capability": "File Management",
                "action": "Araya can help users find, read, and organize files",
                "priority": "HIGH"
            })
            print("✅ Araya CAN: Help with file management")

        # Check API access
        if caps.get("api_access", {}).get("claude") == "✅ Key found":
            self.results["recommendations"].append({
                "capability": "Intelligent Responses",
                "action": "Connect Araya to Claude API for smart conversations",
                "priority": "HIGH"
            })
            print("✅ Araya CAN: Use Claude API for intelligent responses")
        else:
            self.results["recommendations"].append({
                "capability": "Intelligent Responses",
                "action": "Set ANTHROPIC_API_KEY to enable Claude API",
                "priority": "MEDIUM"
            })
            print("⚠️  Araya NEEDS: Claude API key for smart responses")

        # Check knowledge base
        if caps.get("knowledge_base", {}).get("status") == "✅ WORKING":
            self.results["recommendations"].append({
                "capability": "Context-Aware Help",
                "action": "Araya can provide accurate platform information",
                "priority": "HIGH"
            })
            print("✅ Araya CAN: Provide accurate platform information")

        # Check command execution
        if caps.get("command_execution", {}).get("status") == "✅ WORKING":
            self.results["recommendations"].append({
                "capability": "System Automation",
                "action": "Araya can help start services, run scripts",
                "priority": "MEDIUM"
            })
            print("✅ Araya CAN: Run system commands")

        # Check network
        if caps.get("network_access", {}).get("status") == "✅ WORKING":
            self.results["recommendations"].append({
                "capability": "External Integration",
                "action": "Araya can fetch external data, check APIs",
                "priority": "LOW"
            })
            print("✅ Araya CAN: Access external networks")

        print()

    def save_results(self):
        """Save test results"""
        output_file = "C:/Users/dwrek/100X_DEPLOYMENT/ARAYA_CAPABILITY_TEST_RESULTS.json"

        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print("="*70)
        print(f"📝 Results saved to: {output_file}")
        print("="*70)
        print()

    def run_all_tests(self):
        """Run complete capability test suite"""
        self.test_file_access()
        self.test_api_access()
        self.test_knowledge_base()
        self.test_command_execution()
        self.test_network_access()
        self.test_python_libraries()
        self.generate_recommendations()
        self.save_results()

def main():
    tester = ArayaCapabilityTester()
    tester.run_all_tests()

    print("🎯 SUMMARY:")
    print("   Araya now has a complete knowledge base")
    print("   We know what she can and cannot do")
    print("   Recommendations generated for next steps")
    print()
    print("👉 Next: Connect Araya to Claude API for intelligent responses")

if __name__ == "__main__":
    main()
