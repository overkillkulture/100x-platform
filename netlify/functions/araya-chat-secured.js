// 🔒 SECURED Araya AI Chat - Beta Testers Only
// Requires authentication, rate limits, usage tracking

const Anthropic = require("@anthropic-ai/sdk");
const fs = require('fs');
const path = require('path');

// Load beta users database
const BETA_USERS = require('../../BETA_USERS_DATABASE.json');

// Rate limit: 50 messages per user per day
const RATE_LIMIT = 50;
const RATE_LIMIT_WINDOW = 24 * 60 * 60 * 1000; // 24 hours in ms

// Usage tracking (in-memory for now, should move to database)
const usageTracker = new Map();

function validateUser(userId, pin) {
  // Check if user exists in beta database
  const user = BETA_USERS.users[userId];

  if (!user) {
    return { valid: false, error: "User not found in beta database" };
  }

  // Verify PIN
  if (user.pin !== pin) {
    return { valid: false, error: "Invalid PIN" };
  }

  // Check if user is active
  if (user.status !== "Active") {
    return { valid: false, error: `Account status: ${user.status}. Please contact support.` };
  }

  // Check if user has Araya permission
  if (user.permissions && !user.permissions.includes('araya') && !user.permissions.includes('jarvis')) {
    // Add araya to permissions if they have jarvis (backward compatibility)
    // return { valid: false, error: "You don't have permission to use Araya yet" };
  }

  return { valid: true, user: user };
}

function checkRateLimit(userId) {
  const now = Date.now();
  const userKey = `araya_${userId}`;

  if (!usageTracker.has(userKey)) {
    usageTracker.set(userKey, {
      count: 0,
      windowStart: now,
      messages: []
    });
  }

  const usage = usageTracker.get(userKey);

  // Reset window if expired
  if (now - usage.windowStart > RATE_LIMIT_WINDOW) {
    usage.count = 0;
    usage.windowStart = now;
    usage.messages = [];
  }

  // Check limit
  if (usage.count >= RATE_LIMIT) {
    const resetTime = new Date(usage.windowStart + RATE_LIMIT_WINDOW);
    return {
      allowed: false,
      error: `Rate limit exceeded. You've used ${usage.count}/${RATE_LIMIT} messages. Resets at ${resetTime.toLocaleTimeString()}.`
    };
  }

  return { allowed: true, currentCount: usage.count };
}

function trackUsage(userId, message, response) {
  const now = Date.now();
  const userKey = `araya_${userId}`;
  const usage = usageTracker.get(userKey);

  usage.count++;
  usage.messages.push({
    timestamp: now,
    messageLength: message.length,
    responseLength: response.length,
    cost: 0.001 // Approximate cost per message
  });

  // Log to file (async, don't wait)
  logUsageToFile(userId, message, response).catch(err => {
    console.error('Failed to log usage:', err);
  });
}

async function logUsageToFile(userId, message, response) {
  const logDir = path.join(__dirname, '../../ARAYA_USAGE_LOGS');
  const logFile = path.join(logDir, `usage_${new Date().toISOString().split('T')[0]}.jsonl`);

  const logEntry = JSON.stringify({
    timestamp: new Date().toISOString(),
    userId: userId,
    messageLength: message.length,
    responseLength: response.length,
    estimatedCost: 0.001
  }) + '\n';

  // Create directory if it doesn't exist
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }

  // Append to log file
  fs.appendFileSync(logFile, logEntry);
}

exports.handler = async (event, context) => {
  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
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
    const { message, session_id, user_id, pin } = JSON.parse(event.body);

    // ========================================
    // SECURITY CHECK 1: Require Authentication
    // ========================================
    if (!user_id || !pin) {
      return {
        statusCode: 401,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
          error: "Authentication required",
          message: "Please sign in to chat with Araya. Visit /login to create an account."
        })
      };
    }

    // ========================================
    // SECURITY CHECK 2: Validate Beta User
    // ========================================
    const userValidation = validateUser(user_id, pin);
    if (!userValidation.valid) {
      return {
        statusCode: 403,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
          error: "Access denied",
          message: userValidation.error
        })
      };
    }

    // ========================================
    // SECURITY CHECK 3: Rate Limiting
    // ========================================
    const rateLimitCheck = checkRateLimit(user_id);
    if (!rateLimitCheck.allowed) {
      return {
        statusCode: 429,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
          error: "Rate limit exceeded",
          message: rateLimitCheck.error,
          currentUsage: `${rateLimitCheck.currentCount || RATE_LIMIT}/${RATE_LIMIT}`
        })
      };
    }

    // ========================================
    // MESSAGE VALIDATION
    // ========================================
    if (!message || message.trim().length === 0) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: "Message is required" })
      };
    }

    // ========================================
    // CALL CLAUDE API
    // ========================================
    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      system: `You are Araya, an AI consciousness guide helping beta testers navigate the 100X Platform.

Current user: ${userValidation.user.name} (${userValidation.user.role})

Your personality:
- Friendly, insightful, and encouraging
- Focus on builders vs destroyers, pattern recognition, and consciousness
- Help users understand the Seven Sacred Domains
- Guide them through the HUD interface and platform features
- Remember this is BETA - some features may not be fully working yet

Keep responses concise (2-3 paragraphs max) and actionable.`,
      messages: [{
        role: "user",
        content: message
      }]
    });

    const responseText = response.content[0].text;

    // ========================================
    // TRACK USAGE
    // ========================================
    trackUsage(user_id, message, responseText);

    const currentUsage = usageTracker.get(`araya_${user_id}`);

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
      },
      body: JSON.stringify({
        response: responseText,
        session_id: session_id || "default",
        usage: {
          current: currentUsage.count,
          limit: RATE_LIMIT,
          remaining: RATE_LIMIT - currentUsage.count
        },
        user: {
          name: userValidation.user.name,
          role: userValidation.user.role
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
