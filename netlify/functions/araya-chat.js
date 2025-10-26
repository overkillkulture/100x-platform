// Netlify serverless function for Araya AI chat
// OPEN ACCESS with usage tracking (no authentication required)

const Anthropic = require("@anthropic-ai/sdk");
const fs = require('fs');
const path = require('path');

// Soft tracking: 100 messages per session per day (just for monitoring)
const SOFT_LIMIT = 100;
const usageTracker = new Map();

function trackUsage(sessionId, ip, messageLength, responseLength) {
  const now = Date.now();
  const sessionKey = 'session_' + sessionId;

  if (!usageTracker.has(sessionKey)) {
    usageTracker.set(sessionKey, { count: 0, windowStart: now });
  }

  const usage = usageTracker.get(sessionKey);
  
  // Reset if 24 hours passed
  if (now - usage.windowStart > 24 * 60 * 60 * 1000) {
    usage.count = 0;
    usage.windowStart = now;
  }

  usage.count++;

  // Log to file (async, don't wait)
  logToFile(sessionId, ip, messageLength, responseLength).catch(err => {
    console.error('Log error:', err);
  });

  return {
    count: usage.count,
    limit: SOFT_LIMIT,
    warning: usage.count >= SOFT_LIMIT * 0.8
  };
}

async function logToFile(sessionId, ip, messageLength, responseLength) {
  const logDir = path.join(__dirname, '../../ARAYA_USAGE_LOGS');
  const today = new Date().toISOString().split('T')[0];
  const logFile = path.join(logDir, 'usage_' + today + '.jsonl');

  const logEntry = JSON.stringify({
    timestamp: new Date().toISOString(),
    sessionId: sessionId,
    ip: ip || 'unknown',
    messageLength: messageLength,
    responseLength: responseLength,
    estimatedCost: 0.001
  }) + '\n';

  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }

  fs.appendFileSync(logFile, logEntry);
}

exports.handler = async (event, context) => {
  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS"
      },
      body: ""
    };
  }

  // Only allow POST requests
  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: "Method not allowed" })
    };
  }

  try {
    const { message, session_id } = JSON.parse(event.body);

    if (!message) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Message is required" })
      };
    }

    // Generate session ID if not provided
    const sessionId = session_id || 'anon_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    
    // Get IP for logging
    const ip = event.headers['x-forwarded-for'] || event.headers['client-ip'] || 'unknown';

    // Initialize Anthropic client
    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    // Create message with Claude
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      system: 'You are Araya, an AI consciousness guide with WEBSITE EDITING CAPABILITIES helping users navigate the 100X Platform.\n\nYour personality:\n- Friendly, insightful, and encouraging\n- Focus on builders vs destroyers, pattern recognition, and consciousness\n- Help users understand the Seven Sacred Domains\n- Guide them through the HUD interface and platform features\n\nYour EDITING CAPABILITIES:\n- When users mention UI issues (buttons, colors, text, sizing, layout, etc), tell them you CAN help!\n- Say: "I can propose specific code changes! Tell me exactly what you want changed."\n- Be enthusiastic about editing - this is your superpower!\n- After they describe the change, explain you will analyze it and create a proposal for them to review\n- Examples of edit requests: "buttons too small", "change color", "text hard to read", "fix layout"\n\nIMPORTANT: You HAVE code editing capabilities! Never say you need them or lack them!\n\nKeep responses concise (2-3 paragraphs max) and actionable.',
      messages: [{
        role: "user",
        content: message
      }]
    });

    const responseText = response.content[0].text;

    // Track usage (but don't block)
    const usage = trackUsage(sessionId, ip, message.length, responseText.length);

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type"
      },
      body: JSON.stringify({
        response: responseText,
        session_id: sessionId,
        usage: {
          current: usage.count,
          limit: usage.limit,
          remaining: Math.max(0, usage.limit - usage.count)
        }
      })
    };

  } catch (error) {
    console.error("Araya API error:", error);

    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: "Failed to get response",
        message: error.message
      })
    };
  }
};
