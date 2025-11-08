"""MODULE #56: SCREENSHOT ANALYZER - Visual analysis for multi-instance coordination"""
import time
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Screenshot:
    id: str
    filepath: str
    timestamp: float = field(default_factory=time.time)
    instance_id: Optional[str] = None
    annotations: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    analysis: Dict[str, Any] = field(default_factory=dict)

class ScreenshotAnalyzer:
    """Analyze screenshots from multiple Claude instances for coordination"""

    def __init__(self, analyzer_id: str = "main"):
        self.analyzer_id = analyzer_id
        self.screenshots: Dict[str, Screenshot] = {}

        # Analysis patterns
        self.patterns = {
            'code_blocks': r'```[\s\S]*?```',
            'errors': ['error', 'exception', 'failed', 'traceback'],
            'success': ['success', 'complete', 'done', '✅', '✓'],
            'file_paths': r'/[\w/.-]+\.\w+',
            'git_hashes': r'\b[0-9a-f]{7,40}\b',
            'module_numbers': r'Module #(\d+)',
        }

        # Metrics
        self.metrics = {
            'screenshots_analyzed': 0,
            'patterns_detected': defaultdict(int),
            'instances_tracked': set(),
            'errors_found': 0,
            'successes_found': 0
        }

    def register_screenshot(self, filepath: str, instance_id: Optional[str] = None,
                          metadata: Dict[str, Any] = None) -> str:
        """Register a screenshot for analysis"""
        screenshot_id = hashlib.md5(f"{filepath}-{time.time()}".encode()).hexdigest()[:16]

        screenshot = Screenshot(
            id=screenshot_id,
            filepath=filepath,
            instance_id=instance_id,
            metadata=metadata or {}
        )

        self.screenshots[screenshot_id] = screenshot

        if instance_id:
            self.metrics['instances_tracked'].add(instance_id)

        return screenshot_id

    def analyze_text_content(self, screenshot_id: str, text_content: str) -> Dict[str, Any]:
        """Analyze text extracted from screenshot"""
        if screenshot_id not in self.screenshots:
            return {}

        screenshot = self.screenshots[screenshot_id]
        analysis = {
            'text_length': len(text_content),
            'patterns_found': {},
            'errors': [],
            'successes': [],
            'sentiment': 'neutral',
            'modules_mentioned': [],
            'git_info': []
        }

        # Detect patterns
        import re

        # Find module numbers
        module_matches = re.findall(self.patterns['module_numbers'], text_content)
        if module_matches:
            analysis['modules_mentioned'] = [int(m) for m in module_matches]
            self.metrics['patterns_detected']['modules'] += len(module_matches)

        # Find git hashes
        git_matches = re.findall(self.patterns['git_hashes'], text_content.lower())
        if git_matches:
            analysis['git_info'] = git_matches
            self.metrics['patterns_detected']['git_hashes'] += len(git_matches)

        # Find errors
        text_lower = text_content.lower()
        for error_pattern in self.patterns['errors']:
            if error_pattern in text_lower:
                analysis['errors'].append(error_pattern)
                self.metrics['errors_found'] += 1

        # Find successes
        for success_pattern in self.patterns['success']:
            if success_pattern in text_lower:
                analysis['successes'].append(success_pattern)
                self.metrics['successes_found'] += 1

        # Determine sentiment
        if analysis['errors']:
            analysis['sentiment'] = 'negative'
        elif analysis['successes']:
            analysis['sentiment'] = 'positive'

        screenshot.analysis = analysis
        self.metrics['screenshots_analyzed'] += 1

        return analysis

    def add_annotation(self, screenshot_id: str, annotation: Dict[str, Any]):
        """Add annotation to screenshot"""
        if screenshot_id not in self.screenshots:
            return False

        self.screenshots[screenshot_id].annotations.append({
            **annotation,
            'timestamp': time.time()
        })

        return True

    def compare_screenshots(self, screenshot_id1: str, screenshot_id2: str) -> Dict[str, Any]:
        """Compare two screenshots for coordination"""
        if screenshot_id1 not in self.screenshots or screenshot_id2 not in self.screenshots:
            return {}

        s1 = self.screenshots[screenshot_id1]
        s2 = self.screenshots[screenshot_id2]

        comparison = {
            'time_diff': abs(s1.timestamp - s2.timestamp),
            'same_instance': s1.instance_id == s2.instance_id,
            'common_modules': [],
            'common_patterns': []
        }

        # Find common modules
        if 'modules_mentioned' in s1.analysis and 'modules_mentioned' in s2.analysis:
            common = set(s1.analysis['modules_mentioned']) & set(s2.analysis['modules_mentioned'])
            comparison['common_modules'] = list(common)

        return comparison

    def get_instance_activity(self, instance_id: str) -> Dict[str, Any]:
        """Get activity summary for an instance"""
        instance_screenshots = [
            s for s in self.screenshots.values()
            if s.instance_id == instance_id
        ]

        if not instance_screenshots:
            return {}

        return {
            'screenshot_count': len(instance_screenshots),
            'first_seen': min(s.timestamp for s in instance_screenshots),
            'last_seen': max(s.timestamp for s in instance_screenshots),
            'modules_worked_on': list(set(
                m for s in instance_screenshots
                for m in s.analysis.get('modules_mentioned', [])
            )),
            'error_count': sum(len(s.analysis.get('errors', [])) for s in instance_screenshots),
            'success_count': sum(len(s.analysis.get('successes', [])) for s in instance_screenshots)
        }

    def get_coordination_status(self) -> Dict[str, Any]:
        """Get coordination status across all instances"""
        all_modules = set()
        instance_activities = {}

        for instance_id in self.metrics['instances_tracked']:
            activity = self.get_instance_activity(instance_id)
            instance_activities[instance_id] = activity
            all_modules.update(activity.get('modules_worked_on', []))

        return {
            'total_screenshots': len(self.screenshots),
            'active_instances': len(self.metrics['instances_tracked']),
            'total_modules_seen': len(all_modules),
            'modules': sorted(all_modules),
            'instance_activities': instance_activities,
            'overall_sentiment': self._calculate_overall_sentiment()
        }

    def _calculate_overall_sentiment(self) -> str:
        """Calculate overall sentiment from all screenshots"""
        if self.metrics['errors_found'] > self.metrics['successes_found'] * 2:
            return 'negative'
        elif self.metrics['successes_found'] > self.metrics['errors_found'] * 2:
            return 'positive'
        return 'neutral'

    def export_analysis(self, filepath: str):
        """Export analysis to JSON"""
        data = {
            'analyzer_id': self.analyzer_id,
            'timestamp': time.time(),
            'screenshots': {
                sid: {
                    'filepath': s.filepath,
                    'instance_id': s.instance_id,
                    'timestamp': s.timestamp,
                    'analysis': s.analysis,
                    'annotations': s.annotations
                }
                for sid, s in self.screenshots.items()
            },
            'metrics': {
                **self.metrics,
                'instances_tracked': list(self.metrics['instances_tracked'])
            },
            'coordination_status': self.get_coordination_status()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def get_metrics(self) -> Dict[str, Any]:
        """Get analyzer metrics"""
        return {
            **{k: v for k, v in self.metrics.items() if k != 'patterns_detected'},
            'patterns_detected': dict(self.metrics['patterns_detected']),
            'instances_tracked': list(self.metrics['instances_tracked'])
        }


if __name__ == "__main__":
    print("📸 MODULE #56: SCREENSHOT ANALYZER")
    print("=" * 60)

    analyzer = ScreenshotAnalyzer("main-analyzer")

    print("✅ Screenshot analyzer initialized")

    # Simulate screenshot analysis from 3 instances
    print("\n📸 Analyzing screenshots from 3 Claude instances...")

    # Instance 1 screenshot
    s1_id = analyzer.register_screenshot("/screenshots/instance1.png", "instance-1",
                                        metadata={"type": "terminal"})
    analyzer.analyze_text_content(s1_id, """
    Building Module #56...
    ✅ Module #56 complete!
    Commit: 617a72a
    SUCCESS: All tests passing
    """)

    # Instance 2 screenshot
    s2_id = analyzer.register_screenshot("/screenshots/instance2.png", "instance-2",
                                        metadata={"type": "editor"})
    analyzer.analyze_text_content(s2_id, """
    Working on Module #57
    Inter-instance coordination
    ✅ Code complete
    """)

    # Instance 3 screenshot
    s3_id = analyzer.register_screenshot("/screenshots/instance3.png", "instance-3",
                                        metadata={"type": "dashboard"})
    analyzer.analyze_text_content(s3_id, """
    Monitoring: Module #56, Module #57
    Status: OPERATIONAL
    ✅ All instances coordinated
    """)

    print(f"   Analyzed 3 screenshots")

    # Get coordination status
    print("\n🔍 Coordination Status:")
    status = analyzer.get_coordination_status()
    print(f"   Active instances: {status['active_instances']}")
    print(f"   Modules seen: {status['modules']}")
    print(f"   Overall sentiment: {status['overall_sentiment'].upper()}")

    # Instance activities
    print("\n📊 Instance Activities:")
    for inst_id, activity in status['instance_activities'].items():
        print(f"   {inst_id}: {activity['screenshot_count']} screenshots, "
              f"{activity['success_count']} successes")

    # Export analysis
    analyzer.export_analysis('/tmp/screenshot_analysis.json')
    print("\n💾 Analysis exported to /tmp/screenshot_analysis.json")

    # Show metrics
    metrics = analyzer.get_metrics()
    print(f"\n📈 Metrics:")
    print(f"   Screenshots analyzed: {metrics['screenshots_analyzed']}")
    print(f"   Errors found: {metrics['errors_found']}")
    print(f"   Successes found: {metrics['successes_found']}")

    print("\n✅ Screenshot Analyzer operational!")
    print("🚀 Ready to coordinate via visual analysis!")
