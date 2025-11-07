#!/usr/bin/env python3
"""
Automated Bookkeeping System - Module #22
Receipt Scanning, Categorization, Tax Calculation, and Financial Reporting
Integrates with QuickBooks, Xero, and other accounting platforms
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
from decimal import Decimal
import base64


class TransactionType(Enum):
    """Types of financial transactions"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    REFUND = "refund"


class ExpenseCategory(Enum):
    """Standard expense categories for tax purposes"""
    ADVERTISING = "Advertising & Marketing"
    OFFICE_SUPPLIES = "Office Supplies"
    TRAVEL = "Travel & Transportation"
    MEALS = "Meals & Entertainment"
    UTILITIES = "Utilities"
    RENT = "Rent & Lease"
    INSURANCE = "Insurance"
    PROFESSIONAL_SERVICES = "Professional Services"
    SOFTWARE = "Software & Subscriptions"
    PAYROLL = "Payroll & Benefits"
    EQUIPMENT = "Equipment"
    INVENTORY = "Inventory"
    TAXES = "Taxes & Licenses"
    BANK_FEES = "Bank Fees"
    MISCELLANEOUS = "Miscellaneous"


class IncomeCategory(Enum):
    """Income categories"""
    SALES = "Sales Revenue"
    SERVICES = "Service Revenue"
    INTEREST = "Interest Income"
    DIVIDENDS = "Dividend Income"
    RENTAL = "Rental Income"
    OTHER = "Other Income"


@dataclass
class Transaction:
    """Financial transaction record"""
    transaction_id: str
    date: datetime
    amount: Decimal
    transaction_type: TransactionType
    category: str
    vendor: str
    description: str
    payment_method: str
    receipt_url: Optional[str] = None
    tax_deductible: bool = False
    tax_category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Receipt:
    """Scanned receipt data"""
    receipt_id: str
    date: datetime
    vendor: str
    total: Decimal
    tax: Decimal
    items: List[Dict[str, Any]]
    payment_method: str
    raw_text: str
    image_url: Optional[str] = None


@dataclass
class FinancialReport:
    """Financial report structure"""
    report_id: str
    report_type: str
    start_date: datetime
    end_date: datetime
    total_income: Decimal
    total_expenses: Decimal
    net_profit: Decimal
    income_by_category: Dict[str, Decimal]
    expenses_by_category: Dict[str, Decimal]
    tax_deductible_expenses: Decimal
    generated_at: datetime


class ReceiptScanner:
    """AI-powered receipt scanning and OCR"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def scan_receipt(self, image_path: str) -> Receipt:
        """Scan receipt image and extract data using Claude Vision"""
        try:
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

            # Determine media type
            if image_path.lower().endswith('.png'):
                media_type = "image/png"
            elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                media_type = "image/jpeg"
            elif image_path.lower().endswith('.webp'):
                media_type = "image/webp"
            else:
                media_type = "image/jpeg"

            # Call Claude Vision API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": """Analyze this receipt and extract the following information in JSON format:
{
  "vendor": "Vendor name",
  "date": "YYYY-MM-DD",
  "total": "Total amount as decimal",
  "tax": "Tax amount as decimal",
  "payment_method": "Cash/Credit/Debit/etc",
  "items": [
    {"name": "Item name", "quantity": 1, "price": "price as decimal"}
  ],
  "raw_text": "All text from receipt"
}

Be precise with numbers and dates. If information is unclear, use null."""
                        }
                    ]
                }]
            )

            # Parse response
            receipt_data = json.loads(response.content[0].text)

            # Create Receipt object
            receipt = Receipt(
                receipt_id=f"receipt_{int(datetime.now().timestamp())}",
                date=datetime.strptime(receipt_data['date'], "%Y-%m-%d") if receipt_data.get('date') else datetime.now(),
                vendor=receipt_data.get('vendor', 'Unknown'),
                total=Decimal(str(receipt_data.get('total', 0))),
                tax=Decimal(str(receipt_data.get('tax', 0))),
                items=receipt_data.get('items', []),
                payment_method=receipt_data.get('payment_method', 'Unknown'),
                raw_text=receipt_data.get('raw_text', ''),
                image_url=image_path
            )

            return receipt

        except Exception as e:
            print(f"Error scanning receipt: {e}")
            # Return basic receipt with manual entry needed
            return Receipt(
                receipt_id=f"receipt_{int(datetime.now().timestamp())}",
                date=datetime.now(),
                vendor="Unknown - Manual Entry Required",
                total=Decimal('0.00'),
                tax=Decimal('0.00'),
                items=[],
                payment_method="Unknown",
                raw_text=str(e),
                image_url=image_path
            )

    def categorize_expense(self, vendor: str, description: str, items: List[Dict]) -> Tuple[str, bool]:
        """Automatically categorize expense and determine if tax deductible"""

        # Simple rule-based categorization
        vendor_lower = vendor.lower()
        description_lower = description.lower()

        # Advertising & Marketing
        if any(word in vendor_lower for word in ['facebook', 'google ads', 'linkedin', 'twitter']):
            return ExpenseCategory.ADVERTISING.value, True

        # Office Supplies
        if any(word in vendor_lower for word in ['staples', 'office depot', 'amazon']):
            return ExpenseCategory.OFFICE_SUPPLIES.value, True

        # Travel
        if any(word in vendor_lower for word in ['uber', 'lyft', 'airline', 'hotel', 'airbnb']):
            return ExpenseCategory.TRAVEL.value, True

        # Meals
        if any(word in vendor_lower for word in ['restaurant', 'cafe', 'coffee', 'starbucks']):
            return ExpenseCategory.MEALS.value, True  # 50% deductible

        # Utilities
        if any(word in vendor_lower for word in ['electric', 'power', 'gas', 'water', 'internet', 'phone']):
            return ExpenseCategory.UTILITIES.value, True

        # Software
        if any(word in vendor_lower for word in ['software', 'saas', 'adobe', 'microsoft', 'github']):
            return ExpenseCategory.SOFTWARE.value, True

        # Default
        return ExpenseCategory.MISCELLANEOUS.value, False


class AutomatedBookkeepingSystem:
    """Main bookkeeping system with automated categorization and reporting"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize bookkeeping system"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if self.api_key:
            self.receipt_scanner = ReceiptScanner(self.api_key)
        else:
            self.receipt_scanner = None

        self.transactions: Dict[str, Transaction] = {}
        self.receipts: Dict[str, Receipt] = {}

        # Tax rates (US Federal - example)
        self.tax_rates = {
            "federal_income": 0.22,  # 22% bracket
            "self_employment": 0.153,  # 15.3% SE tax
            "state_income": 0.05  # 5% state (varies)
        }

    def import_receipt(self, image_path: str, auto_create_transaction: bool = True) -> Receipt:
        """Import and scan receipt"""
        if not self.receipt_scanner:
            raise ValueError("Receipt scanner requires ANTHROPIC_API_KEY")

        receipt = self.receipt_scanner.scan_receipt(image_path)
        self.receipts[receipt.receipt_id] = receipt

        # Automatically create transaction from receipt
        if auto_create_transaction and receipt.total > 0:
            category, tax_deductible = self.receipt_scanner.categorize_expense(
                receipt.vendor,
                receipt.raw_text,
                receipt.items
            )

            transaction = self.create_transaction(
                date=receipt.date,
                amount=receipt.total,
                transaction_type=TransactionType.EXPENSE,
                category=category,
                vendor=receipt.vendor,
                description=f"Receipt from {receipt.vendor}",
                payment_method=receipt.payment_method,
                receipt_url=receipt.image_url,
                tax_deductible=tax_deductible
            )

        return receipt

    def create_transaction(
        self,
        date: datetime,
        amount: Decimal,
        transaction_type: TransactionType,
        category: str,
        vendor: str,
        description: str,
        payment_method: str,
        receipt_url: Optional[str] = None,
        tax_deductible: bool = False,
        tags: List[str] = None
    ) -> Transaction:
        """Create new transaction record"""

        transaction_id = f"txn_{int(datetime.now().timestamp())}"

        transaction = Transaction(
            transaction_id=transaction_id,
            date=date,
            amount=Decimal(str(amount)),
            transaction_type=transaction_type,
            category=category,
            vendor=vendor,
            description=description,
            payment_method=payment_method,
            receipt_url=receipt_url,
            tax_deductible=tax_deductible,
            tags=tags or [],
            metadata={}
        )

        self.transactions[transaction_id] = transaction
        return transaction

    def get_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        transaction_type: Optional[TransactionType] = None,
        category: Optional[str] = None
    ) -> List[Transaction]:
        """Query transactions with filters"""

        results = list(self.transactions.values())

        if start_date:
            results = [t for t in results if t.date >= start_date]

        if end_date:
            results = [t for t in results if t.date <= end_date]

        if transaction_type:
            results = [t for t in results if t.transaction_type == transaction_type]

        if category:
            results = [t for t in results if t.category == category]

        return sorted(results, key=lambda x: x.date, reverse=True)

    def generate_profit_loss_report(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> FinancialReport:
        """Generate profit & loss statement"""

        transactions = self.get_transactions(start_date, end_date)

        income_by_category: Dict[str, Decimal] = {}
        expenses_by_category: Dict[str, Decimal] = {}
        total_income = Decimal('0.00')
        total_expenses = Decimal('0.00')
        tax_deductible_expenses = Decimal('0.00')

        for txn in transactions:
            if txn.transaction_type == TransactionType.INCOME:
                total_income += txn.amount
                income_by_category[txn.category] = income_by_category.get(txn.category, Decimal('0.00')) + txn.amount

            elif txn.transaction_type == TransactionType.EXPENSE:
                total_expenses += txn.amount
                expenses_by_category[txn.category] = expenses_by_category.get(txn.category, Decimal('0.00')) + txn.amount

                if txn.tax_deductible:
                    # Meals are only 50% deductible
                    if "Meals" in txn.category:
                        tax_deductible_expenses += txn.amount * Decimal('0.5')
                    else:
                        tax_deductible_expenses += txn.amount

        net_profit = total_income - total_expenses

        report = FinancialReport(
            report_id=f"report_{int(datetime.now().timestamp())}",
            report_type="Profit & Loss",
            start_date=start_date,
            end_date=end_date,
            total_income=total_income,
            total_expenses=total_expenses,
            net_profit=net_profit,
            income_by_category=income_by_category,
            expenses_by_category=expenses_by_category,
            tax_deductible_expenses=tax_deductible_expenses,
            generated_at=datetime.now()
        )

        return report

    def calculate_estimated_taxes(self, net_profit: Decimal) -> Dict[str, Decimal]:
        """Calculate estimated tax liability"""

        if net_profit <= 0:
            return {
                "federal_income_tax": Decimal('0.00'),
                "self_employment_tax": Decimal('0.00'),
                "state_income_tax": Decimal('0.00'),
                "total_tax_liability": Decimal('0.00')
            }

        # Calculate taxes
        federal_income_tax = net_profit * Decimal(str(self.tax_rates["federal_income"]))
        self_employment_tax = net_profit * Decimal(str(self.tax_rates["self_employment"]))
        state_income_tax = net_profit * Decimal(str(self.tax_rates["state_income"]))

        total_tax = federal_income_tax + self_employment_tax + state_income_tax

        return {
            "federal_income_tax": round(federal_income_tax, 2),
            "self_employment_tax": round(self_employment_tax, 2),
            "state_income_tax": round(state_income_tax, 2),
            "total_tax_liability": round(total_tax, 2),
            "effective_tax_rate": round((total_tax / net_profit) * 100, 2) if net_profit > 0 else Decimal('0.00')
        }

    def export_to_quickbooks(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """Export transactions to QuickBooks format"""
        # QuickBooks IIF format structure
        export_data = {
            "format": "IIF",
            "transactions": [],
            "export_date": datetime.now().isoformat()
        }

        for txn in transactions:
            export_data["transactions"].append({
                "date": txn.date.strftime("%m/%d/%Y"),
                "type": "GENERAL JOURNAL",
                "name": txn.vendor,
                "memo": txn.description,
                "amount": str(txn.amount),
                "account": txn.category,
                "txn_id": txn.transaction_id
            })

        return export_data

    def export_to_xero(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """Export transactions to Xero format"""
        export_data = {
            "format": "Xero",
            "transactions": [],
            "export_date": datetime.now().isoformat()
        }

        for txn in transactions:
            export_data["transactions"].append({
                "Date": txn.date.isoformat(),
                "Amount": str(txn.amount),
                "Payee": txn.vendor,
                "Description": txn.description,
                "Reference": txn.transaction_id,
                "Account": txn.category,
                "TaxType": "Tax Exempt" if not txn.tax_deductible else "Tax on Purchases"
            })

        return export_data

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary of financial health"""

        # Current month
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        month_end = now

        # Current year
        year_start = datetime(now.year, 1, 1)

        # Generate reports
        month_report = self.generate_profit_loss_report(month_start, month_end)
        year_report = self.generate_profit_loss_report(year_start, month_end)

        # Calculate taxes
        year_taxes = self.calculate_estimated_taxes(year_report.net_profit)

        return {
            "current_month": {
                "income": float(month_report.total_income),
                "expenses": float(month_report.total_expenses),
                "profit": float(month_report.net_profit)
            },
            "year_to_date": {
                "income": float(year_report.total_income),
                "expenses": float(year_report.total_expenses),
                "profit": float(year_report.net_profit),
                "tax_deductible_expenses": float(year_report.tax_deductible_expenses)
            },
            "estimated_taxes": {
                "federal": float(year_taxes["federal_income_tax"]),
                "self_employment": float(year_taxes["self_employment_tax"]),
                "state": float(year_taxes["state_income_tax"]),
                "total": float(year_taxes["total_tax_liability"])
            },
            "top_expense_categories": [
                {"category": k, "amount": float(v)}
                for k, v in sorted(
                    month_report.expenses_by_category.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            ],
            "total_transactions": len(self.transactions),
            "total_receipts": len(self.receipts)
        }


def demo_bookkeeping_system():
    """Demo function showing bookkeeping capabilities"""
    print("=" * 70)
    print("Automated Bookkeeping System - Demo")
    print("=" * 70)

    # Initialize system
    system = AutomatedBookkeepingSystem()

    # Create sample transactions
    print("\n📝 Creating sample transactions...")

    # Income
    system.create_transaction(
        date=datetime(2024, 11, 1),
        amount=Decimal('5000.00'),
        transaction_type=TransactionType.INCOME,
        category=IncomeCategory.SERVICES.value,
        vendor="Client ABC Corp",
        description="Consulting services for November",
        payment_method="Bank Transfer"
    )

    # Expenses
    expenses = [
        {
            "date": datetime(2024, 11, 2),
            "amount": Decimal('89.99'),
            "category": ExpenseCategory.SOFTWARE.value,
            "vendor": "Adobe Creative Cloud",
            "description": "Monthly subscription",
            "tax_deductible": True
        },
        {
            "date": datetime(2024, 11, 3),
            "amount": Decimal('45.50'),
            "category": ExpenseCategory.MEALS.value,
            "vendor": "Starbucks",
            "description": "Client meeting",
            "tax_deductible": True
        },
        {
            "date": datetime(2024, 11, 4),
            "amount": Decimal('1200.00'),
            "category": ExpenseCategory.RENT.value,
            "vendor": "Office Space LLC",
            "description": "November office rent",
            "tax_deductible": True
        },
        {
            "date": datetime(2024, 11, 5),
            "amount": Decimal('299.00'),
            "category": ExpenseCategory.ADVERTISING.value,
            "vendor": "Google Ads",
            "description": "November ad campaign",
            "tax_deductible": True
        }
    ]

    for expense in expenses:
        system.create_transaction(
            date=expense["date"],
            amount=expense["amount"],
            transaction_type=TransactionType.EXPENSE,
            category=expense["category"],
            vendor=expense["vendor"],
            description=expense["description"],
            payment_method="Credit Card",
            tax_deductible=expense["tax_deductible"]
        )

    print(f"✅ Created {len(system.transactions)} transactions")

    # Generate P&L Report
    print("\n" + "=" * 70)
    print("Profit & Loss Report - November 2024")
    print("=" * 70)

    report = system.generate_profit_loss_report(
        datetime(2024, 11, 1),
        datetime(2024, 11, 30)
    )

    print(f"\n💰 Total Income: ${report.total_income:,.2f}")
    print(f"💸 Total Expenses: ${report.total_expenses:,.2f}")
    print(f"📊 Net Profit: ${report.net_profit:,.2f}")
    print(f"🏷️  Tax Deductible Expenses: ${report.tax_deductible_expenses:,.2f}")

    print("\n📈 Income by Category:")
    for category, amount in report.income_by_category.items():
        print(f"  • {category}: ${amount:,.2f}")

    print("\n📉 Expenses by Category:")
    for category, amount in report.expenses_by_category.items():
        print(f"  • {category}: ${amount:,.2f}")

    # Calculate taxes
    print("\n" + "=" * 70)
    print("Estimated Tax Liability")
    print("=" * 70)

    taxes = system.calculate_estimated_taxes(report.net_profit)
    print(f"\n🇺🇸 Federal Income Tax: ${taxes['federal_income_tax']:,.2f}")
    print(f"👔 Self-Employment Tax: ${taxes['self_employment_tax']:,.2f}")
    print(f"🏛️  State Income Tax: ${taxes['state_income_tax']:,.2f}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"💵 Total Tax Liability: ${taxes['total_tax_liability']:,.2f}")
    print(f"📊 Effective Tax Rate: {taxes['effective_tax_rate']}%")

    # Dashboard summary
    print("\n" + "=" * 70)
    print("Dashboard Summary")
    print("=" * 70)

    dashboard = system.get_dashboard_summary()
    print(json.dumps(dashboard, indent=2))

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_bookkeeping_system()
