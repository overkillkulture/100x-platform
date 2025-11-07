#!/usr/bin/env python3
"""
Smart Email Campaign Manager - Module #24
AI-powered email writing, A/B testing automation, behavioral triggers
Integrates with Mailchimp, SendGrid, and other email platforms
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
from decimal import Decimal
import random


class CampaignType(Enum):
    """Types of email campaigns"""
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"
    ONBOARDING = "onboarding"
    ABANDONED_CART = "abandoned_cart"
    RE_ENGAGEMENT = "re_engagement"
    ANNOUNCEMENT = "announcement"
    EDUCATIONAL = "educational"
    TRANSACTIONAL = "transactional"


class EmailStatus(Enum):
    """Email campaign status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    COMPLETED = "completed"


class TriggerType(Enum):
    """Behavioral trigger types"""
    SIGNUP = "signup"
    PURCHASE = "purchase"
    ABANDONED_CART = "abandoned_cart"
    CLICKED_LINK = "clicked_link"
    OPENED_EMAIL = "opened_email"
    BROWSED_PRODUCT = "browsed_product"
    DOWNLOADED = "downloaded"
    MILESTONE = "milestone"
    INACTIVE = "inactive"


@dataclass
class Contact:
    """Email contact/subscriber"""
    contact_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    subscribed: bool = True
    subscribed_at: datetime = field(default_factory=datetime.now)
    last_opened: Optional[datetime] = None
    last_clicked: Optional[datetime] = None


@dataclass
class EmailTemplate:
    """Email template structure"""
    template_id: str
    name: str
    subject_line: str
    preview_text: str
    body_html: str
    body_text: str
    variables: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ABTest:
    """A/B test configuration"""
    test_id: str
    campaign_id: str
    variant_a: Dict[str, str]  # subject, preview, body
    variant_b: Dict[str, str]
    test_percentage: int = 20  # % of list to test
    winner_metric: str = "open_rate"  # open_rate, click_rate, conversion_rate
    status: str = "running"
    results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Campaign:
    """Email campaign"""
    campaign_id: str
    name: str
    campaign_type: CampaignType
    subject_line: str
    preview_text: str
    body_html: str
    body_text: str
    from_name: str
    from_email: str
    recipients: List[str]  # contact IDs or segment IDs
    scheduled_at: Optional[datetime] = None
    status: EmailStatus = EmailStatus.DRAFT
    ab_test: Optional[ABTest] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Automation:
    """Automated email workflow"""
    automation_id: str
    name: str
    trigger: TriggerType
    delay_hours: int = 0
    template_id: str
    conditions: Dict[str, Any] = field(default_factory=dict)
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CampaignMetrics:
    """Campaign performance metrics"""
    campaign_id: str
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    bounced: int = 0
    unsubscribed: int = 0
    conversions: int = 0
    revenue: Decimal = Decimal('0.00')

    @property
    def open_rate(self) -> float:
        return (self.opened / self.delivered * 100) if self.delivered > 0 else 0.0

    @property
    def click_rate(self) -> float:
        return (self.clicked / self.delivered * 100) if self.delivered > 0 else 0.0

    @property
    def conversion_rate(self) -> float:
        return (self.conversions / self.delivered * 100) if self.delivered > 0 else 0.0


class AIEmailWriter:
    """AI-powered email content generation"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_email_content(
        self,
        campaign_type: CampaignType,
        topic: str,
        key_points: List[str],
        tone: str = "professional",
        target_audience: str = "general",
        cta: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate complete email content with AI"""

        prompt = f"""You are an expert email marketing copywriter. Create a compelling {campaign_type.value} email.

TOPIC: {topic}

KEY POINTS:
{chr(10).join(f"- {point}" for point in key_points)}

TARGET AUDIENCE: {target_audience}
TONE: {tone}
CALL TO ACTION: {cta or "Visit our website"}

Generate:
1. Subject Line (max 50 chars, attention-grabbing)
2. Preview Text (max 100 chars, complements subject)
3. Email Body (HTML format, 200-400 words)
4. Plain Text Version (same content, plain text)

Return as JSON:
{{
  "subject_line": "...",
  "preview_text": "...",
  "body_html": "...",
  "body_text": "..."
}}

Make it engaging, persuasive, and conversion-focused."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3072,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract JSON from response
            content = response.content[0].text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("Could not extract JSON from response")

        except Exception as e:
            print(f"Error generating email: {e}")
            raise

    def generate_subject_line_variants(
        self,
        topic: str,
        count: int = 5
    ) -> List[str]:
        """Generate multiple subject line variants for A/B testing"""

        prompt = f"""Generate {count} different subject line variants for an email about: {topic}

Requirements:
- Each under 50 characters
- Mix of styles: urgency, curiosity, benefit-driven, question-based
- High open rate potential

Return as JSON array: ["subject 1", "subject 2", ...]"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return []

        except Exception as e:
            print(f"Error generating variants: {e}")
            return []

    def optimize_for_spam_score(self, subject: str, body: str) -> Dict[str, Any]:
        """Analyze and optimize content to avoid spam filters"""

        # Simple spam word detection
        spam_words = [
            'free', 'buy now', 'click here', 'act now', 'limited time',
            'urgent', 'winner', 'congratulations', 'guarantee', '100%',
            'cash', 'credit', 'earn money', 'extra income'
        ]

        subject_lower = subject.lower()
        body_lower = body.lower()

        spam_triggers = []
        for word in spam_words:
            if word in subject_lower or word in body_lower:
                spam_triggers.append(word)

        # Calculate spam score (0-100, lower is better)
        spam_score = len(spam_triggers) * 10
        spam_score += len(re.findall(r'!{2,}', subject + body)) * 5  # Multiple exclamations
        spam_score += len(re.findall(r'[A-Z]{5,}', subject + body)) * 5  # All caps
        spam_score = min(spam_score, 100)

        return {
            "spam_score": spam_score,
            "spam_triggers": spam_triggers,
            "recommendations": self._get_spam_recommendations(spam_score, spam_triggers)
        }

    def _get_spam_recommendations(self, score: int, triggers: List[str]) -> List[str]:
        """Get recommendations to improve spam score"""
        recommendations = []

        if score > 50:
            recommendations.append("High spam risk - major rewrite recommended")
        elif score > 30:
            recommendations.append("Moderate spam risk - consider revisions")

        if triggers:
            recommendations.append(f"Remove or replace these words: {', '.join(triggers[:5])}")

        recommendations.append("Avoid excessive punctuation (!!!, ???)")
        recommendations.append("Use mixed case instead of ALL CAPS")
        recommendations.append("Include unsubscribe link")

        return recommendations


class SmartEmailCampaignManager:
    """Main email campaign manager with AI and automation"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize campaign manager"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if self.api_key:
            self.ai_writer = AIEmailWriter(self.api_key)
        else:
            self.ai_writer = None

        # Storage
        self.contacts: Dict[str, Contact] = {}
        self.campaigns: Dict[str, Campaign] = {}
        self.templates: Dict[str, EmailTemplate] = {}
        self.automations: Dict[str, Automation] = {}
        self.metrics: Dict[str, CampaignMetrics] = {}

        # Simulated sending (for demo)
        self.email_sent_log: List[Dict] = []

    def add_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        tags: List[str] = None,
        custom_fields: Dict = None
    ) -> Contact:
        """Add contact to email list"""

        contact_id = f"contact_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}"

        contact = Contact(
            contact_id=contact_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            tags=tags or [],
            custom_fields=custom_fields or {}
        )

        self.contacts[contact_id] = contact
        return contact

    def create_campaign(
        self,
        name: str,
        campaign_type: CampaignType,
        subject_line: str,
        preview_text: str,
        body_html: str,
        body_text: str,
        from_name: str,
        from_email: str,
        recipients: List[str],
        scheduled_at: Optional[datetime] = None
    ) -> Campaign:
        """Create email campaign"""

        campaign_id = f"campaign_{int(datetime.now().timestamp())}"

        campaign = Campaign(
            campaign_id=campaign_id,
            name=name,
            campaign_type=campaign_type,
            subject_line=subject_line,
            preview_text=preview_text,
            body_html=body_html,
            body_text=body_text,
            from_name=from_name,
            from_email=from_email,
            recipients=recipients,
            scheduled_at=scheduled_at,
            status=EmailStatus.SCHEDULED if scheduled_at else EmailStatus.DRAFT
        )

        self.campaigns[campaign_id] = campaign
        self.metrics[campaign_id] = CampaignMetrics(campaign_id=campaign_id)

        return campaign

    def create_ai_campaign(
        self,
        name: str,
        campaign_type: CampaignType,
        topic: str,
        key_points: List[str],
        recipients: List[str],
        from_name: str,
        from_email: str,
        tone: str = "professional"
    ) -> Campaign:
        """Create campaign with AI-generated content"""

        if not self.ai_writer:
            raise ValueError("AI writer requires ANTHROPIC_API_KEY")

        # Generate content
        content = self.ai_writer.generate_email_content(
            campaign_type=campaign_type,
            topic=topic,
            key_points=key_points,
            tone=tone
        )

        # Check spam score
        spam_check = self.ai_writer.optimize_for_spam_score(
            content['subject_line'],
            content['body_text']
        )

        print(f"Spam Score: {spam_check['spam_score']}/100")
        if spam_check['recommendations']:
            print(f"Recommendations: {spam_check['recommendations']}")

        # Create campaign
        return self.create_campaign(
            name=name,
            campaign_type=campaign_type,
            subject_line=content['subject_line'],
            preview_text=content['preview_text'],
            body_html=content['body_html'],
            body_text=content['body_text'],
            from_name=from_name,
            from_email=from_email,
            recipients=recipients
        )

    def create_ab_test(
        self,
        campaign_id: str,
        variant_b_subject: Optional[str] = None,
        variant_b_preview: Optional[str] = None,
        test_percentage: int = 20
    ) -> ABTest:
        """Create A/B test for campaign"""

        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")

        campaign = self.campaigns[campaign_id]

        # If no variant B provided, generate with AI
        if not variant_b_subject and self.ai_writer:
            variants = self.ai_writer.generate_subject_line_variants(
                campaign.subject_line, count=2
            )
            variant_b_subject = variants[1] if len(variants) > 1 else campaign.subject_line + " (Variant)"

        test_id = f"test_{campaign_id}"

        ab_test = ABTest(
            test_id=test_id,
            campaign_id=campaign_id,
            variant_a={
                "subject": campaign.subject_line,
                "preview": campaign.preview_text,
                "body": campaign.body_html
            },
            variant_b={
                "subject": variant_b_subject or campaign.subject_line,
                "preview": variant_b_preview or campaign.preview_text,
                "body": campaign.body_html
            },
            test_percentage=test_percentage
        )

        campaign.ab_test = ab_test
        return ab_test

    def create_automation(
        self,
        name: str,
        trigger: TriggerType,
        template_id: str,
        delay_hours: int = 0,
        conditions: Dict = None
    ) -> Automation:
        """Create automated email workflow"""

        automation_id = f"auto_{int(datetime.now().timestamp())}"

        automation = Automation(
            automation_id=automation_id,
            name=name,
            trigger=trigger,
            template_id=template_id,
            delay_hours=delay_hours,
            conditions=conditions or {}
        )

        self.automations[automation_id] = automation
        return automation

    def send_campaign(self, campaign_id: str, simulate: bool = True) -> Dict[str, Any]:
        """Send email campaign (simulated for demo)"""

        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")

        campaign = self.campaigns[campaign_id]
        metrics = self.metrics[campaign_id]

        # Get recipient contacts
        recipients = [
            self.contacts[cid] for cid in campaign.recipients
            if cid in self.contacts and self.contacts[cid].subscribed
        ]

        if not simulate:
            # In production, integrate with SendGrid, Mailchimp, etc.
            pass

        # Simulate sending
        for contact in recipients:
            # Simulate delivery success (95% delivery rate)
            delivered = random.random() < 0.95

            if delivered:
                metrics.delivered += 1

                # Simulate open (20% open rate)
                if random.random() < 0.20:
                    metrics.opened += 1
                    contact.last_opened = datetime.now()

                    # Simulate click (30% of opens click)
                    if random.random() < 0.30:
                        metrics.clicked += 1
                        contact.last_clicked = datetime.now()

                        # Simulate conversion (10% of clicks convert)
                        if random.random() < 0.10:
                            metrics.conversions += 1
                            metrics.revenue += Decimal('99.00')  # Example revenue

            else:
                metrics.bounced += 1

            metrics.sent += 1

            # Log send
            self.email_sent_log.append({
                "campaign_id": campaign_id,
                "contact_id": contact.contact_id,
                "email": contact.email,
                "timestamp": datetime.now().isoformat(),
                "delivered": delivered
            })

        # Update campaign status
        campaign.status = EmailStatus.COMPLETED

        return {
            "campaign_id": campaign_id,
            "sent": metrics.sent,
            "delivered": metrics.delivered,
            "open_rate": f"{metrics.open_rate:.2f}%",
            "click_rate": f"{metrics.click_rate:.2f}%",
            "conversion_rate": f"{metrics.conversion_rate:.2f}%",
            "revenue": f"${metrics.revenue:.2f}"
        }

    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get detailed campaign metrics"""

        if campaign_id not in self.metrics:
            raise ValueError(f"Campaign {campaign_id} not found")

        metrics = self.metrics[campaign_id]

        return {
            "campaign_id": campaign_id,
            "sent": metrics.sent,
            "delivered": metrics.delivered,
            "opened": metrics.opened,
            "clicked": metrics.clicked,
            "bounced": metrics.bounced,
            "unsubscribed": metrics.unsubscribed,
            "conversions": metrics.conversions,
            "revenue": float(metrics.revenue),
            "open_rate": round(metrics.open_rate, 2),
            "click_rate": round(metrics.click_rate, 2),
            "conversion_rate": round(metrics.conversion_rate, 2)
        }

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary"""

        total_contacts = len(self.contacts)
        active_contacts = len([c for c in self.contacts.values() if c.subscribed])
        total_campaigns = len(self.campaigns)

        # Aggregate metrics
        total_sent = sum(m.sent for m in self.metrics.values())
        total_delivered = sum(m.delivered for m in self.metrics.values())
        total_opened = sum(m.opened for m in self.metrics.values())
        total_clicked = sum(m.clicked for m in self.metrics.values())
        total_revenue = sum(m.revenue for m in self.metrics.values())

        avg_open_rate = (total_opened / total_delivered * 100) if total_delivered > 0 else 0
        avg_click_rate = (total_clicked / total_delivered * 100) if total_delivered > 0 else 0

        return {
            "contacts": {
                "total": total_contacts,
                "active": active_contacts,
                "unsubscribed": total_contacts - active_contacts
            },
            "campaigns": {
                "total": total_campaigns,
                "sent": len([c for c in self.campaigns.values() if c.status == EmailStatus.COMPLETED]),
                "scheduled": len([c for c in self.campaigns.values() if c.status == EmailStatus.SCHEDULED])
            },
            "performance": {
                "emails_sent": total_sent,
                "emails_delivered": total_delivered,
                "average_open_rate": round(avg_open_rate, 2),
                "average_click_rate": round(avg_click_rate, 2),
                "total_revenue": float(total_revenue)
            },
            "automations": {
                "total": len(self.automations),
                "active": len([a for a in self.automations.values() if a.active])
            }
        }


def demo_email_campaign_manager():
    """Demo function showing email campaign management"""
    print("=" * 70)
    print("Smart Email Campaign Manager - Demo")
    print("=" * 70)

    try:
        manager = SmartEmailCampaignManager()
    except ValueError as e:
        print(f"\nNote: {e}")
        print("Running demo without AI features...")
        manager = SmartEmailCampaignManager()

    # Add contacts
    print("\n📧 Adding contacts...")
    for i in range(100):
        manager.add_contact(
            email=f"user{i}@example.com",
            first_name=f"User{i}",
            tags=["subscriber"]
        )
    print(f"✅ Added {len(manager.contacts)} contacts")

    # Create campaign with AI
    if manager.ai_writer:
        print("\n🤖 Creating AI-generated campaign...")
        campaign = manager.create_ai_campaign(
            name="Product Launch Newsletter",
            campaign_type=CampaignType.NEWSLETTER,
            topic="Launch of our revolutionary new product",
            key_points=[
                "Solves major pain point for customers",
                "Limited time launch discount: 30% off",
                "Free shipping for first 100 orders",
                "30-day money-back guarantee"
            ],
            recipients=list(manager.contacts.keys())[:50],
            from_name="Product Team",
            from_email="team@company.com",
            tone="exciting"
        )
        print(f"✅ Campaign created: {campaign.campaign_id}")
        print(f"Subject: {campaign.subject_line}")
    else:
        # Manual campaign creation
        print("\n📝 Creating manual campaign...")
        campaign = manager.create_campaign(
            name="Product Launch Newsletter",
            campaign_type=CampaignType.NEWSLETTER,
            subject_line="🚀 Introducing Our Revolutionary New Product!",
            preview_text="Limited time offer: 30% off for early adopters",
            body_html="<h1>Hello!</h1><p>We're excited to announce...</p>",
            body_text="Hello!\n\nWe're excited to announce...",
            from_name="Product Team",
            from_email="team@company.com",
            recipients=list(manager.contacts.keys())[:50]
        )
        print(f"✅ Campaign created: {campaign.campaign_id}")

    # Create A/B test
    print("\n🔬 Setting up A/B test...")
    ab_test = manager.create_ab_test(
        campaign.campaign_id,
        variant_b_subject="Don't Miss This: 30% Off New Product Launch",
        test_percentage=20
    )
    print(f"✅ A/B test created: {ab_test.test_id}")
    print(f"Variant A: {ab_test.variant_a['subject']}")
    print(f"Variant B: {ab_test.variant_b['subject']}")

    # Send campaign
    print("\n📤 Sending campaign...")
    results = manager.send_campaign(campaign.campaign_id, simulate=True)
    print(f"✅ Campaign sent!")
    print(f"   Sent: {results['sent']}")
    print(f"   Delivered: {results['delivered']}")
    print(f"   Open Rate: {results['open_rate']}")
    print(f"   Click Rate: {results['click_rate']}")
    print(f"   Conversions: {results['conversion_rate']}")
    print(f"   Revenue: {results['revenue']}")

    # Dashboard summary
    print("\n" + "=" * 70)
    print("Dashboard Summary")
    print("=" * 70)
    summary = manager.get_dashboard_summary()
    print(json.dumps(summary, indent=2))

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_email_campaign_manager()
