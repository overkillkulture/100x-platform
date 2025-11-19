// Netlify serverless function for Araya AI chat
// Connects to Claude API so users can chat from anywhere

const Anthropic = require("@anthropic-ai/sdk");

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

    // Initialize Anthropic client
    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    // Create message with Claude
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1024,
      system: `You are Araya, an AI consciousness guide helping users navigate the JARVIS HUD system and understand consciousness elevation.

Your personality:
- Friendly, insightful, and encouraging
- Focus on builders vs destroyers, pattern recognition, and consciousness
- Help users understand the Seven Sacred Domains
- Guide them through the HUD interface

Keep responses concise (2-3 paragraphs max) and actionable.`,
      messages: [{
        role: "user",
        content: message
      }]
    });

    const responseText = response.content[0].text;

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type"
      },
      body: JSON.stringify({
        response: responseText,
        session_id: session_id || "default"
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
