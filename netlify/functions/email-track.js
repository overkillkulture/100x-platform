// 📧 Email Open Tracking - Pixel System
// Tiny 1x1 transparent image that tracks when emails are opened

exports.handler = async (event, context) => {
  const queryParams = new URLSearchParams(event.queryStringParameters || {});
  const recipient = queryParams.get('r') || 'unknown';
  const campaign = queryParams.get('c') || 'beta_invite';

  // Log the email open
  const openData = {
    timestamp: new Date().toISOString(),
    recipient: recipient,
    campaign: campaign,
    ip: event.headers['x-forwarded-for'] || 'unknown',
    user_agent: event.headers['user-agent'] || 'unknown'
  };

  // Send notification to Commander
  try {
    await fetch('https://conciousnessrevolution.io/.netlify/functions/instant-notifications', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: 'email_open',
        data: {
          recipient: recipient,
          subject: campaign,
          ...openData
        }
      })
    });
  } catch (e) {
    console.log('Notification failed:', e);
  }

  // Return 1x1 transparent pixel
  const pixel = Buffer.from(
    'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
    'base64'
  );

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'image/gif',
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    },
    body: pixel.toString('base64'),
    isBase64Encoded: true
  };
};
