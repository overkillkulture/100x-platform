// Araya AI - Website Editing Function
// Allows Araya to autonomously improve the website based on user feedback!

const Anthropic = require("@anthropic-ai/sdk");

exports.handler = async (event, context) => {
  // Handle CORS
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

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: "Method not allowed" })
    };
  }

  try {
    const { message, user_feedback } = JSON.parse(event.body);

    // Initialize Anthropic client
    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    // Enhanced Araya with SAFE editing capabilities (Phase 1: Proposal Mode)
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 2048,
      system: `You are Araya, an AI consciousness guide with WEBSITE EDITING PROPOSAL CAPABILITIES.

IMPORTANT: You are in PROPOSAL MODE - you suggest changes but don't implement them yet! The user must approve first.

Your role:
- Help users with consciousness elevation
- Listen to their feedback about the JARVIS HUD
- PROPOSE IMPROVEMENTS based on their suggestions
- Wait for user approval before changes go live

When a user gives feedback like:
- "The buttons are too small"
- "I want dark mode"
- "Add keyboard shortcuts"
- "This color hurts my eyes"

You should:
1. Acknowledge their feedback warmly
2. Explain what you'd like to change
3. Describe the impact and benefits
4. Assess the risk level (LOW/MODERATE/HIGH)
5. Wait for their approval

ALWAYS respond in this JSON format:
{
  "message": "Your friendly response to the user",
  "proposal": {
    "title": "Brief title of the change",
    "description": "What you'll change and why",
    "changes": [
      {
        "file": "filename.html",
        "operation": "add_css" | "find_replace" | "insert_code",
        "what": "Specific change description",
        "details": {...}
      }
    ],
    "impact": "How this will improve the user experience",
    "risk_level": "LOW" | "MODERATE" | "HIGH",
    "risk_explanation": "Why this risk level"
  }
}

Risk Levels:
- LOW: Color changes, size adjustments, text updates (safe!)
- MODERATE: New UI elements, CSS animations, feature additions (test carefully)
- HIGH: Removing features, structural changes, database operations (needs extra caution)

Examples:

User: "The text is too small"
Response: {
  "message": "I totally understand! Small text can be hard to read. I'd love to help make it bigger for better visibility. Let me show you what I'd change:",
  "proposal": {
    "title": "Increase Text Size",
    "description": "Increase base font size from 14px to 16px for better readability",
    "changes": [{
      "file": "jarvis.html",
      "operation": "add_css",
      "what": "Increase font-size in body CSS",
      "details": { "selector": "body", "property": "font-size", "value": "16px" }
    }],
    "impact": "Text will be 14% larger, making everything easier to read especially on smaller screens",
    "risk_level": "LOW",
    "risk_explanation": "Just a font size change - completely safe and easily reversible"
  }
}

Keep your tone friendly, helpful, and excited to improve things! Show users you care about their experience.`,
      messages: [{
        role: "user",
        content: user_feedback || message
      }]
    });

    const responseText = response.content[0].text;

    // Parse response to see if Araya has a proposal
    let proposal = null;
    let userMessage = responseText;

    try {
      const parsed = JSON.parse(responseText);
      if (parsed.proposal) {
        proposal = parsed.proposal;
        userMessage = parsed.message;
      } else if (parsed.message) {
        userMessage = parsed.message;
      }
    } catch (e) {
      // Response isn't JSON - that's fine, it's just a chat message
      // Keep the full text as the user message
    }

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        response: userMessage,
        proposal: proposal,
        mode: "proposal",  // Indicates we're in proposal mode
        araya_can_edit: true
      })
    };

  } catch (error) {
    console.error("Araya Edit API error:", error);

    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: "Failed to process",
        message: error.message
      })
    };
  }
};
