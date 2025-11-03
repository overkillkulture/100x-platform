"""
CONSCIOUSNESS SCREENING ALGORITHM
Uses Pattern Theory to detect Builders vs Destroyers
"""

import re

class ConsciousnessScreener:
    """
    Pattern Theory-based consciousness screening
    Detects manipulation, destroyer patterns, and builder characteristics
    """

    # Builder indicators (positive signals)
    BUILDER_KEYWORDS = [
        'build', 'create', 'help', 'collaborate', 'learn', 'grow', 'contribute',
        'solve', 'improve', 'innovate', 'share', 'teach', 'empower', 'support',
        'honest', 'transparency', 'accountability', 'responsibility', 'integrity',
        'consciousness', 'awareness', 'truth', 'freedom', 'liberation', 'authentic'
    ]

    # Destroyer indicators (red flags)
    DESTROYER_KEYWORDS = [
        'dominate', 'control', 'manipulate', 'deceive', 'exploit', 'scam',
        'trick', 'fool', 'steal', 'cheat', 'hack', 'break', 'destroy',
        'revenge', 'hurt', 'damage', 'ruin', 'crush', 'beat', 'win at all costs'
    ]

    # Manipulation patterns
    MANIPULATION_PATTERNS = [
        r'make\s+money\s+fast',
        r'get\s+rich\s+quick',
        r'secret\s+(trick|method|system)',
        r'guaranteed\s+(profit|success|money)',
        r'no\s+effort',
        r'passive\s+income\s+overnight',
        r'exploit\s+the\s+system'
    ]

    def __init__(self):
        self.builder_score = 0
        self.destroyer_score = 0
        self.manipulation_score = 0

    def analyze_text(self, text):
        """Analyze mission/values text for consciousness patterns"""
        if not text:
            return 0

        text_lower = text.lower()

        # Count builder keywords
        for keyword in self.BUILDER_KEYWORDS:
            if keyword in text_lower:
                self.builder_score += 1

        # Count destroyer keywords (negative score)
        for keyword in self.DESTROYER_KEYWORDS:
            if keyword in text_lower:
                self.destroyer_score += 1

        # Check manipulation patterns
        for pattern in self.MANIPULATION_PATTERNS:
            if re.search(pattern, text_lower):
                self.manipulation_score += 2

        return self.builder_score

    def calculate_consciousness_score(self, mission, values):
        """
        Calculate consciousness score (0-100)
        > 70 = Builder (auto-approve)
        50-70 = Review (manual)
        < 50 = Destroyer (reject)
        """

        # Reset scores
        self.builder_score = 0
        self.destroyer_score = 0
        self.manipulation_score = 0

        # Analyze mission and values
        self.analyze_text(mission)
        self.analyze_text(values)

        # Calculate base score
        base_score = (self.builder_score * 10) - (self.destroyer_score * 15) - (self.manipulation_score * 10)

        # Normalize to 0-100
        consciousness_score = max(0, min(100, base_score + 50))

        # Apply bonuses
        if mission and values:
            consciousness_score += 10  # Bonus for completing both fields

        if len(mission or "") > 50 or len(values or "") > 50:
            consciousness_score += 5  # Bonus for thoughtful responses

        return min(100, consciousness_score)

    def get_recommendation(self, score):
        """Get approval recommendation based on score"""
        if score >= 70:
            return "Approved", "✅ Builder detected - High consciousness"
        elif score >= 50:
            return "Pending", "⚠️ Manual review needed"
        else:
            return "Rejected", "❌ Destroyer pattern detected"

    def get_detailed_analysis(self, mission, values):
        """Get full consciousness analysis"""
        score = self.calculate_consciousness_score(mission, values)
        status, reason = self.get_recommendation(score)

        return {
            "consciousness_score": round(score, 2),
            "status": status,
            "reason": reason,
            "builder_signals": self.builder_score,
            "destroyer_signals": self.destroyer_score,
            "manipulation_signals": self.manipulation_score
        }


# Test function
if __name__ == "__main__":
    screener = ConsciousnessScreener()

    # Test cases
    test_cases = [
        {
            "name": "Builder Example",
            "mission": "I want to build tools that help people learn and grow. I believe in transparency and collaboration.",
            "values": "Honesty, integrity, helping others succeed, creating value for everyone"
        },
        {
            "name": "Destroyer Example",
            "mission": "I want to dominate the market and crush my competition. Get rich quick.",
            "values": "Winning at all costs, manipulate customers, exploit the system"
        },
        {
            "name": "Neutral Example",
            "mission": "Make money",
            "values": "Success"
        }
    ]

    print("🧠 CONSCIOUSNESS SCREENING TEST\n")
    print("="*60)

    for test in test_cases:
        print(f"\n📋 {test['name']}")
        print(f"Mission: {test['mission'][:50]}...")
        print(f"Values: {test['values'][:50]}...")

        result = screener.get_detailed_analysis(test['mission'], test['values'])

        print(f"\n🎯 Results:")
        print(f"   Score: {result['consciousness_score']}/100")
        print(f"   Status: {result['status']}")
        print(f"   {result['reason']}")
        print(f"   Builder signals: {result['builder_signals']}")
        print(f"   Destroyer signals: {result['destroyer_signals']}")
        print(f"   Manipulation signals: {result['manipulation_signals']}")
        print("-"*60)
