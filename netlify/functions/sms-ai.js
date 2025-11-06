// 📱 SMS AI - Text to get AI responses
// Twilio webhook → ChatGPT → Reply

const https = require('https');

// Log to convergence hub
async function logToConvergence(data) {
  try {
    // TODO: Implement convergence logging
    console.log('[CONVERGENCE]', data);
  } catch (error) {
    console.error('Failed to log to convergence:', error);
  }
}

// Call ChatGPT API
async function callChatGPT(message, from) {
  const apiKey = process.env.OPENAI_API_KEY;

  if (!apiKey) {
    return "OpenAI API key not configured. Add OPENAI_API_KEY to environment variables.";
  }

  const prompt = `You are Commander's AI assistant accessible via SMS. Be concise (160 chars max).

Context: This is part of an omnipresent AI mesh network. Commander can text you from anywhere.

User: ${message}

Respond helpfully and briefly:`;

  const requestData = JSON.stringify({
    model: "gpt-4",
    messages: [
      {role: "system", content: "You are a concise AI assistant responding via SMS. Keep responses under 160 characters."},
      {role: "user", content: message}
    ],
    max_tokens: 100,
    temperature: 0.7
  });

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.openai.com',
      port: 443,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': requestData.length
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (response.choices && response.choices[0]) {
            resolve(response.choices[0].message.content.trim());
          } else {
            resolve("AI response error. Check logs.");
          }
        } catch (error) {
          resolve("Failed to parse AI response.");
        }
      });
    });

    req.on('error', (error) => {
      console.error('ChatGPT API error:', error);
      resolve("AI temporarily unavailable. Try again.");
    });

    req.write(requestData);
    req.end();
  });
}

exports.handler = async (event, context) => {
  try {
    // Parse Twilio webhook data
    const body = new URLSearchParams(event.body);
    const from = body.get('From');
    const message = body.get('Body');
    const to = body.get('To');

    console.log(`[SMS] From: ${from}, Message: ${message}`);

    // Log to convergence
    await logToConvergence({
      source: 'sms',
      channel: 'twilio',
      from: from,
      to: to,
      input: message,
      timestamp: new Date().toISOString()
    });

    // Special commands
    let response;

    if (message.toLowerCase().includes('status')) {
      response = "Trinity Status: 9 instances active. Convergence system building. Phone endpoint deployed. ✅";
    } else if (message.toLowerCase().includes('help')) {
      response = "Commands: STATUS, HELP. Or just ask anything! This is your omnipresent AI assistant. 🔺";
    } else {
      // Get AI response
      response = await callChatGPT(message, from);
    }

    // Log response
    await logToConvergence({
      source: 'sms',
      channel: 'twilio',
      to: from,
      output: response,
      timestamp: new Date().toISOString()
    });

    // Return TwiML response
    const twiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>${response}</Message>
</Response>`;

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/xml'
      },
      body: twiml
    };

  } catch (error) {
    console.error('SMS AI error:', error);

    const errorTwiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Error processing request. Try again.</Message>
</Response>`;

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/xml'
      },
      body: errorTwiml
    };
  }
};
