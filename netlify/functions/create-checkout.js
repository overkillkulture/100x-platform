// Stripe Checkout Session Creator
// Creates a Stripe checkout session for paid tier signups

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle OPTIONS request (CORS preflight)
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { name, email, password, tier, price } = JSON.parse(event.body);

    // Validate required fields
    if (!name || !email || !password || !tier || price === undefined) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Missing required fields' })
      };
    }

    // For free tier, just return success (no payment needed)
    if (tier === 'free' || price === 0) {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          tier: 'free',
          message: 'Free account created successfully'
        })
      };
    }

    // Price mapping
    const priceIds = {
      'builder': process.env.STRIPE_PRICE_BUILDER || 'price_builder_99',
      'revolutionary': process.env.STRIPE_PRICE_REVOLUTIONARY || 'price_revolutionary_999'
    };

    const priceId = priceIds[tier];

    if (!priceId) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid tier selected' })
      };
    }

    // Create Stripe Checkout Session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'subscription',
      customer_email: email,
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      success_url: `${process.env.URL || 'https://conciousnessrevolution.io'}/signup-success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.URL || 'https://conciousnessrevolution.io'}/signup.html?tier=${tier}`,
      metadata: {
        name: name,
        tier: tier,
        // Note: Don't store password in Stripe metadata
        // Handle user creation separately after payment confirmation
      },
      // Allow promotion codes
      allow_promotion_codes: true,
      // Billing address collection
      billing_address_collection: 'required',
      // Subscription data
      subscription_data: {
        trial_period_days: 0, // No trial for now
        metadata: {
          tier: tier,
          customer_name: name
        }
      }
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        sessionId: session.id,
        url: session.url
      })
    };

  } catch (error) {
    console.error('Stripe Checkout Error:', error);

    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Failed to create checkout session',
        message: error.message
      })
    };
  }
};
