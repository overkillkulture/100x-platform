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
        if (event.httpMethod === 'POST') {
            // Check-in from an instance
            const instanceData = JSON.parse(event.body);

            // Load existing data
            let allInstances = {};
            try {
                if (fs.existsSync(COORDINATION_FILE)) {
                    const fileData = fs.readFileSync(COORDINATION_FILE, 'utf8');
                    allInstances = JSON.parse(fileData);
                }
            } catch (err) {
                console.log('No existing coordination file, creating new');
            }

            // Update with new instance data
            allInstances[instanceData.instanceNumber] = {
                ...instanceData,
                lastUpdate: new Date().toISOString(),
                timestamp: Date.now()
            };

            // Save back to file
            fs.writeFileSync(COORDINATION_FILE, JSON.stringify(allInstances, null, 2));

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    message: `Instance ${instanceData.instanceNumber} checked in`,
                    totalInstances: Object.keys(allInstances).length
                })
            };
        }

        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };

    } catch (error) {
        console.error('Coordination checkin error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: error.message })
        };
    }
};
