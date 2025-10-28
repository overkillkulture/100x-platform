#!/usr/bin/env python3
"""
🤖 AUTOMATED SYSTEM TESTER
Tests all critical systems without human intervention
Run this every 30 minutes to verify everything works
"""

import requests
import time
import json
from datetime import datetime

# Test configuration
BASE_URL = "https://conciousnessrevolution.io"
TEST_RESULTS_FILE = "C:/Users/dwrek/Desktop/TEST_RESULTS.json"

class SystemTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def test(self, name, func):
        """Run a test and log results"""
        print(f"\n🧪 Testing: {name}")
        try:
            start = time.time()
            result = func()
            elapsed = time.time() - start

            if result['success']:
                print(f"   ✅ PASS ({elapsed:.2f}s)")
                self.passed += 1
                status = 'pass'
            else:
                print(f"   ❌ FAIL ({elapsed:.2f}s)")
                print(f"   Error: {result.get('error', 'Unknown')}")
                self.failed += 1
                status = 'fail'

            self.results.append({
                'test': name,
                'status': status,
                'elapsed': elapsed,
                'timestamp': datetime.now().isoformat(),
                'details': result
            })

            return result
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")
            self.failed += 1
            self.results.append({
                'test': name,
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            })
            return {'success': False, 'error': str(e)}

    def test_araya_api(self):
        """Test Araya chat API"""
        try:
            response = requests.post(
                f"{BASE_URL}/.netlify/functions/araya-chat",
                json={
                    "message": "Test message",
                    "session_id": f"test_{int(time.time())}"
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    return {'success': True, 'response_length': len(data['response'])}

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_email_tracking(self):
        """Test email tracking pixel"""
        try:
            response = requests.get(
                f"{BASE_URL}/.netlify/functions/email-track?r=test@test.com&c=test",
                timeout=10
            )

            # Should return a 1x1 pixel (status 200)
            if response.status_code == 200:
                # Check if it's an image
                if 'image' in response.headers.get('Content-Type', ''):
                    return {'success': True, 'content_type': response.headers['Content-Type']}

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_error_monitor(self):
        """Test error monitoring system"""
        try:
            response = requests.post(
                f"{BASE_URL}/.netlify/functions/error-monitor",
                json={
                    "type": "test_error",
                    "message": "Automated test error",
                    "page": "/test",
                    "impact": "single_user"
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return {'success': True, 'severity': data.get('severity')}

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_cost_tracker(self):
        """Test cost tracking system"""
        try:
            # GET current costs
            response = requests.get(
                f"{BASE_URL}/.netlify/functions/cost-tracker",
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if 'today' in data:
                    return {'success': True, 'today_cost': data['today'].get('total_cost', 0)}

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_instant_notifications(self):
        """Test notification system"""
        try:
            response = requests.post(
                f"{BASE_URL}/.netlify/functions/instant-notifications",
                json={
                    "type": "site_visit",
                    "data": {
                        "page": "/test",
                        "session_id": "test_session"
                    }
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return {'success': True}

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_website_accessibility(self):
        """Test main website pages load"""
        pages = [
            '/',
            '/workspace-v3.html',
            '/COMMAND_CENTER_HUD_COMMS.html',
            '/downloads.html'
        ]

        results = {}
        all_success = True

        for page in pages:
            try:
                response = requests.get(f"{BASE_URL}{page}", timeout=10)
                results[page] = response.status_code == 200
                if response.status_code != 200:
                    all_success = False
            except Exception as e:
                results[page] = False
                all_success = False

        return {
            'success': all_success,
            'pages': results,
            'accessible': sum(1 for v in results.values() if v),
            'total': len(pages)
        }

    def test_araya_failover(self):
        """Test API failover system"""
        try:
            response = requests.post(
                f"{BASE_URL}/.netlify/functions/araya-chat-failover",
                json={
                    "message": "Test failover",
                    "session_id": f"test_{int(time.time())}"
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if 'response' in data and 'api_used' in data:
                    return {
                        'success': True,
                        'api_used': data['api_used'],
                        'failover_attempts': data.get('failover_attempts', 0)
                    }

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def test_bug_reporting_system(self):
        """Test GitHub Issues bug reporting system"""
        try:
            # Submit a test bug
            test_bug = {
                "title": f"AUTOMATED TEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "description": "This is an automated test bug. System is checking that bug reporting works.",
                "reporter": "Automated Tester",
                "url": f"{BASE_URL}/test"
            }

            response = requests.post(
                f"{BASE_URL}/.netlify/functions/submit-bug",
                json=test_bug,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'issueUrl' in data and 'issueNumber' in data:
                    return {
                        'success': True,
                        'issue_number': data['issueNumber'],
                        'issue_url': data['issueUrl']
                    }

            return {'success': False, 'error': f'Status {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def run_all_tests(self):
        """Run complete test suite"""
        print("=" * 60)
        print("🤖 AUTOMATED SYSTEM TEST SUITE")
        print("=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: {BASE_URL}")
        print("=" * 60)

        # Run all tests
        self.test("Araya Chat API", self.test_araya_api)
        self.test("Email Tracking Pixel", self.test_email_tracking)
        self.test("Error Monitor", self.test_error_monitor)
        self.test("Cost Tracker", self.test_cost_tracker)
        self.test("Instant Notifications", self.test_instant_notifications)
        self.test("Website Accessibility", self.test_website_accessibility)
        self.test("API Failover System", self.test_araya_failover)
        self.test("Bug Reporting System (GitHub Issues)", self.test_bug_reporting_system)

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        print("=" * 60)

        # Save results
        report = {
            'timestamp': datetime.now().isoformat(),
            'passed': self.passed,
            'failed': self.failed,
            'success_rate': (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0,
            'results': self.results
        }

        try:
            with open(TEST_RESULTS_FILE, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n✅ Results saved: {TEST_RESULTS_FILE}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")

        return report

if __name__ == "__main__":
    tester = SystemTester()
    report = tester.run_all_tests()

    # Exit with error code if any tests failed
    exit(0 if report['failed'] == 0 else 1)
