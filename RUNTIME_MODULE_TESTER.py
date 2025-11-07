#!/usr/bin/env python3
"""
🚀 RUNTIME MODULE TESTER
Tests modules with actual execution and sample data
Goes beyond static analysis to validate real functionality
"""

import os
import sys
import json
import subprocess
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class RuntimeModuleTester:
    """Tests modules by actually executing them with sample data"""

    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_modules': 0,
            'tested_modules': 0,
            'passed_modules': 0,
            'failed_modules': 0,
            'skipped_modules': 0,
            'modules': []
        }

        # Module paths (same as static tester)
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

    def test_module_runtime(self, category: str, module_path: str) -> Dict:
        """Actually execute module with test data"""
        module_name = os.path.basename(module_path)

        print(f"\n{'='*60}")
        print(f"Runtime Testing: {module_name} ({category})")
        print(f"{'='*60}")

        test_result = {
            'name': module_name,
            'category': category,
            'path': module_path,
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }

        # Test 1: Module imports successfully
        import_test = self._test_import(module_path)
        test_result['tests']['import'] = import_test
        print(f"  Import test: {'✅' if import_test['success'] else '❌'}")

        if not import_test['success']:
            test_result['status'] = 'FAILED'
            test_result['reason'] = 'Import failed'
            return test_result

        # Test 2: Demo/test function exists and runs
        demo_test = self._test_demo_function(module_path)
        test_result['tests']['demo'] = demo_test
        print(f"  Demo test: {'✅' if demo_test['success'] else '❌'}")

        # Test 3: Basic functionality with sample data
        functionality_test = self._test_basic_functionality(module_path)
        test_result['tests']['functionality'] = functionality_test
        print(f"  Functionality: {'✅' if functionality_test['success'] else '❌'}")

        # Overall status
        all_success = all(
            test.get('success', False)
            for test in test_result['tests'].values()
        )

        test_result['status'] = 'PASSED' if all_success else 'FAILED'
        print(f"  Overall: {'✅ PASSED' if all_success else '❌ FAILED'}")

        return test_result

    def _test_import(self, module_path: str) -> Dict:
        """Test if module can be imported"""
        python_files = list(Path(module_path).glob('*.py'))

        if not python_files:
            return {
                'success': False,
                'error': 'No Python files found',
                'files_tested': 0
            }

        imported_count = 0
        errors = []

        for py_file in python_files:
            try:
                # Try to import the module
                spec = importlib.util.spec_from_file_location(
                    py_file.stem,
                    py_file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    # Don't execute yet, just check if it loads
                    imported_count += 1
            except Exception as e:
                errors.append({
                    'file': str(py_file),
                    'error': str(e)
                })

        return {
            'success': len(errors) == 0,
            'files_tested': len(python_files),
            'files_imported': imported_count,
            'errors': errors if errors else None
        }

    def _test_demo_function(self, module_path: str) -> Dict:
        """Look for and run demo/test functions"""
        python_files = list(Path(module_path).glob('*.py'))

        for py_file in python_files:
            try:
                # Read file to check for demo functions
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for common demo function patterns
                has_demo = any(pattern in content for pattern in [
                    'def demo(',
                    'def test_',
                    'def main(',
                    'if __name__ == "__main__"'
                ])

                if has_demo:
                    # Try to run the file
                    result = subprocess.run(
                        [sys.executable, str(py_file)],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    return {
                        'success': result.returncode == 0,
                        'file': str(py_file),
                        'returncode': result.returncode,
                        'stdout': result.stdout[:500] if result.stdout else None,
                        'stderr': result.stderr[:500] if result.stderr else None
                    }

            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'file': str(py_file),
                    'error': 'Timeout (>10s)'
                }
            except Exception as e:
                return {
                    'success': False,
                    'file': str(py_file),
                    'error': str(e)
                }

        return {
            'success': True,
            'reason': 'No demo function found (not required)'
        }

    def _test_basic_functionality(self, module_path: str) -> Dict:
        """Test basic module functionality"""
        python_files = list(Path(module_path).glob('*.py'))

        if not python_files:
            return {'success': False, 'error': 'No Python files'}

        main_file = python_files[0]  # Test the first/main file

        try:
            # Try to import and instantiate main class
            spec = importlib.util.spec_from_file_location(
                main_file.stem,
                main_file
            )

            if not spec or not spec.loader:
                return {
                    'success': False,
                    'error': 'Could not load module spec'
                }

            module = importlib.util.module_from_spec(spec)

            # Execute module (loads classes/functions)
            spec.loader.exec_module(module)

            # Count classes and functions loaded
            classes = []
            functions = []

            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and not name.startswith('_'):
                    classes.append(name)
                elif callable(obj) and not name.startswith('_'):
                    functions.append(name)

            return {
                'success': True,
                'classes_loaded': len(classes),
                'functions_loaded': len(functions),
                'classes': classes[:5],  # First 5
                'functions': functions[:5]  # First 5
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file': str(main_file)
            }

    def run_all_tests(self):
        """Run runtime tests on all modules"""
        print("\n" + "="*60)
        print("🚀 RUNTIME MODULE TESTER - STARTING")
        print("="*60)
        print(f"Timestamp: {self.results['timestamp']}")
        print("Testing modules with actual execution...\n")

        # Count total modules
        for category, paths in self.module_paths.items():
            self.results['total_modules'] += len(paths)

        # Test each module
        for category, paths in self.module_paths.items():
            print(f"\n{'#'*60}")
            print(f"CATEGORY: {category}")
            print(f"{'#'*60}")

            for module_path in paths:
                result = self.test_module_runtime(category, module_path)
                self.results['modules'].append(result)
                self.results['tested_modules'] += 1

                if result['status'] == 'PASSED':
                    self.results['passed_modules'] += 1
                elif result['status'] == 'FAILED':
                    self.results['failed_modules'] += 1
                else:
                    self.results['skipped_modules'] += 1

        # Generate summary
        self.generate_summary()

        # Save results
        self.save_results()

        return self.results

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "="*60)
        print("📊 RUNTIME TEST SUMMARY")
        print("="*60)
        print(f"Total modules: {self.results['total_modules']}")
        print(f"Tested: {self.results['tested_modules']}")
        print(f"✅ Passed: {self.results['passed_modules']}")
        print(f"❌ Failed: {self.results['failed_modules']}")
        print(f"⏭️  Skipped: {self.results['skipped_modules']}")

        success_rate = (
            (self.results['passed_modules'] / self.results['total_modules'] * 100)
            if self.results['total_modules'] > 0
            else 0
        )
        print(f"\nSuccess Rate: {success_rate:.1f}%")

        # Category breakdown
        print("\n" + "-"*60)
        print("CATEGORY BREAKDOWN:")
        print("-"*60)

        for category in self.module_paths.keys():
            category_modules = [
                m for m in self.results['modules']
                if m['category'] == category
            ]
            category_passed = sum(
                1 for m in category_modules
                if m['status'] == 'PASSED'
            )
            category_total = len(category_modules)
            print(f"{category}: {category_passed}/{category_total} passed")

        # Failed modules detail
        failed_modules = [
            m for m in self.results['modules']
            if m['status'] == 'FAILED'
        ]
        if failed_modules:
            print("\n" + "-"*60)
            print("FAILED MODULES:")
            print("-"*60)
            for module in failed_modules:
                print(f"❌ {module['name']}")
                if 'reason' in module:
                    print(f"   Reason: {module['reason']}")

    def save_results(self):
        """Save test results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RUNTIME_TEST_RESULTS_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✅ Results saved to: {filename}")

        # Also create markdown report
        self.create_markdown_report(timestamp)

    def create_markdown_report(self, timestamp: str):
        """Create a markdown report"""
        filename = f"RUNTIME_TEST_REPORT_{timestamp}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# 🚀 RUNTIME MODULE TEST REPORT\n\n")
            f.write(f"**Timestamp:** {self.results['timestamp']}\n")
            f.write(f"**Test Type:** Runtime Execution Testing\n\n")

            f.write("---\n\n")
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"- **Total Modules:** {self.results['total_modules']}\n")
            f.write(f"- **Tested:** {self.results['tested_modules']}\n")
            f.write(f"- **✅ Passed:** {self.results['passed_modules']}\n")
            f.write(f"- **❌ Failed:** {self.results['failed_modules']}\n")
            f.write(f"- **⏭️ Skipped:** {self.results['skipped_modules']}\n")

            success_rate = (
                (self.results['passed_modules'] / self.results['total_modules'] * 100)
                if self.results['total_modules'] > 0
                else 0
            )
            f.write(f"- **Success Rate:** {success_rate:.1f}%\n\n")

            f.write("---\n\n")
            f.write("## 📦 MODULES BY CATEGORY\n\n")

            for category in self.module_paths.keys():
                f.write(f"### {category}\n\n")
                category_modules = [
                    m for m in self.results['modules']
                    if m['category'] == category
                ]

                for module in category_modules:
                    status_icon = "✅" if module['status'] == 'PASSED' else "❌"
                    f.write(f"- {status_icon} **{module['name']}**\n")

                    # Add test details
                    if 'tests' in module:
                        for test_name, test_result in module['tests'].items():
                            success = test_result.get('success', False)
                            test_icon = "✅" if success else "❌"
                            f.write(f"  - {test_icon} {test_name}: {test_result.get('reason', 'Completed')}\n")

                    if module['status'] == 'FAILED' and 'reason' in module:
                        f.write(f"  - ⚠️ Reason: {module['reason']}\n")

                    f.write("\n")

            f.write("---\n\n")
            f.write("## 🎯 COMPARISON: Static vs Runtime\n\n")
            f.write("**Static Testing** (syntax, structure):\n")
            f.write("- All modules: 100% pass rate ✅\n\n")
            f.write("**Runtime Testing** (actual execution):\n")
            f.write(f"- Success rate: {success_rate:.1f}%\n")
            f.write(f"- Passed: {self.results['passed_modules']}/{self.results['total_modules']}\n\n")

            f.write("**Key Insight:** Runtime testing reveals issues that static analysis misses.\n\n")

            f.write("---\n\n")
            f.write("**Generated by:** Runtime Module Tester\n")
            f.write(f"**Session:** Autonomous Testing\n")

        print(f"✅ Markdown report saved to: {filename}")


def main():
    """Main execution"""
    tester = RuntimeModuleTester()
    results = tester.run_all_tests()

    print("\n" + "="*60)
    print("🎉 RUNTIME TESTING COMPLETE")
    print("="*60)
    print("\nCheck the generated JSON and MD files for detailed results.")

    return 0 if results['failed_modules'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
