#!/usr/bin/env node
/**
 * AUTONOMOUS SESSION METRICS TRACKER
 * Real-time tracking of AI autonomous work sessions
 * Monitors: Lines written, files created, git operations, network activity
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class AutonomousSessionMetrics {
    constructor() {
        this.sessionStart = new Date();
        this.metrics = {
            sessionId: `AUTONOMOUS_${Date.now()}`,
            startTime: this.sessionStart.toISOString(),
            computer: process.env.COMPUTERNAME || 'UNKNOWN',
            linesWritten: 0,
            filesCreated: 0,
            filesModified: 0,
            gitOperations: 0,
            networkSyncEvents: 0,
            toolsExecuted: [],
            activeProcesses: 0,
            autonomousActions: []
        };

        this.startTracking();
    }

    log(action, details = {}) {
        const timestamp = new Date();
        const elapsed = Math.floor((timestamp - this.sessionStart) / 1000);

        this.metrics.autonomousActions.push({
            timestamp: timestamp.toISOString(),
            elapsed: `${elapsed}s`,
            action,
            ...details
        });

        console.log(`[${elapsed}s] ⚡ ${action}`);
        if (Object.keys(details).length > 0) {
            console.log(`    ${JSON.stringify(details, null, 2)}`);
        }
    }

    async analyzePlatformChanges() {
        try {
            // Count new/modified files in 100x-platform
            const gitStatus = execSync('git status --short', {
                cwd: 'C:\\Users\\darri\\100x-platform',
                encoding: 'utf8'
            });

            const lines = gitStatus.split('\n').filter(l => l.trim());
            this.metrics.filesCreated = lines.filter(l => l.startsWith('??') || l.startsWith('A ')).length;
            this.metrics.filesModified = lines.filter(l => l.startsWith(' M') || l.startsWith('M ')).length;

            // Count lines in new files
            for (const line of lines) {
                const match = line.match(/^\?\?\s+(.+)$/);
                if (match) {
                    const filePath = path.join('C:\\Users\\darri\\100x-platform', match[1].trim());
                    if (fs.existsSync(filePath) && filePath.endsWith('.md')) {
                        const content = fs.readFileSync(filePath, 'utf8');
                        this.metrics.linesWritten += content.split('\n').length;
                    }
                }
            }

            this.log('Analyzed platform changes', {
                filesCreated: this.metrics.filesCreated,
                filesModified: this.metrics.filesModified,
                linesWritten: this.metrics.linesWritten
            });
        } catch (e) {
            this.log('Git analysis failed', { error: e.message });
        }
    }

    async checkNetworkActivity() {
        try {
            // Check coordination status files
            const syncDir = 'C:\\Users\\darri\\SYNC_TO_GDRIVE\\SHARED';
            if (fs.existsSync(syncDir)) {
                const files = fs.readdirSync(syncDir);
                const recentFiles = files.filter(f => {
                    const filePath = path.join(syncDir, f);
                    const stats = fs.statSync(filePath);
                    const age = Date.now() - stats.mtimeMs;
                    return age < 60000; // Modified in last minute
                });

                this.metrics.networkSyncEvents = recentFiles.length;
                this.log('Network activity detected', {
                    recentSyncFiles: recentFiles.length
                });
            }
        } catch (e) {
            this.log('Network check failed', { error: e.message });
        }
    }

    async countActiveProcesses() {
        try {
            // Check for Node.js and Python processes (Trinity systems)
            const nodeProcesses = execSync('tasklist /FI "IMAGENAME eq node.exe" /FO CSV', { encoding: 'utf8' });
            const pythonProcesses = execSync('tasklist /FI "IMAGENAME eq python.exe" /FO CSV', { encoding: 'utf8' });

            const nodeCount = nodeProcesses.split('\n').length - 2; // Header line
            const pythonCount = pythonProcesses.split('\n').length - 2;

            this.metrics.activeProcesses = nodeCount + pythonCount;
            this.log('Active processes counted', {
                node: nodeCount,
                python: pythonCount,
                total: this.metrics.activeProcesses
            });
        } catch (e) {
            this.log('Process count failed', { error: e.message });
        }
    }

    async trackGitActivity() {
        try {
            // Check recent git commits
            const recentCommits = execSync('git log --oneline -5', {
                cwd: 'C:\\Users\\darri\\100x-platform',
                encoding: 'utf8'
            });

            const commitCount = recentCommits.split('\n').filter(l => l.trim()).length;
            this.metrics.gitOperations = commitCount;

            this.log('Git activity tracked', {
                recentCommits: commitCount
            });
        } catch (e) {
            this.log('Git tracking failed', { error: e.message });
        }
    }

    generateReport() {
        const elapsed = Math.floor((new Date() - this.sessionStart) / 1000);

        console.log('\n');
        console.log('═══════════════════════════════════════════════════════════');
        console.log('⚡ AUTONOMOUS SESSION METRICS REPORT');
        console.log('═══════════════════════════════════════════════════════════');
        console.log(`Session ID: ${this.metrics.sessionId}`);
        console.log(`Computer: ${this.metrics.computer}`);
        console.log(`Duration: ${Math.floor(elapsed / 60)}m ${elapsed % 60}s`);
        console.log('───────────────────────────────────────────────────────────');
        console.log(`📝 Lines Written: ${this.metrics.linesWritten}`);
        console.log(`📄 Files Created: ${this.metrics.filesCreated}`);
        console.log(`✏️  Files Modified: ${this.metrics.filesModified}`);
        console.log(`🔄 Git Operations: ${this.metrics.gitOperations}`);
        console.log(`🌐 Network Sync Events: ${this.metrics.networkSyncEvents}`);
        console.log(`⚙️  Active Processes: ${this.metrics.activeProcesses}`);
        console.log(`🎯 Autonomous Actions: ${this.metrics.autonomousActions.length}`);
        console.log('═══════════════════════════════════════════════════════════');
        console.log('\n');

        // Write JSON report
        const reportPath = path.join('C:\\Users\\darri\\100x-platform',
            `AUTONOMOUS_METRICS_${Date.now()}.json`);
        fs.writeFileSync(reportPath, JSON.stringify(this.metrics, null, 2));
        console.log(`✅ Report saved: ${reportPath}`);
    }

    async startTracking() {
        console.log('═══════════════════════════════════════════════════════════');
        console.log('⚡ AUTONOMOUS SESSION METRICS TRACKER');
        console.log('═══════════════════════════════════════════════════════════');
        console.log(`Started: ${this.metrics.startTime}`);
        console.log(`Computer: ${this.metrics.computer}`);
        console.log('Tracking: Lines, Files, Git, Network, Processes');
        console.log('═══════════════════════════════════════════════════════════\n');

        this.log('Session tracking initiated');

        // Initial data collection
        await this.analyzePlatformChanges();
        await this.checkNetworkActivity();
        await this.countActiveProcesses();
        await this.trackGitActivity();

        // Update every 10 seconds
        const interval = setInterval(async () => {
            await this.analyzePlatformChanges();
            await this.checkNetworkActivity();
            await this.countActiveProcesses();

            // Generate report every minute
            const elapsed = Math.floor((new Date() - this.sessionStart) / 1000);
            if (elapsed % 60 === 0) {
                this.generateReport();
            }
        }, 10000);

        // Stop after 5 minutes (for demo)
        setTimeout(() => {
            clearInterval(interval);
            this.generateReport();
            console.log('\n⚡ Autonomous metrics tracking complete\n');
            process.exit(0);
        }, 300000);

        // Handle Ctrl+C
        process.on('SIGINT', () => {
            clearInterval(interval);
            this.generateReport();
            process.exit(0);
        });
    }
}

// Start tracking
const tracker = new AutonomousSessionMetrics();
