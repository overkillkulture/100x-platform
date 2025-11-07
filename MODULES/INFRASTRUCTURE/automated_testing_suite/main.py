#!/usr/bin/env python3
"""
Automated Testing Suite Module
AI-Generated Test Cases, Visual Regression, Load Testing & Security Scanning
Powered by Claude AI
"""

import os
import json
import asyncio
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
import uuid
import subprocess
import time


class TestType(Enum):
    """Types of tests"""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    VISUAL_REGRESSION = "visual_regression"
    LOAD = "load"
    SECURITY = "security"
    API = "api"
    PERFORMANCE = "performance"


class TestStatus(Enum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class SecurityLevel(Enum):
    """Security scan severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class TestCase:
    """Represents a test case"""
    id: str
    name: str
    description: str
    test_type: TestType
    code: str
    file_path: str
    status: TestStatus
    created_at: datetime
    last_run: Optional[datetime]
    execution_time: float  # seconds
    assertions: int
    passed_assertions: int
    failed_assertions: int
    error_message: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualTest:
    """Visual regression test"""
    id: str
    name: str
    url: str
    baseline_screenshot: Optional[str]
    current_screenshot: Optional[str]
    diff_screenshot: Optional[str]
    diff_percentage: float
    status: TestStatus
    threshold: float  # acceptable difference percentage
    created_at: datetime
    last_run: Optional[datetime]


@dataclass
class LoadTest:
    """Load/stress test configuration"""
    id: str
    name: str
    target_url: str
    virtual_users: int
    duration_seconds: int
    ramp_up_time: int
    requests_per_second: float
    response_times: List[float]
    success_rate: float
    error_count: int
    status: TestStatus
    created_at: datetime
    last_run: Optional[datetime]


@dataclass
class SecurityVulnerability:
    """Security vulnerability found"""
    id: str
    severity: SecurityLevel
    title: str
    description: str
    affected_component: str
    cve_id: Optional[str]
    fix_recommendation: str
    false_positive: bool


@dataclass
class SecurityScan:
    """Security scan results"""
    id: str
    scan_type: str  # dependency, code_analysis, penetration
    target: str
    vulnerabilities: List[SecurityVulnerability]
    status: TestStatus
    created_at: datetime
    scan_duration: float


@dataclass
class TestSuite:
    """Collection of related tests"""
    id: str
    name: str
    description: str
    test_cases: List[str]  # Test case IDs
    created_at: datetime
    last_run: Optional[datetime]
    total_tests: int
    passed_tests: int
    failed_tests: int
    coverage_percentage: float


class AITestGenerator:
    """AI-powered test case generation"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    async def generate_unit_tests(
        self,
        source_code: str,
        language: str = "python"
    ) -> List[str]:
        """Generate unit tests for source code"""

        test_prompt = f"""Generate comprehensive unit tests for this {language} code.

Source code:
```{language}
{source_code}
```

Requirements:
1. Test all public functions/methods
2. Include edge cases and error conditions
3. Use appropriate testing framework (pytest for Python)
4. Add clear test names and docstrings
5. Mock external dependencies
6. Aim for >90% code coverage

Generate test code:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": test_prompt
                }]
            )

            test_code = response.content[0].text

            # Extract test functions
            test_functions = self._extract_test_functions(test_code, language)
            return test_functions

        except Exception as e:
            print(f"Test generation error: {e}")
            return []

    def _extract_test_functions(self, code: str, language: str) -> List[str]:
        """Extract individual test functions from generated code"""

        if language == "python":
            # Split by test function definitions
            import re
            pattern = r'(def test_\w+\(.*?\):.*?)(?=def test_|\Z)'
            matches = re.findall(pattern, code, re.DOTALL)
            return matches

        return [code]  # Return full code if can't split

    async def generate_integration_tests(
        self,
        api_spec: Dict[str, Any]
    ) -> List[str]:
        """Generate integration tests from API specification"""

        test_prompt = f"""Generate integration tests for this API specification.

API Spec:
{json.dumps(api_spec, indent=2)}

Requirements:
1. Test all endpoints
2. Verify request/response formats
3. Test authentication and authorization
4. Test error handling
5. Validate status codes
6. Check response schemas

Generate test code using pytest and requests library:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": test_prompt
                }]
            )

            return [response.content[0].text]

        except Exception as e:
            print(f"Integration test generation error: {e}")
            return []

    async def generate_e2e_tests(
        self,
        user_flows: List[str]
    ) -> List[str]:
        """Generate end-to-end tests from user flows"""

        flows_text = "\n".join([f"{i+1}. {flow}" for i, flow in enumerate(user_flows)])

        test_prompt = f"""Generate end-to-end tests for these user flows using Playwright or Selenium.

User Flows:
{flows_text}

Requirements:
1. Test complete user journeys
2. Include setup and teardown
3. Handle async operations
4. Take screenshots on failure
5. Add meaningful assertions
6. Make tests maintainable

Generate test code:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": test_prompt
                }]
            )

            return [response.content[0].text]

        except Exception as e:
            print(f"E2E test generation error: {e}")
            return []


class VisualRegressionTester:
    """Visual regression testing"""

    def __init__(self):
        self.baseline_dir = "/tmp/visual_baselines"
        self.current_dir = "/tmp/visual_current"
        self.diff_dir = "/tmp/visual_diffs"

        os.makedirs(self.baseline_dir, exist_ok=True)
        os.makedirs(self.current_dir, exist_ok=True)
        os.makedirs(self.diff_dir, exist_ok=True)

    async def capture_screenshot(
        self,
        url: str,
        output_path: str,
        viewport_width: int = 1920,
        viewport_height: int = 1080
    ) -> str:
        """Capture screenshot of URL"""

        # In production, use Playwright or Selenium
        # Mock implementation

        print(f"Capturing screenshot of {url}")
        await asyncio.sleep(0.5)  # Simulate capture time

        # Create mock screenshot file
        with open(output_path, 'wb') as f:
            f.write(b'mock_screenshot_data')

        return output_path

    async def compare_screenshots(
        self,
        baseline_path: str,
        current_path: str,
        diff_path: str,
        threshold: float = 0.1
    ) -> Tuple[float, bool]:
        """Compare two screenshots and generate diff"""

        # In production, use pixelmatch or similar
        # Mock implementation

        await asyncio.sleep(0.3)

        # Simulate comparison
        import random
        diff_percentage = random.uniform(0, 15)  # 0-15% difference
        passed = diff_percentage <= threshold

        # Create mock diff image
        with open(diff_path, 'wb') as f:
            f.write(b'mock_diff_data')

        return diff_percentage, passed

    async def run_visual_test(
        self,
        test: VisualTest
    ) -> VisualTest:
        """Run visual regression test"""

        # Capture current screenshot
        current_path = os.path.join(
            self.current_dir,
            f"{test.id}_{int(time.time())}.png"
        )
        await self.capture_screenshot(test.url, current_path)
        test.current_screenshot = current_path

        # If no baseline, set current as baseline
        if not test.baseline_screenshot:
            baseline_path = os.path.join(self.baseline_dir, f"{test.id}_baseline.png")
            import shutil
            shutil.copy(current_path, baseline_path)
            test.baseline_screenshot = baseline_path
            test.status = TestStatus.PASSED
            test.diff_percentage = 0.0
            return test

        # Compare with baseline
        diff_path = os.path.join(
            self.diff_dir,
            f"{test.id}_diff.png"
        )
        diff_percentage, passed = await self.compare_screenshots(
            test.baseline_screenshot,
            current_path,
            diff_path,
            test.threshold
        )

        test.diff_screenshot = diff_path
        test.diff_percentage = diff_percentage
        test.status = TestStatus.PASSED if passed else TestStatus.FAILED
        test.last_run = datetime.now()

        return test


class LoadTester:
    """Load and performance testing"""

    def __init__(self):
        pass

    async def run_load_test(
        self,
        test: LoadTest
    ) -> LoadTest:
        """Execute load test"""

        print(f"Running load test: {test.name}")
        print(f"Target: {test.target_url}")
        print(f"Virtual users: {test.virtual_users}")
        print(f"Duration: {test.duration_seconds}s")

        test.status = TestStatus.RUNNING
        test.last_run = datetime.now()

        # In production, use Locust, JMeter, or k6
        # Mock implementation

        response_times = []
        error_count = 0
        total_requests = test.virtual_users * test.requests_per_second * test.duration_seconds

        # Simulate load test
        for i in range(int(total_requests)):
            # Simulate request
            import random
            response_time = random.uniform(50, 500)  # ms
            response_times.append(response_time)

            # Simulate some errors (5% error rate)
            if random.random() < 0.05:
                error_count += 1

            # Small delay to simulate time
            if i % 100 == 0:
                await asyncio.sleep(0.01)

        test.response_times = response_times
        test.success_rate = 1.0 - (error_count / total_requests)
        test.error_count = error_count
        test.status = TestStatus.PASSED if test.success_rate > 0.95 else TestStatus.FAILED

        return test

    def analyze_performance(self, test: LoadTest) -> Dict[str, Any]:
        """Analyze load test results"""

        if not test.response_times:
            return {}

        response_times = sorted(test.response_times)
        total = len(response_times)

        return {
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "mean_response_time": sum(response_times) / total,
            "median_response_time": response_times[total // 2],
            "p95_response_time": response_times[int(total * 0.95)],
            "p99_response_time": response_times[int(total * 0.99)],
            "success_rate": test.success_rate,
            "error_count": test.error_count,
            "requests_per_second": len(response_times) / test.duration_seconds
        }


class SecurityScanner:
    """Security vulnerability scanning"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    async def scan_dependencies(
        self,
        requirements_file: str
    ) -> SecurityScan:
        """Scan dependencies for vulnerabilities"""

        scan_id = str(uuid.uuid4())
        start_time = time.time()

        # In production, use:
        # - Safety (Python)
        # - npm audit (Node.js)
        # - OWASP Dependency-Check
        # - Snyk

        vulnerabilities = []

        # Mock vulnerability
        vulnerabilities.append(SecurityVulnerability(
            id=str(uuid.uuid4()),
            severity=SecurityLevel.HIGH,
            title="Outdated cryptography library",
            description="cryptography 2.8 has known vulnerabilities",
            affected_component="cryptography==2.8",
            cve_id="CVE-2020-36242",
            fix_recommendation="Update to cryptography>=3.4.8",
            false_positive=False
        ))

        scan = SecurityScan(
            id=scan_id,
            scan_type="dependency",
            target=requirements_file,
            vulnerabilities=vulnerabilities,
            status=TestStatus.PASSED if not vulnerabilities else TestStatus.FAILED,
            created_at=datetime.now(),
            scan_duration=time.time() - start_time
        )

        return scan

    async def scan_code(
        self,
        source_code: str,
        language: str = "python"
    ) -> SecurityScan:
        """Scan source code for security issues"""

        scan_id = str(uuid.uuid4())
        start_time = time.time()

        # Use AI to identify security issues
        security_prompt = f"""Analyze this {language} code for security vulnerabilities.

Code:
```{language}
{source_code}
```

Look for:
1. SQL injection vulnerabilities
2. XSS vulnerabilities
3. CSRF issues
4. Insecure cryptography
5. Hardcoded secrets
6. Insufficient input validation
7. Insecure deserialization
8. Path traversal issues

Provide findings as JSON array:
[
  {{
    "severity": "high",
    "title": "SQL Injection Risk",
    "description": "User input concatenated into SQL query",
    "line_number": 42,
    "recommendation": "Use parameterized queries"
  }}
]
"""

        vulnerabilities = []

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": security_prompt
                }]
            )

            result = response.content[0].text

            # Parse vulnerabilities
            import re
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                findings = json.loads(json_match.group())

                for finding in findings:
                    severity_map = {
                        "critical": SecurityLevel.CRITICAL,
                        "high": SecurityLevel.HIGH,
                        "medium": SecurityLevel.MEDIUM,
                        "low": SecurityLevel.LOW,
                        "info": SecurityLevel.INFO
                    }

                    vulnerabilities.append(SecurityVulnerability(
                        id=str(uuid.uuid4()),
                        severity=severity_map.get(finding.get("severity", "medium"), SecurityLevel.MEDIUM),
                        title=finding.get("title", "Security Issue"),
                        description=finding.get("description", ""),
                        affected_component=f"Line {finding.get('line_number', 0)}",
                        cve_id=None,
                        fix_recommendation=finding.get("recommendation", ""),
                        false_positive=False
                    ))

        except Exception as e:
            print(f"Code scanning error: {e}")

        scan = SecurityScan(
            id=scan_id,
            scan_type="code_analysis",
            target="source_code",
            vulnerabilities=vulnerabilities,
            status=TestStatus.PASSED if not vulnerabilities else TestStatus.FAILED,
            created_at=datetime.now(),
            scan_duration=time.time() - start_time
        )

        return scan

    async def penetration_test(
        self,
        target_url: str
    ) -> SecurityScan:
        """Run automated penetration test"""

        scan_id = str(uuid.uuid4())
        start_time = time.time()

        # In production, use:
        # - OWASP ZAP
        # - Burp Suite
        # - Nikto

        vulnerabilities = []

        # Mock findings
        vulnerabilities.append(SecurityVulnerability(
            id=str(uuid.uuid4()),
            severity=SecurityLevel.MEDIUM,
            title="Missing Security Headers",
            description="X-Frame-Options header not set",
            affected_component=target_url,
            cve_id=None,
            fix_recommendation="Add X-Frame-Options: DENY header",
            false_positive=False
        ))

        scan = SecurityScan(
            id=scan_id,
            scan_type="penetration",
            target=target_url,
            vulnerabilities=vulnerabilities,
            status=TestStatus.PASSED if not vulnerabilities else TestStatus.FAILED,
            created_at=datetime.now(),
            scan_duration=time.time() - start_time
        )

        return scan


class AutomatedTestingSuite:
    """Main automated testing suite"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize testing suite"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.test_generator = AITestGenerator(self.api_key)
        self.visual_tester = VisualRegressionTester()
        self.load_tester = LoadTester()
        self.security_scanner = SecurityScanner(self.api_key)

        # Storage
        self.test_cases: Dict[str, TestCase] = {}
        self.visual_tests: Dict[str, VisualTest] = {}
        self.load_tests: Dict[str, LoadTest] = {}
        self.security_scans: List[SecurityScan] = []
        self.test_suites: Dict[str, TestSuite] = {}

    async def generate_tests(
        self,
        source_code: str,
        test_type: TestType = TestType.UNIT,
        language: str = "python"
    ) -> List[TestCase]:
        """Generate test cases using AI"""

        if test_type == TestType.UNIT:
            test_codes = await self.test_generator.generate_unit_tests(source_code, language)
        else:
            test_codes = [source_code]  # Placeholder

        test_cases = []
        for i, code in enumerate(test_codes):
            test_id = str(uuid.uuid4())

            test_case = TestCase(
                id=test_id,
                name=f"test_{test_type.value}_{i+1}",
                description=f"Auto-generated {test_type.value} test",
                test_type=test_type,
                code=code,
                file_path=f"tests/test_{test_id}.py",
                status=TestStatus.PENDING,
                created_at=datetime.now(),
                last_run=None,
                execution_time=0.0,
                assertions=0,
                passed_assertions=0,
                failed_assertions=0,
                error_message=None
            )

            self.test_cases[test_id] = test_case
            test_cases.append(test_case)

        return test_cases

    async def run_test(self, test_id: str) -> TestCase:
        """Execute a test case"""

        if test_id not in self.test_cases:
            raise ValueError(f"Test {test_id} not found")

        test = self.test_cases[test_id]
        test.status = TestStatus.RUNNING
        test.last_run = datetime.now()

        start_time = time.time()

        # In production, actually execute the test code
        # For now, mock execution
        await asyncio.sleep(0.5)

        # Simulate test result
        import random
        passed = random.random() > 0.1  # 90% pass rate

        test.execution_time = time.time() - start_time
        test.assertions = 5
        test.passed_assertions = 5 if passed else 3
        test.failed_assertions = 0 if passed else 2
        test.status = TestStatus.PASSED if passed else TestStatus.FAILED

        if not passed:
            test.error_message = "Assertion failed: expected 42, got 41"

        return test

    async def run_visual_test(self, test_id: str) -> VisualTest:
        """Run visual regression test"""

        if test_id not in self.visual_tests:
            raise ValueError(f"Visual test {test_id} not found")

        test = self.visual_tests[test_id]
        return await self.visual_tester.run_visual_test(test)

    async def run_load_test(self, test_id: str) -> LoadTest:
        """Run load test"""

        if test_id not in self.load_tests:
            raise ValueError(f"Load test {test_id} not found")

        test = self.load_tests[test_id]
        return await self.load_tester.run_load_test(test)

    def create_visual_test(
        self,
        name: str,
        url: str,
        threshold: float = 1.0
    ) -> VisualTest:
        """Create visual regression test"""

        test_id = str(uuid.uuid4())

        test = VisualTest(
            id=test_id,
            name=name,
            url=url,
            baseline_screenshot=None,
            current_screenshot=None,
            diff_screenshot=None,
            diff_percentage=0.0,
            status=TestStatus.PENDING,
            threshold=threshold,
            created_at=datetime.now(),
            last_run=None
        )

        self.visual_tests[test_id] = test
        return test

    def create_load_test(
        self,
        name: str,
        target_url: str,
        virtual_users: int = 100,
        duration_seconds: int = 60
    ) -> LoadTest:
        """Create load test"""

        test_id = str(uuid.uuid4())

        test = LoadTest(
            id=test_id,
            name=name,
            target_url=target_url,
            virtual_users=virtual_users,
            duration_seconds=duration_seconds,
            ramp_up_time=10,
            requests_per_second=10.0,
            response_times=[],
            success_rate=0.0,
            error_count=0,
            status=TestStatus.PENDING,
            created_at=datetime.now(),
            last_run=None
        )

        self.load_tests[test_id] = test
        return test

    async def run_security_scan(
        self,
        scan_type: str,
        target: str
    ) -> SecurityScan:
        """Run security scan"""

        if scan_type == "dependency":
            scan = await self.security_scanner.scan_dependencies(target)
        elif scan_type == "code":
            scan = await self.security_scanner.scan_code(target)
        elif scan_type == "penetration":
            scan = await self.security_scanner.penetration_test(target)
        else:
            raise ValueError(f"Unknown scan type: {scan_type}")

        self.security_scans.append(scan)
        return scan

    def get_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""

        total_tests = len(self.test_cases)
        passed = sum(1 for t in self.test_cases.values() if t.status == TestStatus.PASSED)
        failed = sum(1 for t in self.test_cases.values() if t.status == TestStatus.FAILED)
        pending = sum(1 for t in self.test_cases.values() if t.status == TestStatus.PENDING)

        # Visual tests
        visual_total = len(self.visual_tests)
        visual_passed = sum(1 for t in self.visual_tests.values() if t.status == TestStatus.PASSED)

        # Load tests
        load_total = len(self.load_tests)
        load_passed = sum(1 for t in self.load_tests.values() if t.status == TestStatus.PASSED)

        # Security scans
        security_total = len(self.security_scans)
        total_vulnerabilities = sum(len(scan.vulnerabilities) for scan in self.security_scans)

        return {
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "pending": pending,
                "pass_rate": (passed / total_tests * 100) if total_tests > 0 else 0
            },
            "unit_tests": {
                "total": sum(1 for t in self.test_cases.values() if t.test_type == TestType.UNIT),
                "passed": sum(1 for t in self.test_cases.values() if t.test_type == TestType.UNIT and t.status == TestStatus.PASSED)
            },
            "visual_tests": {
                "total": visual_total,
                "passed": visual_passed
            },
            "load_tests": {
                "total": load_total,
                "passed": load_passed
            },
            "security": {
                "total_scans": security_total,
                "total_vulnerabilities": total_vulnerabilities,
                "critical": sum(1 for scan in self.security_scans for v in scan.vulnerabilities if v.severity == SecurityLevel.CRITICAL),
                "high": sum(1 for scan in self.security_scans for v in scan.vulnerabilities if v.severity == SecurityLevel.HIGH)
            }
        }

    def get_analytics(self) -> Dict[str, Any]:
        """Get testing analytics"""

        return {
            "total_test_cases": len(self.test_cases),
            "total_visual_tests": len(self.visual_tests),
            "total_load_tests": len(self.load_tests),
            "total_security_scans": len(self.security_scans),
            "total_test_suites": len(self.test_suites)
        }


def demo_testing_suite():
    """Demo function showing testing suite capabilities"""
    print("=" * 80)
    print("Automated Testing Suite - Demo")
    print("=" * 80)

    # Initialize
    try:
        suite = AutomatedTestingSuite()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    async def run_demo():
        # Generate unit tests
        print("\n🤖 Generating Unit Tests...")

        sample_code = """
def calculate_discount(price, discount_percent):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)

def process_order(items, customer_tier):
    total = sum(item['price'] for item in items)
    if customer_tier == 'premium':
        total = calculate_discount(total, 10)
    return total
"""

        tests = await suite.generate_tests(sample_code, TestType.UNIT)
        print(f"✅ Generated {len(tests)} test cases")

        # Run unit tests
        print("\n🧪 Running Unit Tests...")
        for test in tests[:3]:  # Run first 3
            result = await suite.run_test(test.id)
            status_icon = "✅" if result.status == TestStatus.PASSED else "❌"
            print(f"   {status_icon} {result.name}: {result.status.value} ({result.execution_time:.2f}s)")

        # Create and run visual test
        print("\n👁️  Running Visual Regression Test...")
        visual_test = suite.create_visual_test(
            name="Homepage UI Test",
            url="https://example.com",
            threshold=2.0  # 2% acceptable difference
        )
        visual_result = await suite.run_visual_test(visual_test.id)
        print(f"   Difference: {visual_result.diff_percentage:.2f}%")
        print(f"   Status: {visual_result.status.value}")

        # Create and run load test
        print("\n⚡ Running Load Test...")
        load_test = suite.create_load_test(
            name="API Load Test",
            target_url="https://api.example.com/users",
            virtual_users=50,
            duration_seconds=30
        )
        load_result = await suite.run_load_test(load_test.id)
        perf_metrics = suite.load_tester.analyze_performance(load_result)

        print(f"   Requests: {len(load_result.response_times)}")
        print(f"   Success Rate: {load_result.success_rate:.1%}")
        print(f"   Mean Response: {perf_metrics['mean_response_time']:.0f}ms")
        print(f"   P95 Response: {perf_metrics['p95_response_time']:.0f}ms")

        # Run security scans
        print("\n🔒 Running Security Scans...")

        # Dependency scan
        dep_scan = await suite.run_security_scan("dependency", "requirements.txt")
        print(f"   Dependency Scan: {len(dep_scan.vulnerabilities)} vulnerabilities found")

        # Code scan
        code_scan = await suite.run_security_scan("code", sample_code)
        print(f"   Code Scan: {len(code_scan.vulnerabilities)} issues found")

        if code_scan.vulnerabilities:
            for vuln in code_scan.vulnerabilities[:2]:
                print(f"      - [{vuln.severity.value}] {vuln.title}")

        # Generate report
        print("\n" + "=" * 80)
        print("Test Report")
        print("=" * 80)
        report = suite.get_test_report()
        print(json.dumps(report, indent=2))

        # Analytics
        print("\n" + "=" * 80)
        print("Analytics")
        print("=" * 80)
        analytics = suite.get_analytics()
        print(json.dumps(analytics, indent=2))

        print("\n✅ Demo completed successfully!")

    # Run async demo
    asyncio.run(run_demo())


if __name__ == "__main__":
    demo_testing_suite()
