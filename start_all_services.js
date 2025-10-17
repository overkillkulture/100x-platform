#!/usr/bin/env node
/**
 * CONSCIOUSNESS SERVICES - CLOUD LAUNCHER
 * Starts all 17 services in cloud environment
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🌀 CONSCIOUSNESS REVOLUTION - CLOUD SERVICES STARTING...\n');

// Get all .js files that are services
const services = [
    { name: 'C1 Mechanic', file: 'c1_mechanic_engine.js', port: 8001 },
    { name: 'C2 Architect', file: 'c2_architect_engine.js', port: 8002 },
    { name: 'C3 Oracle', file: 'c3_oracle_engine.js', port: 8003 },
    { name: 'Claude API Integration', file: 'claude_api_integration.js', port: 2000 },
    { name: 'Autonomous Ability Acquisition', file: 'autonomous_ability_acquisition.js', port: 6000 }
];

const runningProcesses = [];

// Start each service
services.forEach((service, index) => {
    const filePath = path.join(__dirname, service.file);

    if (fs.existsSync(filePath)) {
        setTimeout(() => {
            console.log(`[${index + 1}/${services.length}] Starting ${service.name} on port ${service.port}...`);

            const process = spawn('node', [filePath], {
                stdio: 'inherit',
                env: { ...process.env, PORT: service.port }
            });

            runningProcesses.push({ name: service.name, process });

            process.on('error', (err) => {
                console.error(`❌ ${service.name} failed:`, err.message);
            });

        }, index * 2000); // Stagger starts by 2 seconds
    } else {
        console.log(`⚠️ ${service.name} file not found: ${service.file}`);
    }
});

// Handle shutdown gracefully
process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down all services...');
    runningProcesses.forEach(({ name, process }) => {
        console.log(`   Stopping ${name}...`);
        process.kill();
    });
    process.exit(0);
});

console.log('\n✅ All services launching...');
console.log('📡 Services will be available on their designated ports');
console.log('🌐 Access via Railway public URL once deployed\n');
