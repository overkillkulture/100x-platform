// SMS Bug Report via Twilio
// Beta testers text bugs to phone number → Creates GitHub issue

export const handler = async (event, context) => {
  console.log('📱 SMS RECEIVED');
  console.log('Full event:', JSON.stringify(event, null, 2));

  try {
    // Parse Twilio POST data (form-encoded)
    const params = new URLSearchParams(event.body);

    const from = params.get('From'); // Sender's phone number
    const body = params.get('Body'); // Message text
    const messageSid = params.get('MessageSid');

    console.log(`From: ${from}`);
    console.log(`Message: ${body}`);

    // Parse bug from SMS
    // Format: "BUG: title\nDETAILS: description"
    // Or just send any text and we'll create bug from it

    let title = 'Bug via SMS';
    let description = body;

    // Try to parse structured format
    if (body.includes('BUG:') || body.includes('Bug:') || body.includes('bug:')) {
      const lines = body.split('\n');
      const bugLine = lines.find(l => l.toLowerCase().includes('bug:'));
      if (bugLine) {
        title = bugLine.replace(/bug:/i, '').trim();
      }

      const detailsLine = lines.find(l => l.toLowerCase().includes('details:'));
      if (detailsLine) {
        description = detailsLine.replace(/details:/i, '').trim();
      } else {
        // Everything after title is description
        const titleIndex = lines.findIndex(l => l.toLowerCase().includes('bug:'));
        if (titleIndex >= 0 && titleIndex < lines.length - 1) {
          description = lines.slice(titleIndex + 1).join('\n').trim();
        }
      }
    }

    // Create GitHub issue
    console.log('Creating GitHub issue...');

    const githubResponse = await fetch(
      `https://api.github.com/repos/${process.env.GITHUB_REPO}/issues`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: title || 'Bug via SMS',
          body: `**Bug reported via SMS**

**From:** ${from}

**Message:**
${description || body}

**Message ID:** ${messageSid}
**Received:** ${new Date().toISOString()}`
        })
      }
    );

    if (githubResponse.ok) {
      const issue = await githubResponse.json();
      console.log(`✅ GitHub issue created: #${issue.number}`);

      // Send SMS confirmation back to user
      const confirmationMessage = `✅ Bug received!
Issue #${issue.number} created.
View: ${issue.html_url}

Thank you!`;

      // Use Twilio to send reply
      const twilioResponse = await fetch(
        `https://api.twilio.com/2010-04-01/Accounts/${process.env.TWILIO_ACCOUNT_SID}/Messages.json`,
        {
          method: 'POST',
          headers: {
            'Authorization': 'Basic ' + Buffer.from(
              `${process.env.TWILIO_ACCOUNT_SID}:${process.env.TWILIO_AUTH_TOKEN}`
            ).toString('base64'),
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({
            From: params.get('To'), // Our Twilio number
            To: from, // Send back to user
            Body: confirmationMessage
          })
        }
      );

      if (twilioResponse.ok) {
        console.log('✅ Confirmation SMS sent');
      } else {
        console.log('⚠️  Failed to send confirmation SMS');
      }

      // Return TwiML response (Twilio expects XML)
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'text/xml'
        },
        body: `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>✅ Bug received! Issue #${issue.number} created. Thank you!</Message>
</Response>`
      };

    } else {
      const error = await githubResponse.text();
      console.error('GitHub API error:', error);

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'text/xml'
        },
        body: `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>❌ Error creating bug. Please try again or contact support.</Message>
</Response>`
      };
    }

  } catch (error) {
    console.error('Error:', error);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/xml'
      },
      body: `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>❌ Error processing message. Please try again.</Message>
</Response>`
    };
  }
};
