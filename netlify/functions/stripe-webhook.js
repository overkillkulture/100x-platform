// Stripe Webhook Handler
// Handles payment confirmations and creates user accounts

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event, context) => {
  const sig = event.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let stripeEvent;

  try {
    // Verify webhook signature
    stripeEvent = stripe.webhooks.constructEvent(
      event.body,
      sig,
      webhookSecret
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Webhook signature verification failed' })
    };
  }

  // Handle the event
  switch (stripeEvent.type) {
    case 'checkout.session.completed':
      const session = stripeEvent.data.object;
      console.log('Payment successful:', session.id);

      // TODO: Create user account in database
      // For now, log the details
      const customerEmail = session.customer_email;
      const tier = session.metadata.tier;
      const name = session.metadata.name;

      console.log('New user signup:', {
        email: customerEmail,
        name: name,
        tier: tier,
        subscriptionId: session.subscription,
        customerId: session.customer
      });

      // TODO: Send welcome email
      // TODO: Grant platform access

      break;

    case 'customer.subscription.deleted':
      const subscription = stripeEvent.data.object;
      console.log('Subscription cancelled:', subscription.id);

      // TODO: Revoke platform access
      // TODO: Send cancellation email

      break;

    case 'invoice.payment_failed':
      const invoice = stripeEvent.data.object;
      console.log('Payment failed:', invoice.id);

      // TODO: Send payment failed email
      // TODO: Suspend account if needed

      break;

    default:
      console.log(`Unhandled event type: ${stripeEvent.type}`);
  }

  return {
    statusCode: 200,
    body: JSON.stringify({ received: true })
  };
};
