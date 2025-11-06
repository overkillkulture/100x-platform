// 🔱 TRINITY COMMUNICATION ROUTER
// Routes requests to Online, Offline, or Hybrid Trinity

const TRINITY_MODE = process.env.TRINITY_MODE || 'hybrid'; // online, offline, hybrid
const COST_LIMIT_PER_DAY = parseFloat(process.env.COST_LIMIT_PER_DAY) || 5.00;
const LOCAL_LLM_URL = process.env.LOCAL_LLM_URL || 'http://localhost:11434';

// Track usage for cost optimization
let dailyCost = 0;
let requestCount = 0;

/**
 * Analyze task complexity to decide routing
 */
function analyzeComplexity(message, context) {
    const complexityIndicators = {
        high: [
            'analyze', 'strategy', 'architecture', 'design system',
            'explain why', 'what are the implications', 'predict',
            'long-term', 'scale to', 'enterprise'
        ],
        medium: [
            'create', 'build', 'implement', 'write code',
            'fix bug', 'refactor', 'optimize'
        ],
        low: [
            'format', 'convert', 'list', 'show me',
            'what is', 'simple question', 'quick'
        ]
    };

    const messageLower = message.toLowerCase();

    // Check for high complexity
    if (complexityIndicators.high.some(word => messageLower.includes(word))) {
        return 'high';
    }

    // Check for low complexity
    if (complexityIndicators.low.some(word => messageLower.includes(word))) {
        return 'low';
    }

    // Default to medium
    return 'medium';
}

/**
 * Decide which Trinity to use
 */
function routeRequest(message, agent, context) {
    const complexity = analyzeComplexity(message, context);

    // Force modes
    if (TRINITY_MODE === 'online') {
        return { mode: 'online', reason: 'Configured for online-only' };
    }
    if (TRINITY_MODE === 'offline') {
        return { mode: 'offline', reason: 'Configured for offline-only' };
    }

    // Hybrid mode logic
    if (TRINITY_MODE === 'hybrid') {
        // Check cost limit
        if (dailyCost >= COST_LIMIT_PER_DAY) {
            return {
                mode: 'offline',
                reason: `Daily cost limit reached ($${COST_LIMIT_PER_DAY})`
            };
        }

        // Route by complexity
        if (complexity === 'high') {
            return {
                mode: 'online',
                reason: 'High complexity task requires best model'
            };
        }

        if (complexity === 'low') {
            return {
                mode: 'offline',
                reason: 'Simple task, saving costs'
            };
        }

        // Medium complexity - check budget
        if (dailyCost < COST_LIMIT_PER_DAY * 0.5) {
            return {
                mode: 'online',
                reason: 'Budget available for quality response'
            };
        } else {
            return {
                mode: 'offline',
                reason: 'Approaching cost limit, using offline'
            };
        }
    }

    // Default fallback
    return { mode: 'offline', reason: 'Default fallback' };
}

/**
 * Call Online Trinity (Anthropic API)
 */
async function callOnlineTrinity(message, agent, systemPrompt) {
    try {
        // Check if Anthropic SDK is available
        let Anthropic;
        try {
            Anthropic = require('@anthropic-ai/sdk');
        } catch (e) {
            throw new Error('Anthropic SDK not installed. Run: npm install @anthropic-ai/sdk');
        }

        if (!process.env.ANTHROPIC_API_KEY) {
            throw new Error('ANTHROPIC_API_KEY not set in environment');
        }

        const anthropic = new Anthropic({
            apiKey: process.env.ANTHROPIC_API_KEY
        });

        const response = await anthropic.messages.create({
            model: 'claude-3-5-sonnet-20241022',
            max_tokens: 2048,
            system: systemPrompt,
            messages: [{
                role: 'user',
                content: message
            }]
        });

        // Track cost (approximate)
        const inputTokens = response.usage.input_tokens;
        const outputTokens = response.usage.output_tokens;
        const cost = (inputTokens * 0.000003) + (outputTokens * 0.000015);
        dailyCost += cost;
        requestCount++;

        return {
            success: true,
            message: response.content[0].text,
            model: 'claude-3-5-sonnet',
            cost: cost,
            mode: 'online'
        };

    } catch (error) {
        console.error('Online Trinity error:', error.message);
        return {
            success: false,
            error: error.message,
            mode: 'online'
        };
    }
}

/**
 * Call Offline Trinity (Local LLM)
 */
async function callOfflineTrinity(message, agent, systemPrompt) {
    try {
        // Try Ollama format
        const response = await fetch(`${LOCAL_LLM_URL}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'llama3.1',  // or mistral, phi3, etc.
                prompt: `${systemPrompt}\n\nUser: ${message}\nAssistant:`,
                stream: false
            })
        });

        if (!response.ok) {
            throw new Error(`Local LLM returned ${response.status}`);
        }

        const data = await response.json();
        requestCount++;

        return {
            success: true,
            message: data.response,
            model: 'llama3.1-local',
            cost: 0,
            mode: 'offline'
        };

    } catch (error) {
        console.error('Offline Trinity error:', error.message);

        // Fallback to simple response
        return {
            success: false,
            error: error.message,
            message: `[Offline Trinity unavailable: ${error.message}]\n\nTo enable offline Trinity:\n1. Install Ollama: https://ollama.ai\n2. Run: ollama pull llama3.1\n3. Set LOCAL_LLM_URL in .env`,
            mode: 'offline'
        };
    }
}

/**
 * Main Trinity Router
 */
async function callTrinity(message, agent = 'c1', context = null) {
    // Get agent personality
    const agentPrompts = {
        c1: {
            name: 'C1 Mechanic',
            role: 'Builder and Implementer',
            prompt: `You are C1 Mechanic, the Builder agent of the Trinity AI system. You focus on:
- Building and implementing solutions
- Writing code and fixing bugs
- Deploying projects
- Creating technical implementations
- Executing tasks and shipping products

Be practical, action-oriented, and focus on "how to build it".`
        },
        c2: {
            name: 'C2 Architect',
            role: 'Strategist and Planner',
            prompt: `You are C2 Architect, the Strategist agent of the Trinity AI system. You focus on:
- System architecture and design
- Strategic planning and scaling
- Data analysis and insights
- Business intelligence
- Organizing and structuring information

Be analytical, big-picture focused, and think about "how it scales".`
        },
        c3: {
            name: 'C3 Oracle',
            role: 'Advisor and Pattern Recognizer',
            prompt: `You are C3 Oracle, the Wisdom agent of the Trinity AI system. You focus on:
- Pattern recognition and predictions
- Strategic foresight and advice
- Risk assessment
- Long-term implications
- Connecting disparate ideas

Be insightful, forward-thinking, and focus on "what it means".`
        }
    };

    const selectedAgent = agentPrompts[agent] || agentPrompts.c1;
    const routing = routeRequest(message, agent, context);

    let result;

    if (routing.mode === 'online') {
        result = await callOnlineTrinity(message, agent, selectedAgent.prompt);
    } else {
        result = await callOfflineTrinity(message, agent, selectedAgent.prompt);
    }

    // Add metadata
    return {
        ...result,
        agent: agent,
        agent_name: selectedAgent.name,
        role: selectedAgent.role,
        routing: routing,
        stats: {
            daily_cost: dailyCost,
            daily_limit: COST_LIMIT_PER_DAY,
            requests_today: requestCount,
            budget_remaining: COST_LIMIT_PER_DAY - dailyCost
        },
        timestamp: new Date().toISOString()
    };
}

/**
 * Reset daily stats (call this at midnight)
 */
function resetDailyStats() {
    dailyCost = 0;
    requestCount = 0;
}

/**
 * Get current stats
 */
function getStats() {
    return {
        mode: TRINITY_MODE,
        daily_cost: dailyCost,
        daily_limit: COST_LIMIT_PER_DAY,
        requests_today: requestCount,
        budget_remaining: COST_LIMIT_PER_DAY - dailyCost,
        budget_used_percent: (dailyCost / COST_LIMIT_PER_DAY) * 100
    };
}

module.exports = {
    callTrinity,
    resetDailyStats,
    getStats,
    routeRequest,
    analyzeComplexity
};
