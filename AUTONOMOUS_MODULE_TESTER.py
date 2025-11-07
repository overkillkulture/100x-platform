#!/usr/bin/env python3
"""
🤖 AUTONOMOUS MODULE TESTER
Comprehensive testing system for all 20 platform modules
Runs autonomously to validate platform health
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class ModuleTester:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_modules': 0,
            'tested_modules': 0,
            'passed_modules': 0,
            'failed_modules': 0,
            'modules': []
        }

        # Module categories and their locations
        self.module_paths = {
            'INFRASTRUCTURE': [
                'MODULES/INFRASTRUCTURE/fundraising_integration',
                'MODULES/INFRASTRUCTURE/marketing_automation',
                'MODULES/INFRASTRUCTURE/design_engineering_hub',
                'MODULES/INFRASTRUCTURE/social_media_automation_suite'
            ],
            'LEGAL': [
                'MODULES/LEGAL/corruption_mapping_3d',
                'MODULES/LEGAL/law_module',
                'MODULES/LEGAL/pi_mapping_system'
            ],
            'ADVANCED': [
                'MODULES/ADVANCED/ai_code_sandbox',
                'MODULES/ADVANCED/autonomous_drone_system'
            ],
            'CONTENT': [
                'MODULES/CONTENT/ai_stock_media_generator',
                'MODULES/CONTENT/automatic_video_editing',
                'MODULES/CONTENT/music_production_suite',
                'MODULES/CONTENT/podcast_production'
            ],
            'HEALTH': [
                'MODULES/HEALTH/ai_personal_trainer'
            ],
            'AUTOMATION': [
                'MODULES/AUTOMATION/jarvis_assistant',
                'MODULES/AUTOMATION/social_media_automation'
            ],
            'KNOWLEDGE': [
                'MODULES/KNOWLEDGE/spreadsheet_brain',
                'MODULES/KNOWLEDGE/pattern_recognition_training',
                'MODULES/KNOWLEDGE/ai_data_crystals'
            ]
        }

    def test_module_exists(self, module_path):
        """Check if module directory exists"""
        return os.path.exists(module_path)

    def test_module_structure(self, module_path):
        """Validate module has proper structure"""
        checks = {
            'has_readme': os.path.exists(f'{module_path}/README.md'),
            'has_python_file': len(list(Path(module_path).glob('*.py'))) > 0,
            'has_requirements': os.path.exists(f'{module_path}/requirements.txt')
        }
        return checks

    def test_python_syntax(self, module_path):
        """Test Python files for syntax errors"""
        python_files = list(Path(module_path).glob('*.py'))
        syntax_results = []

        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    compile(code, str(py_file), 'exec')
                syntax_results.append({
                    'file': str(py_file),
                    'status': 'valid',
                    'error': None
                })
            except SyntaxError as e:
                syntax_results.append({
                    'file': str(py_file),
                    'status': 'error',
                    'error': str(e)
                })

        return syntax_results

    def test_imports(self, module_path):
        """Check if module imports work (static analysis)"""
        python_files = list(Path(module_path).glob('*.py'))
        import_results = []

        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    imports = [line.strip() for line in lines if line.strip().startswith(('import ', 'from '))]
                    import_results.append({
                        'file': str(py_file),
                        'import_count': len(imports),
                        'imports': imports[:5]  # First 5 imports
                    })
            except Exception as e:
                import_results.append({
                    'file': str(py_file),
                    'error': str(e)
                })

        return import_results

    def analyze_module_complexity(self, module_path):
        """Analyze module code complexity"""
        python_files = list(Path(module_path).glob('*.py'))
        total_lines = 0
        total_functions = 0
        total_classes = 0

        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    total_functions += sum(1 for line in lines if line.strip().startswith('def '))
                    total_classes += sum(1 for line in lines if line.strip().startswith('class '))
            except:
                pass

        return {
            'total_lines': total_lines,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'complexity_score': min(100, (total_lines // 10 + total_functions * 2 + total_classes * 5))
        }

    def test_single_module(self, category, module_path):
        """Run all tests on a single module"""
        module_name = os.path.basename(module_path)

        print(f"\n{'='*60}")
        print(f"Testing: {module_name} ({category})")
        print(f"{'='*60}")

        test_result = {
            'name': module_name,
            'category': category,
            'path': module_path,
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }

        # Test 1: Module exists
        exists = self.test_module_exists(module_path)
        test_result['tests']['exists'] = exists
        print(f"✓ Exists: {exists}")

        if not exists:
            test_result['status'] = 'FAILED'
            test_result['reason'] = 'Module directory not found'
            return test_result

        # Test 2: Structure validation
        structure = self.test_module_structure(module_path)
        test_result['tests']['structure'] = structure
        print(f"✓ README: {structure['has_readme']}")
        print(f"✓ Python files: {structure['has_python_file']}")
        print(f"✓ Requirements: {structure['has_requirements']}")

        # Test 3: Python syntax
        syntax = self.test_python_syntax(module_path)
        test_result['tests']['syntax'] = syntax
        syntax_valid = all(s['status'] == 'valid' for s in syntax)
        print(f"✓ Syntax check: {len(syntax)} files, all valid: {syntax_valid}")

        # Test 4: Import analysis
        imports = self.test_imports(module_path)
        test_result['tests']['imports'] = imports
        print(f"✓ Import analysis: {len(imports)} files analyzed")

        # Test 5: Complexity analysis
        complexity = self.analyze_module_complexity(module_path)
        test_result['tests']['complexity'] = complexity
        print(f"✓ Complexity: {complexity['total_lines']} lines, {complexity['total_functions']} functions, {complexity['total_classes']} classes")

        # Overall status
        if exists and structure['has_python_file'] and syntax_valid:
            test_result['status'] = 'PASSED'
            print(f"\n✅ {module_name}: PASSED")
        else:
            test_result['status'] = 'FAILED'
            print(f"\n❌ {module_name}: FAILED")

        return test_result

    def run_all_tests(self):
        """Run tests on all modules"""
        print("\n" + "="*60)
        print("🤖 AUTONOMOUS MODULE TESTER - STARTING")
        print("="*60)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Testing all platform modules...\n")

        # Count total modules
        for category, paths in self.module_paths.items():
            self.results['total_modules'] += len(paths)

        # Test each module
        for category, paths in self.module_paths.items():
            print(f"\n{'#'*60}")
            print(f"CATEGORY: {category}")
            print(f"{'#'*60}")

            for module_path in paths:
                result = self.test_single_module(category, module_path)
                self.results['modules'].append(result)
                self.results['tested_modules'] += 1

                if result['status'] == 'PASSED':
                    self.results['passed_modules'] += 1
                else:
                    self.results['failed_modules'] += 1

        # Generate summary
        self.generate_summary()

        # Save results
        self.save_results()

        return self.results

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total modules: {self.results['total_modules']}")
        print(f"Tested: {self.results['tested_modules']}")
        print(f"✅ Passed: {self.results['passed_modules']}")
        print(f"❌ Failed: {self.results['failed_modules']}")

        success_rate = (self.results['passed_modules'] / self.results['total_modules'] * 100) if self.results['total_modules'] > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.1f}%")

        # Category breakdown
        print("\n" + "-"*60)
        print("CATEGORY BREAKDOWN:")
        print("-"*60)

        for category in self.module_paths.keys():
            category_modules = [m for m in self.results['modules'] if m['category'] == category]
            category_passed = sum(1 for m in category_modules if m['status'] == 'PASSED')
            category_total = len(category_modules)
            print(f"{category}: {category_passed}/{category_total} passed")

        # Failed modules detail
        failed_modules = [m for m in self.results['modules'] if m['status'] == 'FAILED']
        if failed_modules:
            print("\n" + "-"*60)
            print("FAILED MODULES:")
            print("-"*60)
            for module in failed_modules:
                print(f"❌ {module['name']}: {module.get('reason', 'See details in JSON report')}")

    def save_results(self):
        """Save test results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"AUTONOMOUS_TEST_RESULTS_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✅ Results saved to: {filename}")

        # Also create a human-readable markdown report
        self.create_markdown_report(timestamp)

    def create_markdown_report(self, timestamp):
        """Create a markdown report"""
        filename = f"AUTONOMOUS_TEST_REPORT_{timestamp}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 🤖 AUTONOMOUS MODULE TEST REPORT\n\n")
            f.write(f"**Timestamp:** {self.results['timestamp']}\n")
            f.write(f"**Tester:** Autonomous Claude Instance\n\n")

            f.write("---\n\n")
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"- **Total Modules:** {self.results['total_modules']}\n")
            f.write(f"- **Tested:** {self.results['tested_modules']}\n")
            f.write(f"- **✅ Passed:** {self.results['passed_modules']}\n")
            f.write(f"- **❌ Failed:** {self.results['failed_modules']}\n")

            success_rate = (self.results['passed_modules'] / self.results['total_modules'] * 100) if self.results['total_modules'] > 0 else 0
            f.write(f"- **Success Rate:** {success_rate:.1f}%\n\n")

            f.write("---\n\n")
            f.write("## 📦 MODULES BY CATEGORY\n\n")

            for category in self.module_paths.keys():
                f.write(f"### {category}\n\n")
                category_modules = [m for m in self.results['modules'] if m['category'] == category]

                for module in category_modules:
                    status_icon = "✅" if module['status'] == 'PASSED' else "❌"
                    f.write(f"- {status_icon} **{module['name']}**\n")

                    if 'tests' in module and 'complexity' in module['tests']:
                        comp = module['tests']['complexity']
                        f.write(f"  - Lines: {comp['total_lines']}, Functions: {comp['total_functions']}, Classes: {comp['total_classes']}\n")

                    if module['status'] == 'FAILED' and 'reason' in module:
                        f.write(f"  - ⚠️ Reason: {module['reason']}\n")

                    f.write("\n")

            f.write("---\n\n")
            f.write("## 🎯 NEXT STEPS\n\n")

            if self.results['failed_modules'] > 0:
                f.write("### Failed Modules to Fix:\n\n")
                failed = [m for m in self.results['modules'] if m['status'] == 'FAILED']
                for module in failed:
                    f.write(f"1. **{module['name']}**: {module.get('reason', 'Investigate failures')}\n")
                f.write("\n")

            f.write("### Recommended Actions:\n\n")
            f.write("1. Review failed modules and fix issues\n")
            f.write("2. Add missing requirements.txt files\n")
            f.write("3. Run integration tests on passed modules\n")
            f.write("4. Deploy beta testing environment\n")
            f.write("5. Continue building additional modules\n\n")

            f.write("---\n\n")
            f.write("**Generated by:** Autonomous Claude Instance (Computer 2)\n")
            f.write(f"**Branch:** claude/autonomous-contact-test-011CUtYhH6FjHJiY9ZgmCLtR\n")
            f.write(f"**Session:** Autonomous Contact Test\n")

        print(f"✅ Markdown report saved to: {filename}")

def main():
    """Main execution"""
    tester = ModuleTester()
    results = tester.run_all_tests()

    print("\n" + "="*60)
    print("🎉 AUTONOMOUS TESTING COMPLETE")
    print("="*60)
    print("\nCheck the generated JSON and MD files for detailed results.")

    return 0 if results['failed_modules'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
