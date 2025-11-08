"""
MODULE #22: AUTONOMOUS LEARNING SYSTEM
Instance 3: Module Developer
Built: 2025-11-08

Self-improving AI that learns from experience without manual training.
Adapts to user behavior and discovers new patterns autonomously.
"""

import json
import time
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import random


class FeedbackType(Enum):
    """Types of feedback for learning"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CORRECTION = "correction"


class LearningStrategy(Enum):
    """Learning approaches"""
    REINFORCEMENT = "reinforcement"  # Learn from rewards/penalties
    IMITATION = "imitation"  # Learn from examples
    EXPLORATION = "exploration"  # Try new things
    EXPLOITATION = "exploitation"  # Use what works


@dataclass
class Experience:
    """Represents a learning experience"""
    timestamp: float
    context: Dict[str, Any]
    action: str
    result: Any
    feedback: FeedbackType
    reward: float
    metadata: Dict[str, Any]


@dataclass
class LearningMetrics:
    """Track learning progress"""
    total_experiences: int
    positive_outcomes: int
    negative_outcomes: int
    accuracy_rate: float
    improvement_rate: float
    exploration_rate: float
    confidence_score: float


class AutonomousLearningSystem:
    """
    Self-improving AI that learns from experience.

    Key features:
    - No manual training required
    - Learns from user feedback
    - Discovers patterns autonomously
    - Adapts strategies based on success
    - Improves over time
    """

    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.experience_buffer: List[Experience] = []
        self.knowledge_base: Dict[str, Any] = defaultdict(dict)
        self.strategy_scores: Dict[LearningStrategy, float] = {
            strategy: 1.0 for strategy in LearningStrategy
        }
        self.action_success_rate: Dict[str, List[bool]] = defaultdict(list)
        self.pattern_library: Dict[str, Dict[str, Any]] = {}
        self.metrics = LearningMetrics(0, 0, 0, 0.0, 0.0, 0.3, 0.5)
        self.start_time = time.time()

    def record_experience(
        self,
        context: Dict[str, Any],
        action: str,
        result: Any,
        feedback: FeedbackType,
        reward: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Experience:
        """
        Record an experience for learning

        Args:
            context: Situation/state when action was taken
            action: What action was performed
            result: What happened
            feedback: Type of feedback received
            reward: Numeric reward (-1.0 to 1.0)
            metadata: Additional information
        """
        exp = Experience(
            timestamp=time.time(),
            context=context,
            action=action,
            result=result,
            feedback=feedback,
            reward=reward,
            metadata=metadata or {}
        )

        self.experience_buffer.append(exp)

        # Update action success tracking
        success = feedback in [FeedbackType.POSITIVE, FeedbackType.NEUTRAL]
        self.action_success_rate[action].append(success)

        # Learn from experience
        self._learn_from_experience(exp)

        # Update metrics
        self._update_metrics()

        return exp

    def _learn_from_experience(self, exp: Experience):
        """Extract knowledge from experience"""

        # 1. Update knowledge base
        context_key = self._hash_context(exp.context)
        if context_key not in self.knowledge_base:
            self.knowledge_base[context_key] = {
                "actions_tried": [],
                "best_action": None,
                "best_reward": -float('inf')
            }

        kb_entry = self.knowledge_base[context_key]
        kb_entry["actions_tried"].append({
            "action": exp.action,
            "reward": exp.reward,
            "feedback": exp.feedback.value
        })

        if exp.reward > kb_entry["best_reward"]:
            kb_entry["best_action"] = exp.action
            kb_entry["best_reward"] = exp.reward

        # 2. Discover patterns
        if exp.feedback == FeedbackType.POSITIVE:
            self._discover_pattern(exp)

        # 3. Update strategy scores
        self._update_strategy_scores(exp)

    def _hash_context(self, context: Dict[str, Any]) -> str:
        """Create a hash key from context"""
        # Simple hash - in production would use more sophisticated method
        items = sorted(context.items())
        return str(hash(tuple(items)))

    def _discover_pattern(self, exp: Experience):
        """Automatically discover patterns from positive experiences"""

        # Look for recurring elements in positive experiences
        positive_exps = [
            e for e in self.experience_buffer
            if e.feedback == FeedbackType.POSITIVE
        ]

        if len(positive_exps) < 3:
            return  # Need more data

        # Find common context elements
        common_keys = set(exp.context.keys())
        for other_exp in positive_exps[-5:]:  # Last 5 positive experiences
            common_keys &= set(other_exp.context.keys())

        if common_keys:
            pattern_id = f"pattern_{len(self.pattern_library) + 1}"
            self.pattern_library[pattern_id] = {
                "common_context_keys": list(common_keys),
                "successful_actions": [e.action for e in positive_exps[-5:]],
                "avg_reward": sum(e.reward for e in positive_exps[-5:]) / len(positive_exps[-5:]),
                "discovered_at": time.time(),
                "confidence": min(len(positive_exps) / 10, 1.0)
            }

    def _update_strategy_scores(self, exp: Experience):
        """Adjust strategy scores based on success"""

        # Determine which strategy was likely used
        # (In practice, would track which strategy was explicitly used)

        # Update all strategies with small learning rate
        adjustment = self.learning_rate * exp.reward

        for strategy in LearningStrategy:
            # Decay factor to prevent scores from growing unbounded
            self.strategy_scores[strategy] *= 0.99

            # Add adjustment
            if exp.feedback == FeedbackType.POSITIVE:
                self.strategy_scores[strategy] += adjustment
            elif exp.feedback == FeedbackType.NEGATIVE:
                self.strategy_scores[strategy] -= adjustment

    def _update_metrics(self):
        """Update learning metrics"""
        if not self.experience_buffer:
            return

        total = len(self.experience_buffer)
        positive = sum(1 for e in self.experience_buffer if e.feedback == FeedbackType.POSITIVE)
        negative = sum(1 for e in self.experience_buffer if e.feedback == FeedbackType.NEGATIVE)

        # Calculate accuracy over last 20 experiences
        recent = self.experience_buffer[-20:]
        accuracy = sum(1 for e in recent if e.feedback in [FeedbackType.POSITIVE, FeedbackType.NEUTRAL]) / len(recent)

        # Calculate improvement (compare first half vs second half accuracy)
        if total >= 10:
            half = total // 2
            first_half_acc = sum(1 for e in self.experience_buffer[:half] if e.feedback == FeedbackType.POSITIVE) / half
            second_half_acc = sum(1 for e in self.experience_buffer[half:] if e.feedback == FeedbackType.POSITIVE) / (total - half)
            improvement = second_half_acc - first_half_acc
        else:
            improvement = 0.0

        # Exploration rate (how often trying new things)
        exploration = 1.0 - (len(self.knowledge_base) / max(total, 1))

        # Confidence (based on pattern library and success rate)
        confidence = min((len(self.pattern_library) / 10 + accuracy) / 2, 1.0)

        self.metrics = LearningMetrics(
            total_experiences=total,
            positive_outcomes=positive,
            negative_outcomes=negative,
            accuracy_rate=accuracy,
            improvement_rate=improvement,
            exploration_rate=exploration,
            confidence_score=confidence
        )

    def suggest_action(
        self,
        context: Dict[str, Any],
        available_actions: List[str],
        strategy: Optional[LearningStrategy] = None
    ) -> Tuple[str, float]:
        """
        Suggest best action for given context

        Args:
            context: Current situation
            available_actions: List of possible actions
            strategy: Which learning strategy to use (or auto-select)

        Returns:
            (suggested_action, confidence)
        """

        # Auto-select strategy if not specified
        if strategy is None:
            strategy = self._select_best_strategy()

        context_key = self._hash_context(context)

        if strategy == LearningStrategy.EXPLOITATION:
            # Use what we know works
            if context_key in self.knowledge_base:
                best_action = self.knowledge_base[context_key]["best_action"]
                if best_action and best_action in available_actions:
                    confidence = self.knowledge_base[context_key]["best_reward"]
                    return best_action, max(0, min(confidence, 1.0))

        elif strategy == LearningStrategy.EXPLORATION:
            # Try something new
            return random.choice(available_actions), 0.3

        elif strategy == LearningStrategy.IMITATION:
            # Use most commonly successful action
            action_counts = defaultdict(int)
            for exp in self.experience_buffer:
                if exp.feedback == FeedbackType.POSITIVE:
                    action_counts[exp.action] += 1

            if action_counts:
                best = max(action_counts.items(), key=lambda x: x[1])
                if best[0] in available_actions:
                    return best[0], min(best[1] / len(self.experience_buffer), 1.0)

        # Default: random choice with low confidence
        return random.choice(available_actions), 0.1

    def _select_best_strategy(self) -> LearningStrategy:
        """Choose which learning strategy to use"""

        # If we don't have much experience, explore
        if len(self.experience_buffer) < 10:
            return LearningStrategy.EXPLORATION

        # If accuracy is low, try imitation
        if self.metrics.accuracy_rate < 0.5:
            return LearningStrategy.IMITATION

        # If accuracy is high, exploit what works
        if self.metrics.accuracy_rate > 0.7:
            return LearningStrategy.EXPLOITATION

        # Otherwise, use best scoring strategy
        best_strategy = max(self.strategy_scores.items(), key=lambda x: x[1])
        return best_strategy[0]

    def get_action_recommendation(self, action: str) -> Dict[str, Any]:
        """Get detailed recommendation for an action"""

        if action not in self.action_success_rate:
            return {
                "action": action,
                "recommendation": "UNKNOWN",
                "success_rate": 0.0,
                "sample_size": 0,
                "advice": "No data yet - proceed with caution"
            }

        results = self.action_success_rate[action]
        success_rate = sum(results) / len(results)

        if success_rate >= 0.7:
            recommendation = "HIGHLY RECOMMENDED"
            advice = "This action has high success rate"
        elif success_rate >= 0.5:
            recommendation = "RECOMMENDED"
            advice = "This action works more often than not"
        elif success_rate >= 0.3:
            recommendation = "RISKY"
            advice = "This action often fails - consider alternatives"
        else:
            recommendation = "NOT RECOMMENDED"
            advice = "This action has low success rate - avoid if possible"

        return {
            "action": action,
            "recommendation": recommendation,
            "success_rate": success_rate,
            "sample_size": len(results),
            "advice": advice
        }

    def generate_learning_report(self) -> str:
        """Generate human-readable learning report"""

        runtime = time.time() - self.start_time

        report = "=" * 60 + "\n"
        report += "AUTONOMOUS LEARNING SYSTEM - REPORT\n"
        report += "=" * 60 + "\n\n"

        report += f"Runtime: {runtime:.1f} seconds\n"
        report += f"Total Experiences: {self.metrics.total_experiences}\n"
        report += f"Positive Outcomes: {self.metrics.positive_outcomes}\n"
        report += f"Negative Outcomes: {self.metrics.negative_outcomes}\n"
        report += f"Accuracy Rate: {self.metrics.accuracy_rate * 100:.1f}%\n"
        report += f"Improvement Rate: {self.metrics.improvement_rate * 100:.1f}%\n"
        report += f"Confidence Score: {self.metrics.confidence_score * 100:.1f}%\n\n"

        report += "PATTERNS DISCOVERED:\n"
        if self.pattern_library:
            for pattern_id, pattern in self.pattern_library.items():
                report += f"  - {pattern_id}: {len(pattern['common_context_keys'])} common elements, "
                report += f"{pattern['confidence'] * 100:.0f}% confidence\n"
        else:
            report += "  (No patterns discovered yet)\n"
        report += "\n"

        report += "STRATEGY SCORES:\n"
        for strategy, score in sorted(self.strategy_scores.items(), key=lambda x: x[1], reverse=True):
            report += f"  - {strategy.value}: {score:.2f}\n"
        report += "\n"

        report += "TOP ACTIONS:\n"
        action_scores = []
        for action, results in self.action_success_rate.items():
            if len(results) >= 3:  # Only show actions with enough data
                success_rate = sum(results) / len(results)
                action_scores.append((action, success_rate, len(results)))

        action_scores.sort(key=lambda x: x[1], reverse=True)
        for action, rate, count in action_scores[:5]:
            report += f"  - {action}: {rate * 100:.0f}% success ({count} attempts)\n"

        if not action_scores:
            report += "  (Not enough data yet)\n"

        report += "\n" + "=" * 60 + "\n"

        return report

    def save_state(self, filepath: str):
        """Save learning state to file"""
        state = {
            "learning_rate": self.learning_rate,
            "experience_buffer": [asdict(e) for e in self.experience_buffer],
            "knowledge_base": dict(self.knowledge_base),
            "strategy_scores": {s.value: score for s, score in self.strategy_scores.items()},
            "action_success_rate": {k: v for k, v in self.action_success_rate.items()},
            "pattern_library": self.pattern_library,
            "start_time": self.start_time
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, filepath: str):
        """Load learning state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)

        self.learning_rate = state["learning_rate"]
        self.knowledge_base = defaultdict(dict, state["knowledge_base"])
        self.strategy_scores = {
            LearningStrategy(k): v for k, v in state["strategy_scores"].items()
        }
        self.action_success_rate = defaultdict(list, state["action_success_rate"])
        self.pattern_library = state["pattern_library"]
        self.start_time = state["start_time"]

        # Reconstruct experiences
        self.experience_buffer = []
        for exp_dict in state["experience_buffer"]:
            exp_dict["feedback"] = FeedbackType(exp_dict["feedback"])
            self.experience_buffer.append(Experience(**exp_dict))

        self._update_metrics()


def demo():
    """Demonstrate the autonomous learning system"""

    print("=" * 60)
    print("AUTONOMOUS LEARNING SYSTEM - DEMO")
    print("=" * 60)
    print()

    learner = AutonomousLearningSystem(learning_rate=0.2)

    # Simulate learning to play a simple game
    print("SCENARIO: Learning to navigate a maze")
    print()

    # Define actions
    actions = ["go_north", "go_south", "go_east", "go_west"]

    # Simulate 50 experiences
    for i in range(50):
        context = {"position": random.randint(0, 10), "step": i}

        # Get suggested action
        action, confidence = learner.suggest_action(context, actions)

        # Simulate result (north and east are generally better)
        if action in ["go_north", "go_east"]:
            result = "moved closer to goal"
            feedback = FeedbackType.POSITIVE
            reward = 1.0
        elif action == "go_south":
            result = "moved away from goal"
            feedback = FeedbackType.NEGATIVE
            reward = -1.0
        else:
            result = "no change"
            feedback = FeedbackType.NEUTRAL
            reward = 0.0

        # Record experience
        learner.record_experience(
            context=context,
            action=action,
            result=result,
            feedback=feedback,
            reward=reward
        )

        if i % 10 == 0:
            print(f"Step {i}: {action} (confidence: {confidence:.2f}) -> {result}")

    print()
    print(learner.generate_learning_report())

    # Show action recommendations
    print("\nACTION RECOMMENDATIONS:")
    for action in actions:
        rec = learner.get_action_recommendation(action)
        print(f"{action}: {rec['recommendation']} ({rec['success_rate'] * 100:.0f}% success)")

    print()
    print("=" * 60)
    print("Demo complete. The system learned from experience!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
