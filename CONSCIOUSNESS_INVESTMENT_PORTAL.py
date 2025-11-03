"""
CONSCIOUSNESS INVESTMENT PORTAL
50% Return in 6 Months - Automated System

Mission: Accept investments, track payments, automate 50% returns
Model: $5K investment → $7,500 return (6 monthly payments of $1,250)
"""

import json
import os
from datetime import datetime, timedelta


class ConsciousnessInvestmentPortal:
    """
    Manage 50% interest investments from consciousness-aligned investors

    Features:
    - Track investments
    - Calculate monthly payouts
    - Generate payment schedules
    - Monitor total raised
    - Export for Stripe automation
    """

    def __init__(self, data_file='consciousness_investments.json'):
        self.data_file = data_file
        self.investments = self.load_investments()

    def load_investments(self):
        """Load existing investments from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            'investors': [],
            'total_raised': 0,
            'total_owed': 0,
            'total_paid': 0,
            'goal': 25000,
            'max_investors': 5
        }

    def save_investments(self):
        """Save investments to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.investments, f, indent=2)

    def add_investment(self, name, email, amount, payment_method='bank_transfer'):
        """
        Add new investment

        Args:
            name: Investor name
            email: Contact email
            amount: Investment amount ($1K-$25K)
            payment_method: How they paid
        """

        # Validate
        if amount < 1000:
            return {
                'success': False,
                'message': 'Minimum investment: $1,000'
            }

        if amount > 25000:
            return {
                'success': False,
                'message': 'Maximum investment: $25,000'
            }

        if len(self.investments['investors']) >= self.investments['max_investors']:
            return {
                'success': False,
                'message': f"Maximum {self.investments['max_investors']} investors reached"
            }

        # Calculate returns
        total_return = amount * 1.5  # 50% return
        monthly_payment = total_return / 6

        # Create payment schedule
        investment_date = datetime.now()
        payment_schedule = []

        for month in range(1, 7):
            payment_date = investment_date + timedelta(days=30 * month)
            payment_schedule.append({
                'month': month,
                'due_date': payment_date.strftime('%Y-%m-%d'),
                'amount': round(monthly_payment, 2),
                'status': 'pending',
                'paid_date': None
            })

        # Add investor
        investor = {
            'id': len(self.investments['investors']) + 1,
            'name': name,
            'email': email,
            'investment_amount': amount,
            'total_return': total_return,
            'monthly_payment': round(monthly_payment, 2),
            'payment_method': payment_method,
            'investment_date': investment_date.strftime('%Y-%m-%d'),
            'payment_schedule': payment_schedule,
            'total_paid': 0,
            'status': 'active'
        }

        self.investments['investors'].append(investor)
        self.investments['total_raised'] += amount
        self.investments['total_owed'] += total_return

        self.save_investments()

        return {
            'success': True,
            'message': f"✅ Investment recorded: ${amount} → ${total_return} return",
            'investor_id': investor['id'],
            'monthly_payment': round(monthly_payment, 2)
        }

    def get_upcoming_payments(self, days_ahead=30):
        """Get all payments due in next X days"""

        today = datetime.now()
        cutoff = today + timedelta(days=days_ahead)

        upcoming = []

        for investor in self.investments['investors']:
            for payment in investor['payment_schedule']:
                if payment['status'] == 'pending':
                    due_date = datetime.strptime(payment['due_date'], '%Y-%m-%d')

                    if today <= due_date <= cutoff:
                        upcoming.append({
                            'investor_name': investor['name'],
                            'investor_email': investor['email'],
                            'amount': payment['amount'],
                            'due_date': payment['due_date'],
                            'month': payment['month']
                        })

        return sorted(upcoming, key=lambda x: x['due_date'])

    def mark_payment_made(self, investor_id, month):
        """Mark a payment as completed"""

        for investor in self.investments['investors']:
            if investor['id'] == investor_id:
                for payment in investor['payment_schedule']:
                    if payment['month'] == month:
                        payment['status'] = 'paid'
                        payment['paid_date'] = datetime.now().strftime('%Y-%m-%d')

                        investor['total_paid'] += payment['amount']
                        self.investments['total_paid'] += payment['amount']

                        self.save_investments()

                        return {
                            'success': True,
                            'message': f"✅ Payment marked: ${payment['amount']} to {investor['name']}"
                        }

        return {
            'success': False,
            'message': 'Payment not found'
        }

    def generate_stripe_schedule(self):
        """
        Generate Stripe subscription schedules for automation

        Returns code to create automated payments via Stripe
        """

        stripe_code = []

        for investor in self.investments['investors']:
            if investor['status'] == 'active':
                code = f"""
# Investor: {investor['name']}
# Investment: ${investor['investment_amount']} → ${investor['total_return']}
# Monthly: ${investor['monthly_payment']} × 6 months

stripe.SubscriptionSchedule.create(
    customer="{investor['email']}",  # Create customer first
    start_date={int(datetime.strptime(investor['payment_schedule'][0]['due_date'], '%Y-%m-%d').timestamp())},
    end_behavior='release',
    phases=[{{
        'items': [{{
            'price_data': {{
                'currency': 'usd',
                'product': 'consciousness_investment_return',
                'unit_amount': {int(investor['monthly_payment'] * 100)},  # Cents
                'recurring': {{'interval': 'month'}}
            }},
        }}],
        'iterations': 6,
    }}],
)
"""
                stripe_code.append(code)

        return "\n".join(stripe_code)

    def dashboard_summary(self):
        """Generate summary for display"""

        active_investors = [i for i in self.investments['investors'] if i['status'] == 'active']

        return f"""
╔══════════════════════════════════════════════════════════╗
║   CONSCIOUSNESS INVESTMENT PORTAL - DASHBOARD           ║
╚══════════════════════════════════════════════════════════╝

CAPITAL RAISED:
• Total Raised: ${self.investments['total_raised']:,}
• Goal: ${self.investments['goal']:,}
• Progress: {(self.investments['total_raised'] / self.investments['goal'] * 100):.1f}%

INVESTORS:
• Active: {len(active_investors)}
• Maximum: {self.investments['max_investors']}
• Slots Remaining: {self.investments['max_investors'] - len(active_investors)}

RETURNS:
• Total Owed: ${self.investments['total_owed']:,}
• Total Paid: ${self.investments['total_paid']:,}
• Remaining: ${self.investments['total_owed'] - self.investments['total_paid']:,}

NEXT 30 DAYS:
"""

        upcoming = self.get_upcoming_payments(30)
        if upcoming:
            for payment in upcoming:
                return f"• {payment['due_date']}: ${payment['amount']:.2f} to {payment['investor_name']}"
        else:
            return "• No payments due"


# ==============================================
# COMMAND LINE INTERFACE
# ==============================================

def main():
    """Interactive portal for managing investments"""

    print()
    print("="*60)
    print("  CONSCIOUSNESS INVESTMENT PORTAL")
    print("  50% Return in 6 Months")
    print("="*60)
    print()

    portal = ConsciousnessInvestmentPortal()

    while True:
        print()
        print("Options:")
        print("1. View dashboard")
        print("2. Add new investment")
        print("3. View upcoming payments")
        print("4. Mark payment as made")
        print("5. Generate Stripe automation code")
        print("6. Exit")
        print()

        choice = input("Select (1-6): ").strip()

        if choice == '1':
            print(portal.dashboard_summary())

        elif choice == '2':
            print()
            print("NEW INVESTMENT")
            print("-" * 60)
            name = input("Investor name: ").strip()
            email = input("Email: ").strip()
            amount = float(input("Amount ($1K-$25K): ").strip())
            method = input("Payment method (bank_transfer/venmo/zelle): ").strip()

            result = portal.add_investment(name, email, amount, method)

            print()
            print("="*60)
            print(result['message'])
            if result['success']:
                print(f"Monthly payments: ${result['monthly_payment']:.2f} × 6 months")
            print("="*60)

        elif choice == '3':
            print()
            days = int(input("Days ahead (default 30): ").strip() or 30)
            upcoming = portal.get_upcoming_payments(days)

            print()
            print("="*60)
            print(f"  PAYMENTS DUE IN NEXT {days} DAYS")
            print("="*60)

            if upcoming:
                for p in upcoming:
                    print(f"{p['due_date']}: ${p['amount']:.2f} to {p['investor_name']} (Month {p['month']})")
            else:
                print("No payments due")

            print("="*60)

        elif choice == '4':
            print()
            investor_id = int(input("Investor ID: ").strip())
            month = int(input("Month (1-6): ").strip())

            result = portal.mark_payment_made(investor_id, month)

            print()
            print("="*60)
            print(result['message'])
            print("="*60)

        elif choice == '5':
            print()
            print("="*60)
            print("  STRIPE AUTOMATION CODE")
            print("="*60)
            print()
            print(portal.generate_stripe_schedule())
            print()
            print("Copy this code and run after setting up Stripe")
            print("="*60)

        elif choice == '6':
            print()
            print("Saving and exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
