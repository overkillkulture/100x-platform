"""
COINBASE PERMANENT ACCESS - Never Get Locked Out Again
Build this AFTER extracting your $5K

Mission: Permanent API access to Coinbase (no OTP needed for basic ops)
Trinity: C1 Mechanic execution
"""

import os
import json
from datetime import datetime

try:
    from coinbase.wallet.client import Client
    COINBASE_INSTALLED = True
except ImportError:
    COINBASE_INSTALLED = False
    print("⚠️ Coinbase library not installed")
    print("Run: pip install coinbase")


class CoinbaseVault:
    """
    Permanent Coinbase access via API
    No OTP needed for:
    - Checking balances
    - Viewing transactions
    - Automated withdrawals (if enabled)
    """

    def __init__(self):
        """Initialize with API credentials from environment"""

        # Get from environment or config file
        api_key = os.getenv('COINBASE_API_KEY')
        api_secret = os.getenv('COINBASE_API_SECRET')

        if not api_key or not api_secret:
            print("\n⚠️ SETUP REQUIRED ⚠️")
            print("="*60)
            print()
            print("1. Go to: https://www.coinbase.com/settings/api")
            print("2. Click 'New API Key'")
            print("3. Permissions:")
            print("   ✅ wallet:accounts:read")
            print("   ✅ wallet:transactions:read")
            print("   ✅ wallet:withdrawals:create (optional)")
            print("4. Copy API Key + Secret")
            print()
            print("5. Set environment variables:")
            print("   setx COINBASE_API_KEY \"your_key_here\"")
            print("   setx COINBASE_API_SECRET \"your_secret_here\"")
            print()
            print("6. Restart terminal and run again")
            print()
            print("="*60)
            self.client = None
            return

        if not COINBASE_INSTALLED:
            print("Run: pip install coinbase")
            self.client = None
            return

        try:
            self.client = Client(api_key, api_secret)
            print("✅ Coinbase API connected!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            self.client = None

    def get_balance(self):
        """
        Check all crypto balances without logging in
        NO OTP NEEDED
        """
        if not self.client:
            return None

        try:
            accounts = self.client.get_accounts()

            balances = {}
            total_usd = 0

            for account in accounts.data:
                currency = account.currency
                balance = float(account.balance.amount)
                usd_value = float(account.native_balance.amount)

                if balance > 0:  # Only show accounts with balance
                    balances[currency] = {
                        'balance': balance,
                        'usd_value': usd_value
                    }
                    total_usd += usd_value

            return {
                'accounts': balances,
                'total_usd': total_usd,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error getting balance: {e}")
            return None

    def get_payment_methods(self):
        """Get linked bank accounts"""
        if not self.client:
            return None

        try:
            methods = self.client.get_payment_methods()

            banks = []
            for method in methods.data:
                if method.type == 'ach_bank_account':
                    banks.append({
                        'id': method.id,
                        'name': method.name,
                        'type': method.type
                    })

            return banks

        except Exception as e:
            print(f"Error getting payment methods: {e}")
            return None

    def auto_withdraw_to_bank(self, threshold=1000):
        """
        Automated withdrawal when USD balance exceeds threshold
        NO OTP NEEDED (if API permissions granted)

        Args:
            threshold: Minimum USD balance to trigger withdrawal (default $1000)

        Returns:
            Status message
        """
        if not self.client:
            return "Client not initialized"

        try:
            # Get USD account
            accounts = self.client.get_accounts()
            usd_account = None

            for account in accounts.data:
                if account.currency == 'USD':
                    usd_account = account
                    break

            if not usd_account:
                return "No USD account found"

            balance = float(usd_account.balance.amount)

            if balance < threshold:
                return f"Balance ${balance:.2f} below threshold ${threshold}"

            # Get primary bank account
            banks = self.get_payment_methods()
            if not banks:
                return "No bank account linked"

            primary_bank = banks[0]  # Use first bank

            # Initiate withdrawal
            withdrawal = usd_account.withdraw(
                amount=balance,
                currency='USD',
                payment_method=primary_bank['id']
            )

            return {
                'status': 'success',
                'amount': balance,
                'bank': primary_bank['name'],
                'withdrawal_id': withdrawal.id,
                'message': f"✅ Transferred ${balance:.2f} to {primary_bank['name']}"
            }

        except Exception as e:
            return f"❌ Withdrawal failed: {e}"

    def export_for_quantum_vault(self):
        """
        Export crypto data for Quantum Vault Dashboard
        Real-time tracking without logging in
        """
        balances = self.get_balance()

        if not balances:
            return None

        # Format for dashboard
        export = {
            'crypto_portfolio': {
                'total_usd': balances['total_usd'],
                'breakdown': balances['accounts'],
                'last_updated': balances['timestamp'],
                'source': 'coinbase_api'
            }
        }

        # Save to file for dashboard to read
        with open('quantum_vault_crypto.json', 'w') as f:
            json.dump(export, f, indent=2)

        print(f"✅ Exported to quantum_vault_crypto.json")
        print(f"Total Crypto Value: ${balances['total_usd']:.2f}")

        return export


# ==============================================
# COMMAND LINE INTERFACE
# ==============================================

def main():
    """Interactive menu for Coinbase operations"""

    print()
    print("="*60)
    print("   COINBASE PERMANENT ACCESS - API INTERFACE")
    print("="*60)
    print()

    vault = CoinbaseVault()

    if not vault.client:
        print("\n⚠️ Setup API credentials first (see instructions above)")
        return

    while True:
        print()
        print("Options:")
        print("1. Check balances")
        print("2. View linked banks")
        print("3. Auto-withdraw to bank (if balance > $1000)")
        print("4. Export to Quantum Vault Dashboard")
        print("5. Exit")
        print()

        choice = input("Select (1-5): ").strip()

        if choice == '1':
            print()
            print("Fetching balances...")
            balances = vault.get_balance()

            if balances:
                print()
                print("="*60)
                print("  COINBASE BALANCES")
                print("="*60)
                print()

                for currency, data in balances['accounts'].items():
                    print(f"{currency}: {data['balance']:.8f} (${data['usd_value']:.2f})")

                print()
                print("-"*60)
                print(f"TOTAL: ${balances['total_usd']:.2f} USD")
                print("="*60)

        elif choice == '2':
            print()
            print("Fetching banks...")
            banks = vault.get_payment_methods()

            if banks:
                print()
                print("="*60)
                print("  LINKED BANK ACCOUNTS")
                print("="*60)
                for bank in banks:
                    print(f"• {bank['name']} ({bank['type']})")
                print("="*60)

        elif choice == '3':
            print()
            threshold = input("Enter threshold (default $1000): ").strip()
            threshold = float(threshold) if threshold else 1000

            print(f"\nChecking if balance > ${threshold}...")
            result = vault.auto_withdraw_to_bank(threshold)

            print()
            print("="*60)
            if isinstance(result, dict):
                print(result['message'])
            else:
                print(result)
            print("="*60)

        elif choice == '4':
            print()
            print("Exporting to Quantum Vault...")
            export = vault.export_for_quantum_vault()

            if export:
                print()
                print("="*60)
                print("✅ EXPORT COMPLETE")
                print("="*60)
                print(f"File: quantum_vault_crypto.json")
                print(f"Total Value: ${export['crypto_portfolio']['total_usd']:.2f}")
                print("="*60)

        elif choice == '5':
            print()
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
