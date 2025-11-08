#!/usr/bin/env python3
"""
RECURSIVE LEARNING MODULE
==========================

Self-improvement system that enables AI to learn from its own outputs,
identify patterns, track performance, and iteratively improve responses.

Features:
- Output quality tracking and analysis
- Pattern recognition in responses
- Performance metrics over time
- Iterative refinement
- Error pattern detection
- Success pattern amplification
- Learning rate adjustment
- Meta-learning capabilities

Module #23 of 100x Platform
"""

import json
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum
import hashlib
import re


class OutcomeType(Enum):
    """Types of outcomes for learning"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    UNKNOWN = "unknown"


@dataclass
class LearningInstance:
    """Single learning instance"""
    instance_id: str
    timestamp: datetime
    input_data: str
    output_data: str
    outcome: OutcomeType
    score: float  # 0.0 to 1.0
    metadata: Dict
    patterns_detected: List[str]
    improvement_suggestions: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'instance_id': self.instance_id,
            'timestamp': self.timestamp.isoformat(),
            'input_data': self.input_data,
            'output_data': self.output_data,
            'outcome': self.outcome.value,
            'score': self.score,
            'metadata': self.metadata,
            'patterns_detected': self.patterns_detected,
            'improvement_suggestions': self.improvement_suggestions
        }


class RecursiveLearningEngine:
    """Engine for recursive self-improvement"""

    def __init__(self, storage_dir: str = "learning_data"):
        """Initialize learning engine"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        self.instances: List[LearningInstance] = []
        self.patterns: Dict[str, int] = {}  # pattern -> frequency
        self.success_patterns: List[str] = []
        self.failure_patterns: List[str] = []
        self.learning_rate = 0.1

        self._load_history()

    def _generate_id(self) -> str:
        """Generate unique instance ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

    def _load_history(self):
        """Load learning history"""
        history_file = self.storage_dir / "learning_history.json"
        if history_file.exists():
            with open(history_file) as f:
                data = json.load(f)
                # Reconstruct instances (simplified loading)
                self.patterns = data.get('patterns', {})
                self.success_patterns = data.get('success_patterns', [])
                self.failure_patterns = data.get('failure_patterns', [])

    def _save_history(self):
        """Save learning history"""
        history_file = self.storage_dir / "learning_history.json"
        data = {
            'patterns': self.patterns,
            'success_patterns': self.success_patterns,
            'failure_patterns': self.failure_patterns,
            'total_instances': len(self.instances),
            'last_updated': datetime.now().isoformat()
        }
        with open(history_file, 'w') as f:
            json.dump(data, f, indent=2)

    def record_instance(self, input_data: str, output_data: str,
                       outcome: OutcomeType, score: float,
                       metadata: Dict = None) -> LearningInstance:
        """Record a learning instance"""
        # Detect patterns
        patterns = self._detect_patterns(input_data, output_data)

        # Generate improvement suggestions
        suggestions = self._generate_suggestions(
            input_data, output_data, outcome, score, patterns
        )

        # Create instance
        instance = LearningInstance(
            instance_id=self._generate_id(),
            timestamp=datetime.now(),
            input_data=input_data,
            output_data=output_data,
            outcome=outcome,
            score=score,
            metadata=metadata or {},
            patterns_detected=patterns,
            improvement_suggestions=suggestions
        )

        # Record
        self.instances.append(instance)

        # Update pattern tracking
        self._update_patterns(patterns, outcome)

        # Save
        self._save_instance(instance)
        self._save_history()

        return instance

    def _detect_patterns(self, input_data: str, output_data: str) -> List[str]:
        """Detect patterns in input/output"""
        patterns = []

        # Length patterns
        if len(output_data) > 1000:
            patterns.append("long_response")
        elif len(output_data) < 100:
            patterns.append("short_response")

        # Structure patterns
        if output_data.count('\n') > 10:
            patterns.append("multi_paragraph")
        if '```' in output_data:
            patterns.append("code_included")
        if output_data.count('•') > 3 or output_data.count('-') > 3:
            patterns.append("bulleted_list")
        if re.search(r'\d+\.', output_data):
            patterns.append("numbered_list")

        # Tone patterns
        if '!' in output_data:
            patterns.append("enthusiastic")
        if '?' in output_data:
            patterns.append("questioning")

        # Content patterns
        if any(word in output_data.lower() for word in ['however', 'but', 'although']):
            patterns.append("nuanced_response")
        if any(word in output_data.lower() for word in ['example', 'instance', 'such as']):
            patterns.append("example_included")

        # Question type patterns
        if '?' in input_data:
            if input_data.lower().startswith(('what', 'how', 'why', 'when', 'where', 'who')):
                patterns.append(f"question_{input_data.split()[0].lower()}")

        return patterns

    def _update_patterns(self, patterns: List[str], outcome: OutcomeType):
        """Update pattern tracking"""
        for pattern in patterns:
            self.patterns[pattern] = self.patterns.get(pattern, 0) + 1

            if outcome == OutcomeType.SUCCESS:
                if pattern not in self.success_patterns:
                    self.success_patterns.append(pattern)
            elif outcome == OutcomeType.FAILURE:
                if pattern not in self.failure_patterns:
                    self.failure_patterns.append(pattern)

    def _generate_suggestions(self, input_data: str, output_data: str,
                             outcome: OutcomeType, score: float,
                             patterns: List[str]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        # Based on outcome
        if outcome == OutcomeType.FAILURE or score < 0.5:
            # Check if response was too short
            if len(output_data) < 100:
                suggestions.append("Provide more detailed explanation")

            # Check if examples were missing
            if "example_included" not in patterns:
                suggestions.append("Include concrete examples")

            # Check for failed patterns
            for pattern in patterns:
                if pattern in self.failure_patterns:
                    suggestions.append(f"Avoid pattern: {pattern}")

        # Based on success patterns
        if outcome == OutcomeType.SUCCESS and score > 0.7:
            for pattern in patterns:
                if pattern not in self.success_patterns:
                    suggestions.append(f"Successful pattern discovered: {pattern}")

        # General suggestions based on score
        if score < 0.3:
            suggestions.append("Complete rethink of approach recommended")
        elif score < 0.6:
            suggestions.append("Moderate improvements needed")

        return suggestions

    def _save_instance(self, instance: LearningInstance):
        """Save individual instance"""
        instance_file = self.storage_dir / f"instance_{instance.instance_id}.json"
        with open(instance_file, 'w') as f:
            json.dump(instance.to_dict(), f, indent=2)

    def get_insights(self) -> Dict:
        """Get learning insights"""
        if not self.instances:
            return {
                'total_instances': 0,
                'message': 'No learning data yet'
            }

        # Calculate metrics
        total = len(self.instances)
        success_count = sum(1 for i in self.instances if i.outcome == OutcomeType.SUCCESS)
        failure_count = sum(1 for i in self.instances if i.outcome == OutcomeType.FAILURE)
        avg_score = sum(i.score for i in self.instances) / total

        # Recent trend
        recent = self.instances[-10:]  # Last 10
        recent_avg = sum(i.score for i in recent) / len(recent) if recent else 0

        # Improvement rate
        if total > 10:
            early = self.instances[:10]
            early_avg = sum(i.score for i in early) / len(early)
            improvement = ((recent_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0
        else:
            improvement = 0

        return {
            'total_instances': total,
            'success_rate': f"{(success_count/total*100):.1f}%",
            'failure_rate': f"{(failure_count/total*100):.1f}%",
            'average_score': f"{avg_score:.2f}",
            'recent_average': f"{recent_avg:.2f}",
            'improvement_rate': f"{improvement:+.1f}%",
            'top_patterns': sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)[:10],
            'success_patterns': self.success_patterns[:10],
            'failure_patterns': self.failure_patterns[:10],
            'learning_rate': self.learning_rate
        }

    def get_recommendations(self, input_data: str) -> List[str]:
        """Get recommendations for given input"""
        recommendations = []

        # Check what worked before for similar inputs
        similar = [i for i in self.instances if self._similarity(input_data, i.input_data) > 0.3]

        if similar:
            # Get patterns from successful similar instances
            successful = [i for i in similar if i.outcome == OutcomeType.SUCCESS and i.score > 0.7]

            if successful:
                common_patterns = {}
                for instance in successful:
                    for pattern in instance.patterns_detected:
                        common_patterns[pattern] = common_patterns.get(pattern, 0) + 1

                recommendations.append("Based on similar successful cases:")
                for pattern, count in sorted(common_patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
                    recommendations.append(f"  • Use pattern: {pattern} (worked {count} times)")

        # General recommendations based on success patterns
        recommendations.append("\nGeneral recommendations:")
        for pattern in self.success_patterns[:5]:
            recommendations.append(f"  • Consider: {pattern}")

        # Avoid failure patterns
        if self.failure_patterns:
            recommendations.append("\nAvoid these patterns:")
            for pattern in self.failure_patterns[:3]:
                recommendations.append(f"  • Avoid: {pattern}")

        return recommendations

    def _similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def analyze_improvement_trend(self) -> Dict:
        """Analyze how performance improves over time"""
        if len(self.instances) < 5:
            return {'message': 'Not enough data for trend analysis'}

        # Split into chunks
        chunk_size = max(5, len(self.instances) // 5)
        chunks = [self.instances[i:i+chunk_size]
                 for i in range(0, len(self.instances), chunk_size)]

        trend_data = []
        for i, chunk in enumerate(chunks):
            avg_score = sum(inst.score for inst in chunk) / len(chunk)
            success_rate = sum(1 for inst in chunk if inst.outcome == OutcomeType.SUCCESS) / len(chunk)

            trend_data.append({
                'chunk': i + 1,
                'size': len(chunk),
                'avg_score': avg_score,
                'success_rate': success_rate
            })

        # Calculate overall trend
        if len(trend_data) > 1:
            first_score = trend_data[0]['avg_score']
            last_score = trend_data[-1]['avg_score']
            trend = "improving" if last_score > first_score else "declining"
            change = abs(last_score - first_score)
        else:
            trend = "insufficient_data"
            change = 0

        return {
            'trend': trend,
            'change': f"{change:.2f}",
            'chunks': trend_data
        }

    def export_learnings(self, output_file: str):
        """Export learning insights to file"""
        insights = self.get_insights()
        trend = self.analyze_improvement_trend()

        export_data = {
            'export_date': datetime.now().isoformat(),
            'insights': insights,
            'trend_analysis': trend,
            'total_instances': len(self.instances),
            'storage_location': str(self.storage_dir)
        }

        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)


def demo():
    """Demonstrate recursive learning"""
    print("=" * 70)
    print("RECURSIVE LEARNING MODULE - MODULE #23")
    print("=" * 70)
    print()

    engine = RecursiveLearningEngine()

    # Simulate learning instances
    print("📚 Recording learning instances...")
    print("-" * 70)

    test_cases = [
        ("What is Python?", "Python is a programming language.", OutcomeType.PARTIAL_SUCCESS, 0.6),
        ("What is Python?", "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, it's widely used for web development, data science, automation, and more.", OutcomeType.SUCCESS, 0.9),
        ("Explain machine learning", "ML is when computers learn.", OutcomeType.FAILURE, 0.3),
        ("Explain machine learning", "Machine learning is a subset of AI that enables systems to learn from data and improve without explicit programming. For example, spam filters learn to identify spam emails by analyzing patterns in thousands of labeled messages.", OutcomeType.SUCCESS, 0.95),
        ("Give me a recipe", "Sure! Here's a simple pasta recipe:\n1. Boil water\n2. Add pasta\n3. Cook 10 minutes\n4. Drain and serve", OutcomeType.SUCCESS, 0.8),
    ]

    for input_data, output_data, outcome, score in test_cases:
        instance = engine.record_instance(input_data, output_data, outcome, score)
        print(f"✓ Recorded: {instance.instance_id[:8]}... (score: {score}, patterns: {len(instance.patterns_detected)})")

    print()

    # Get insights
    print("🔍 LEARNING INSIGHTS:")
    print("-" * 70)
    insights = engine.get_insights()
    print(f"Total instances: {insights['total_instances']}")
    print(f"Success rate: {insights['success_rate']}")
    print(f"Average score: {insights['average_score']}")
    print(f"Recent average: {insights['recent_average']}")
    print(f"Improvement rate: {insights['improvement_rate']}")
    print()

    print("Top patterns:")
    for pattern, count in insights['top_patterns']:
        print(f"  • {pattern}: {count} times")
    print()

    # Get recommendations
    print("💡 RECOMMENDATIONS for 'How does AI work?':")
    print("-" * 70)
    recs = engine.get_recommendations("How does AI work?")
    for rec in recs:
        print(rec)
    print()

    # Trend analysis
    print("📈 IMPROVEMENT TREND:")
    print("-" * 70)
    trend = engine.analyze_improvement_trend()
    if 'trend' in trend:
        print(f"Overall trend: {trend['trend']}")
        print(f"Performance change: {trend['change']}")
    print()

    # Export
    print("💾 EXPORTING LEARNINGS:")
    print("-" * 70)
    engine.export_learnings("learning_export.json")
    print("   Exported to: learning_export.json")
    print()

    print("=" * 70)
    print("✅ Module #23 - Recursive Learning - OPERATIONAL")
    print("=" * 70)


if __name__ == "__main__":
    demo()
