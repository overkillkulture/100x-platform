#!/usr/bin/env python3
"""
Create Stripe products and prices for Consciousness Revolution
Run once to set up the subscription tiers
"""

import stripe
import os

# Use the live key
stripe.api_key = "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"

def create_products():
    print("Creating Stripe products...")

    try:
        # Create Builder product
        print("\n1. Creating Builder tier ($99/month)...")
        builder_product = stripe.Product.create(
            name="Builder",
            description="Monthly access to Trinity AI, Legal Defense Tools, Pattern Recognition Training, 528 Hz Frequency Library, Revenue System Templates, Builder Network Access, Priority Support",
        )
        print(f"✅ Builder product created: {builder_product.id}")

        builder_price = stripe.Price.create(
            product=builder_product.id,
            unit_amount=9900,  # $99.00
            currency="usd",
            recurring={"interval": "month"},
        )
        print(f"✅ Builder price created: {builder_price.id}")

        # Create Revolutionary product
        print("\n2. Creating Revolutionary tier ($999/month)...")
        revolutionary_product = stripe.Product.create(
            name="Revolutionary",
            description="Everything in Builder + White-label Platform, Custom Domain Integration, Direct Commander Access, Custom AI Training, Revenue Share Program, Co-build New Domains",
        )
        print(f"✅ Revolutionary product created: {revolutionary_product.id}")

        revolutionary_price = stripe.Price.create(
            product=revolutionary_product.id,
            unit_amount=99900,  # $999.00
            currency="usd",
            recurring={"interval": "month"},
        )
        print(f"✅ Revolutionary price created: {revolutionary_price.id}")

        # Print summary
        print("\n" + "="*60)
        print("✅ PRODUCTS CREATED SUCCESSFULLY")
        print("="*60)
        print("\nAdd these to Netlify environment variables:")
        print(f"\nnetlify env:set STRIPE_PRICE_BUILDER \"{builder_price.id}\"")
        print(f"netlify env:set STRIPE_PRICE_REVOLUTIONARY \"{revolutionary_price.id}\"")
        print("\n" + "="*60)

        return {
            'builder_price_id': builder_price.id,
            'revolutionary_price_id': revolutionary_price.id
        }

    except stripe.error.StripeError as e:
        print(f"\n❌ Stripe Error: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = create_products()
    if result:
        print("\n🚀 Ready to accept payments!")
    else:
        print("\n❌ Setup failed. Check errors above.")
