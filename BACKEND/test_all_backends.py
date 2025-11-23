#!/usr/bin/env python3
"""
BACKEND INTEGRATION TESTER
Tests all 3 backend APIs to verify they're operational
Provides comprehensive health check and connectivity report
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple

# Backend configurations
BACKENDS = {
    'User Dashboard': {
        'url': 'http://localhost:3001',
        'health_endpoint': '/api/health',
        'test_endpoints': [
            ('/api/health', 'GET'),
        ]
    },
    'Philosopher AI': {
        'url': 'http://localhost:5001',
        'health_endpoint': '/api/health',
        'test_endpoints': [
            ('/api/health', 'GET'),
        ]
    },
    'Intelligent Terminal': {
        'url': 'http://localhost:5002',
        'health_endpoint': '/api/health',
        'test_endpoints': [
            ('/api/health', 'GET'),
            ('/terminal/status', 'GET'),
        ]
    },
    'Analytics Dashboard': {
        'url': 'http://localhost:5100',
        'health_endpoint': '/api/health',
        'test_endpoints': [
            ('/api/health', 'GET'),
            ('/api/dashboard', 'GET'),
            ('/api/business-phase', 'GET'),
        ]
    }
}

class BackendTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def test_endpoint(self, name: str, url: str, endpoint: str, method: str = 'GET') -> Tuple[bool, str, dict]:
        """Test a single endpoint"""
        full_url = f"{url}{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(full_url, timeout=5)
            elif method == 'POST':
                response = requests.post(full_url, json={}, timeout=5)
            else:
                return False, f"Unsupported method: {method}", {}

            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, "OK", data
                except:
                    return True, "OK (non-JSON)", {}
            else:
                return False, f"HTTP {response.status_code}", {}

        except requests.exceptions.ConnectionError:
            return False, "Connection refused (backend not running)", {}
        except requests.exceptions.Timeout:
            return False, "Timeout", {}
        except Exception as e:
            return False, f"Error: {str(e)}", {}

    def test_backend(self, name: str, config: dict):
        """Test all endpoints for a backend"""
        print(f"\n{'='*70}")
        print(f"Testing: {name}")
        print(f"URL: {config['url']}")
        print(f"{'='*70}")

        backend_results = {
            'name': name,
            'url': config['url'],
            'tests': [],
            'overall_status': 'UNKNOWN'
        }

        all_passed = True

        for endpoint, method in config['test_endpoints']:
            success, message, data = self.test_endpoint(name, config['url'], endpoint, method)

            test_result = {
                'endpoint': endpoint,
                'method': method,
                'success': success,
                'message': message,
                'data': data
            }

            backend_results['tests'].append(test_result)

            # Print result
            status_symbol = "✅" if success else "❌"
            print(f"  {status_symbol} {method:4} {endpoint:30} - {message}")

            if success:
                self.passed += 1
            else:
                self.failed += 1
                all_passed = False

            # Show interesting data
            if success and data:
                if 'status' in data:
                    print(f"       Status: {data['status']}")
                if 'service' in data:
                    print(f"       Service: {data['service']}")
                if 'anthropic_configured' in data:
                    api_status = "✅ Configured" if data['anthropic_configured'] else "⚠️  Not configured (demo mode)"
                    print(f"       Anthropic API: {api_status}")
                    if not data['anthropic_configured']:
                        self.warnings += 1

        backend_results['overall_status'] = 'PASS' if all_passed else 'FAIL'
        self.results.append(backend_results)

        print(f"\n{name} Overall: {'✅ PASS' if all_passed else '❌ FAIL'}")

    def run_all_tests(self):
        """Run tests for all backends"""
        print("="*70)
        print("100X PLATFORM - BACKEND INTEGRATION TESTER")
        print("="*70)
        print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Testing {len(BACKENDS)} backend services...")

        for name, config in BACKENDS.items():
            self.test_backend(name, config)

        self.print_summary()
        self.save_report()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)

        total_tests = self.passed + self.failed

        print(f"\nTotal Tests Run: {total_tests}")
        print(f"  ✅ Passed: {self.passed}")
        print(f"  ❌ Failed: {self.failed}")
        print(f"  ⚠️  Warnings: {self.warnings}")

        print(f"\nSuccess Rate: {(self.passed/total_tests*100) if total_tests > 0 else 0:.1f}%")

        print("\n" + "-"*70)
        print("BACKEND STATUS:")
        print("-"*70)

        for result in self.results:
            status_symbol = "✅" if result['overall_status'] == 'PASS' else "❌"
            print(f"{status_symbol} {result['name']:25} - {result['overall_status']:4} ({result['url']})")

        print("\n" + "="*70)
        print("RECOMMENDATIONS:")
        print("="*70)

        # Check if any backends are down
        failed_backends = [r for r in self.results if r['overall_status'] == 'FAIL']
        if failed_backends:
            print("\n⚠️  Some backends are not running. To start them:")
            for backend in failed_backends:
                if 'User Dashboard' in backend['name']:
                    print(f"   - Run: BACKEND/user-dashboard/START_USER_DASHBOARD.bat")
                elif 'Philosopher' in backend['name']:
                    print(f"   - Run: BACKEND/philosopher-ai/START_PHILOSOPHER_AI.bat")
                elif 'Terminal' in backend['name']:
                    print(f"   - Run: BACKEND/terminal/START_TERMINAL.bat")
                elif 'Analytics' in backend['name']:
                    print(f"   - Run: BACKEND/analytics-dashboard/START_ANALYTICS_DASHBOARD.bat")

            print(f"\n   Or launch all at once:")
            print(f"   - Run: BACKEND/UNIFIED_BACKEND_LAUNCHER.bat")

        # Check for API key warnings
        if self.warnings > 0:
            print(f"\n💡 API Key Configuration:")
            print(f"   Some backends are running in demo mode (no ANTHROPIC_API_KEY)")
            print(f"   To enable full AI features:")
            print(f"   1. Get API key from https://console.anthropic.com/")
            print(f"   2. Add to respective .env files")
            print(f"   3. Restart the backends")

        if self.failed == 0:
            print(f"\n🎉 All backends operational! Platform ready for use.")

        print("\n" + "="*70)

    def save_report(self):
        """Save detailed JSON report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': self.passed + self.failed,
                'passed': self.passed,
                'failed': self.failed,
                'warnings': self.warnings,
                'success_rate': (self.passed/(self.passed + self.failed)*100) if (self.passed + self.failed) > 0 else 0
            },
            'backends': self.results
        }

        report_file = f"backend_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Detailed report saved: {report_file}")


def main():
    tester = BackendTester()
    tester.run_all_tests()


if __name__ == '__main__':
    main()
