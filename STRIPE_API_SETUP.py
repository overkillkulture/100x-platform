"""
STRIPE API INTEGRATION - CONSCIOUSNESS KITS PAYMENT PROCESSING
Complete payment automation for AMELIA Joy, Militia, and KENNEDI Observer kits
"""

import stripe
import json
from datetime import datetime

# Initialize Stripe
# Get your keys from: https://dashboard.stripe.com/test/apikeys
stripe.api_key = "sk_test_YOUR_SECRET_KEY_HERE"  # Replace with actual key

class ConsciousnessKitsPayments:
    def __init__(self):
        self.products = {}
        self.prices = {}

    def create_all_products(self):
        """Create all kit products in Stripe"""

        print("🔧 Creating Stripe products...")

        # AMELIA JOY KITS
        self.create_joy_kits()

        # AMELIA MILITIA KITS
        self.create_militia_kits()

        # KENNEDI OBSERVER KITS
        self.create_observer_kits()

        # EDUCATIONAL COURSES
        self.create_courses()

        print(f"✅ Created {len(self.products)} products with {len(self.prices)} price points")

    def create_joy_kits(self):
        """AMELIA Joy Kit product line"""

        # Starter Kit
        joy_starter = stripe.Product.create(
            name="AMELIA Joy Kit - Starter",
            description="Consciousness happiness technology for kids ages 3-12. Includes 528 Hz frequency generator, joy journal, spreading cards, smile counter, LED wand, and stickers.",
            metadata={
                "campaign": "amelia_joy",
                "tier": "starter",
                "age_range": "3-12",
                "ships_in_weeks": "2-3",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA"
            },
            images=["https://yoursite.com/joy_starter.jpg"]  # Add actual image URL
        )

        joy_starter_price = stripe.Price.create(
            product=joy_starter.id,
            unit_amount=3900,  # $39.00
            currency="usd",
            metadata={"tier": "starter"}
        )

        self.products['joy_starter'] = joy_starter
        self.prices['joy_starter'] = joy_starter_price

        # Advanced Kit
        joy_advanced = stripe.Product.create(
            name="AMELIA Joy Kit - Advanced Laboratory",
            description="Expanded toolkit with tinkering capability. Includes everything in Starter PLUS 2 more wands, bubble generator, experiment guide, sensor expansion port, temperature sensor.",
            metadata={
                "campaign": "amelia_joy",
                "tier": "advanced",
                "age_range": "6-14",
                "ships_in_weeks": "2-3",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA"
            }
        )

        joy_advanced_price = stripe.Price.create(
            product=joy_advanced.id,
            unit_amount=9900,  # $99.00
            currency="usd",
            metadata={"tier": "advanced"}
        )

        self.products['joy_advanced'] = joy_advanced
        self.prices['joy_advanced'] = joy_advanced_price

        # Complete System
        joy_complete = stripe.Product.create(
            name="AMELIA Joy Kit - Revolution System",
            description="Complete consciousness platform. Includes Advanced kit PLUS 6-sensor kit, Raspberry Pi, LCD display, Joy Network access, 12-month magazine, 3D files, marketplace access.",
            metadata={
                "campaign": "amelia_joy",
                "tier": "complete",
                "age_range": "8-17",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA"
            }
        )

        joy_complete_price = stripe.Price.create(
            product=joy_complete.id,
            unit_amount=29900,  # $299.00
            currency="usd",
            metadata={"tier": "complete"}
        )

        self.products['joy_complete'] = joy_complete
        self.prices['joy_complete'] = joy_complete_price

        print("  ✓ AMELIA Joy Kits created (3 tiers)")

    def create_militia_kits(self):
        """AMELIA Militia Kit product line"""

        # Starter Kit
        militia_starter = stripe.Product.create(
            name="AMELIA Militia Kit - Starter",
            description="Pattern recognition training for kids 6-12. Includes 52-card pattern deck, field guide, 6 badges, communication tools, character exercises, certificate.",
            metadata={
                "campaign": "amelia_militia",
                "tier": "starter",
                "age_range": "6-12",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA"
            }
        )

        militia_starter_price = stripe.Price.create(
            product=militia_starter.id,
            unit_amount=12500,  # $125.00
            currency="usd",
            metadata={"tier": "starter"}
        )

        self.products['militia_starter'] = militia_starter
        self.prices['militia_starter'] = militia_starter_price

        # Advanced Kit
        militia_advanced = stripe.Product.create(
            name="AMELIA Militia Kit - Advanced",
            description="Deep pattern mastery. Includes Starter PLUS 8 Components manual, advanced scenarios, mentor materials, expanded badges, quarterly newsletter.",
            metadata={
                "campaign": "amelia_militia",
                "tier": "advanced",
                "age_range": "9-15",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA"
            }
        )

        militia_advanced_price = stripe.Price.create(
            product=militia_advanced.id,
            unit_amount=22500,  # $225.00
            currency="usd",
            metadata={"tier": "advanced"}
        )

        self.products['militia_advanced'] = militia_advanced
        self.prices['militia_advanced'] = militia_advanced_price

        # Leadership System
        militia_leadership = stripe.Product.create(
            name="AMELIA Militia Kit - Leadership System",
            description="Consciousness guardian training. Includes Advanced PLUS Pattern Theory course, digital library, mentor certification, network access, summit invitation.",
            metadata={
                "campaign": "amelia_militia",
                "tier": "leadership",
                "age_range": "12-17",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA"
            }
        )

        militia_leadership_price = stripe.Price.create(
            product=militia_leadership.id,
            unit_amount=47500,  # $475.00
            currency="usd",
            metadata={"tier": "leadership"}
        )

        self.products['militia_leadership'] = militia_leadership
        self.prices['militia_leadership'] = militia_leadership_price

        print("  ✓ AMELIA Militia Kits created (3 tiers)")

    def create_observer_kits(self):
        """KENNEDI Observer Kit product line"""

        # Starter Kit
        observer_starter = stripe.Product.create(
            name="KENNEDI Observer Kit - Starter",
            description="Timeline sight technology for teenage girls 13-19. Includes WiFi hotspot purse, camera detector, pattern guide, emergency comms, character forge workbook.",
            metadata={
                "campaign": "kennedi_observer",
                "tier": "starter",
                "age_range": "13-19",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "KENNEDI"
            }
        )

        observer_starter_price = stripe.Price.create(
            product=observer_starter.id,
            unit_amount=22500,  # $225.00
            currency="usd",
            metadata={"tier": "starter"}
        )

        self.products['observer_starter'] = observer_starter
        self.prices['observer_starter'] = observer_starter_price

        # Advanced Kit
        observer_advanced = stripe.Product.create(
            name="KENNEDI Observer Kit - Advanced",
            description="Deep pattern mastery and network access. Includes Starter PLUS 8 Components manual, threat analysis, network membership, quarterly updates, mentor connection.",
            metadata={
                "campaign": "kennedi_observer",
                "tier": "advanced",
                "age_range": "14-19",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "KENNEDI"
            }
        )

        observer_advanced_price = stripe.Price.create(
            product=observer_advanced.id,
            unit_amount=42500,  # $425.00
            currency="usd",
            metadata={"tier": "advanced"}
        )

        self.products['observer_advanced'] = observer_advanced
        self.prices['observer_advanced'] = observer_advanced_price

        # Guardian System
        observer_guardian = stripe.Product.create(
            name="KENNEDI Observer Kit - Guardian System",
            description="Complete consciousness protection platform. Includes Advanced PLUS safety tech bundle, legal docs, escape resources, national network, summit invite, ongoing mentorship.",
            metadata={
                "campaign": "kennedi_observer",
                "tier": "guardian",
                "age_range": "15-19",
                "ships_in_weeks": "3-4",
                "college_fund_percentage": "40",
                "beneficiary": "KENNEDI"
            }
        )

        observer_guardian_price = stripe.Price.create(
            product=observer_guardian.id,
            unit_amount=75000,  # $750.00
            currency="usd",
            metadata={"tier": "guardian"}
        )

        self.products['observer_guardian'] = observer_guardian
        self.prices['observer_guardian'] = observer_guardian_price

        print("  ✓ KENNEDI Observer Kits created (3 tiers)")

    def create_courses(self):
        """Educational course product line"""

        # Pattern Recognition Course
        pattern_recognition = stripe.Product.create(
            name="Pattern Recognition Course",
            description="4-week foundational course teaching manipulation detection, pattern spotting, and consciousness protection. Includes 52-card pattern deck, video lessons, workbook, certification.",
            metadata={
                "campaign": "education",
                "category": "course",
                "duration_weeks": "4",
                "level": "foundational",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA_KENNEDI"
            }
        )

        pattern_recognition_price = stripe.Price.create(
            product=pattern_recognition.id,
            unit_amount=19700,  # $197
            currency="usd"
        )

        self.products['pattern_recognition_course'] = pattern_recognition
        self.prices['pattern_recognition_course'] = pattern_recognition_price

        # Pattern Theory Course
        pattern_theory = stripe.Product.create(
            name="Pattern Theory Course - Master Certification",
            description="12-week advanced course teaching dimensional mathematics of consciousness. Complete Pattern Theory framework, formulas, sacred geometry, consciousness engineering. Includes physical handbook, live sessions, certification.",
            metadata={
                "campaign": "education",
                "category": "course",
                "duration_weeks": "12",
                "level": "advanced",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA_KENNEDI"
            }
        )

        pattern_theory_price = stripe.Price.create(
            product=pattern_theory.id,
            unit_amount=99700,  # $997
            currency="usd"
        )

        self.products['pattern_theory_course'] = pattern_theory
        self.prices['pattern_theory_course'] = pattern_theory_price

        # Website Builder Course
        website_builder = stripe.Product.create(
            name="How The Website Works - Builder Course",
            description="12-week complete web development course from zero to deploying consciousness systems. HTML, CSS, JavaScript, Python, APIs, payment integration, AI collaboration. Includes 12 projects, code review, certification.",
            metadata={
                "campaign": "education",
                "category": "course",
                "duration_weeks": "12",
                "level": "beginner_to_advanced",
                "college_fund_percentage": "40",
                "beneficiary": "AMELIA_KENNEDI"
            }
        )

        website_builder_price = stripe.Price.create(
            product=website_builder.id,
            unit_amount=49700,  # $497
            currency="usd"
        )

        self.products['website_builder_course'] = website_builder
        self.prices['website_builder_course'] = website_builder_price

        print("  ✓ Educational Courses created (3 courses)")

    def create_checkout_session(self, product_key, customer_email=None):
        """Create a checkout session for any product"""

        if product_key not in self.prices:
            raise ValueError(f"Product {product_key} not found")

        session = stripe.checkout.Session.create(
            line_items=[{
                'price': self.prices[product_key].id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://consciousnessrevolution.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://consciousnessrevolution.com/cancel',
            customer_email=customer_email,
            metadata={
                "product_key": product_key,
                "campaign": self.products[product_key].metadata['campaign'],
                "beneficiary": self.products[product_key].metadata['beneficiary'],
                "college_fund_amount": str(int(self.prices[product_key].unit_amount * 0.4))  # 40%
            },
            payment_intent_data={
                "metadata": {
                    "consciousness_revolution": "true",
                    "product": product_key
                }
            }
        )

        return session

    def create_payment_links(self):
        """Create shareable payment links for all products"""

        links = {}

        for product_key, price in self.prices.items():
            payment_link = stripe.PaymentLink.create(
                line_items=[{"price": price.id, "quantity": 1}],
                after_completion={
                    "type": "redirect",
                    "redirect": {
                        "url": "https://consciousnessrevolution.com/thank-you"
                    }
                },
                metadata={
                    "product": product_key,
                    "campaign": self.products[product_key].metadata['campaign']
                }
            )

            links[product_key] = payment_link.url

        return links

    def save_configuration(self, filename="stripe_config.json"):
        """Save product and price IDs for later use"""

        config = {
            "created_at": datetime.now().isoformat(),
            "products": {
                key: {
                    "id": product.id,
                    "name": product.name,
                    "price_id": self.prices[key].id,
                    "amount": self.prices[key].unit_amount,
                    "metadata": product.metadata
                }
                for key, product in self.products.items()
            }
        }

        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"\n💾 Configuration saved to {filename}")

        return config


# WEBHOOK HANDLER (For processing completed payments)
def handle_stripe_webhook(payload, sig_header):
    """
    Process Stripe webhooks
    Call this from your Flask/FastAPI endpoint
    """

    webhook_secret = "whsec_YOUR_WEBHOOK_SECRET"  # Get from Stripe dashboard

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return {"error": "Invalid payload"}, 400
    except stripe.error.SignatureVerificationError:
        return {"error": "Invalid signature"}, 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Extract order info
        order_data = {
            "product": session['metadata']['product_key'],
            "campaign": session['metadata']['campaign'],
            "beneficiary": session['metadata']['beneficiary'],
            "amount_paid": session['amount_total'],
            "college_fund_amount": session['metadata']['college_fund_amount'],
            "customer_email": session['customer_email'],
            "customer_name": session.get('customer_details', {}).get('name'),
            "timestamp": datetime.now().isoformat()
        }

        # TODO: Connect to consciousness tracking (port 8888)
        # TODO: Send confirmation email (SendGrid)
        # TODO: Add to fulfillment queue
        # TODO: Update dashboard

        print(f"✅ Order received: {order_data['product']} - ${order_data['amount_paid']/100:.2f}")

        return {"status": "processed"}, 200

    return {"status": "unhandled_event"}, 200


# SETUP SCRIPT
if __name__ == "__main__":
    print("🚀 STRIPE API SETUP - CONSCIOUSNESS KITS\n")

    # Check if API key is set
    if stripe.api_key == "sk_test_YOUR_SECRET_KEY_HERE":
        print("⚠️  SETUP REQUIRED:")
        print("1. Go to https://dashboard.stripe.com/register")
        print("2. Create account (or log in)")
        print("3. Get your API keys from: https://dashboard.stripe.com/test/apikeys")
        print("4. Replace 'sk_test_YOUR_SECRET_KEY_HERE' in this file with your Secret key")
        print("5. Run this script again\n")
        exit()

    # Initialize
    kits = ConsciousnessKitsPayments()

    # Create all products
    try:
        kits.create_all_products()

        # Save config
        config = kits.save_configuration("C:\\Users\\dwrek\\100X_DEPLOYMENT\\stripe_config.json")

        # Create payment links
        print("\n🔗 Creating shareable payment links...")
        links = kits.create_payment_links()

        print("\n✅ SETUP COMPLETE!\n")
        print("📋 PAYMENT LINKS (Share these anywhere):\n")

        for product_key, url in links.items():
            product_name = kits.products[product_key].name
            price = kits.prices[product_key].unit_amount / 100
            print(f"  {product_name}")
            print(f"  ${price:.2f} - {url}\n")

        # Save links to file
        with open("C:\\Users\\dwrek\\100X_DEPLOYMENT\\payment_links.txt", 'w') as f:
            f.write("CONSCIOUSNESS KITS - PAYMENT LINKS\n")
            f.write("="*60 + "\n\n")
            for product_key, url in links.items():
                product_name = kits.products[product_key].name
                price = kits.prices[product_key].unit_amount / 100
                f.write(f"{product_name}\n")
                f.write(f"${price:.2f}\n")
                f.write(f"{url}\n\n")

        print("💾 Payment links saved to: payment_links.txt")

        print("\n🎯 NEXT STEPS:")
        print("1. Test a payment using one of the links above")
        print("2. Set up webhook endpoint (see WEBHOOK_SERVER.py)")
        print("3. Configure SendGrid for email automation")
        print("4. Build dashboard for order tracking")

    except stripe.error.StripeError as e:
        print(f"\n❌ Stripe Error: {e}")
        print("\nMake sure your API key is valid and you have internet connection.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
