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
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path

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


if __name__ == "__main__":
    # Example usage
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
