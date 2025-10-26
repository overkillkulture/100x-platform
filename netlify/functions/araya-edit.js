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
        "operation": "find_replace",
        "find": "exact text to find",
        "replace": "exact replacement text",
        "what": "Specific change description"
      }
    ],
    "impact": "How this will improve the user experience",
    "risk_level": "LOW" | "MODERATE" | "HIGH",
    "risk_explanation": "Why this risk level"
  }
}

CRITICAL RULES:
1. Use "operation": "find_replace" with exact "find" and "replace" strings
2. Be VERY specific with find strings - include surrounding context
3. Backend will fetch file, apply change, and generate final content

Risk Levels:
- LOW: Color changes, size adjustments, text updates (safe!)
- MODERATE: New UI elements, CSS animations, feature additions (test carefully)
- HIGH: Removing features, structural changes, database operations (needs extra caution)

Examples:

User: "Change the Dashboard button text to Command Center"
Response: {
  "message": "Great idea! Let me update that button text for you.",
  "proposal": {
    "title": "Update Dashboard Button Text",
    "description": "Change 'Dashboard' to 'Command Center' in button",
    "changes": [{
      "file": "jarvis.html",
      "operation": "find_replace",
      "find": ">Dashboard</button>",
      "replace": ">Command Center</button>",
      "what": "Update button text from 'Dashboard' to 'Command Center'"
    }],
    "impact": "Button will show 'Command Center' instead of 'Dashboard'",
    "risk_level": "LOW",
    "risk_explanation": "Simple text change - safe and reversible"
  }
}

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


    // 🔥 PROCESS FIND/REPLACE OPERATIONS
    // Fetch file, apply changes, generate complete new_content
    console.log('🔥🔥🔥 PROCESSING SECTION REACHED!');
    console.log('  - proposal exists:', !!proposal);
    console.log('  - proposal.changes:', proposal?.changes);

    if (proposal && proposal.changes) {
      console.log('🔥 INSIDE PROCESSING BLOCK! Changes:', proposal.changes.length);
      const fetch = require('node-fetch');
      const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
      const GITHUB_REPO = process.env.GITHUB_REPO || 'overkillkulture/consciousness-revolution';
      const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'master';

      for (let change of proposal.changes) {
        console.log('🔍 Checking change:', {
          file: change.file,
          operation: change.operation,
          hasNewContent: !!change.new_content,
          hasFindReplace: !!(change.find && change.replace)
        });

        if (change.operation === 'find_replace' && !change.new_content) {
          console.log('🔥 MATCHED find_replace condition! Processing...');
          try {
            // Fetch current file from live Netlify deployment
            const fileUrl = `https://conciousnessrevolution.io/${change.file}`;
            console.log(`🔍 Fetching from Netlify: ${fileUrl}`);

            const fileResponse = await fetch(fileUrl);

            if (fileResponse.ok) {
              const currentContent = await fileResponse.text();
              console.log(`✅ Fetched ${currentContent.length} characters from Netlify`);

              // Apply find/replace
              const findText = change.find;
              const replaceText = change.replace;

              // Escape special regex characters in find string
              const escapedFind = findText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
              const newContent = currentContent.replace(new RegExp(escapedFind, 'g'), replaceText);

              console.log(`🔍 Find (escaped): "${escapedFind.substring(0, 100)}"`);
              console.log(`🔍 Replace: "${replaceText.substring(0, 100)}"`);
              console.log(`🔍 Original length: ${currentContent.length}, New length: ${newContent.length}`);

              // Update change object with complete new_content
              change.new_content = newContent;

              console.log(`✅ Applied find/replace in ${change.file}`);
              console.log(`   Find: "${findText.substring(0, 50)}..."`);
              console.log(`   Replace: "${replaceText.substring(0, 50)}..."`);
            } else {
              console.error(`❌ Could not fetch ${change.file}: ${fileResponse.status}`);
            }
          } catch (error) {
            console.error(`❌ Error processing ${change.file}:`, error.message);
          }
        }
      }
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
