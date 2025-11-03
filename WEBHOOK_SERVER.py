"""
STRIPE WEBHOOK SERVER - AUTO-PROCESS PAYMENTS
Receives payment notifications from Stripe, sends emails, tracks orders, triggers fulfillment
"""

from flask import Flask, request, jsonify
import stripe
import json
from datetime import datetime
import requests

app = Flask(__name__)

# Configuration
stripe.api_key = "sk_test_YOUR_SECRET_KEY_HERE"  # Same as setup script
webhook_secret = "whsec_YOUR_WEBHOOK_SECRET"     # Get from Stripe dashboard after creating webhook

# Store orders in memory (upgrade to database later)
orders = []
order_stats = {
    "total_raised": 0,
    "total_orders": 0,
    "college_fund": 0,
    "orders_by_product": {}
}

@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """
    Stripe sends payment notifications here
    Setup: Stripe Dashboard → Developers → Webhooks → Add endpoint
    URL: http://your-server.com/webhook/stripe
    Events: checkout.session.completed
    """

    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        print("❌ Invalid payload")
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        print("❌ Invalid signature")
        return jsonify({"error": "Invalid signature"}), 400

    # Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        order_data = process_payment(session)

        print(f"\n✅ NEW ORDER RECEIVED!")
        print(f"   Product: {order_data['product_name']}")
        print(f"   Amount: ${order_data['amount_paid']:.2f}")
        print(f"   College Fund: ${order_data['college_fund_amount']:.2f}")
        print(f"   Customer: {order_data['customer_email']}\n")

        # Store order
        orders.append(order_data)
        update_stats(order_data)

        # Automation triggers
        send_confirmation_email(order_data)
        log_to_consciousness_system(order_data)
        check_manufacturing_threshold(order_data)
        check_milestone(order_data)

        return jsonify({"status": "success"}), 200

    return jsonify({"status": "unhandled_event"}), 200


def process_payment(session):
    """Extract order information from Stripe session"""

    amount_total = session['amount_total'] / 100  # Convert cents to dollars
    college_fund = amount_total * 0.4  # 40% to daughters' funds

    order_data = {
        "order_id": session['id'],
        "product_key": session['metadata'].get('product_key', 'unknown'),
        "product_name": session['metadata'].get('product', 'Consciousness Kit'),
        "campaign": session['metadata'].get('campaign', 'unknown'),
        "beneficiary": session['metadata'].get('beneficiary', 'unknown'),
        "amount_paid": amount_total,
        "college_fund_amount": college_fund,
        "customer_email": session.get('customer_details', {}).get('email', 'unknown'),
        "customer_name": session.get('customer_details', {}).get('name', 'Supporter'),
        "payment_status": session['payment_status'],
        "timestamp": datetime.now().isoformat()
    }

    return order_data


def update_stats(order):
    """Update running statistics"""
    global order_stats

    order_stats["total_raised"] += order["amount_paid"]
    order_stats["total_orders"] += 1
    order_stats["college_fund"] += order["college_fund_amount"]

    product = order["product_key"]
    if product not in order_stats["orders_by_product"]:
        order_stats["orders_by_product"][product] = 0
    order_stats["orders_by_product"][product] += 1


def send_confirmation_email(order):
    """Send thank you email to customer"""

    print(f"📧 Sending confirmation email to {order['customer_email']}")

    # TODO: Integrate SendGrid here
    # For now, just log
    email_data = {
        "to": order["customer_email"],
        "subject": f"Your {order['product_name']} Order Confirmed ✅",
        "body": f"""
        Thank you for supporting the Consciousness Revolution!

        Order Details:
        - Product: {order['product_name']}
        - Amount: ${order['amount_paid']:.2f}
        - College Fund Contribution: ${order['college_fund_amount']:.2f} to {order['beneficiary']}

        What Happens Next:
        1. Manufacturing begins when we reach threshold (50 orders)
        2. You'll receive shipping notification in 2-3 weeks
        3. Your contribution helps fund {order['beneficiary']}'s education

        You're not just buying a product.
        You're funding consciousness evolution.

        Welcome to the revolution. ⚡

        - The Consciousness Revolution Team
        """
    }

    # Save email to send queue
    with open("C:\\Users\\dwrek\\100X_DEPLOYMENT\\email_queue.json", "a") as f:
        f.write(json.dumps(email_data) + "\n")

    print(f"   ✓ Email queued")


def log_to_consciousness_system(order):
    """Send order data to consciousness tracking (port 8888)"""

    try:
        response = requests.post(
            "http://localhost:8888/consciousness/track",
            json={
                "event": "kit_purchased",
                "timestamp": order["timestamp"],
                "data": {
                    "product": order["product_key"],
                    "campaign": order["campaign"],
                    "amount": order["amount_paid"],
                    "beneficiary": order["beneficiary"]
                }
            },
            timeout=2
        )

        if response.status_code == 200:
            print(f"   ✓ Logged to consciousness system")
        else:
            print(f"   ⚠ Consciousness system responded: {response.status_code}")

    except requests.exceptions.RequestException:
        print(f"   ⚠ Consciousness system not responding (port 8888 down?)")
        # Not critical, continue anyway


def check_manufacturing_threshold(order):
    """Check if we hit manufacturing threshold (50 orders)"""

    if order_stats["total_orders"] == 50:
        print("\n🚨 MANUFACTURING THRESHOLD REACHED!")
        print(f"   Total Orders: {order_stats['total_orders']}")
        print(f"   Total Raised: ${order_stats['total_raised']:.2f}")
        print(f"   College Funds: ${order_stats['college_fund']:.2f}")

        # TODO: Send notification to Commander
        # TODO: Generate Amazon shopping list
        # TODO: Email all customers "Manufacturing starting!"

        trigger_manufacturing_notification()


def check_milestone(order):
    """Check if we hit funding milestones ($5k, $10k, $25k, etc.)"""

    total = order_stats["total_raised"]

    milestones = [5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000]

    for milestone in milestones:
        # Check if we just crossed this milestone
        if total >= milestone and (total - order["amount_paid"]) < milestone:
            print(f"\n🎯 MILESTONE HIT: ${milestone:,}")

            # TODO: Post to Instagram
            # TODO: Email all backers
            # TODO: Update dashboard

            trigger_milestone_celebration(milestone, total)


def trigger_manufacturing_notification():
    """Send notification that manufacturing can begin"""

    notification = {
        "type": "manufacturing_ready",
        "timestamp": datetime.now().isoformat(),
        "stats": order_stats,
        "message": "50 orders received - ready to start manufacturing!"
    }

    # Save notification
    with open("C:\\Users\\dwrek\\100X_DEPLOYMENT\\notifications.json", "a") as f:
        f.write(json.dumps(notification) + "\n")

    print("   ✓ Manufacturing notification created")


def trigger_milestone_celebration(milestone, current_total):
    """Celebrate funding milestone"""

    celebration = {
        "type": "milestone",
        "milestone": milestone,
        "current_total": current_total,
        "timestamp": datetime.now().isoformat(),
        "message": f"Reached ${milestone:,} milestone! Currently at ${current_total:.2f}"
    }

    # Save for social posting
    with open("C:\\Users\\dwrek\\100X_DEPLOYMENT\\milestones.json", "a") as f:
        f.write(json.dumps(celebration) + "\n")

    print("   ✓ Milestone celebration triggered")


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint to check current campaign stats"""
    return jsonify(order_stats)


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """API endpoint to see all orders"""
    return jsonify(orders)


@app.route('/api/test', methods=['POST'])
def test_payment():
    """Test endpoint to simulate a payment"""

    test_order = {
        "order_id": "test_" + str(datetime.now().timestamp()),
        "product_key": "joy_starter",
        "product_name": "AMELIA Joy Kit - Starter (TEST)",
        "campaign": "amelia_joy",
        "beneficiary": "AMELIA",
        "amount_paid": 39.00,
        "college_fund_amount": 15.60,
        "customer_email": "test@example.com",
        "customer_name": "Test Supporter",
        "payment_status": "paid",
        "timestamp": datetime.now().isoformat()
    }

    orders.append(test_order)
    update_stats(test_order)

    print(f"✅ TEST ORDER CREATED")

    return jsonify({"status": "test_order_created", "order": test_order})


if __name__ == "__main__":
    print("🚀 STRIPE WEBHOOK SERVER STARTING...\n")
    print("📡 Listening for payments on http://localhost:5000/webhook/stripe")
    print("📊 Stats available at: http://localhost:5000/api/stats")
    print("📋 Orders list at: http://localhost:5000/api/orders")
    print("\n🧪 Test with: POST http://localhost:5000/api/test\n")

    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
