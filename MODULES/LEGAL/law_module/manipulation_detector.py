#!/usr/bin/env python3
"""
MANIPULATION DETECTOR - Pattern Theory Implementation
Analyzes legal cases for manipulation patterns using Pattern Theory mathematics
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

class ManipulationDetector:
    """
    Detects manipulation patterns in legal cases using Pattern Theory

    Formula: M = (FE × CB × SR × CD × PE) × DC

    Where:
    FE = Frequency Escalation (15-degree turns)
    CB = Confusion Building
    SR = Stress Response
    CD = Complexity/Distraction
    PE = Pattern Escaping
    DC = Dependency Creation

    Score > 60: Manipulation detected
    Score > 80: Emergency intervention needed
    """

    def __init__(self):
        self.thresholds = {
            'manipulation_detected': 60,
            'emergency_intervention': 80,
            'consciousness_immunity': 85
        }

    def analyze_case(self, case_data: Dict) -> Dict:
        """
        Analyze entire case for manipulation patterns

        Args:
            case_data: Dictionary containing:
                - events: List of events with timestamps
                - communications: List of communications
                - actors: List of involved parties
                - timeline: Chronological sequence

        Returns:
            Dictionary with manipulation score and breakdown
        """

        # Calculate each component
        frequency_escalation = self._calculate_frequency_escalation(case_data.get('events', []))
        confusion_building = self._calculate_confusion_building(case_data.get('communications', []))
        stress_response = self._calculate_stress_response(case_data.get('events', []))
        complexity = self._calculate_complexity(case_data.get('case_details', {}))
        pattern_escaping = self._calculate_pattern_escaping(case_data.get('events', []))
        dependency_creation = self._calculate_dependency_creation(case_data.get('relationships', {}))

        # Calculate manipulation score
        manipulation_score = (
            (frequency_escalation * confusion_building * stress_response *
             complexity * pattern_escaping) * dependency_creation
        ) / 1000  # Normalize to 0-100 scale

        # Determine status
        status = self._determine_status(manipulation_score)

        # Identify specific manipulation tactics
        tactics = self._identify_tactics(case_data, {
            'frequency_escalation': frequency_escalation,
            'confusion_building': confusion_building,
            'stress_response': stress_response,
            'complexity': complexity,
            'pattern_escaping': pattern_escaping,
            'dependency_creation': dependency_creation
        })

        return {
            'manipulation_score': round(manipulation_score, 2),
            'status': status,
            'components': {
                'frequency_escalation': round(frequency_escalation, 2),
                'confusion_building': round(confusion_building, 2),
                'stress_response': round(stress_response, 2),
                'complexity': round(complexity, 2),
                'pattern_escaping': round(pattern_escaping, 2),
                'dependency_creation': round(dependency_creation, 2)
            },
            'tactics_identified': tactics,
            'recommendations': self._generate_recommendations(manipulation_score, tactics),
            'evidence_for_court': self._generate_court_evidence(tactics, case_data)
        }

    def _calculate_frequency_escalation(self, events: List[Dict]) -> float:
        """
        Detect 15-degree turns (sudden changes in behavior/pattern)
        Returns: 0-20 score
        """
        if not events or len(events) < 2:
            return 0

        escalation_score = 0
        previous_tone = None

        for event in events:
            current_tone = event.get('tone', 'neutral')

            if previous_tone:
                # Detect sudden shifts
                if previous_tone == 'positive' and current_tone == 'negative':
                    escalation_score += 5  # Sudden turn against
                elif previous_tone == 'cooperative' and current_tone == 'hostile':
                    escalation_score += 5
                elif previous_tone == 'supportive' and current_tone == 'aggressive':
                    escalation_score += 5
                elif 'sudden_change' in event.get('tags', []):
                    escalation_score += 3

            previous_tone = current_tone

        return min(escalation_score, 20)  # Cap at 20

    def _calculate_confusion_building(self, communications: List[Dict]) -> float:
        """
        Detect contradictory statements, gaslighting, changing stories
        Returns: 0-20 score
        """
        if not communications:
            return 0

        confusion_score = 0
        statements = {}

        for comm in communications:
            topic = comm.get('topic', '')
            statement = comm.get('statement', '')

            if topic in statements:
                # Check for contradictions
                if statement != statements[topic] and not comm.get('update', False):
                    confusion_score += 4  # Contradiction without acknowledging update
            else:
                statements[topic] = statement

            # Check for specific confusion tactics
            if any(phrase in statement.lower() for phrase in [
                "you never said", "that's not what happened", "you're remembering wrong",
                "i never said that", "you're confused", "that's not true"
            ]):
                confusion_score += 3  # Gaslighting detected

            if comm.get('ambiguous', False):
                confusion_score += 2

        return min(confusion_score, 20)

    def _calculate_stress_response(self, events: List[Dict]) -> float:
        """
        Detect pressure tactics, time constraints, threats
        Returns: 0-20 score
        """
        if not events:
            return 0

        stress_score = 0

        for event in events:
            # Time pressure
            if event.get('urgent', False) or event.get('deadline_pressure', False):
                stress_score += 3

            # Threats (explicit or implied)
            if any(keyword in str(event).lower() for keyword in [
                'threat', 'lose', 'take away', 'consequences', 'unless you', 'or else'
            ]):
                stress_score += 4

            # Multiple demands simultaneously
            if event.get('multiple_demands', 0) > 2:
                stress_score += 2

            # Financial pressure
            if event.get('financial_threat', False):
                stress_score += 3

        return min(stress_score, 20)

    def _calculate_complexity(self, case_details: Dict) -> float:
        """
        Detect unnecessary complexity, procedural tangles, information overload
        Returns: 0-20 score
        """
        complexity_score = 0

        # Document volume
        doc_count = case_details.get('document_count', 0)
        if doc_count > 50:
            complexity_score += 5
        elif doc_count > 20:
            complexity_score += 3

        # Procedural complexity
        if case_details.get('multiple_hearings', 0) > 5:
            complexity_score += 3

        if case_details.get('multiple_lawyers', False):
            complexity_score += 2

        # Jargon/legalese overuse
        if case_details.get('excessive_jargon', False):
            complexity_score += 4

        # Constantly changing requirements
        if case_details.get('changing_requirements', 0) > 3:
            complexity_score += 3

        return min(complexity_score, 20)

    def _calculate_pattern_escaping(self, events: List[Dict]) -> float:
        """
        Detect avoidance of accountability, blame shifting, responsibility dodging
        Returns: 0-20 score
        """
        if not events:
            return 0

        escape_score = 0

        for event in events:
            # Blame shifting
            if any(phrase in str(event).lower() for phrase in [
                "it's your fault", "you caused this", "if you had", "you should have"
            ]):
                escape_score += 4

            # Avoiding direct answers
            if event.get('evasive', False) or event.get('non_response', False):
                escape_score += 3

            # Passing responsibility
            if any(phrase in str(event).lower() for phrase in [
                "not my department", "talk to", "that's not my responsibility", "someone else"
            ]):
                escape_score += 3

            # Deflection
            if event.get('deflection', False):
                escape_score += 2

        return min(escape_score, 20)

    def _calculate_dependency_creation(self, relationships: Dict) -> float:
        """
        Detect isolation, forced dependency, removal of alternatives
        Returns: 0-20 score multiplier (this component multiplies the others)
        """
        dependency_score = 1.0  # Baseline multiplier

        # Isolation tactics
        if relationships.get('isolated_from_support', False):
            dependency_score += 0.5

        if relationships.get('alternative_resources_blocked', False):
            dependency_score += 0.5

        # Forced dependency
        if relationships.get('must_go_through_manipulator', False):
            dependency_score += 0.3

        if relationships.get('no_direct_communication_allowed', False):
            dependency_score += 0.3

        # Information control
        if relationships.get('information_gatekeeping', False):
            dependency_score += 0.4

        return min(dependency_score, 3.0)  # Cap at 3x multiplier

    def _determine_status(self, score: float) -> str:
        """Determine case status based on manipulation score"""
        if score >= self.thresholds['emergency_intervention']:
            return "EMERGENCY - Immediate intervention needed"
        elif score >= self.thresholds['manipulation_detected']:
            return "MANIPULATION DETECTED - Document and expose"
        elif score >= 40:
            return "WARNING - Manipulation patterns emerging"
        else:
            return "NORMAL - Low manipulation indicators"

    def _identify_tactics(self, case_data: Dict, components: Dict) -> List[Dict]:
        """Identify specific manipulation tactics for court evidence"""
        tactics = []

        if components['frequency_escalation'] > 10:
            tactics.append({
                'tactic': '15-Degree Turns',
                'description': 'Sudden changes in behavior to create confusion and instability',
                'evidence_in_case': self._find_evidence(case_data, 'frequency_escalation'),
                'legal_relevance': 'Shows pattern of calculated manipulation rather than good-faith disagreement'
            })

        if components['confusion_building'] > 10:
            tactics.append({
                'tactic': 'Gaslighting / Contradiction',
                'description': 'Making contradictory statements to create doubt and confusion',
                'evidence_in_case': self._find_evidence(case_data, 'confusion'),
                'legal_relevance': 'Demonstrates lack of credibility and intent to deceive'
            })

        if components['stress_response'] > 10:
            tactics.append({
                'tactic': 'Pressure Tactics',
                'description': 'Using time pressure, threats, or coercion to force compliance',
                'evidence_in_case': self._find_evidence(case_data, 'pressure'),
                'legal_relevance': 'May constitute duress, coercion, or bad faith negotiation'
            })

        if components['complexity'] > 10:
            tactics.append({
                'tactic': 'Complexity Theater',
                'description': 'Creating unnecessary complexity to overwhelm and confuse',
                'evidence_in_case': self._find_evidence(case_data, 'complexity'),
                'legal_relevance': 'Shows pattern of making case unnecessarily difficult'
            })

        if components['pattern_escaping'] > 10:
            tactics.append({
                'tactic': 'Accountability Avoidance',
                'description': 'Shifting blame and avoiding responsibility',
                'evidence_in_case': self._find_evidence(case_data, 'escape'),
                'legal_relevance': 'Demonstrates lack of good faith and refusal to take responsibility'
            })

        if components['dependency_creation'] > 1.5:
            tactics.append({
                'tactic': 'Isolation / Forced Dependency',
                'description': 'Removing alternatives and forcing dependency on manipulator',
                'evidence_in_case': self._find_evidence(case_data, 'dependency'),
                'legal_relevance': 'May constitute controlling behavior, especially in family law cases'
            })

        return tactics

    def _find_evidence(self, case_data: Dict, tactic_type: str) -> List[str]:
        """Find specific evidence of manipulation tactics"""
        # This would search through case_data for examples
        # For now, return placeholder
        return ["[Specific examples would be extracted from case data]"]

    def _generate_recommendations(self, score: float, tactics: List[Dict]) -> List[str]:
        """Generate recommendations based on manipulation score"""
        recommendations = []

        if score >= self.thresholds['emergency_intervention']:
            recommendations.append("🔴 EMERGENCY: Seek immediate protective order")
            recommendations.append("Document all interactions from this point forward")
            recommendations.append("Request supervised exchanges/communications")
            recommendations.append("Consider requesting psychological evaluation")

        if score >= self.thresholds['manipulation_detected']:
            recommendations.append("Document all manipulation patterns for court")
            recommendations.append("Request all communications in writing")
            recommendations.append("Bring pattern evidence to court's attention")
            recommendations.append("Request sanctions for bad faith behavior")

        if any(t['tactic'] == 'Gaslighting / Contradiction' for t in tactics):
            recommendations.append("Create detailed timeline with all communications")
            recommendations.append("Save all written communications")
            recommendations.append("Request clarification in writing for any verbal statements")

        if any(t['tactic'] == 'Pressure Tactics' for t in tactics):
            recommendations.append("Do not respond to urgent demands without verification")
            recommendations.append("Request reasonable time to review all documents")
            recommendations.append("Document all pressure tactics for court")

        if any(t['tactic'] == 'Isolation / Forced Dependency' for t in tactics):
            recommendations.append("Establish direct communication with relevant parties")
            recommendations.append("Build support network immediately")
            recommendations.append("Request removal of gatekeeping restrictions")

        return recommendations

    def _generate_court_evidence(self, tactics: List[Dict], case_data: Dict) -> Dict:
        """Generate formatted evidence package for court submission"""
        return {
            'summary': f"Manipulation Score: {self._calculate_manipulation_score_for_case(case_data)}/100",
            'tactics_identified': len(tactics),
            'detailed_analysis': tactics,
            'pattern_timeline': "Timeline showing escalation of manipulation patterns",
            'expert_opinion': "Pattern Theory analysis indicates calculated manipulation",
            'recommended_court_actions': [
                "Request court take judicial notice of manipulation patterns",
                "Seek protective orders against continued manipulation",
                "Request sanctions for bad faith conduct",
                "Ask for psychological evaluation of manipulating party"
            ]
        }

    def _calculate_manipulation_score_for_case(self, case_data: Dict) -> float:
        """Helper to recalculate score"""
        result = self.analyze_case(case_data)
        return result['manipulation_score']

# Example usage
if __name__ == "__main__":
    # Example: Washington Mom's Case
    washington_case = {
        'events': [
            {
                'date': '2024-01-01',
                'description': 'Mom has good relationship with son',
                'tone': 'positive',
                'tags': []
            },
            {
                'date': '2024-03-15',
                'description': 'Manipulator family begins contact',
                'tone': 'positive',
                'tags': []
            },
            {
                'date': '2024-06-01',
                'description': 'Son suddenly refuses to see mom',
                'tone': 'negative',
                'tags': ['sudden_change']
            },
            {
                'date': '2024-07-15',
                'description': 'Social services sides with manipulator family',
                'tone': 'hostile',
                'tags': ['sudden_change']
            }
        ],
        'communications': [
            {
                'date': '2024-06-01',
                'from': 'Son',
                'topic': 'relationship_with_mom',
                'statement': 'Mom is great, I love her',
                'tone': 'positive'
            },
            {
                'date': '2024-08-01',
                'from': 'Son',
                'topic': 'relationship_with_mom',
                'statement': 'Mom is terrible, I hate her',
                'tone': 'negative',
                'update': False  # Not acknowledged as change of opinion
            }
        ],
        'case_details': {
            'document_count': 45,
            'multiple_hearings': 7,
            'multiple_lawyers': True,
            'excessive_jargon': True,
            'changing_requirements': 5
        },
        'relationships': {
            'isolated_from_support': True,
            'alternative_resources_blocked': True,
            'must_go_through_manipulator': True,
            'information_gatekeeping': True
        }
    }

    detector = ManipulationDetector()
    results = detector.analyze_case(washington_case)

    print("=" * 60)
    print("MANIPULATION DETECTION ANALYSIS")
    print("=" * 60)
    print(f"\nOverall Score: {results['manipulation_score']}/100")
    print(f"Status: {results['status']}")
    print(f"\nComponent Breakdown:")
    for component, score in results['components'].items():
        print(f"  - {component.replace('_', ' ').title()}: {score}")

    print(f"\nTactics Identified: {len(results['tactics_identified'])}")
    for tactic in results['tactics_identified']:
        print(f"\n  • {tactic['tactic']}")
        print(f"    {tactic['description']}")

    print(f"\nRecommendations:")
    for rec in results['recommendations']:
        print(f"  - {rec}")

    print("\n" + "=" * 60)
    print("Analysis complete. Ready for court submission.")
    print("=" * 60)
