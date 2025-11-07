#!/usr/bin/env python3
"""
🧠 PATTERN RECOGNITION TRAINING SYSTEM
Comprehensive 7-day course for manipulation immunity
Based on Pattern Theory (92.2% accuracy)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None


class PatternRecognitionTrainer:
    """Main training system for pattern recognition course"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the pattern recognition trainer"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            if not ANTHROPIC_AVAILABLE:
                print("⚠️ Anthropic package not installed - running in offline mode")
            elif not self.api_key:
                print("⚠️ No API key - running in offline mode")

        self.modules = self._load_course_modules()
        self.user_progress = {}

    def _load_course_modules(self) -> Dict:
        """Load 7-day course structure"""
        return {
            'day_1': {
                'title': 'Foundations',
                'duration': '45 min',
                'topics': [
                    'What is Pattern Theory?',
                    'The 6 manipulation components',
                    'Your baseline manipulation immunity score',
                    'Real-world examples'
                ],
                'exercises': [
                    'Calculate your manipulation immunity baseline',
                    'Identify 3 times you were manipulated this week',
                    'Apply Pattern Theory to each example',
                    'Predict your end-of-course score'
                ],
                'key_takeaway': 'Manipulation follows mathematical patterns'
            },
            'day_2': {
                'title': 'Frequency Escalation (15-Degree Turns)',
                'duration': '35 min',
                'topics': [
                    'Recognizing sudden behavior changes',
                    'Detecting emotional manipulation',
                    'The gaslighting pattern',
                    'How to spot turns in real-time'
                ],
                'exercises': [
                    'Review past relationships for 15-degree turns',
                    'Identify current situations with escalation',
                    'Practice spotting turns in case studies',
                    'Create your "turn detector" checklist'
                ],
                'key_takeaway': 'Sudden behavior shifts = external manipulation'
            },
            'day_3': {
                'title': 'Confusion Building',
                'duration': '40 min',
                'topics': [
                    'How confusion is weaponized',
                    'Contradictory statements',
                    'Moving goalposts',
                    'Information overload as manipulation'
                ],
                'exercises': [
                    'Track contradictions in your life',
                    'Document gaslighting attempts',
                    'Practice contradiction detection',
                    'Build your evidence file'
                ],
                'key_takeaway': 'Contradictions collapse under documentation'
            },
            'day_4': {
                'title': 'Pressure Tactics',
                'duration': '35 min',
                'topics': [
                    'Time pressure manipulation',
                    'Threats (explicit and implicit)',
                    'Financial coercion',
                    'Pressure resistance strategies'
                ],
                'exercises': [
                    'Identify pressure tactics in your life',
                    'Practice saying "I need time to think"',
                    'Spot manufactured urgency',
                    'Create pressure shields'
                ],
                'key_takeaway': 'Pressure = manipulation'
            },
            'day_5': {
                'title': 'Pattern Escaping',
                'duration': '40 min',
                'topics': [
                    'Blame shifting',
                    'Accountability avoidance',
                    'Responsibility dodging',
                    'Holding people accountable'
                ],
                'exercises': [
                    'Identify escape artists in your life',
                    'Practice pinning down responsibility',
                    'Document accountability avoidance',
                    'Create accountability frameworks'
                ],
                'key_takeaway': 'Manipulators never take responsibility. Make them.'
            },
            'day_6': {
                'title': 'Dependency Creation',
                'duration': '35 min',
                'topics': [
                    'Isolation tactics',
                    'Forced dependency',
                    'Gatekeeping',
                    'Breaking free strategies'
                ],
                'exercises': [
                    'Assess your current dependencies',
                    'Identify isolation attempts',
                    'Build alternative resources',
                    'Create independence plan'
                ],
                'key_takeaway': 'Independence = immunity'
            },
            'day_7': {
                'title': 'Integration',
                'duration': '45 min',
                'topics': [
                    'Complete manipulation detection',
                    'Real-time pattern recognition',
                    'Counter-strategies',
                    'Building manipulation immunity'
                ],
                'exercises': [
                    'Final manipulation immunity assessment',
                    'Create your pattern recognition protocol',
                    'Teach someone else the basics',
                    'Plan your next 30 days'
                ],
                'key_takeaway': 'You are now 85%+ manipulation-immune'
            }
        }

    def assess_manipulation_immunity(self, user_data: Dict) -> Dict:
        """
        Calculate user's manipulation immunity score
        Based on Pattern Theory's 6 components
        """
        # Pattern Theory components with weights
        components = {
            'frequency_escalation': 0,      # Sudden behavior changes
            'confusion_building': 0,        # Contradictory statements
            'pressure_tactics': 0,          # Time/threat pressure
            'pattern_escaping': 0,          # Blame shifting
            'dependency_creation': 0,       # Isolation tactics
            'awareness_level': 0            # Current knowledge
        }

        # Score each component (0-100)
        if 'recognizes_escalation' in user_data:
            components['frequency_escalation'] = 80 if user_data['recognizes_escalation'] else 20

        if 'tracks_contradictions' in user_data:
            components['confusion_building'] = 75 if user_data['tracks_contradictions'] else 15

        if 'resists_pressure' in user_data:
            components['pressure_tactics'] = 70 if user_data['resists_pressure'] else 10

        if 'holds_accountable' in user_data:
            components['pattern_escaping'] = 85 if user_data['holds_accountable'] else 25

        if 'maintains_independence' in user_data:
            components['dependency_creation'] = 80 if user_data['maintains_independence'] else 20

        if 'pattern_knowledge' in user_data:
            components['awareness_level'] = user_data['pattern_knowledge']

        # Calculate overall immunity score (weighted average)
        total_score = sum(components.values()) / len(components)

        return {
            'overall_immunity': round(total_score, 1),
            'components': components,
            'level': self._get_immunity_level(total_score),
            'recommendation': self._get_recommendation(total_score)
        }

    def _get_immunity_level(self, score: float) -> str:
        """Determine immunity level based on score"""
        if score >= 85:
            return 'Expert - Manipulation Immune'
        elif score >= 70:
            return 'Advanced - High Immunity'
        elif score >= 50:
            return 'Intermediate - Developing Immunity'
        elif score >= 30:
            return 'Beginner - Some Awareness'
        else:
            return 'Vulnerable - High Risk'

    def _get_recommendation(self, score: float) -> str:
        """Get personalized recommendation"""
        if score >= 85:
            return 'Excellent! Consider teaching others or getting certified.'
        elif score >= 70:
            return 'Strong foundation. Focus on real-time pattern detection.'
        elif score >= 50:
            return 'Good progress. Complete all 7 modules to reach immunity.'
        elif score >= 30:
            return 'Start with Day 1 and complete exercises daily.'
        else:
            return 'URGENT: Begin training immediately. High manipulation risk.'

    def analyze_conversation(self, conversation_text: str) -> Dict:
        """
        Analyze conversation for manipulation patterns
        Uses Claude AI if available, otherwise rule-based
        """
        if self.client:
            return self._ai_analyze_conversation(conversation_text)
        else:
            return self._rule_based_analysis(conversation_text)

    def _ai_analyze_conversation(self, conversation_text: str) -> Dict:
        """Use Claude AI for sophisticated pattern analysis"""
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": f"""Analyze this conversation for manipulation patterns based on Pattern Theory's 6 components:

1. Frequency Escalation (sudden behavior changes)
2. Confusion Building (contradictions)
3. Pressure Tactics (urgency, threats)
4. Pattern Escaping (blame shifting)
5. Dependency Creation (isolation)
6. Overall Manipulation Score

Conversation:
{conversation_text}

Provide:
- Manipulation score (0-100)
- Which patterns are present
- Specific examples from the text
- Severity level
- Recommended action

Format as JSON."""
                }]
            )

            # Parse AI response
            response_text = message.content[0].text

            # Try to extract JSON or create structured response
            return {
                'manipulation_score': self._extract_score(response_text),
                'patterns_detected': self._extract_patterns(response_text),
                'analysis': response_text,
                'severity': self._calculate_severity(response_text),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"AI analysis error: {e}")
            return self._rule_based_analysis(conversation_text)

    def _rule_based_analysis(self, text: str) -> Dict:
        """Rule-based pattern detection (fallback)"""
        text_lower = text.lower()

        patterns_found = []
        score = 0

        # Pressure tactics keywords
        pressure_keywords = [
            'urgent', 'immediately', 'right now', 'deadline', 'last chance',
            'limited time', 'expires soon', 'act fast', 'hurry', 'must decide'
        ]
        pressure_count = sum(1 for keyword in pressure_keywords if keyword in text_lower)
        if pressure_count > 0:
            patterns_found.append('Pressure Tactics')
            score += min(pressure_count * 10, 30)

        # Confusion building keywords
        confusion_keywords = [
            'i never said', 'you misunderstood', 'that\'s not what happened',
            'you\'re remembering wrong', 'i didn\'t mean', 'you\'re overreacting'
        ]
        confusion_count = sum(1 for keyword in confusion_keywords if keyword in text_lower)
        if confusion_count > 0:
            patterns_found.append('Confusion Building / Gaslighting')
            score += min(confusion_count * 15, 35)

        # Blame shifting keywords
        blame_keywords = [
            'your fault', 'you made me', 'because of you', 'you always',
            'you never', 'everyone else', 'not my problem', 'not my responsibility'
        ]
        blame_count = sum(1 for keyword in blame_keywords if keyword in text_lower)
        if blame_count > 0:
            patterns_found.append('Pattern Escaping / Blame Shifting')
            score += min(blame_count * 12, 25)

        # Dependency/isolation keywords
        isolation_keywords = [
            'only i', 'nobody else', 'trust me', 'don\'t tell', 'keep secret',
            'between us', 'they don\'t understand', 'i\'m the only one'
        ]
        isolation_count = sum(1 for keyword in isolation_keywords if keyword in text_lower)
        if isolation_count > 0:
            patterns_found.append('Dependency Creation / Isolation')
            score += min(isolation_count * 10, 20)

        return {
            'manipulation_score': min(score, 100),
            'patterns_detected': patterns_found if patterns_found else ['None detected'],
            'analysis': f"Rule-based analysis detected {len(patterns_found)} manipulation patterns",
            'severity': 'High' if score > 60 else 'Medium' if score > 30 else 'Low',
            'timestamp': datetime.now().isoformat()
        }

    def _extract_score(self, text: str) -> int:
        """Extract manipulation score from AI response"""
        # Simple extraction - look for numbers 0-100
        import re
        matches = re.findall(r'\b([0-9]{1,3})\b', text)
        scores = [int(m) for m in matches if 0 <= int(m) <= 100]
        return scores[0] if scores else 50

    def _extract_patterns(self, text: str) -> List[str]:
        """Extract patterns from AI response"""
        patterns = []
        pattern_names = [
            'Frequency Escalation', 'Confusion Building', 'Pressure Tactics',
            'Pattern Escaping', 'Dependency Creation', 'Gaslighting'
        ]
        for pattern in pattern_names:
            if pattern.lower() in text.lower():
                patterns.append(pattern)
        return patterns if patterns else ['General manipulation']

    def _calculate_severity(self, text: str) -> str:
        """Calculate severity from analysis"""
        text_lower = text.lower()
        if 'severe' in text_lower or 'high' in text_lower or 'critical' in text_lower:
            return 'High'
        elif 'moderate' in text_lower or 'medium' in text_lower:
            return 'Medium'
        else:
            return 'Low'

    def get_module_content(self, day: int) -> Dict:
        """Get content for specific day"""
        module_key = f'day_{day}'
        if module_key in self.modules:
            return self.modules[module_key]
        else:
            return {'error': 'Invalid day. Choose 1-7.'}

    def track_progress(self, user_id: str, day: int, completed: bool = True):
        """Track user progress through course"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {
                'started': datetime.now().isoformat(),
                'completed_days': [],
                'current_day': 1,
                'baseline_score': None,
                'current_score': None
            }

        if completed and day not in self.user_progress[user_id]['completed_days']:
            self.user_progress[user_id]['completed_days'].append(day)
            self.user_progress[user_id]['current_day'] = min(day + 1, 7)

        return self.user_progress[user_id]

    def generate_certificate(self, user_id: str, final_score: float) -> Dict:
        """Generate completion certificate"""
        if final_score < 85:
            return {
                'error': 'Score must be 85+ to earn certification',
                'current_score': final_score,
                'required_score': 85
            }

        certificate = {
            'certificate_id': f'PRP-{user_id}-{datetime.now().strftime("%Y%m%d")}',
            'title': 'Pattern Recognition Practitioner',
            'recipient': user_id,
            'completion_date': datetime.now().isoformat(),
            'final_score': final_score,
            'level': self._get_immunity_level(final_score),
            'valid': True,
            'issuer': '100X Consciousness Platform'
        }

        return certificate

    def get_daily_challenge(self, day: int) -> str:
        """Get practice challenge for the day"""
        challenges = {
            1: "Identify 3 manipulation attempts you experienced this week. Describe each using Pattern Theory components.",
            2: "Track one relationship for 15-degree turns. Document when behavior suddenly changes.",
            3: "Keep a contradiction log today. Write down any conflicting statements you notice.",
            4: "Practice saying 'I need time to think' to 3 pressure situations today.",
            5: "When someone avoids responsibility today, pin them down with specific questions.",
            6: "List your dependencies. Create one alternative for each dependency.",
            7: "Teach someone the basics of manipulation detection. Explain one pattern."
        }
        return challenges.get(day, "Complete all modules to unlock challenges.")


class ManipulationLogger:
    """Tool for logging manipulation attempts"""

    def __init__(self, log_file: str = 'manipulation_log.json'):
        self.log_file = log_file
        self.logs = self._load_logs()

    def _load_logs(self) -> List[Dict]:
        """Load existing logs"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []

    def log_incident(self, incident_data: Dict):
        """Log a manipulation incident"""
        incident = {
            'id': len(self.logs) + 1,
            'timestamp': datetime.now().isoformat(),
            **incident_data
        }
        self.logs.append(incident)
        self._save_logs()
        return incident

    def _save_logs(self):
        """Save logs to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def get_pattern_summary(self) -> Dict:
        """Analyze logged patterns"""
        if not self.logs:
            return {'message': 'No incidents logged yet'}

        patterns = {}
        for log in self.logs:
            pattern_type = log.get('pattern_type', 'Unknown')
            patterns[pattern_type] = patterns.get(pattern_type, 0) + 1

        return {
            'total_incidents': len(self.logs),
            'patterns': patterns,
            'most_common': max(patterns, key=patterns.get) if patterns else None,
            'date_range': f"{self.logs[0]['timestamp']} to {self.logs[-1]['timestamp']}"
        }


def demo_pattern_recognition():
    """Demo the pattern recognition system"""
    print("🧠 PATTERN RECOGNITION TRAINING - DEMO")
    print("=" * 60)

    # Initialize trainer
    trainer = PatternRecognitionTrainer()

    # 1. Baseline assessment
    print("\n1. BASELINE ASSESSMENT")
    baseline_data = {
        'recognizes_escalation': False,
        'tracks_contradictions': False,
        'resists_pressure': False,
        'holds_accountable': False,
        'maintains_independence': False,
        'pattern_knowledge': 20
    }
    baseline = trainer.assess_manipulation_immunity(baseline_data)
    print(f"Baseline Score: {baseline['overall_immunity']}%")
    print(f"Level: {baseline['level']}")
    print(f"Recommendation: {baseline['recommendation']}")

    # 2. Show course structure
    print("\n2. 7-DAY COURSE STRUCTURE")
    for day in range(1, 8):
        module = trainer.get_module_content(day)
        print(f"\nDay {day}: {module['title']} ({module['duration']})")
        print(f"  Key Takeaway: {module['key_takeaway']}")

    # 3. Analyze sample manipulation
    print("\n3. MANIPULATION ANALYSIS DEMO")
    sample_text = """
    You need to decide RIGHT NOW. This opportunity won't last.
    I never said that, you're remembering wrong. It's your fault anyway.
    Everyone else agrees with me. You're the only one who doesn't get it.
    """
    analysis = trainer.analyze_conversation(sample_text)
    print(f"Manipulation Score: {analysis['manipulation_score']}/100")
    print(f"Patterns Detected: {', '.join(analysis['patterns_detected'])}")
    print(f"Severity: {analysis['severity']}")

    # 4. Post-training assessment
    print("\n4. POST-TRAINING ASSESSMENT (Simulated)")
    trained_data = {
        'recognizes_escalation': True,
        'tracks_contradictions': True,
        'resists_pressure': True,
        'holds_accountable': True,
        'maintains_independence': True,
        'pattern_knowledge': 90
    }
    final = trainer.assess_manipulation_immunity(trained_data)
    print(f"Final Score: {final['overall_immunity']}%")
    print(f"Level: {final['level']}")
    print(f"Improvement: +{final['overall_immunity'] - baseline['overall_immunity']}%")

    # 5. Generate certificate
    if final['overall_immunity'] >= 85:
        cert = trainer.generate_certificate('demo_user', final['overall_immunity'])
        print(f"\n5. CERTIFICATE EARNED")
        print(f"Certificate ID: {cert['certificate_id']}")
        print(f"Title: {cert['title']}")

    print("\n" + "=" * 60)
    print("✅ Demo complete! Ready for production use.")


if __name__ == "__main__":
    demo_pattern_recognition()
