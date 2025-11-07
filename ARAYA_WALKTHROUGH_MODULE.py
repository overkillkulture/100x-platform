"""
ARAYA WALKTHROUGH MODULE
Integrates Gamma (presentations) and Userpilot (tours) with Araya AI

Usage:
    from ARAYA_WALKTHROUGH_MODULE import ArayaWalkthroughSystem

    walkthrough = ArayaWalkthroughSystem()

    # Create presentation
    result = walkthrough.create_presentation("Quantum Vault Guide")

    # Trigger tour
    walkthrough.trigger_tour(user_id="user123", tour_name="marketplace_tour")
"""

import os
import requests
import json
from datetime import datetime

class GammaAPI:
    """
    Interface to Gamma presentation service
    Docs: https://gamma.app/docs/api (hypothetical - check actual docs)
    """

    def __init__(self):
        self.api_key = os.getenv('GAMMA_API_KEY')
        self.base_url = "https://api.gamma.app/v1"

        if not self.api_key:
            print("⚠️  GAMMA_API_KEY not set in environment")
            print("   Get your key from: https://gamma.app/settings/api")

    def create_presentation(self, title, prompt, num_cards=10, style="modern"):
        """
        Create a Gamma presentation

        Args:
            title: Presentation title
            prompt: AI prompt for content generation
            num_cards: Number of cards to generate (default 10)
            style: Visual style (modern, minimal, bold, etc.)

        Returns:
            {
                "success": True/False,
                "url": "https://gamma.app/docs/xyz",
                "embed_code": "<iframe...>",
                "presentation_id": "xyz123"
            }
        """

        if not self.api_key:
            return {"success": False, "error": "API key not configured"}

        endpoint = f"{self.base_url}/presentations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "title": title,
            "prompt": prompt,
            "num_cards": num_cards,
            "style": style,
            "brand": {
                "primary_color": "#6366f1",  # Consciousness Revolution purple
                "font": "Inter"
            }
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload)

            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                return {
                    "success": True,
                    "url": data.get('url'),
                    "embed_code": data.get('embed_code'),
                    "presentation_id": data.get('id'),
                    "cards_generated": data.get('num_cards')
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_presentation(self, presentation_id):
        """Get existing presentation details"""
        endpoint = f"{self.base_url}/presentations/{presentation_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_presentations(self, limit=20):
        """List all presentations"""
        endpoint = f"{self.base_url}/presentations?limit={limit}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                return {"success": True, "presentations": response.json()}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}


class UserpilotAPI:
    """
    Interface to Userpilot walkthrough service
    Docs: https://docs.userpilot.com/api (check actual docs)
    """

    def __init__(self):
        self.api_key = os.getenv('USERPILOT_API_KEY')
        self.app_token = os.getenv('USERPILOT_APP_TOKEN')
        self.base_url = "https://api.userpilot.com/v1"

        if not self.api_key:
            print("⚠️  USERPILOT_API_KEY not set in environment")
            print("   Get your key from: https://app.userpilot.com/settings/api")

    def trigger_tour(self, user_id, tour_id, force=True):
        """
        Trigger a specific tour for a user

        Args:
            user_id: User identifier
            tour_id: Tour/flow identifier from Userpilot dashboard
            force: Force show even if user has seen it before

        Returns:
            {"success": True/False, "message": "..."}
        """

        if not self.api_key:
            return {"success": False, "error": "API key not configured"}

        endpoint = f"{self.base_url}/users/{user_id}/flows/{tour_id}/trigger"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "force_show": force,
            "trigger_source": "araya_ai"
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload)

            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"Tour '{tour_id}' triggered for user {user_id}",
                    "tour_id": tour_id
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def track_event(self, user_id, event_name, properties=None):
        """
        Track custom event (can trigger tours based on events)
        """
        endpoint = f"{self.base_url}/track"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "user_id": user_id,
            "event": event_name,
            "properties": properties or {},
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            return response.status_code == 200
        except:
            return False

    def update_user(self, user_id, properties):
        """
        Update user properties (for tour segmentation)
        """
        endpoint = f"{self.base_url}/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = properties

        try:
            response = requests.put(endpoint, headers=headers, json=payload)
            return response.status_code == 200
        except:
            return False


class ArayaWalkthroughSystem:
    """
    Main integration class - combines Gamma + Userpilot with AI intelligence
    """

    def __init__(self):
        self.gamma = GammaAPI()
        self.userpilot = UserpilotAPI()

        # Tour library (maps user requests to tour IDs)
        self.tours = {
            "marketplace": "marketplace_onboarding",
            "quantum_vault": "quantum_vault_tutorial",
            "creator": "creator_signup_flow",
            "overview": "platform_overview",
            "revenue": "revenue_model_explanation",
            "upload": "content_upload_guide"
        }

        print("✅ Araya Walkthrough System initialized")
        print(f"   Gamma API: {'Configured' if self.gamma.api_key else 'Not configured'}")
        print(f"   Userpilot API: {'Configured' if self.userpilot.api_key else 'Not configured'}")

    def handle_presentation_request(self, user_message, user_context=None):
        """
        Analyze user message and create appropriate presentation

        Args:
            user_message: What the user asked
            user_context: Optional context (user role, page, etc.)

        Returns:
            Presentation URL or error message
        """

        message_lower = user_message.lower()

        # Detect intent
        if any(word in message_lower for word in ["investor", "funding", "pitch", "raise"]):
            topic = "Investment Opportunity"
            prompt = """
            Create an investor pitch deck for Consciousness Revolution:
            - 70/30 revenue split model (creators keep 70%)
            - Multi-domain platform (7 domains)
            - Market opportunity in creator economy
            - Revenue projections
            - Competitive advantages
            - Team and vision
            """
            num_cards = 15

        elif any(word in message_lower for word in ["creator", "sell", "earn", "upload"]):
            topic = "Creator's Guide to 70% Revenue"
            prompt = """
            Create a guide for creators on Consciousness Revolution:
            - How to sign up
            - Upload process
            - 70% revenue share explained
            - Payment processing
            - Tips for success
            - Examples of successful creators
            """
            num_cards = 10

        elif any(word in message_lower for word in ["quantum vault", "vault", "storage"]):
            topic = "Quantum Vault Guide"
            prompt = """
            Explain the Quantum Vault system:
            - What it is
            - How to use it
            - Revenue tracking
            - Content management
            - Security features
            """
            num_cards = 8

        elif any(word in message_lower for word in ["marketplace", "buy", "browse"]):
            topic = "Marketplace Guide"
            prompt = """
            Guide to the Consciousness Revolution Marketplace:
            - How to browse products
            - Categories available
            - Purchase process
            - Supporting creators
            - 70% goes to creators
            """
            num_cards = 8

        else:
            # Generic presentation about platform
            topic = "Consciousness Revolution Overview"
            prompt = f"""
            Create a presentation about: {user_message}
            Focus on the Consciousness Revolution platform and its features.
            """
            num_cards = 10

        # Create presentation
        result = self.gamma.create_presentation(
            title=topic,
            prompt=prompt,
            num_cards=num_cards
        )

        if result['success']:
            return {
                "type": "presentation",
                "url": result['url'],
                "embed_code": result['embed_code'],
                "message": f"Created {num_cards}-card presentation: {topic}"
            }
        else:
            return {
                "type": "error",
                "message": "Couldn't create presentation. Please try again."
            }

    def handle_tour_request(self, user_message, user_id, current_page=None):
        """
        Analyze user message and trigger appropriate tour

        Args:
            user_message: What the user asked
            user_id: User identifier
            current_page: Current page URL (optional)

        Returns:
            Success message or error
        """

        message_lower = user_message.lower()

        # Detect which tour they need
        tour_id = None

        if "marketplace" in message_lower:
            tour_id = self.tours.get("marketplace")
            tour_name = "Marketplace"

        elif "quantum vault" in message_lower or "vault" in message_lower:
            tour_id = self.tours.get("quantum_vault")
            tour_name = "Quantum Vault"

        elif "creator" in message_lower or "upload" in message_lower or "sell" in message_lower:
            tour_id = self.tours.get("creator")
            tour_name = "Creator Signup"

        elif "revenue" in message_lower or "money" in message_lower or "70" in message_lower:
            tour_id = self.tours.get("revenue")
            tour_name = "Revenue Model"

        else:
            # Default to platform overview
            tour_id = self.tours.get("overview")
            tour_name = "Platform Overview"

        # Trigger tour
        result = self.userpilot.trigger_tour(user_id, tour_id)

        if result['success']:
            return {
                "type": "tour",
                "tour_id": tour_id,
                "message": f"Starting {tour_name} walkthrough! Watch for guided pop-ups."
            }
        else:
            return {
                "type": "error",
                "message": "Couldn't start tour. Tours may not be configured yet."
            }

    def proactive_assistance(self, user_id, current_page, time_on_page, user_actions):
        """
        Proactively detect when user needs help

        Args:
            user_id: User identifier
            current_page: Current page URL
            time_on_page: Seconds on current page
            user_actions: List of recent actions

        Returns:
            Tour to trigger (if any) or None
        """

        # User on marketplace for 2+ minutes with no clicks
        if "/marketplace" in current_page and time_on_page > 120 and len(user_actions) == 0:
            return {
                "tour_id": self.tours["marketplace"],
                "reason": "User appears confused on marketplace page",
                "confidence": 0.8
            }

        # User viewing quantum vault but hasn't uploaded anything
        if "/quantum-vault" in current_page and "has_uploaded" not in user_actions:
            return {
                "tour_id": self.tours["quantum_vault"],
                "reason": "First-time vault visitor",
                "confidence": 0.9
            }

        # New user (< 24 hours old) on homepage
        if current_page == "/" and user_actions.get("account_age_hours", 999) < 24:
            return {
                "tour_id": self.tours["overview"],
                "reason": "New user needs platform overview",
                "confidence": 0.95
            }

        return None


# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_gamma_api():
    """Test Gamma API connection"""
    print("\n🧪 TESTING GAMMA API")
    print("=" * 60)

    gamma = GammaAPI()

    if not gamma.api_key:
        print("❌ No API key configured")
        print("   Set GAMMA_API_KEY environment variable first")
        return False

    # Try to create a simple presentation
    result = gamma.create_presentation(
        title="Test Presentation",
        prompt="Create a 3-card presentation about AI and creativity",
        num_cards=3
    )

    if result['success']:
        print("✅ Gamma API working!")
        print(f"   Presentation URL: {result['url']}")
        return True
    else:
        print(f"❌ Error: {result['error']}")
        return False


def test_userpilot_api():
    """Test Userpilot API connection"""
    print("\n🧪 TESTING USERPILOT API")
    print("=" * 60)

    userpilot = UserpilotAPI()

    if not userpilot.api_key:
        print("❌ No API key configured")
        print("   Set USERPILOT_API_KEY environment variable first")
        return False

    # Try to trigger a test tour
    result = userpilot.trigger_tour(
        user_id="test_user_123",
        tour_id="test_tour"
    )

    if result['success']:
        print("✅ Userpilot API working!")
        print(f"   {result['message']}")
        return True
    else:
        print(f"❌ Error: {result['error']}")
        return False


def test_full_system():
    """Test the complete Araya walkthrough system"""
    print("\n🚀 TESTING ARAYA WALKTHROUGH SYSTEM")
    print("=" * 60)

    system = ArayaWalkthroughSystem()

    # Test 1: Presentation request
    print("\nTest 1: Creating investor presentation...")
    result1 = system.handle_presentation_request("explain our platform to investors")
    print(f"   Result: {result1}")

    # Test 2: Tour request
    print("\nTest 2: Triggering marketplace tour...")
    result2 = system.handle_tour_request(
        "show me how the marketplace works",
        user_id="test_user",
        current_page="/marketplace"
    )
    print(f"   Result: {result2}")

    # Test 3: Proactive assistance
    print("\nTest 3: Proactive help detection...")
    result3 = system.proactive_assistance(
        user_id="test_user",
        current_page="/marketplace",
        time_on_page=150,
        user_actions=[]
    )
    print(f"   Result: {result3}")

    print("\n" + "=" * 60)
    print("✅ All tests complete!")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "test-gamma":
            test_gamma_api()
        elif command == "test-userpilot":
            test_userpilot_api()
        elif command == "test-all":
            test_full_system()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python ARAYA_WALKTHROUGH_MODULE.py [test-gamma|test-userpilot|test-all]")
    else:
        # Interactive mode
        print("🤖 ARAYA WALKTHROUGH MODULE")
        print("=" * 60)
        print()
        print("This module integrates Gamma and Userpilot with Araya AI.")
        print()
        print("Commands:")
        print("  python ARAYA_WALKTHROUGH_MODULE.py test-gamma")
        print("  python ARAYA_WALKTHROUGH_MODULE.py test-userpilot")
        print("  python ARAYA_WALKTHROUGH_MODULE.py test-all")
        print()
        print("To use in your code:")
        print("  from ARAYA_WALKTHROUGH_MODULE import ArayaWalkthroughSystem")
        print("  walkthrough = ArayaWalkthroughSystem()")
        print()
