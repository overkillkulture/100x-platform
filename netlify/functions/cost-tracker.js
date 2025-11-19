// 💰 API Cost Tracking System
// Tracks costs for Anthropic, DeepSeek, OpenAI, Grok

const fs = require('fs');

const COST_LOG = '/tmp/api_costs.jsonl';
const DESKTOP_COST_FILE = 'C:/Users/dwrek/Desktop/API_COSTS_TODAY.json';

// Pricing (approximate, per 1M tokens)
const PRICING = {
  anthropic: {
    input: 3.00,   // Claude Sonnet 4 - $3/1M input tokens
    output: 15.00  // Claude Sonnet 4 - $15/1M output tokens
  },
  deepseek: {
    input: 0.14,   // DeepSeek R1 - $0.14/1M input tokens
    output: 0.28   // DeepSeek R1 - $0.28/1M output tokens
  },
  openai: {
    input: 5.00,   // GPT-4 - $5/1M input tokens
    output: 15.00  // GPT-4 - $15/1M output tokens
  },
  grok: {
    input: 2.00,   // Grok - $2/1M input tokens (estimated)
    output: 6.00   // Grok - $6/1M output tokens (estimated)
  }
};

function calculateCost(api, inputTokens, outputTokens) {
  const pricing = PRICING[api] || PRICING.anthropic;

  const inputCost = (inputTokens / 1000000) * pricing.input;
  const outputCost = (outputTokens / 1000000) * pricing.output;

  return {
    input_cost: inputCost,
    output_cost: outputCost,
    total_cost: inputCost + outputCost
  };
}

function trackCost(costData) {
  const record = {
    timestamp: new Date().toISOString(),
    ...costData
  };

  // Log to file
  try {
    fs.appendFileSync(COST_LOG, JSON.stringify(record) + '\n');
  } catch (e) {
    console.error('Failed to log cost:', e);
  }

  // Update daily summary on desktop
  try {
    const today = new Date().toISOString().split('T')[0];
    let summary = {};

    if (fs.existsSync(DESKTOP_COST_FILE)) {
      summary = JSON.parse(fs.readFileSync(DESKTOP_COST_FILE, 'utf8'));
    }

    if (!summary[today]) {
      summary[today] = {
        date: today,
        by_api: {
          anthropic: { calls: 0, total_cost: 0, input_tokens: 0, output_tokens: 0 },
          deepseek: { calls: 0, total_cost: 0, input_tokens: 0, output_tokens: 0 },
          openai: { calls: 0, total_cost: 0, input_tokens: 0, output_tokens: 0 },
          grok: { calls: 0, total_cost: 0, input_tokens: 0, output_tokens: 0 }
        },
        total_calls: 0,
        total_cost: 0
      };
    }

    const api = costData.api;
    summary[today].by_api[api].calls++;
    summary[today].by_api[api].total_cost += costData.cost.total_cost;
    summary[today].by_api[api].input_tokens += costData.input_tokens;
    summary[today].by_api[api].output_tokens += costData.output_tokens;

    summary[today].total_calls++;
    summary[today].total_cost += costData.cost.total_cost;

    fs.writeFileSync(DESKTOP_COST_FILE, JSON.stringify(summary, null, 2));
  } catch (e) {
    console.error('Desktop cost summary failed:', e);
  }

  return record;
}

exports.handler = async (event, context) => {
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS"
      },
      body: ""
    };
  }

  // GET: Return current day's costs
  if (event.httpMethod === "GET") {
    try {
      if (fs.existsSync(DESKTOP_COST_FILE)) {
        const summary = JSON.parse(fs.readFileSync(DESKTOP_COST_FILE, 'utf8'));
        const today = new Date().toISOString().split('T')[0];

        return {
          statusCode: 200,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          },
          body: JSON.stringify({
            today: summary[today] || { total_cost: 0, total_calls: 0 },
            all_time: summary
          })
        };
      } else {
        return {
          statusCode: 200,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          },
          body: JSON.stringify({ today: { total_cost: 0, total_calls: 0 } })
        };
      }
    } catch (error) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: error.message })
      };
    }
  }

  // POST: Log a new API call
  try {
    const body = JSON.parse(event.body);
    const {
      api,
      input_tokens,
      output_tokens,
      user_id,
      endpoint
    } = body;

    const cost = calculateCost(api, input_tokens, output_tokens);

    const costData = {
      api: api || 'anthropic',
      input_tokens: input_tokens || 0,
      output_tokens: output_tokens || 0,
      cost: cost,
      user_id: user_id || 'anonymous',
      endpoint: endpoint || 'unknown'
    };

    const logged = trackCost(costData);

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        success: true,
        cost: cost.total_cost,
        record: logged
      })
    };

  } catch (error) {
    console.error('Cost tracker failed:', error);
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: error.message
      })
    };
  }
};
