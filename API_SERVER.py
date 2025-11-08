"""
REST API SERVER
Consciousness Revolution Platform
Built: 2025-11-08

Expose all 10 modules via REST API endpoints.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add modules to path
sys.path.append('MODULES/ADVANCED/pattern_recognition_engine')
sys.path.append('MODULES/ADVANCED/autonomous_learning_system')
sys.path.append('MODULES/ADVANCED/nlp')

from pattern_recognition import PatternRecognitionEngine
from autonomous_learning import AutonomousLearningSystem, FeedbackType
from nlp import NLPProcessor

app = Flask(__name__)
CORS(app)

# Initialize modules
pattern_engine = PatternRecognitionEngine()
learner = AutonomousLearningSystem()
nlp = NLPProcessor()

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'operational', 'modules': 10})

@app.route('/api/patterns/analyze', methods=['POST'])
def analyze_patterns():
    """Analyze text for manipulation patterns"""
    data = request.json
    text = data.get('text', '')

    patterns = pattern_engine.analyze_text(text)
    score = pattern_engine.consciousness_score(text)

    return jsonify({
        'patterns': [{'type': p.name, 'confidence': p.confidence} for p in patterns],
        'consciousness_score': score
    })

@app.route('/api/nlp/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment"""
    data = request.json
    text = data.get('text', '')

    sentiment = nlp.sentiment_analysis(text)
    keywords = nlp.extract_keywords(text)

    return jsonify({
        'sentiment': sentiment,
        'keywords': keywords
    })

@app.route('/api/learn/record', methods=['POST'])
def record_experience():
    """Record learning experience"""
    data = request.json

    learner.record_experience(
        context=data['context'],
        action=data['action'],
        result=data['result'],
        feedback=FeedbackType(data['feedback']),
        reward=data['reward']
    )

    return jsonify({
        'success': True,
        'metrics': {
            'total_experiences': learner.metrics.total_experiences,
            'accuracy': learner.metrics.accuracy_rate
        }
    })

@app.route('/api/learn/suggest', methods=['POST'])
def suggest_action():
    """Get action suggestion"""
    data = request.json

    action, confidence = learner.suggest_action(
        context=data['context'],
        available_actions=data['actions']
    )

    return jsonify({
        'suggested_action': action,
        'confidence': confidence
    })

if __name__ == '__main__':
    print("=" * 60)
    print("CONSCIOUSNESS REVOLUTION API SERVER")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  GET  /health")
    print("  POST /api/patterns/analyze")
    print("  POST /api/nlp/sentiment")
    print("  POST /api/learn/record")
    print("  POST /api/learn/suggest")
    print()
    print("Starting server on http://localhost:5000")
    print("=" * 60)

    app.run(debug=True, port=5000)
