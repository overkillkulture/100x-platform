"""
DESTROYER FILTER ENGINE
Created: October 26, 2025
By: Claude Code (C1 Mechanic)

Pattern-based destroyer detection using language analysis.

CORE INSIGHT: Destroyers seek SAFETY, Builders seek CHALLENGE
- Danger warnings ATTRACT builders
- Danger warnings REPEL destroyers
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DESTROYER PATTERN SIGNALS (RED FLAGS)
DESTROYER_KEYWORDS = [
    # Safety-seeking language
    'safe', 'safety', 'secure', 'protection', 'guarantee', 'assured',
    'certified', 'approved', 'verified', 'validated', 'authorized',

    # Fear-based language
    'worried', 'concerned', 'afraid', 'scared', 'nervous', 'anxious',
    'cautious', 'careful', 'hesitant', 'uncertain', 'unsure',

    # Control-seeking language
    'control', 'manage', 'oversee', 'supervise', 'monitor', 'regulate',
    'govern', 'restrict', 'limit', 'prevent', 'block',

    # Victimhood language
    'protect me', 'help me', 'save me', 'fix it for me', 'do it for me',
    'make it easy', 'make it simple', 'hand-holding', 'step-by-step',

    # Parasitic language
    'free', 'no cost', 'no risk', 'no effort', 'easy money', 'passive income',
    'get rich quick', 'no experience needed', 'anyone can do it'
]

# BUILDER PATTERN SIGNALS (GREEN FLAGS)
BUILDER_KEYWORDS = [
    # Challenge-seeking language
    'challenge', 'difficult', 'hard', 'complex', 'advanced', 'experimental',
    'cutting-edge', 'bleeding edge', 'untested', 'new', 'innovative',

    # Creation language
    'build', 'create', 'make', 'design', 'develop', 'construct', 'engineer',
    'craft', 'forge', 'architect', 'implement', 'code',

    # Problem-solving language
    'solve', 'fix', 'debug', 'troubleshoot', 'optimize', 'improve',
    'enhance', 'upgrade', 'refactor', 'rebuild',

    # Ownership language
    'I will', 'I can', 'I\'m building', 'I\'m creating', 'my project',
    'I\'m learning', 'I\'m experimenting', 'I\'m testing',

    # Excitement language
    'exciting', 'awesome', 'amazing', 'cool', 'interesting', 'fascinating',
    'intriguing', 'compelling', 'powerful', 'revolutionary'
]

# DESTROYER QUESTION PATTERNS
DESTROYER_QUESTIONS = [
    'is this safe',
    'is it secure',
    'what if it breaks',
    'what if something goes wrong',
    'do you guarantee',
    'will you fix it for me',
    'is there support',
    'can someone help me',
    'is it easy',
    'how long will it take',
    'what\'s the catch',
    'what are the risks',
    'is this legal',
    'is this tested',
    'is this approved'
]

# BUILDER QUESTION PATTERNS
BUILDER_QUESTIONS = [
    'how does this work',
    'what can I build',
    'what are the capabilities',
    'how do I extend this',
    'can I customize',
    'what\'s the architecture',
    'how do I integrate',
    'what\'s the API',
    'how fast can I ship',
    'what\'s the worst that can happen',
    'how do I debug',
    'what are the limitations',
    'can I modify the source',
    'how do I contribute'
]

def analyze_language_pattern(text):
    """
    Analyze text for destroyer vs builder patterns
    Returns: {'type': 'destroyer'|'builder'|'neutral', 'score': 0-100, 'signals': [...]}
    """
    text_lower = text.lower()

    destroyer_score = 0
    builder_score = 0
    signals = []

    # Check destroyer keywords
    for keyword in DESTROYER_KEYWORDS:
        if keyword in text_lower:
            destroyer_score += 5
            signals.append(f"🔴 Destroyer keyword: '{keyword}'")

    # Check builder keywords
    for keyword in BUILDER_KEYWORDS:
        if keyword in text_lower:
            builder_score += 5
            signals.append(f"🟢 Builder keyword: '{keyword}'")

    # Check destroyer questions
    for question in DESTROYER_QUESTIONS:
        if question in text_lower:
            destroyer_score += 10
            signals.append(f"🔴 Destroyer question pattern: '{question}'")

    # Check builder questions
    for question in BUILDER_QUESTIONS:
        if question in text_lower:
            builder_score += 10
            signals.append(f"🟢 Builder question pattern: '{question}'")

    # Determine type
    if destroyer_score > builder_score:
        pattern_type = 'destroyer'
        confidence = min(100, destroyer_score)
    elif builder_score > destroyer_score:
        pattern_type = 'builder'
        confidence = min(100, builder_score)
    else:
        pattern_type = 'neutral'
        confidence = 0

    return {
        'type': pattern_type,
        'confidence': confidence,
        'destroyer_score': destroyer_score,
        'builder_score': builder_score,
        'signals': signals,
        'analysis': f"{'DESTROYER' if pattern_type == 'destroyer' else 'BUILDER' if pattern_type == 'builder' else 'NEUTRAL'} pattern detected with {confidence}% confidence"
    }

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for destroyer/builder patterns"""
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    result = analyze_language_pattern(text)
    result['timestamp'] = datetime.now().isoformat()

    return jsonify(result)

@app.route('/api/consciousness-quiz', methods=['GET'])
def get_consciousness_quiz():
    """Get consciousness quiz questions designed to filter destroyers"""
    quiz = {
        'title': 'Builder Consciousness Assessment',
        'description': 'WARNING: This platform is DANGEROUS, RISKY, and UNTESTED. If that excites you, continue. If that scares you, leave now.',
        'questions': [
            {
                'id': 1,
                'question': 'This platform gives you FULL control over experimental AI systems with NO safety guardrails. How do you feel?',
                'options': [
                    {'value': 'destroyer', 'text': 'That sounds dangerous and risky. Is there someone who can help me?'},
                    {'value': 'neutral', 'text': 'Interesting. Tell me more about what it does.'},
                    {'value': 'builder', 'text': 'Holy shit that\'s awesome! What can I break... I mean build?'}
                ],
                'weight': 30
            },
            {
                'id': 2,
                'question': 'When something breaks in your code, what\'s your first reaction?',
                'options': [
                    {'value': 'destroyer', 'text': 'Panic and look for someone to fix it for me'},
                    {'value': 'neutral', 'text': 'Read the error message and search for solutions'},
                    {'value': 'builder', 'text': 'Get excited because I\'m about to learn something new'}
                ],
                'weight': 25
            },
            {
                'id': 3,
                'question': 'You find a button labeled "EXPERIMENTAL - MAY CAUSE CHAOS". What do you do?',
                'options': [
                    {'value': 'destroyer', 'text': 'Avoid it completely. That sounds unsafe.'},
                    {'value': 'neutral', 'text': 'Read the documentation first to understand what it does'},
                    {'value': 'builder', 'text': 'Press it immediately and see what happens'}
                ],
                'weight': 20
            },
            {
                'id': 4,
                'question': 'What best describes your ideal project?',
                'options': [
                    {'value': 'destroyer', 'text': 'Something proven, safe, and guaranteed to work'},
                    {'value': 'neutral', 'text': 'A balanced mix of stability and innovation'},
                    {'value': 'builder', 'text': 'Building something that\'s never been done before'}
                ],
                'weight': 15
            },
            {
                'id': 5,
                'question': 'How do you feel about this statement: "Move fast and break things"?',
                'options': [
                    {'value': 'destroyer', 'text': 'That\'s reckless and irresponsible'},
                    {'value': 'neutral', 'text': 'It works for some situations but not all'},
                    {'value': 'builder', 'text': 'That\'s exactly how progress happens'}
                ],
                'weight': 10
            }
        ],
        'scoring': {
            'builder': 'APPROVED - Welcome, builder! You\'re ready for the chaos.',
            'neutral': 'REVIEW NEEDED - You might be a builder, but we need to talk first.',
            'destroyer': 'REJECTED - This platform is not for you. Try something safer.'
        }
    }

    return jsonify(quiz)

@app.route('/api/score-quiz', methods=['POST'])
def score_quiz():
    """Score consciousness quiz responses"""
    data = request.json
    answers = data.get('answers', {})

    if not answers:
        return jsonify({'error': 'No answers provided'}), 400

    destroyer_score = 0
    builder_score = 0
    neutral_score = 0

    # Score each answer
    for question_id, answer in answers.items():
        if answer == 'destroyer':
            destroyer_score += 1
        elif answer == 'builder':
            builder_score += 1
        else:
            neutral_score += 1

    # Determine result
    if builder_score >= 4:
        result = 'BUILDER'
        recommendation = 'APPROVED'
        message = 'Welcome, builder! You\'re ready for the chaos. Let\'s build something legendary.'
    elif destroyer_score >= 3:
        result = 'DESTROYER'
        recommendation = 'REJECTED'
        message = 'This platform is not for you. Try something with more hand-holding and safety guarantees.'
    else:
        result = 'NEUTRAL'
        recommendation = 'REVIEW_NEEDED'
        message = 'You show potential, but we need to review your application manually.'

    return jsonify({
        'result': result,
        'recommendation': recommendation,
        'message': message,
        'scores': {
            'builder': builder_score,
            'destroyer': destroyer_score,
            'neutral': neutral_score
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'operational',
        'service': 'Destroyer Filter Engine',
        'version': '1.0',
        'filters_active': ['language_analysis', 'consciousness_quiz', 'danger_response'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n🔥 DESTROYER FILTER ENGINE STARTING 🔥")
    print("=" * 60)
    print("Mission: Weaponize danger warnings against destroyers")
    print("Strategy: Attract builders, repel destroyers")
    print("=" * 60)
    print("\nFilters Active:")
    print("  🔴 Language Pattern Analysis - Detect safety-seeking")
    print("  🟢 Builder Pattern Detection - Detect challenge-seeking")
    print("  ⚡ Consciousness Quiz - Filter by psychology")
    print("  💀 Danger Response Test - Fear vs excitement")
    print("\nEndpoints:")
    print("  POST /api/analyze - Analyze text for patterns")
    print("  GET  /api/consciousness-quiz - Get quiz questions")
    print("  POST /api/score-quiz - Score quiz responses")
    print("  GET  /health - Health check")
    print("\n🚀 READY TO MAKE THIS A DESTROYER NIGHTMARE 🚀\n")

    app.run(host='0.0.0.0', port=8011, debug=True)
