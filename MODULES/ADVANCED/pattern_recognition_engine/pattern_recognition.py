"""
MODULE #21: PATTERN RECOGNITION ENGINE
Instance 3: Module Developer
Built: 2025-11-07

Detects patterns in data, behavior, and systems.
Helps users see what unconscious people miss.
"""

import json
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class PatternType(Enum):
    """Types of patterns the engine can detect"""
    MANIPULATION = "manipulation"
    EXTRACTION = "extraction"
    BEHAVIORAL = "behavioral"
    LINGUISTIC = "linguistic"
    TEMPORAL = "temporal"
    SYSTEMIC = "systemic"


@dataclass
class Pattern:
    """Represents a detected pattern"""
    type: PatternType
    name: str
    description: str
    confidence: float
    examples: List[str]
    indicators: List[str]


class PatternRecognitionEngine:
    """
    Analyzes text, data, and behavior to detect patterns.
    Helps users become conscious of manipulation and extraction.
    """

    def __init__(self):
        self.patterns_db = self._load_pattern_database()
        self.detection_history = []

    def _load_pattern_database(self) -> Dict[str, Pattern]:
        """Load known patterns for detection"""
        return {
            # Manipulation Patterns
            "fear_amplification": Pattern(
                type=PatternType.MANIPULATION,
                name="Fear Amplification",
                description="Creating/exaggerating threats to maintain control",
                confidence=0.0,
                examples=[
                    "If you don't act now, disaster will strike",
                    "Without us, you're in danger",
                    "The world is falling apart"
                ],
                indicators=["urgent", "crisis", "disaster", "threat", "danger", "emergency"]
            ),

            "false_dichotomy": Pattern(
                type=PatternType.MANIPULATION,
                name="False Dichotomy",
                description="Presenting only two options when more exist",
                confidence=0.0,
                examples=[
                    "Either you're with us or against us",
                    "You have to choose: A or B"
                ],
                indicators=["either", "or", "only two", "must choose", "no other option"]
            ),

            "authority_worship": Pattern(
                type=PatternType.MANIPULATION,
                name="Authority Worship",
                description="Appeal to authority without allowing questions",
                confidence=0.0,
                examples=[
                    "Trust the experts",
                    "The science is settled",
                    "Don't question the authorities"
                ],
                indicators=["trust the", "experts say", "settled", "don't question", "authorities"]
            ),

            "gaslighting": Pattern(
                type=PatternType.MANIPULATION,
                name="Gaslighting",
                description="Denying reality to make someone doubt themselves",
                confidence=0.0,
                examples=[
                    "That never happened",
                    "You're imagining things",
                    "You're being too sensitive"
                ],
                indicators=["never happened", "imagining", "too sensitive", "overreacting", "crazy"]
            ),

            # Extraction Patterns
            "attention_extraction": Pattern(
                type=PatternType.EXTRACTION,
                name="Attention Extraction",
                description="Designed to capture and hold attention for profit",
                confidence=0.0,
                examples=[
                    "Infinite scroll",
                    "Autoplay next video",
                    "Push notifications"
                ],
                indicators=["scroll", "autoplay", "notification", "breaking", "you won't believe"]
            ),

            "monetary_extraction": Pattern(
                type=PatternType.EXTRACTION,
                name="Monetary Extraction",
                description="Recurring charges or hidden fees",
                confidence=0.0,
                examples=[
                    "Monthly subscription (auto-renew)",
                    "Free trial (credit card required)",
                    "Hidden fees"
                ],
                indicators=["subscription", "auto-renew", "trial", "fees apply", "recurring"]
            ),

            "data_extraction": Pattern(
                type=PatternType.EXTRACTION,
                name="Data Extraction",
                description="Harvesting personal data for profit",
                confidence=0.0,
                examples=[
                    "Accept all cookies",
                    "Share your location",
                    "Access to contacts"
                ],
                indicators=["cookies", "location", "permissions", "access to", "share"]
            ),

            # Behavioral Patterns
            "addiction_loop": Pattern(
                type=PatternType.BEHAVIORAL,
                name="Addiction Loop",
                description="Trigger → Action → Reward → Repeat",
                confidence=0.0,
                examples=[
                    "Check phone when bored",
                    "Scroll when anxious",
                    "Buy when sad"
                ],
                indicators=["when", "every time", "can't stop", "always", "habit"]
            ),

            "conformity_pressure": Pattern(
                type=PatternType.BEHAVIORAL,
                name="Conformity Pressure",
                description="Social pressure to conform",
                confidence=0.0,
                examples=[
                    "Everyone else is doing it",
                    "Don't be left behind",
                    "Join the crowd"
                ],
                indicators=["everyone", "all", "majority", "normal", "left behind"]
            ),

            # Systemic Patterns
            "planned_obsolescence": Pattern(
                type=PatternType.SYSTEMIC,
                name="Planned Obsolescence",
                description="Designed to fail to force replacement",
                confidence=0.0,
                examples=[
                    "Software updates slow down old devices",
                    "Parts designed to break after warranty",
                    "Non-replaceable batteries"
                ],
                indicators=["upgrade", "new model", "outdated", "no longer supported", "replace"]
            ),

            "regulatory_capture": Pattern(
                type=PatternType.SYSTEMIC,
                name="Regulatory Capture",
                description="Industry controls its own regulation",
                confidence=0.0,
                examples=[
                    "Former industry executives become regulators",
                    "Regulations written by lobbyists",
                    "Revolving door between industry and government"
                ],
                indicators=["industry", "lobbyist", "former executive", "appointed", "advisory"]
            )
        }

    def analyze_text(self, text: str) -> List[Pattern]:
        """
        Analyze text for manipulation and extraction patterns
        """
        text_lower = text.lower()
        detected_patterns = []

        for pattern_id, pattern in self.patterns_db.items():
            # Check how many indicators are present
            matches = sum(1 for indicator in pattern.indicators if indicator in text_lower)

            if matches > 0:
                # Calculate confidence based on indicator matches
                confidence = min(matches / len(pattern.indicators), 1.0)

                if confidence > 0.3:  # Threshold for detection
                    detected_pattern = Pattern(
                        type=pattern.type,
                        name=pattern.name,
                        description=pattern.description,
                        confidence=confidence,
                        examples=pattern.examples,
                        indicators=pattern.indicators
                    )
                    detected_patterns.append(detected_pattern)

        # Sort by confidence
        detected_patterns.sort(key=lambda p: p.confidence, reverse=True)

        # Store in history
        self.detection_history.append({
            "text": text[:100],  # First 100 chars
            "patterns_found": len(detected_patterns),
            "highest_confidence": detected_patterns[0].confidence if detected_patterns else 0
        })

        return detected_patterns

    def analyze_behavior_sequence(self, events: List[str]) -> Dict[str, Any]:
        """
        Analyze sequence of events for behavioral patterns
        """
        patterns_found = []

        # Check for repetitive behavior
        if len(events) != len(set(events)):
            patterns_found.append({
                "pattern": "Repetitive Behavior",
                "description": "Same actions repeated",
                "frequency": len(events) - len(set(events))
            })

        # Check for addiction loop (same action at same intervals)
        time_deltas = []
        for i in range(1, len(events)):
            if events[i] == events[0]:
                time_deltas.append(i)

        if len(time_deltas) >= 3:
            # Check if intervals are consistent
            avg_interval = sum(time_deltas) / len(time_deltas)
            if all(abs(delta - avg_interval) < 2 for delta in time_deltas):
                patterns_found.append({
                    "pattern": "Addiction Loop Detected",
                    "description": f"Action '{events[0]}' repeats every ~{avg_interval} events",
                    "confidence": 0.8
                })

        return {
            "total_events": len(events),
            "unique_events": len(set(events)),
            "patterns": patterns_found,
            "is_conscious": len(patterns_found) == 0  # Conscious = no repetitive patterns
        }

    def detect_manipulation_tactics(self, conversation: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Analyze a conversation for manipulation tactics
        """
        tactics_detected = []

        for i, message in enumerate(conversation):
            text = message.get("text", "")
            speaker = message.get("speaker", "unknown")

            # Detect patterns in this message
            patterns = self.analyze_text(text)

            if patterns:
                tactics_detected.append({
                    "message_index": i,
                    "speaker": speaker,
                    "tactics": [
                        {
                            "name": p.name,
                            "type": p.type.value,
                            "confidence": p.confidence
                        }
                        for p in patterns
                    ]
                })

        return tactics_detected

    def generate_report(self, text: str) -> str:
        """
        Generate human-readable report of detected patterns
        """
        patterns = self.analyze_text(text)

        if not patterns:
            return "✅ No manipulation or extraction patterns detected."

        report = "⚠️ PATTERNS DETECTED:\n\n"

        for i, pattern in enumerate(patterns, 1):
            report += f"{i}. {pattern.name} ({pattern.confidence * 100:.0f}% confidence)\n"
            report += f"   Type: {pattern.type.value}\n"
            report += f"   Description: {pattern.description}\n"
            report += f"   Examples: {', '.join(pattern.examples[:2])}\n\n"

        return report

    def consciousness_score(self, text: str) -> Dict[str, Any]:
        """
        Score text on consciousness level (inverse of manipulation)
        """
        patterns = self.analyze_text(text)

        if not patterns:
            consciousness = 100
        else:
            # More patterns = less conscious
            avg_confidence = sum(p.confidence for p in patterns) / len(patterns)
            consciousness = max(0, 100 - (len(patterns) * 10 + avg_confidence * 20))

        return {
            "consciousness_score": round(consciousness, 1),
            "level": "Conscious" if consciousness > 70 else "Awakening" if consciousness > 40 else "Unconscious",
            "patterns_detected": len(patterns),
            "recommendation": "Keep questioning" if consciousness > 70 else "Study the patterns" if consciousness > 40 else "Wake up - you're being manipulated"
        }


def demo():
    """Demonstrate the pattern recognition engine"""
    engine = PatternRecognitionEngine()

    print("=" * 60)
    print("PATTERN RECOGNITION ENGINE - DEMO")
    print("=" * 60)
    print()

    # Test 1: Fear amplification
    print("TEST 1: News headline")
    text1 = "BREAKING: Crisis alert! Experts say we're in grave danger. You must act now before disaster strikes!"
    print(f"Text: {text1}")
    print()
    print(engine.generate_report(text1))

    # Test 2: Social media
    print("TEST 2: Social media post")
    text2 = "Everyone is upgrading to the new model. Don't be left behind! Limited time offer - act now!"
    print(f"Text: {text2}")
    print()
    print(engine.generate_report(text2))

    # Test 3: Conscious text
    print("TEST 3: Conscious communication")
    text3 = "I've analyzed multiple sources and here are my findings. Please verify independently and make your own decision."
    print(f"Text: {text3}")
    print()
    print(engine.generate_report(text3))

    # Test 4: Consciousness score
    print("TEST 4: Consciousness scores")
    for text, label in [(text1, "News"), (text2, "Social"), (text3, "Conscious")]:
        score = engine.consciousness_score(text)
        print(f"{label}: {score['consciousness_score']}/100 ({score['level']}) - {score['recommendation']}")
    print()

    # Test 5: Behavior analysis
    print("TEST 5: Behavior pattern detection")
    events = ["check_phone", "work", "check_phone", "eat", "check_phone", "sleep", "check_phone"]
    result = engine.analyze_behavior_sequence(events)
    print(f"Events: {events}")
    print(f"Patterns found: {result['patterns']}")
    print(f"Is conscious: {result['is_conscious']}")
    print()

    print("=" * 60)
    print("Demo complete. Pattern recognition engine operational.")
    print("=" * 60)


if __name__ == "__main__":
    demo()
