"""
STRIPE PAYMENT SYSTEM
Simple payment processing for consciousness investment offers
"""

import os
import stripe

# Get from environment or set here temporarily
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')  # Replace with actual key

class StripePayments:
    """Handle 50% interest investment payments"""

    def create_customer(self, email, name):
        """Create Stripe customer for investor"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                description=f"Consciousness Revolution Investor - {name}"
            )
            return {
                'success': True,
                'customer_id': customer.id,
                'message': f'Customer created: {customer.id}'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_subscription_schedule(self, customer_id, monthly_amount, months=6):
        """
        Create 6-month payment schedule for 50% interest returns

        Args:
            customer_id: Stripe customer ID
            monthly_amount: Monthly payment in dollars (e.g., 1250 for $1,250)
            months: Number of months (default 6)
        """
        try:
            schedule = stripe.SubscriptionSchedule.create(
                customer=customer_id,
                start_date='now',
                end_behavior='release',
                phases=[{
                    'items': [{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Consciousness Investment Return',
                            },
                            'unit_amount': int(monthly_amount * 100),  # Convert to cents
                            'recurring': {'interval': 'month'},
                        },
                    }],
                    'iterations': months,
                }],
            )

            return {
                'success': True,
                'schedule_id': schedule.id,
                'message': f'Payment schedule created: ${monthly_amount}/month × {months} months'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_one_time_payment(self, amount, description, success_url, cancel_url):
        """Create one-time payment link (for initial investment)"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': description},
                        'unit_amount': int(amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )

            return {
                'success': True,
                'url': session.url,
                'session_id': session.id
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Quick setup function
def setup_stripe_for_investments():
    """Setup instructions"""
    print("STRIPE SETUP FOR 50% INTEREST INVESTMENTS")
    print("=" * 60)
    print()
    print("1. Get API keys from: https://dashboard.stripe.com/apikeys")
    print("2. Set environment variable:")
    print("   setx STRIPE_SECRET_KEY \"sk_live_...\"")
    print()
    print("3. Test creating customer:")
    print("   payments = StripePayments()")
    print("   payments.create_customer('investor@email.com', 'Investor Name')")
    print()
    print("4. Create payment schedule:")
    print("   payments.create_subscription_schedule(customer_id, 1250, 6)")
    print("   # $1,250/month for 6 months")
    print()


if __name__ == "__main__":
    setup_stripe_for_investments()
