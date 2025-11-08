"""
COMPREHENSIVE TESTING FRAMEWORK
Tests all modules automatically
"""

import sys
import os
import importlib
import time

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def test_module(self, module_path: str, module_name: str):
        """Test a single module"""
        print(f"\nTesting {module_name}...")

        try:
            # Add to path
            sys.path.insert(0, module_path)

            # Import module
            module = importlib.import_module(module_name)

            # Check if has __main__ demo
            if hasattr(module, '__name__'):
                # Run module's own test
                exec(open(os.path.join(module_path, f"{module_name}.py")).read())

            print(f"  ✅ {module_name} PASSED")
            self.passed += 1

        except Exception as e:
            print(f"  ❌ {module_name} FAILED: {e}")
            self.failed += 1
            self.errors.append((module_name, str(e)))

        finally:
            sys.path.pop(0)

    def run_all_tests(self):
        """Test all modules"""
        print("=" * 70)
        print("CONSCIOUSNESS REVOLUTION - COMPREHENSIVE TEST SUITE")
        print("=" * 70)

        start = time.time()

        # Test modules #21-40
        modules = [
            ("MODULES/ADVANCED/pattern_recognition_engine", "pattern_recognition"),
            ("MODULES/ADVANCED/autonomous_learning_system", "autonomous_learning"),
            ("MODULES/ADVANCED/blockchain_integration_suite", "blockchain"),
            ("MODULES/ADVANCED/quantum_computing_interface", "quantum_computing"),
            ("MODULES/ADVANCED/neural_network_trainer", "neural_network"),
            ("MODULES/ADVANCED/time_series_forecasting", "time_series"),
            ("MODULES/ADVANCED/recommendation_engine", "recommender"),
            ("MODULES/ADVANCED/natural_language_processing", "nlp"),
            ("MODULES/ADVANCED/data_pipeline", "pipeline"),
            ("MODULES/ADVANCED/cache_system", "cache"),
            ("MODULES/ADVANCED/api_gateway", "gateway"),
            ("MODULES/ADVANCED/message_queue", "queue"),
            ("MODULES/ADVANCED/vector_database", "vector_db"),
            ("MODULES/ADVANCED/event_system", "events"),
            ("MODULES/ADVANCED/task_scheduler", "scheduler"),
            ("MODULES/ADVANCED/file_storage", "storage"),
            ("MODULES/ADVANCED/search_engine", "search"),
        ]

        for module_path, module_name in modules:
            self.test_module(module_path, module_name)

        duration = time.time() - start

        # Print summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Duration: {duration:.2f}s")

        if self.errors:
            print("\nERRORS:")
            for module, error in self.errors:
                print(f"  {module}: {error[:100]}")

        print("=" * 70)

        return self.failed == 0


if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()

    if success:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)
