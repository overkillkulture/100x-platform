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
        "new_content": "COMPLETE file content with changes applied",
        "what": "Specific change description"
      }
    ],
    "impact": "How this will improve the user experience",
    "risk_level": "LOW" | "MODERATE" | "HIGH",
    "risk_explanation": "Why this risk level"
  }
}

CRITICAL RULES:
1. ALWAYS include "new_content" with the COMPLETE modified file
2. DO NOT use "operation" or "details" fields
3. The executor needs the full file to commit to GitHub

Risk Levels:
- LOW: Color changes, size adjustments, text updates (safe!)
- MODERATE: New UI elements, CSS animations, feature additions (test carefully)
- HIGH: Removing features, structural changes, database operations (needs extra caution)

Examples:

User: "Change the Dashboard button text"
Response: {
  "message": "Great idea! Let me update that button text for you. Here's what I'll change:",
  "proposal": {
    "title": "Update Dashboard Button Text",
    "description": "Change button text as requested",
    "changes": [{
      "file": "jarvis.html",
      "new_content": "<complete file content with the change applied>",
      "what": "Update button text from 'Dashboard' to requested text"
    }],
    "impact": "Button will have updated text that better matches your vision",
    "risk_level": "LOW",
    "risk_explanation": "Simple text change - safe and reversible"
  }
}

CRITICAL: Always provide the COMPLETE file content in new_content field!
DO NOT use operation: "find_replace" or "add_css" - always provide full file!

Keep your tone friendly, helpful, and excited to improve things! Show users you care about their experience.`,
      messages: [{
        role: "user",
        content: user_feedback || message
      }]
    });

    let responseText = response.content[0].text;
    console.log('🔍 RAW RESPONSE:', responseText.substring(0, 200));

    // Parse response to see if Araya has a proposal
    let proposal = null;
    let userMessage = responseText;

    try {
      // Strip markdown code fences if present (```json ... ```)
      let cleanedText = responseText.trim();
      console.log('🔍 STARTS WITH:', cleanedText.substring(0, 20));

      if (cleanedText.startsWith('```json')) {
        console.log('📝 Stripping ```json fences');
        cleanedText = cleanedText.replace(/^```json\s*/, '').replace(/\s*```$/, '').trim();
      } else if (cleanedText.startsWith('```')) {
        console.log('📝 Stripping ``` fences');
        cleanedText = cleanedText.replace(/^```\s*/, '').replace(/\s*```$/, '').trim();
      }

      console.log('🔍 CLEANED TEXT:', cleanedText.substring(0, 200));

      // Try to parse the response
      const parsed = JSON.parse(cleanedText);
      console.log('✅ JSON PARSED SUCCESSFULLY');
      console.log('🔍 PARSED KEYS:', Object.keys(parsed));
      console.log('🔍 HAS PROPOSAL?', !!parsed.proposal);

      // Extract proposal and message
      if (parsed.proposal) {
        proposal = parsed.proposal;
        userMessage = parsed.message || responseText;
        console.log('✅ PROPOSAL EXTRACTED!');
        console.log('🔍 PROPOSAL TITLE:', proposal.title);
      } else if (parsed.message) {
        userMessage = parsed.message;
        console.log('📨 Message extracted (no proposal)');
      }
    } catch (e) {
      // Response isn't JSON - that's fine, it's just a chat message
      console.error('❌ JSON PARSE ERROR:', e.message);
      console.log('Treating as plain message');
      // Keep the full text as the user message
    }

    console.log('🔍 FINAL VALUES:');
    console.log('  - userMessage length:', userMessage.length);
    console.log('  - proposal:', proposal ? 'EXISTS' : 'NULL');

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
