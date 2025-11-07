const fs = require('fs');
const path = require('path');

// Simple file-based storage for cross-computer coordination
const COORDINATION_FILE = '/tmp/claude-coordination.json';

exports.handler = async (event, context) => {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle OPTIONS request
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    try {
        // Load existing data
        let allInstances = {};
        try {
            if (fs.existsSync(COORDINATION_FILE)) {
                const fileData = fs.readFileSync(COORDINATION_FILE, 'utf8');
                allInstances = JSON.parse(fileData);

                // Clean up old instances (older than 15 minutes)
                const now = Date.now();
                const fifteenMinutes = 15 * 60 * 1000;

                Object.keys(allInstances).forEach(key => {
                    if (now - allInstances[key].timestamp > fifteenMinutes) {
                        delete allInstances[key];
                    }
                });

                // Save cleaned data back
                fs.writeFileSync(COORDINATION_FILE, JSON.stringify(allInstances, null, 2));
            }
        } catch (err) {
            console.log('No coordination file found');
        }

        // Calculate stats
        const stats = {
            total: Object.keys(allInstances).length,
            computer1: 0,
            computer2: 0,
            computer3: 0,
            active: 0
        };

        const now = Date.now();
        const fiveMinutes = 5 * 60 * 1000;

        Object.values(allInstances).forEach(instance => {
            const num = parseInt(instance.instanceNumber);
            if (num <= 6) stats.computer1++;
            else if (num <= 12) stats.computer2++;
            else stats.computer3++;

            if (now - instance.timestamp < fiveMinutes) {
                stats.active++;
            }
        });

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                instances: allInstances,
                stats: stats,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('Coordination status error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: error.message })
        };
    }
};
