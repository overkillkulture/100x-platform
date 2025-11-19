/**
 * STRIPE CHECKOUT API
 * Backend endpoint for creating Stripe checkout sessions
 * Usage: POST /api/stripe/create-checkout
 */

const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY || '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'); // LIVE KEY
const router = express.Router();

/**
 * Create Stripe Checkout Session
 * POST /api/stripe/create-checkout
 */
router.post('/api/stripe/create-checkout', async (req, res) => {
    try {
        const { items, successUrl, cancelUrl } = req.body;

        // Validate items
        if (!items || !Array.isArray(items) || items.length === 0) {
            return res.status(400).json({ error: 'Invalid cart items' });
        }

        // Convert cart items to Stripe line items
        const lineItems = items.map(item => ({
            price_data: {
                currency: 'usd',
                product_data: {
                    name: item.name,
                    description: item.description || '',
                    images: item.image ? [item.image] : [],
                },
                unit_amount: Math.round(item.price * 100), // Convert to cents
            },
            quantity: item.quantity || 1,
        }));

        // Create Checkout Session
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            line_items: lineItems,
            mode: 'payment',
            success_url: successUrl,
            cancel_url: cancelUrl,
            metadata: {
                userId: req.user?.id || 'guest',
                timestamp: new Date().toISOString()
            }
        });

        res.json({
            id: session.id,
            url: session.url
        });

    } catch (error) {
        console.error('Stripe checkout error:', error);
        res.status(500).json({ error: error.message });
    }
});

/**
 * Stripe Webhook Handler
 * POST /api/stripe/webhook
 * Handles events from Stripe (payment success, failure, etc.)
 */
router.post('/api/stripe/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

    let event;

    try {
        event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
    } catch (err) {
        console.error('Webhook signature verification failed:', err.message);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Handle the event
    switch (event.type) {
        case 'checkout.session.completed':
            const session = event.data.object;
            console.log('✓ Payment successful:', session.id);
            // TODO: Fulfill the order (send products, unlock content, etc.)
            await fulfillOrder(session);
            break;

        case 'checkout.session.expired':
            console.log('⚠ Checkout session expired:', event.data.object.id);
            break;

        case 'payment_intent.succeeded':
            console.log('✓ Payment intent succeeded:', event.data.object.id);
            break;

        case 'payment_intent.payment_failed':
            console.log('❌ Payment failed:', event.data.object.id);
            break;

        default:
            // 🛡️ SECURITY: Log event type only (not full event data)
            console.log(`Unhandled Stripe event: ${event.type}`);
    }

    res.json({ received: true });
});

/**
 * Fulfill order after successful payment
 */
async function fulfillOrder(session) {
    try {
        // Get session details
        const lineItems = await stripe.checkout.sessions.listLineItems(session.id);

        // 🛡️ SECURITY: Removed customer email and items logging (PII/PCI disclosure)
        console.log('Fulfilling order for session:', session.id);

        // TODO: Implement order fulfillment
        // - Send digital products via email
        // - Update database with purchase records
        // - Grant access to modules
        // - Send confirmation email
        // - Update user's account with purchased items

        // Example: Send email
        // await sendOrderConfirmation(session.customer_details.email, lineItems);

        console.log('✓ Order fulfilled successfully');

    } catch (error) {
        console.error('Order fulfillment error:', error);
        // TODO: Log to monitoring system for manual review
    }
}

/**
 * Get customer's purchase history
 * GET /api/stripe/purchases
 */
router.get('/api/stripe/purchases', async (req, res) => {
    try {
        const userId = req.user?.id;
        if (!userId) {
            return res.status(401).json({ error: 'Unauthorized' });
        }

        // Get customer's payment history from Stripe
        // TODO: Implement lookup by userId
        // For now, return empty array
        res.json({ purchases: [] });

    } catch (error) {
        console.error('Purchase history error:', error);
        res.status(500).json({ error: error.message });
    }
});

/**
 * Refund a payment
 * POST /api/stripe/refund
 */
router.post('/api/stripe/refund', async (req, res) => {
    try {
        const { paymentIntentId, amount, reason } = req.body;

        // Only admin can issue refunds
        if (!req.user?.isAdmin) {
            return res.status(403).json({ error: 'Forbidden' });
        }

        const refund = await stripe.refunds.create({
            payment_intent: paymentIntentId,
            amount: amount, // Amount in cents, or omit for full refund
            reason: reason || 'requested_by_customer'
        });

        res.json({ success: true, refund });

    } catch (error) {
        console.error('Refund error:', error);
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
