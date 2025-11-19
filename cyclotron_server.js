/**
 * CYCLOTRON LOCAL SERVER
 *
 * Provides HTTP endpoints for the Cyclotron Engine
 * Mimics Netlify function behavior for local development
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// Import Cyclotron Engine and Araya Feed
const CyclotronEngine = require('./cyclotron_engine.js');
const ArayaKnowledgeFeed = require('./araya_knowledge_feed.js');

const PORT = 3000;
const cyclotron = new CyclotronEngine();
const arayaFeed = new ArayaKnowledgeFeed();

// Start the cyclotron daemon
cyclotron.start();

// Create HTTP server
const server = http.createServer((req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    // Route: GET /.netlify/functions/cyclotron-status
    if (req.url === '/.netlify/functions/cyclotron-status' || req.url === '/cyclotron-status') {
        const status = cyclotron.getStatus();

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(status));

        console.log(`📊 Status requested - Atoms: ${status.total_atoms}, Running: ${status.is_running}`);
        return;
    }

    // Route: POST /.netlify/functions/cyclotron-control
    if (req.url === '/.netlify/functions/cyclotron-control' || req.url === '/cyclotron-control') {
        let body = '';

        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            try {
                const { action } = JSON.parse(body);

                let result = {};

                switch (action) {
                    case 'start':
                        cyclotron.start();
                        result = { success: true, message: 'Cyclotron started' };
                        break;
                    case 'stop':
                        cyclotron.stop();
                        result = { success: true, message: 'Cyclotron stopped' };
                        break;
                    case 'rake':
                        const data = cyclotron.performRake();
                        result = { success: true, message: 'Rake performed', data };
                        break;
                    default:
                        result = { success: false, message: 'Unknown action' };
                }

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(result));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: error.message }));
            }
        });

        return;
    }

    // Route: GET /araya/knowledge (get all knowledge)
    if (req.url === '/araya/knowledge' || req.url === '/.netlify/functions/araya-knowledge') {
        const knowledge = arayaFeed.exportForAI('full');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(knowledge));
        console.log('🧠 Araya knowledge feed accessed');
        return;
    }

    // Route: GET /araya/summary (get knowledge summary)
    if (req.url === '/araya/summary' || req.url === '/.netlify/functions/araya-summary') {
        const summary = arayaFeed.exportForAI('summary');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(summary));
        console.log('🧠 Araya summary accessed');
        return;
    }

    // Route: GET /araya/stats (get statistics)
    if (req.url === '/araya/stats' || req.url === '/.netlify/functions/araya-stats') {
        const stats = arayaFeed.getStats();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(stats));
        console.log('🧠 Araya stats accessed');
        return;
    }

    // Route: GET /araya/recent (get recent knowledge)
    if (req.url.startsWith('/araya/recent')) {
        const urlParts = req.url.split('?');
        const params = new URLSearchParams(urlParts[1] || '');
        const limit = parseInt(params.get('limit')) || 10;
        const recent = arayaFeed.getRecentKnowledge(limit);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(recent));
        console.log(`🧠 Araya recent knowledge accessed (${limit} items)`);
        return;
    }

    // Route: GET /araya/search?q=keyword
    if (req.url.startsWith('/araya/search')) {
        const urlParts = req.url.split('?');
        const params = new URLSearchParams(urlParts[1] || '');
        const keyword = params.get('q') || '';
        const results = arayaFeed.searchKnowledge(keyword);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(results));
        console.log(`🧠 Araya search: "${keyword}" (${results.length} results)`);
        return;
    }

    // 404 for unknown routes
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
});

// Start server
server.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════════════╗
║   🌀 AUTONOMOUS CYCLOTRON SERVER ONLINE 🌀    ║
╠════════════════════════════════════════════════╣
║  Port: ${PORT}                                    ║
║  Status: http://localhost:${PORT}/cyclotron-status  ║
║  Netlify: http://localhost:${PORT}/.netlify/functions/cyclotron-status  ║
╠════════════════════════════════════════════════╣
║  Daemon: ACTIVE                                ║
║  Rake Interval: 30 seconds (MAXIMUM SPEED!)    ║
║  Growth Rate: 4.0 atoms/min (MAXIMUM SPEED!)   ║
╚════════════════════════════════════════════════╝
    `);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Cyclotron server...');
    cyclotron.stop();
    server.close(() => {
        console.log('✅ Server stopped');
        process.exit(0);
    });
});
