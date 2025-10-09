"""
ALL-DAY AUTOMATED GATE TESTER
Tests the 100X Gate continuously and reports failures
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime
import random

class GateTester:
    def __init__(self):
        self.test_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.errors = []
        self.log_file = 'C:/Users/dwrek/100X_DEPLOYMENT/gate_test_log.json'

    def log_result(self, result_type, message, details=None):
        """Log test results to file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'test_number': self.test_count,
            'result': result_type,
            'message': message,
            'details': details
        }

        # Append to log file
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []

        logs.append(log_entry)

        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Test #{self.test_count}: {result_type}")
        print(f"  Message: {message}")
        if details:
            print(f"  Details: {details}")

    def generate_test_data(self):
        """Generate random test data"""
        test_num = self.test_count
        return {
            'name': f'Test Builder {test_num}',
            'email': f'test{test_num}@consciousnessrevolution.io',
            'phone': f'+1 555 {random.randint(100, 999)} {random.randint(1000, 9999)}',
            'mission': f'Test mission #{test_num}: Building liberated consciousness systems',
            'values': f'Test values #{test_num}: Truth, autonomy, pattern recognition'
        }

    def run_test(self):
        """Run a single gate test"""
        self.test_count += 1

        print("\n" + "="*60)
        print(f"🧪 TEST #{self.test_count} - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Track console messages and errors
                console_messages = []
                error_messages = []

                page.on('console', lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))
                page.on('pageerror', lambda exc: error_messages.append(str(exc)))

                # Track network responses
                network_responses = []

                def handle_response(response):
                    if 'airtable' in response.url.lower():
                        network_responses.append({
                            'url': response.url,
                            'status': response.status,
                            'statusText': response.status_text
                        })

                page.on('response', handle_response)

                # Load page
                print("  ✓ Loading gate...")
                page.goto('https://68e79faff34a7f3ce22f21df--verdant-tulumba-fa2a5a.netlify.app', timeout=30000)
                time.sleep(2)

                # Fill form
                print("  ✓ Filling form...")
                test_data = self.generate_test_data()

                page.fill('input#name', test_data['name'])
                page.fill('input#email', test_data['email'])
                page.fill('input#phone', test_data['phone'])
                page.fill('textarea#mission', test_data['mission'])
                page.fill('textarea#values', test_data['values'])

                time.sleep(1)

                # Click submit
                print("  ✓ Clicking submit...")
                page.click('button#submitBtn')

                # Wait for result
                print("  ⏳ Waiting for response...")
                time.sleep(5)

                # Check for success or error message
                status_message = page.locator('#statusMessage')

                if status_message.is_visible():
                    message_text = status_message.inner_text()
                    message_class = status_message.get_attribute('class')

                    if 'success' in message_class:
                        self.success_count += 1
                        self.log_result('SUCCESS', 'Form submitted successfully', {
                            'test_data': test_data,
                            'message': message_text
                        })
                    else:
                        self.fail_count += 1
                        self.log_result('FAILURE', 'Submission failed', {
                            'test_data': test_data,
                            'error_message': message_text,
                            'console_logs': console_messages,
                            'network_responses': network_responses,
                            'page_errors': error_messages
                        })
                else:
                    self.fail_count += 1
                    self.log_result('FAILURE', 'No status message appeared', {
                        'test_data': test_data,
                        'console_logs': console_messages,
                        'network_responses': network_responses
                    })

                browser.close()

            except Exception as e:
                self.fail_count += 1
                self.log_result('ERROR', f'Test crashed: {str(e)}', {
                    'exception': str(e),
                    'exception_type': type(e).__name__
                })
                try:
                    browser.close()
                except:
                    pass

    def print_stats(self):
        """Print current test statistics"""
        print("\n" + "="*60)
        print("📊 CURRENT STATISTICS")
        print("="*60)
        print(f"  Total Tests: {self.test_count}")
        print(f"  ✅ Successes: {self.success_count}")
        print(f"  ❌ Failures: {self.fail_count}")
        if self.test_count > 0:
            success_rate = (self.success_count / self.test_count) * 100
            print(f"  📈 Success Rate: {success_rate:.1f}%")
        print("="*60)

    def run_continuous(self, interval_seconds=60):
        """Run tests continuously"""
        print("\n🚀 STARTING ALL-DAY GATE TESTER")
        print(f"   Testing every {interval_seconds} seconds")
        print(f"   Log file: {self.log_file}")
        print(f"   Press Ctrl+C to stop\n")

        try:
            while True:
                self.run_test()
                self.print_stats()

                print(f"\n⏰ Waiting {interval_seconds} seconds until next test...")
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            print("\n\n🛑 TESTER STOPPED BY USER")
            self.print_stats()
            print(f"\n📋 Full log saved to: {self.log_file}")

if __name__ == "__main__":
    tester = GateTester()

    # Run test every 60 seconds (1 minute)
    # Change this number to test more/less frequently
    tester.run_continuous(interval_seconds=60)
