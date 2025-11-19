#!/usr/bin/env python3
"""
⚡ BUSINESS PHASE TRANSITION DETECTOR ⚡
Consciousness Revolution - Predictive Analytics

MISSION: Watch business metrics and PREDICT phase transitions BEFORE they happen
- Analyzes revenue, team size, workload, patterns
- Detects when you're about to shift phases
- Recommends what to prepare for NEXT

The genius: It doesn't just track where you ARE, it predicts where you're GOING
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from pathlib import Path


class PhaseTransitionDetector:
    """Predicts business phase transitions using pattern recognition"""

    def __init__(self):
        self.phases = [
            {
                'id': 'get-work',
                'name': 'Get Work',
                'indicators': {
                    'revenue_monthly': (0, 10000),
                    'team_size': (0, 2),
                    'client_count': (0, 5),
                    'workload_capacity': (0, 60)  # % utilized
                },
                'transition_signals': [
                    'Revenue consistently hitting target',
                    'More work than you can handle',
                    'Turning down clients',
                    'Working 60+ hours/week'
                ]
            },
            {
                'id': 'get-employees',
                'name': 'Get Employees',
                'indicators': {
                    'revenue_monthly': (10000, 50000),
                    'team_size': (1, 5),
                    'client_count': (5, 20),
                    'workload_capacity': (60, 95)
                },
                'transition_signals': [
                    'Team is hired and onboarded',
                    'Operations running smoothly',
                    'Growth is limited by capital',
                    'Ready to scale but need funding'
                ]
            },
            {
                'id': 'get-money',
                'name': 'Get Money',
                'indicators': {
                    'revenue_monthly': (20000, 100000),
                    'team_size': (3, 15),
                    'client_count': (10, 50),
                    'burn_rate': (5000, 50000)
                },
                'transition_signals': [
                    'Funding secured',
                    'Cash flow stabilized',
                    'Ready to invest in growth',
                    'Clear expansion opportunities'
                ]
            },
            {
                'id': 'expand',
                'name': 'Expand',
                'indicators': {
                    'revenue_monthly': (50000, 500000),
                    'team_size': (10, 50),
                    'client_count': (25, 200),
                    'market_presence': (50, 90)  # % of target market
                },
                'transition_signals': [
                    'Expanded into new markets',
                    'Operations scaled successfully',
                    'Team growing rapidly',
                    'Need consistency and training'
                ]
            },
            {
                'id': 'train',
                'name': 'Train',
                'indicators': {
                    'revenue_monthly': (100000, 1000000),
                    'team_size': (20, 100),
                    'process_documentation': (50, 90),  # % documented
                    'employee_turnover': (5, 20)  # % annual
                },
                'transition_signals': [
                    'Team is well-trained',
                    'Systems are documented',
                    'Operations mature',
                    'Ready for strategic planning'
                ]
            },
            {
                'id': 'future-mission',
                'name': 'Future Mission',
                'indicators': {
                    'revenue_monthly': (500000, float('inf')),
                    'team_size': (50, float('inf')),
                    'market_position': (70, 100),  # Leadership position
                    'innovation_index': (60, 100)  # % of revenue in R&D
                },
                'transition_signals': [
                    'Vision for next 5-10 years clear',
                    'Market leadership established',
                    'Looking for new challenges',
                    'Ready to restart cycle with new venture'
                ]
            }
        ]

    def detect_current_phase(self, metrics: Dict) -> Tuple[str, float]:
        """
        Detect current business phase based on metrics
        Returns: (phase_id, confidence_score)
        """
        scores = []

        for phase in self.phases:
            confidence = self._calculate_phase_confidence(phase, metrics)
            scores.append({
                'phase_id': phase['id'],
                'phase_name': phase['name'],
                'confidence': confidence
            })

        # Sort by confidence
        scores.sort(key=lambda x: x['confidence'], reverse=True)

        best_match = scores[0]
        return best_match['phase_id'], best_match['confidence']

    def _calculate_phase_confidence(self, phase: Dict, metrics: Dict) -> float:
        """Calculate how well current metrics match a phase"""
        matches = 0
        total = 0

        for indicator, (min_val, max_val) in phase['indicators'].items():
            if indicator in metrics:
                value = metrics[indicator]
                total += 1

                # Check if value is in range
                if min_val <= value <= max_val:
                    matches += 1
                    # Bonus for being in middle of range
                    mid_point = (min_val + max_val) / 2
                    if abs(value - mid_point) / (max_val - min_val) < 0.3:
                        matches += 0.5

        if total == 0:
            return 0.0

        return (matches / total) * 100

    def predict_transition(self, metrics: Dict, historical_data: List[Dict]) -> Dict:
        """
        Predict upcoming phase transition
        Returns: {
            'current_phase': str,
            'next_phase': str,
            'transition_probability': float (0-100),
            'estimated_days': int,
            'preparation_needed': List[str]
        }
        """
        current_phase_id, confidence = self.detect_current_phase(metrics)

        # Find current phase index
        current_index = next(i for i, p in enumerate(self.phases) if p['id'] == current_phase_id)
        next_index = (current_index + 1) % len(self.phases)
        next_phase = self.phases[next_index]

        # Calculate transition probability based on:
        # 1. How close metrics are to next phase
        # 2. Velocity of metric changes
        # 3. Historical pattern

        transition_prob = self._calculate_transition_probability(
            metrics,
            self.phases[current_index],
            next_phase,
            historical_data
        )

        # Estimate days to transition
        estimated_days = self._estimate_transition_days(
            transition_prob,
            historical_data
        )

        return {
            'current_phase': self.phases[current_index]['name'],
            'current_phase_id': current_phase_id,
            'confidence': confidence,
            'next_phase': next_phase['name'],
            'next_phase_id': next_phase['id'],
            'transition_probability': transition_prob,
            'estimated_days': estimated_days,
            'transition_signals': next_phase['transition_signals'],
            'preparation_items': self._get_preparation_items(next_phase)
        }

    def _calculate_transition_probability(
        self,
        current_metrics: Dict,
        current_phase: Dict,
        next_phase: Dict,
        historical_data: List[Dict]
    ) -> float:
        """Calculate probability of transitioning to next phase"""

        # Check how many metrics are already in next phase range
        metrics_in_next_range = 0
        total_metrics = 0

        for indicator, (min_val, max_val) in next_phase['indicators'].items():
            if indicator in current_metrics:
                total_metrics += 1
                value = current_metrics[indicator]
                if min_val <= value <= max_val:
                    metrics_in_next_range += 1

        if total_metrics == 0:
            return 0.0

        # Base probability on metric overlap
        base_prob = (metrics_in_next_range / total_metrics) * 100

        # Adjust for velocity (are metrics trending toward next phase?)
        if len(historical_data) >= 2:
            velocity_factor = self._calculate_velocity_factor(
                historical_data,
                next_phase['indicators']
            )
            base_prob = base_prob * velocity_factor

        return min(100, base_prob)

    def _calculate_velocity_factor(
        self,
        historical_data: List[Dict],
        target_indicators: Dict
    ) -> float:
        """Calculate if metrics are trending toward target"""
        if len(historical_data) < 2:
            return 1.0

        recent = historical_data[-1]
        previous = historical_data[-2]

        positive_trends = 0
        total_trends = 0

        for indicator in target_indicators.keys():
            if indicator in recent and indicator in previous:
                total_trends += 1
                if recent[indicator] > previous[indicator]:
                    positive_trends += 1

        if total_trends == 0:
            return 1.0

        # 1.0 = no change, 1.5 = all metrics trending up
        return 1.0 + (positive_trends / total_trends) * 0.5

    def _estimate_transition_days(
        self,
        transition_prob: float,
        historical_data: List[Dict]
    ) -> int:
        """Estimate days until transition"""
        if transition_prob >= 90:
            return 7  # Imminent
        elif transition_prob >= 70:
            return 21  # ~3 weeks
        elif transition_prob >= 50:
            return 45  # ~1.5 months
        elif transition_prob >= 30:
            return 90  # ~3 months
        else:
            return 180  # ~6 months

    def _get_preparation_items(self, next_phase: Dict) -> List[str]:
        """Get specific preparation items for next phase"""
        prep_map = {
            'get-employees': [
                'Draft job descriptions',
                'Set up hiring pipeline',
                'Prepare onboarding materials',
                'Calculate salary budget'
            ],
            'get-money': [
                'Create financial projections',
                'Build investor pitch deck',
                'Research funding sources',
                'Clean up financials'
            ],
            'expand': [
                'Identify growth markets',
                'Plan product extensions',
                'Build scaling infrastructure',
                'Develop partnerships'
            ],
            'train': [
                'Document all processes',
                'Create training curriculum',
                'Set up knowledge base',
                'Define career paths'
            ],
            'future-mission': [
                'Draft 5-year vision',
                'Analyze market trends',
                'Plan innovation projects',
                'Consider acquisition/exit'
            ],
            'get-work': [
                'Refine service offerings',
                'Build marketing assets',
                'Network actively',
                'Optimize pricing'
            ]
        }

        return prep_map.get(next_phase['id'], [])


def demo_prediction():
    """Demo the phase prediction system"""
    detector = PhaseTransitionDetector()

    # Example: Growing startup metrics
    current_metrics = {
        'revenue_monthly': 35000,  # In Get Employees range but trending up
        'team_size': 4,
        'client_count': 15,
        'workload_capacity': 85,  # High capacity utilization
        'burn_rate': 25000
    }

    # Historical data showing growth
    historical = [
        {
            'date': '2025-08-01',
            'revenue_monthly': 15000,
            'team_size': 2,
            'client_count': 8
        },
        {
            'date': '2025-09-01',
            'revenue_monthly': 25000,
            'team_size': 3,
            'client_count': 12
        },
        {
            'date': '2025-10-01',
            'revenue_monthly': 35000,
            'team_size': 4,
            'client_count': 15
        }
    ]

    print("⚡ BUSINESS PHASE TRANSITION DETECTOR ⚡")
    print("=" * 70)
    print("\n📊 CURRENT METRICS:")
    for key, value in current_metrics.items():
        print(f"  {key}: {value}")

    prediction = detector.predict_transition(current_metrics, historical)

    print("\n" + "=" * 70)
    print("🔮 PREDICTION RESULTS:")
    print("=" * 70)
    print(f"\n✅ Current Phase: {prediction['current_phase']}")
    print(f"   Confidence: {prediction['confidence']:.1f}%")
    print(f"\n⏭️  Next Phase: {prediction['next_phase']}")
    print(f"   Transition Probability: {prediction['transition_probability']:.1f}%")
    print(f"   Estimated Days: ~{prediction['estimated_days']} days")

    print(f"\n🎯 SIGNALS TO WATCH FOR:")
    for signal in prediction['transition_signals']:
        print(f"  • {signal}")

    print(f"\n📋 START PREPARING NOW:")
    for i, item in enumerate(prediction['preparation_items'], 1):
        print(f"  {i}. {item}")

    # Save prediction
    output = {
        'timestamp': datetime.now().isoformat(),
        'metrics': current_metrics,
        'prediction': prediction
    }

    output_path = Path('C:/Users/dwrek/100X_DEPLOYMENT/phase_prediction.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n💾 Prediction saved to: {output_path}")

    return detector, prediction


if __name__ == '__main__':
    detector, prediction = demo_prediction()
