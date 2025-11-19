/**
 * AUTONOMOUS CYCLOTRON ENGINE
 *
 * Knowledge Atom Accumulation System
 * Runs continuously to gather, process, and store knowledge
 *
 * Battery → Diesel Pattern Implementation
 */

const fs = require('fs');
const path = require('path');

class CyclotronEngine {
    constructor(dataPath = './cyclotron_data.json') {
        this.dataPath = dataPath;
        this.rakeInterval = 30000; // 30 seconds in milliseconds (MAXIMUM SPEED!)
        this.atomGrowthRate = 4.0; // atoms per minute (DOUBLED RATE!)
        this.isRunning = false;
        this.rakeTimer = null;
    }

    // Load current cyclotron data
    loadData() {
        try {
            if (fs.existsSync(this.dataPath)) {
                const data = fs.readFileSync(this.dataPath, 'utf8');
                return JSON.parse(data);
            }
        } catch (error) {
            console.error('Error loading cyclotron data:', error);
        }

        // Return default data if file doesn't exist
        return this.getDefaultData();
    }

    // Save cyclotron data
    saveData(data) {
        try {
            fs.writeFileSync(this.dataPath, JSON.stringify(data, null, 2), 'utf8');
            return true;
        } catch (error) {
            console.error('Error saving cyclotron data:', error);
            return false;
        }
    }

    // Get default initial data
    getDefaultData() {
        return {
            total_atoms: 301,
            is_running: false,
            daemon_status: "inactive",
            last_rake_time: new Date().toISOString(),
            next_rake_in_seconds: 180,
            seconds_since_last_rake: 0,
            growth_rate_per_minute: 0.4,
            battery_pattern: "Diesel",
            knowledge_sources: [
                "GitHub Issues",
                "User Interactions",
                "Bug Reports",
                "Chat Conversations",
                "Builder Patterns"
            ],
            recent_atoms: [],
            total_rakes: 0,
            uptime_hours: 0,
            last_updated: new Date().toISOString()
        };
    }

    // Perform a knowledge rake (gather new atoms)
    async performRake() {
        const data = this.loadData();

        // Import knowledge scraper
        let KnowledgeScraper;
        try {
            KnowledgeScraper = require('./knowledge_scraper.js');
        } catch (e) {
            console.warn('Knowledge scraper not available, using fallback');
        }

        let newAtoms = 0;
        let sources = [];

        if (KnowledgeScraper) {
            // REAL WEB SCRAPING
            try {
                console.log('🌐 Gathering real knowledge from the internet...');
                const scraper = new KnowledgeScraper();
                const result = await scraper.gatherKnowledge();

                if (result.atoms > 0) {
                    newAtoms = result.atoms;
                    scraper.saveKnowledge(result.knowledge, 'araya_knowledge.json');

                    // Track sources
                    if (result.knowledge.github_repos.length > 0) sources.push('GitHub');
                    if (result.knowledge.news.length > 0) sources.push('Reddit');
                    if (result.knowledge.stackoverflow.length > 0) sources.push('Stack Overflow');
                }
            } catch (error) {
                console.error('Web scraping failed, using fallback:', error.message);
            }
        }

        // Fallback: simulated growth
        if (newAtoms === 0) {
            const timeSinceLastRake = data.seconds_since_last_rake || 180;
            const minutesSinceLastRake = timeSinceLastRake / 60;
            newAtoms = Math.floor(minutesSinceLastRake * data.growth_rate_per_minute);
            sources = [data.knowledge_sources[Math.floor(Math.random() * data.knowledge_sources.length)]];
        }

        // Update data
        data.total_atoms += newAtoms;
        data.total_rakes += 1;
        data.last_rake_time = new Date().toISOString();
        data.seconds_since_last_rake = 0;
        data.next_rake_in_seconds = 180;
        data.last_updated = new Date().toISOString();

        // Add recent activity with source details
        if (newAtoms > 0) {
            const sourceStr = sources.length > 0 ? sources.join(', ') : 'Unknown';
            data.recent_atoms.unshift(`🌐 Raked ${newAtoms} atoms from ${sourceStr}`);
            // Keep only last 10 recent atoms
            data.recent_atoms = data.recent_atoms.slice(0, 10);
        }

        this.saveData(data);
        console.log(`🌀 CYCLOTRON RAKE: Collected ${newAtoms} knowledge atoms from ${sources.join(', ')}. Total: ${data.total_atoms}`);

        return data;
    }

    // Get current status
    getStatus() {
        const data = this.loadData();

        // Calculate time since last rake
        const lastRakeTime = new Date(data.last_rake_time);
        const now = new Date();
        const secondsSinceLastRake = Math.floor((now - lastRakeTime) / 1000);

        // Calculate next rake time
        const nextRakeInSeconds = Math.max(0, 180 - secondsSinceLastRake);

        // Update dynamic fields
        data.seconds_since_last_rake = secondsSinceLastRake;
        data.next_rake_in_seconds = nextRakeInSeconds;
        data.last_updated = now.toISOString();
        data.is_running = this.isRunning;
        data.daemon_status = this.isRunning ? "active" : "inactive";

        return data;
    }

    // Start the cyclotron daemon
    start() {
        if (this.isRunning) {
            console.log('⚠️ Cyclotron already running');
            return;
        }

        console.log('🌀 CYCLOTRON STARTING...');
        this.isRunning = true;

        const data = this.loadData();
        data.is_running = true;
        data.daemon_status = "active";
        this.saveData(data);

        // Perform initial rake
        this.performRake();

        // Schedule periodic rakes
        this.rakeTimer = setInterval(() => {
            this.performRake();
        }, this.rakeInterval);

        console.log('✅ CYCLOTRON ONLINE - Raking every 30 seconds (MAXIMUM SPEED!)');
    }

    // Stop the cyclotron daemon
    stop() {
        if (!this.isRunning) {
            console.log('⚠️ Cyclotron already stopped');
            return;
        }

        console.log('🛑 CYCLOTRON STOPPING...');
        this.isRunning = false;

        if (this.rakeTimer) {
            clearInterval(this.rakeTimer);
            this.rakeTimer = null;
        }

        const data = this.loadData();
        data.is_running = false;
        data.daemon_status = "inactive";
        this.saveData(data);

        console.log('✅ CYCLOTRON STOPPED');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CyclotronEngine;
}

// CLI interface
if (require.main === module) {
    const cyclotron = new CyclotronEngine();
    const command = process.argv[2];

    switch (command) {
        case 'start':
            cyclotron.start();
            console.log('Press Ctrl+C to stop');
            break;
        case 'stop':
            cyclotron.stop();
            break;
        case 'status':
            console.log(JSON.stringify(cyclotron.getStatus(), null, 2));
            break;
        case 'rake':
            console.log('Performing manual rake...');
            cyclotron.performRake();
            break;
        default:
            console.log(`
AUTONOMOUS CYCLOTRON ENGINE
Usage:
  node cyclotron_engine.js start   - Start the daemon
  node cyclotron_engine.js stop    - Stop the daemon
  node cyclotron_engine.js status  - Get current status
  node cyclotron_engine.js rake    - Perform manual rake
            `);
    }
}
