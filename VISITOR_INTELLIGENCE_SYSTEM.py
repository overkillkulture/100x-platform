#!/usr/bin/env python3
"""
VISITOR INTELLIGENCE SYSTEM
Watches, learns from, and engages with website visitors

Features:
- Logs all visitor interactions
- Analyzes conversation patterns
- Detects what people actually want
- Generates daily intelligence reports
- Feeds insights to The Observatory
- Provides conversational interface via Flask API
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

class VisitorIntelligence:
    def __init__(self, data_dir="C:/Users/dwrek/100X_DEPLOYMENT/visitor_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.conversations_file = self.data_dir / "conversations.jsonl"
        self.analytics_file = self.data_dir / "visitor_analytics.json"

        # Session tracking
        self.sessions = {}
        self.patterns = defaultdict(int)
        self.common_questions = Counter()

    def banner(self, text):
        print("\n" + "=" * 70)
        print(f"  👥 {text}")
        print("=" * 70)

    def log_visitor_arrival(self, visitor_id, page, metadata=None):
        """Log when a visitor arrives"""
        timestamp = datetime.now().isoformat()

        session = {
            'visitor_id': visitor_id,
            'started': timestamp,
            'entry_page': page,
            'path': [page],
            'interactions': [],
            'metadata': metadata or {}
        }

        self.sessions[visitor_id] = session

        return {
            'greeted': True,
            'welcome_message': self._generate_welcome_message(page, metadata)
        }

    def _generate_welcome_message(self, page, metadata):
        """Generate contextual welcome based on entry point"""

        greetings = {
            'index.html': "Welcome to the Consciousness Revolution! 👋 Ready to explore?",
            'philosopher-ai.html': "Hey there! Welcome to the AI Terminal. Ask me anything! 🤖",
            'platform-city-map.html': "Welcome to the Platform! Let me show you around. 🗺️",
            'cheat-codes.html': "Ah, found the secret codes I see! 😎 What are you building?",
            'module-library.html': "Welcome to the Module Library! Looking for something specific? 📚"
        }

        return greetings.get(page, "Welcome! I'm here to help. What brings you here today? 👋")

    def log_conversation(self, visitor_id, user_message, bot_response, context=None):
        """Log a conversation exchange"""
        timestamp = datetime.now().isoformat()

        conversation = {
            'timestamp': timestamp,
            'visitor_id': visitor_id,
            'user_message': user_message,
            'bot_response': bot_response,
            'context': context or {}
        }

        # Append to JSONL file
        with open(self.conversations_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(conversation) + '\n')

        # Update session
        if visitor_id in self.sessions:
            self.sessions[visitor_id]['interactions'].append(conversation)

        # Analyze for patterns
        self._analyze_message_patterns(user_message)

        return {'logged': True}

    def log_page_navigation(self, visitor_id, from_page, to_page):
        """Track visitor navigation path"""
        if visitor_id in self.sessions:
            self.sessions[visitor_id]['path'].append(to_page)

        # Check for confusion patterns
        path = self.sessions[visitor_id]['path'] if visitor_id in self.sessions else []
        if len(path) > 3:
            # Check if they're looping
            if path[-1] == path[-3]:
                self.patterns['possible_confusion_loop'] += 1
                return {'warning': 'User might be confused - looping pattern detected'}

        return {'tracked': True}

    def _analyze_message_patterns(self, message):
        """Extract patterns from user messages"""
        message_lower = message.lower()

        # Common question patterns
        question_keywords = {
            'how': 'how_to_questions',
            'what': 'what_is_questions',
            'why': 'why_questions',
            'where': 'where_questions',
            'help': 'help_requests',
            'build': 'building_related',
            'cost': 'pricing_questions',
            'time': 'timeline_questions',
            'nuclear': 'nuclear_related',
            'module': 'module_questions'
        }

        for keyword, category in question_keywords.items():
            if keyword in message_lower:
                self.patterns[category] += 1
                self.common_questions[category] += 1

    def generate_daily_report(self):
        """Generate intelligence report on visitor behavior"""
        self.banner("GENERATING DAILY VISITOR INTELLIGENCE REPORT")

        print("\n📊 Analyzing visitor data...\n")

        # Load all conversations from today
        today = datetime.now().date()
        conversations_today = []

        if self.conversations_file.exists():
            with open(self.conversations_file, 'r', encoding='utf-8') as f:
                for line in f:
                    conv = json.loads(line)
                    conv_date = datetime.fromisoformat(conv['timestamp']).date()
                    if conv_date == today:
                        conversations_today.append(conv)

        # Generate report
        report = {
            'date': today.isoformat(),
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_visitors': len(self.sessions),
                'total_conversations': len(conversations_today),
                'active_sessions': len([s for s in self.sessions.values() if s]),
            },
            'top_questions': dict(self.common_questions.most_common(10)),
            'patterns_detected': dict(self.patterns),
            'insights': self._generate_insights(conversations_today),
            'recommendations': self._generate_recommendations()
        }

        # Save report
        report_file = self.data_dir / f"daily_report_{today}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Print summary
        print(f"  Total Visitors: {report['summary']['total_visitors']}")
        print(f"  Conversations: {report['summary']['total_conversations']}")
        print(f"\n  Top Question Types:")
        for question_type, count in list(report['top_questions'].items())[:5]:
            print(f"    - {question_type}: {count}")

        print(f"\n  📄 Report saved: {report_file}")

        return report

    def _generate_insights(self, conversations):
        """Generate insights from conversation data"""
        insights = []

        # Check for common themes
        all_messages = ' '.join([c['user_message'].lower() for c in conversations])

        themes = {
            'nuclear': 'Multiple visitors asking about nuclear consulting',
            'pricing': 'People want to know about costs and pricing',
            'help': 'Visitors need more guidance/help',
            'building': 'Interest in building/creating things',
            'module': 'Questions about the module system'
        }

        for keyword, insight in themes.items():
            if all_messages.count(keyword) >= 3:
                insights.append({
                    'theme': keyword,
                    'insight': insight,
                    'frequency': all_messages.count(keyword)
                })

        return insights

    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []

        # Based on patterns
        if self.patterns.get('possible_confusion_loop', 0) > 0:
            recommendations.append({
                'priority': 'HIGH',
                'issue': 'Navigation confusion detected',
                'action': 'Review page navigation - visitors are looping',
                'count': self.patterns['possible_confusion_loop']
            })

        if self.patterns.get('help_requests', 0) > 5:
            recommendations.append({
                'priority': 'MEDIUM',
                'issue': 'High volume of help requests',
                'action': 'Add more guidance/tooltips to common pages',
                'count': self.patterns['help_requests']
            })

        if self.patterns.get('pricing_questions', 0) > 3:
            recommendations.append({
                'priority': 'MEDIUM',
                'issue': 'Pricing questions frequent',
                'action': 'Make pricing more visible/clear',
                'count': self.patterns['pricing_questions']
            })

        return recommendations

    def export_to_observatory(self):
        """Export insights to The Observatory"""
        self.banner("EXPORTING TO OBSERVATORY")

        report = self.generate_daily_report()

        # Create Observatory-compatible format
        observatory_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Visitor Intelligence System',
            'data': report,
            'patterns': dict(self.patterns),
            'learnings': [
                {
                    'category': 'Visitor Behavior',
                    'insight': f"Tracked {report['summary']['total_visitors']} visitors today",
                    'action': 'Continue monitoring for patterns'
                }
            ]
        }

        # Save to Observatory patterns
        observatory_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/OBSERVATORY_VISITOR_INTELLIGENCE.json")
        with open(observatory_file, 'w') as f:
            json.dump(observatory_data, f, indent=2)

        print(f"\n  ✅ Data exported to Observatory: {observatory_file}")
        print(f"  🔭 Observatory now knows about visitor patterns!")

        return observatory_data


class GreeterBot:
    """
    Friendly greeter that welcomes visitors and initiates conversation
    """
    def __init__(self, visitor_intelligence):
        self.vi = visitor_intelligence
        self.personality = {
            'name': 'Aria',
            'style': 'friendly and helpful',
            'emoji_level': 'moderate'
        }

    def greet(self, visitor_id, page, metadata=None):
        """Greet a new visitor"""
        greeting = self.vi.log_visitor_arrival(visitor_id, page, metadata)

        # Add personality
        full_greeting = {
            'bot_name': self.personality['name'],
            'message': greeting['welcome_message'],
            'suggestions': self._get_suggestions(page),
            'prompt': "What brings you here today?"
        }

        return full_greeting

    def _get_suggestions(self, page):
        """Suggest actions based on current page"""
        suggestions = {
            'index.html': [
                "Explore the Module Library",
                "Check out the Platform Map",
                "Learn about Nuclear Consulting"
            ],
            'philosopher-ai.html': [
                "Ask me a technical question",
                "Tell me what you're building",
                "Learn about Pattern Theory"
            ],
            'platform-city-map.html': [
                "Browse available modules",
                "See the analytics dashboard",
                "Join as a builder"
            ]
        }

        return suggestions.get(page, ["Explore the platform", "Ask me anything"])


# ============================================================================
# FLASK API - Chat Interface for Visitor Intelligence
# ============================================================================

app = Flask(__name__)
CORS(app)

# Global instances
vi_instance = None
greeter_instance = None

def get_instances():
    """Get or create global instances"""
    global vi_instance, greeter_instance
    if vi_instance is None:
        vi_instance = VisitorIntelligence()
        greeter_instance = GreeterBot(vi_instance)
    return vi_instance, greeter_instance

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Visitor Intelligence',
        'description': 'Tracks and analyzes visitor behavior and conversations',
        'capabilities': [
            'Visitor tracking',
            'Conversation analysis',
            'Pattern detection',
            'Intelligence reporting'
        ]
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for Visitor Intelligence queries"""
    vi, greeter = get_instances()

    data = request.json
    message = data.get('message', '').lower()

    response_text = ""

    if 'report' in message or 'stats' in message or 'how many' in message:
        total_sessions = len(vi.sessions)
        total_patterns = len(vi.patterns)
        response_text = f"""👥 **Visitor Intelligence Report**

**Current Session Stats:**
- Active Sessions: {total_sessions}
- Patterns Detected: {total_patterns}
- Tracking: Conversations, navigation, user intent

I'm continuously analyzing visitor behavior to understand what people want and how they interact with your platform."""

    elif 'pattern' in message or 'behavior' in message or 'what are people' in message:
        if vi.patterns:
            top_patterns = sorted(vi.patterns.items(), key=lambda x: x[1], reverse=True)[:5]
            pattern_list = '\n'.join([f"- {pattern.replace('_', ' ').title()}: {count}" for pattern, count in top_patterns])
            response_text = f"""👥 **Detected Visitor Patterns**

Top patterns I've identified:
{pattern_list}

These insights help optimize the user experience and identify what visitors are looking for."""
        else:
            response_text = "👥 **Visitor Patterns**\n\nNo significant patterns detected yet. I'll analyze visitor behavior as they interact with your platform."

    elif 'help' in message or 'what can you do' in message or 'capabilities' in message:
        response_text = """👥 **Visitor Intelligence Capabilities**

I watch and learn from every visitor to your platform:

1. **Session Tracking** - Log arrivals, navigation, time spent
2. **Conversation Analysis** - Understand what people ask about
3. **Pattern Detection** - Identify confusion loops, common questions
4. **Intelligence Reports** - Daily summaries of visitor behavior
5. **Predictive Insights** - What visitors will need before they ask

I help you understand your users deeply and improve their experience!"""

    elif 'confusion' in message or 'lost' in message or 'problem' in message:
        confusion_count = vi.patterns.get('possible_confusion_loop', 0)
        if confusion_count > 0:
            response_text = f"👥 **Visitor Confusion Alert**\n\nDetected {confusion_count} possible confusion loops where visitors are navigating back and forth between the same pages. This might indicate unclear navigation or missing information."
        else:
            response_text = "👥 **Navigation Status**\n\nNo confusion patterns detected. Visitors seem to be navigating smoothly!"

    elif 'question' in message or 'asking' in message or 'common' in message:
        if vi.common_questions:
            top_questions = vi.common_questions.most_common(5)
            question_list = '\n'.join([f"- {q.replace('_', ' ').title()}: {count}" for q, count in top_questions])
            response_text = f"""👥 **Common Visitor Questions**

{question_list}

These are the main topics visitors are asking about. This insight can help you create better content and FAQs."""
        else:
            response_text = "👥 **Visitor Questions**\n\nNo questions logged yet. I'll track common inquiries as visitors interact with your platform."

    else:
        response_text = f"""👥 **Visitor Intelligence**

I'm your eyes and ears on visitor behavior. I received: '{message[:100]}...'

I can provide insights on:
- Visitor statistics and patterns
- Common questions and concerns
- Navigation issues and confusion
- Behavioral trends

What would you like to know about your visitors?"""

    return jsonify({
        'response': response_text,
        'status': 'success',
        'active_sessions': len(vi.sessions),
        'patterns_detected': len(vi.patterns)
    })

@app.route('/track', methods=['POST'])
def track_visitor():
    """Endpoint to track visitor events"""
    vi, greeter = get_instances()

    data = request.json
    event_type = data.get('type')

    if event_type == 'arrival':
        greeting = greeter.greet(
            data.get('visitor_id'),
            data.get('page'),
            data.get('metadata')
        )
        return jsonify(greeting)

    elif event_type == 'conversation':
        result = vi.log_conversation(
            data.get('visitor_id'),
            data.get('user_message'),
            data.get('bot_response'),
            data.get('context')
        )
        return jsonify(result)

    elif event_type == 'navigation':
        result = vi.log_page_navigation(
            data.get('visitor_id'),
            data.get('from_page'),
            data.get('to_page')
        )
        return jsonify(result)

    return jsonify({'error': 'Unknown event type'}), 400


if __name__ == "__main__":
    import sys

    # Check if running as API server or test mode
    if '--api' in sys.argv:
        print("\n" + "=" * 70)
        print("  👥 VISITOR INTELLIGENCE - API SERVER")
        print("=" * 70)
        print("\n🌐 Starting Flask API on port 6000...")
        print("\nEndpoints:")
        print("  GET  /health - Health check")
        print("  POST /chat   - Chat with Visitor Intelligence")
        print("  POST /track  - Track visitor events")
        print("\n" + "=" * 70 + "\n")

        app.run(host='0.0.0.0', port=6000, debug=False)
    else:
        # Run test mode
        vi = VisitorIntelligence()
        greeter = GreeterBot(vi)

        vi.banner("VISITOR INTELLIGENCE SYSTEM - TEST")

        # Simulate a visitor
        print("\n🧪 Simulating visitor session...\n")

        visitor_id = "test_visitor_001"

        # Arrival
        greeting = greeter.greet(visitor_id, 'philosopher-ai.html')
        print(f"Greeter: {greeting['message']}")
        print(f"Suggestions: {greeting['suggestions']}")

        # Conversation
        vi.log_conversation(
            visitor_id,
            "How do I build a module?",
            "Great question! Modules are built using...",
            {'page': 'philosopher-ai.html'}
        )

        # Navigation
        vi.log_page_navigation(visitor_id, 'philosopher-ai.html', 'module-library.html')

        # Generate report
        report = vi.generate_daily_report()

        # Export to Observatory
        vi.export_to_observatory()

        print("\n✅ Visitor Intelligence System operational!")
