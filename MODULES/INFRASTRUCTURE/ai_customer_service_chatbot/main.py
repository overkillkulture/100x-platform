#!/usr/bin/env python3
"""
AI Customer Service Chatbot Module
24/7 Automated Multi-Channel Support System
Powered by Claude AI
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import anthropic
from enum import Enum


class Channel(Enum):
    """Supported communication channels"""
    WEB = "web"
    SMS = "sms"
    EMAIL = "email"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"


class TicketPriority(Enum):
    """Support ticket priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class ConversationContext:
    """Context for ongoing conversation"""
    conversation_id: str
    user_id: str
    channel: Channel
    history: List[Dict[str, str]]
    metadata: Dict[str, Any]
    created_at: datetime
    last_updated: datetime


@dataclass
class SupportTicket:
    """Support ticket data structure"""
    ticket_id: str
    user_id: str
    subject: str
    description: str
    priority: TicketPriority
    channel: Channel
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]
    ai_resolved: bool
    conversation_id: Optional[str]


class KnowledgeBase:
    """Simple knowledge base for common queries"""

    def __init__(self):
        self.articles = {
            "password_reset": {
                "title": "How to Reset Your Password",
                "content": "To reset your password: 1) Go to login page 2) Click 'Forgot Password' 3) Enter your email 4) Check your inbox for reset link 5) Follow the link and create a new password",
                "tags": ["password", "reset", "login", "account"]
            },
            "billing": {
                "title": "Billing and Payments",
                "content": "We accept credit cards, PayPal, and bank transfers. Billing occurs monthly or annually. View your invoices in Account Settings > Billing.",
                "tags": ["billing", "payment", "invoice", "subscription"]
            },
            "refund_policy": {
                "title": "Refund Policy",
                "content": "We offer a 30-day money-back guarantee. Contact support within 30 days of purchase for a full refund, no questions asked.",
                "tags": ["refund", "money back", "guarantee", "cancel"]
            },
            "api_access": {
                "title": "API Access and Documentation",
                "content": "API documentation is available at docs.yourplatform.com/api. Get your API key from Settings > Developer > API Keys.",
                "tags": ["api", "developer", "integration", "documentation"]
            }
        }

    def search(self, query: str) -> List[Dict]:
        """Search knowledge base for relevant articles"""
        query_lower = query.lower()
        results = []

        for article_id, article in self.articles.items():
            # Simple relevance scoring
            score = 0
            for tag in article["tags"]:
                if tag in query_lower:
                    score += 2
            if any(word in article["title"].lower() for word in query_lower.split()):
                score += 1

            if score > 0:
                results.append({
                    "id": article_id,
                    "score": score,
                    **article
                })

        return sorted(results, key=lambda x: x["score"], reverse=True)


class AICustomerServiceChatbot:
    """Main chatbot class for multi-channel customer service"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize chatbot with Anthropic API key"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.knowledge_base = KnowledgeBase()
        self.conversations: Dict[str, ConversationContext] = {}
        self.tickets: Dict[str, SupportTicket] = {}

        # Configuration
        self.system_prompt = """You are a helpful, professional customer service agent.
Your goal is to assist customers with their questions and resolve their issues efficiently.
Be friendly, empathetic, and solution-oriented. If you can't resolve an issue,
escalate it to a human agent. Always maintain a positive and professional tone."""

        self.max_conversation_turns = 50
        self.model = "claude-3-5-sonnet-20241022"

    def create_conversation(
        self,
        user_id: str,
        channel: Channel,
        initial_message: str
    ) -> str:
        """Create a new conversation"""
        conversation_id = f"conv_{user_id}_{int(datetime.now().timestamp())}"

        context = ConversationContext(
            conversation_id=conversation_id,
            user_id=user_id,
            channel=channel,
            history=[{
                "role": "user",
                "content": initial_message
            }],
            metadata={
                "initial_message": initial_message,
                "channel": channel.value
            },
            created_at=datetime.now(),
            last_updated=datetime.now()
        )

        self.conversations[conversation_id] = context
        return conversation_id

    def get_response(
        self,
        conversation_id: str,
        user_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get AI response for a conversation"""
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        context = self.conversations[conversation_id]

        # Add user message if provided
        if user_message:
            context.history.append({
                "role": "user",
                "content": user_message
            })

        # Search knowledge base for relevant information
        kb_context = ""
        if user_message:
            kb_results = self.knowledge_base.search(user_message)
            if kb_results:
                kb_context = "\n\nRelevant Knowledge Base Articles:\n"
                for result in kb_results[:3]:
                    kb_context += f"\n{result['title']}: {result['content']}\n"

        # Build enhanced system prompt with knowledge base context
        enhanced_system = self.system_prompt
        if kb_context:
            enhanced_system += kb_context

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=enhanced_system,
                messages=context.history
            )

            assistant_message = response.content[0].text

            # Add assistant response to history
            context.history.append({
                "role": "assistant",
                "content": assistant_message
            })

            context.last_updated = datetime.now()

            # Analyze if ticket should be created
            should_escalate = self._should_escalate(user_message, assistant_message)

            return {
                "success": True,
                "conversation_id": conversation_id,
                "message": assistant_message,
                "should_escalate": should_escalate,
                "channel": context.channel.value,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id
            }

    def _should_escalate(self, user_message: str, ai_response: str) -> bool:
        """Determine if conversation should be escalated to human agent"""
        escalation_keywords = [
            "speak to human", "human agent", "real person",
            "not helpful", "doesn't work", "still broken",
            "urgent", "emergency", "asap", "immediately"
        ]

        if user_message:
            user_lower = user_message.lower()
            if any(keyword in user_lower for keyword in escalation_keywords):
                return True

        return False

    def create_ticket(
        self,
        conversation_id: str,
        subject: str,
        priority: TicketPriority = TicketPriority.MEDIUM
    ) -> SupportTicket:
        """Create support ticket from conversation"""
        if conversation_id not in self.conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        context = self.conversations[conversation_id]
        ticket_id = f"ticket_{int(datetime.now().timestamp())}"

        # Extract description from conversation history
        description = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in context.history[:5]  # First 5 messages
        ])

        ticket = SupportTicket(
            ticket_id=ticket_id,
            user_id=context.user_id,
            subject=subject,
            description=description,
            priority=priority,
            channel=context.channel,
            status="open",
            created_at=datetime.now(),
            resolved_at=None,
            ai_resolved=False,
            conversation_id=conversation_id
        )

        self.tickets[ticket_id] = ticket
        return ticket

    def handle_channel_message(
        self,
        channel: Channel,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Handle incoming message from any channel"""

        # Create or retrieve conversation
        if not conversation_id:
            conversation_id = self.create_conversation(user_id, channel, message)
            response = self.get_response(conversation_id)
        else:
            response = self.get_response(conversation_id, message)

        # Add channel-specific formatting
        formatted_response = self._format_for_channel(
            response["message"],
            channel
        )
        response["formatted_message"] = formatted_response

        return response

    def _format_for_channel(self, message: str, channel: Channel) -> str:
        """Format message for specific channel requirements"""
        if channel == Channel.SMS:
            # SMS has character limits (160 chars)
            if len(message) > 160:
                return message[:157] + "..."

        elif channel == Channel.TWITTER:
            # Twitter has 280 character limit
            if len(message) > 280:
                return message[:277] + "..."

        # Add channel-specific formatting as needed
        return message

    def get_analytics(self) -> Dict[str, Any]:
        """Get chatbot analytics and metrics"""
        total_conversations = len(self.conversations)
        total_tickets = len(self.tickets)

        # Calculate resolution metrics
        resolved_by_ai = sum(
            1 for ticket in self.tickets.values()
            if ticket.ai_resolved
        )

        # Channel distribution
        channel_dist = {}
        for conv in self.conversations.values():
            channel_name = conv.channel.value
            channel_dist[channel_name] = channel_dist.get(channel_name, 0) + 1

        return {
            "total_conversations": total_conversations,
            "total_tickets": total_tickets,
            "ai_resolution_rate": resolved_by_ai / total_tickets if total_tickets > 0 else 0,
            "channel_distribution": channel_dist,
            "average_conversation_length": sum(
                len(conv.history) for conv in self.conversations.values()
            ) / total_conversations if total_conversations > 0 else 0
        }


class MultiChannelIntegration:
    """Integration layer for multiple communication channels"""

    def __init__(self, chatbot: AICustomerServiceChatbot):
        self.chatbot = chatbot

    async def handle_web_chat(self, user_id: str, message: str, session_id: Optional[str] = None):
        """Handle web chat messages"""
        return self.chatbot.handle_channel_message(
            Channel.WEB, user_id, message, session_id
        )

    async def handle_sms(self, phone_number: str, message: str):
        """Handle SMS messages via Twilio"""
        # In production, integrate with Twilio API
        return self.chatbot.handle_channel_message(
            Channel.SMS, phone_number, message
        )

    async def handle_email(self, email_address: str, subject: str, body: str):
        """Handle email support requests"""
        full_message = f"Subject: {subject}\n\n{body}"
        return self.chatbot.handle_channel_message(
            Channel.EMAIL, email_address, full_message
        )

    async def handle_social_media(
        self,
        platform: str,
        user_handle: str,
        message: str
    ):
        """Handle social media messages"""
        channel_map = {
            "facebook": Channel.FACEBOOK,
            "twitter": Channel.TWITTER,
            "instagram": Channel.INSTAGRAM,
            "whatsapp": Channel.WHATSAPP
        }

        channel = channel_map.get(platform.lower(), Channel.WEB)
        return self.chatbot.handle_channel_message(
            channel, user_handle, message
        )


def demo_chatbot():
    """Demo function showing chatbot capabilities"""
    print("=" * 60)
    print("AI Customer Service Chatbot - Demo")
    print("=" * 60)

    # Initialize chatbot (requires ANTHROPIC_API_KEY environment variable)
    try:
        chatbot = AICustomerServiceChatbot()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Simulate customer conversation
    print("\n📱 Simulating Web Chat Conversation...")

    # Start conversation
    conv_id = chatbot.create_conversation(
        user_id="user_12345",
        channel=Channel.WEB,
        initial_message="Hi, I forgot my password and can't log in. Can you help?"
    )

    # Get AI response
    response1 = chatbot.get_response(conv_id)
    print(f"\n👤 Customer: Hi, I forgot my password and can't log in. Can you help?")
    print(f"🤖 AI Agent: {response1['message']}")

    # Continue conversation
    response2 = chatbot.get_response(
        conv_id,
        "I tried that but didn't receive the email. What should I do?"
    )
    print(f"\n👤 Customer: I tried that but didn't receive the email. What should I do?")
    print(f"🤖 AI Agent: {response2['message']}")

    # Check if escalation needed
    if response2.get('should_escalate'):
        print("\n⚠️  Escalation recommended - creating support ticket...")
        ticket = chatbot.create_ticket(
            conv_id,
            "Password reset email not received",
            TicketPriority.MEDIUM
        )
        print(f"📋 Ticket created: {ticket.ticket_id}")

    # Show analytics
    print("\n" + "=" * 60)
    print("Analytics Dashboard")
    print("=" * 60)
    analytics = chatbot.get_analytics()
    print(json.dumps(analytics, indent=2))

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_chatbot()
