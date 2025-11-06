// Quick test script for Trinity integration
// Uses native fetch (Node 18+)

const BASE_URL = 'http://localhost:3100';
let sessionCookie = null;

async function registerUser() {
    console.log('📝 Registering test user...');
    const response = await fetch(`${BASE_URL}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: `testuser_${Date.now()}`,
            password: 'testpass123',
            email: 'test@example.com'
        })
    });
    const data = await response.json();
    console.log('✅ User registered:', data.user.username);
    return data.user.username;
}

async function login(username) {
    console.log('🔐 Logging in...');
    const response = await fetch(`${BASE_URL}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            password: 'testpass123'
        })
    });

    // Get session cookie
    const cookies = response.headers.get('set-cookie');
    if (cookies) {
        sessionCookie = cookies.split(';')[0];
    }

    const data = await response.json();
    console.log('✅ Logged in:', data.user.username);
}

async function testTrinityChat(message, agent) {
    console.log(`\n🔱 Testing Trinity (${agent.toUpperCase()})...`);
    console.log(`📨 Message: "${message}"`);

    const response = await fetch(`${BASE_URL}/api/trinity/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': sessionCookie
        },
        body: JSON.stringify({
            message: message,
            agent: agent
        })
    });

    const data = await response.json();

    if (data.error) {
        console.error('❌ Error:', data.error);
        return;
    }

    console.log('\n📊 TRINITY RESPONSE:');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`🤖 Agent: ${data.agent_name}`);
    console.log(`📍 Role: ${data.role}`);
    console.log(`🎯 Routing: ${data.routing.mode.toUpperCase()}`);
    console.log(`💭 Reason: ${data.routing.reason}`);
    console.log(`\n💬 Response:\n${data.message}`);
    console.log('\n📈 STATS:');
    console.log(`   Cost Today: $${data.stats.daily_cost.toFixed(4)}`);
    console.log(`   Requests: ${data.stats.requests_today}`);
    console.log(`   Budget Remaining: $${data.stats.budget_remaining.toFixed(2)}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
}

async function getTrinityStats() {
    console.log('📊 Getting Trinity stats...');
    const response = await fetch(`${BASE_URL}/api/trinity/stats`, {
        method: 'GET',
        headers: {
            'Cookie': sessionCookie
        }
    });
    const data = await response.json();
    console.log('Trinity Stats:', data);
}

async function runTests() {
    try {
        // Setup
        const username = await registerUser();
        await login(username);

        // Test different complexity levels
        await testTrinityChat('Format this JSON: {"name":"test"}', 'c1');
        await testTrinityChat('How should I architect a scalable microservices system?', 'c2');
        await testTrinityChat('What are the long-term implications of AI in software development?', 'c3');

        // Get final stats
        await getTrinityStats();

        console.log('\n✅ All tests completed!');

    } catch (error) {
        console.error('❌ Test failed:', error.message);
        console.error(error.stack);
    }

    process.exit(0);
}

runTests();
