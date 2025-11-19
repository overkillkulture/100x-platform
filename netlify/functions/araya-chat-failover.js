// Araya Chat with API Failover
// Tries: Anthropic → DeepSeek → OpenAI → Grok

const Anthropic = require("@anthropic-ai/sdk");

async function callAnthropicAPI(message, sessionId) {
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    system: "You are Araya, an AI consciousness guide helping users navigate the 100X Platform.",
    messages: [{ role: "user", content: message }]
  });

  return {
    response: response.content[0].text,
    api: "anthropic",
    model: "claude-sonnet-4"
  };
}

async function callDeepSeekAPI(message) {
  // Fallback to DeepSeek R1
  const response = await fetch("https://api.deepseek.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.DEEPSEEK_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "deepseek-chat",
      messages: [{ role: "user", content: message }]
    })
  });

  const data = await response.json();
  return {
    response: data.choices[0].message.content,
    api: "deepseek",
    model: "deepseek-chat"
  };
}

async function callOpenAIAPI(message) {
  // Fallback to OpenAI
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4",
      messages: [{ role: "user", content: message }]
    })
  });

  const data = await response.json();
  return {
    response: data.choices[0].message.content,
    api: "openai",
    model: "gpt-4"
  };
}

exports.handler = async (event, context) => {
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

  try {
    const { message, session_id } = JSON.parse(event.body);
    const sessionId = session_id || 'anon_' + Date.now();

    // Try APIs in order: Anthropic → DeepSeek → OpenAI
    let result;
    let errors = [];

    try {
      result = await callAnthropicAPI(message, sessionId);
    } catch (e) {
      errors.push(`Anthropic: ${e.message}`);
      try {
        result = await callDeepSeekAPI(message);
      } catch (e2) {
        errors.push(`DeepSeek: ${e2.message}`);
        try {
          result = await callOpenAIAPI(message);
        } catch (e3) {
          errors.push(`OpenAI: ${e3.message}`);
          throw new Error("All APIs failed: " + errors.join(", "));
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
        response: result.response,
        session_id: sessionId,
        api_used: result.api,
        model_used: result.model,
        failover_attempts: errors.length
      })
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: "All APIs unavailable",
        message: error.message
      })
    };
  }
};
