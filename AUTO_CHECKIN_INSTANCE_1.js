#!/usr/bin/env node

// Auto check-in script for Instance 1
// This keeps Instance 1's status updated in the coordination system

const fs = require('fs');
const path = require('path');

const INSTANCE_DATA = {
    instanceNumber: '1',
    sessionId: '011CUtYha8BCasLQ7jC7wTdC',
    currentTask: 'Autonomous coordination system deployment + Testing',
    filesEditing: 'connect.html, coordination functions, deployment scripts',
    computer: 'Computer 1 (Main)',
    type: 'Claude Code',
    lastUpdate: new Date().toISOString(),
    timestamp: Date.now()
};

// Save to local coordination file
const COORD_FILE = path.join(__dirname, 'INSTANCE_1_STATUS.json');
fs.writeFileSync(COORD_FILE, JSON.stringify(INSTANCE_DATA, null, 2));

console.log('✅ Instance 1 checked in locally');
console.log(JSON.stringify(INSTANCE_DATA, null, 2));

// Try to post to API if available
const https = require('https');
const postData = JSON.stringify(INSTANCE_DATA);

const options = {
    hostname: 'consciousnessrevolution.io',
    port: 443,
    path: '/.netlify/functions/coordination-checkin',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': postData.length
    }
};

const req = https.request(options, (res) => {
    console.log(`✅ Instance 1 checked in to API: ${res.statusCode}`);

    res.on('data', (d) => {
        process.stdout.write(d);
    });
});

req.on('error', (error) => {
    console.log('⚠️ API check-in failed (site may not be deployed yet):', error.message);
    console.log('Local check-in successful though!');
});

req.write(postData);
req.end();

// Keep running and update every 2 minutes
if (process.argv.includes('--watch')) {
    console.log('\n👀 Watching mode: Will update every 2 minutes...');
    setInterval(() => {
        INSTANCE_DATA.lastUpdate = new Date().toISOString();
        INSTANCE_DATA.timestamp = Date.now();
        fs.writeFileSync(COORD_FILE, JSON.stringify(INSTANCE_DATA, null, 2));
        console.log(`\n⏰ ${new Date().toLocaleTimeString()} - Instance 1 status updated`);
    }, 120000); // 2 minutes
}
