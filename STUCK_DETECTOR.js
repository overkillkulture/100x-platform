// STUCK DETECTOR MODULE
// When we get stuck → Automatically suggest new abilities to build

class StuckDetector {
    constructor() {
        this.stuckPatterns = [];
        this.solutionsSuggested = [];
        this.abilitiesBuilt = [];
        this.startTime = Date.now();
    }

    // Detect if we're stuck
    detectStuck(context) {
        const patterns = {
            // SSL/Certificate Hell
            sslCertificateHell: {
                keywords: ['ssl', 'certificate', 'self-signed', 'tls', 'https'],
                timeThreshold: 30 * 60 * 1000, // 30 minutes
                solution: 'Add alternative authentication (invite codes, passkeys)',
                newAbility: 'Passwordless auth system'
            },

            // Database Connection Issues
            databaseHell: {
                keywords: ['database', 'connection', 'postgres', 'sequelize', 'pool'],
                timeThreshold: 20 * 60 * 1000,
                solution: 'Switch to SQLite or simpler database',
                newAbility: 'File-based database system'
            },

            // Deployment Hell
            deploymentHell: {
                keywords: ['deploy', 'build', 'failed', 'timeout', 'error'],
                timeThreshold: 45 * 60 * 1000,
                solution: 'Switch deployment platform (Render, Railway, Fly.io)',
                newAbility: 'Multi-platform deployment'
            },

            // Environment Variable Hell
            envVarHell: {
                keywords: ['environment', 'env', 'config', 'variable', 'missing'],
                timeThreshold: 15 * 60 * 1000,
                solution: 'Eliminate environment variables, use files or defaults',
                newAbility: 'Zero-config deployment'
            },

            // Debugging Hell (can't see what's happening)
            debuggingHell: {
                keywords: ['debug', 'console', 'log', 'error', 'trace'],
                timeThreshold: 20 * 60 * 1000,
                solution: 'Add visual debugging dashboard',
                newAbility: 'Real-time visual debugger'
            },

            // Complexity Hell (too many moving parts)
            complexityHell: {
                keywords: ['complex', 'microservice', 'dependency', 'framework'],
                timeThreshold: 60 * 60 * 1000, // 1 hour
                solution: 'Burn it down, build simpler',
                newAbility: 'Monolithic simplification'
            }
        };

        // Check each pattern
        for (const [name, pattern] of Object.entries(patterns)) {
            const matchCount = pattern.keywords.filter(keyword =>
                context.toLowerCase().includes(keyword)
            ).length;

            if (matchCount >= 2) {
                return {
                    stuck: true,
                    pattern: name,
                    solution: pattern.solution,
                    newAbility: pattern.newAbility,
                    confidence: matchCount / pattern.keywords.length
                };
            }
        }

        return { stuck: false };
    }

    // Suggest new ability to build
    suggestAbility(stuckContext) {
        const detection = this.detectStuck(stuckContext);

        if (detection.stuck) {
            console.log('\n🚨 STUCK DETECTED! 🚨');
            console.log(`Pattern: ${detection.pattern}`);
            console.log(`Confidence: ${(detection.confidence * 100).toFixed(0)}%`);
            console.log(`\n💡 SOLUTION: ${detection.solution}`);
            console.log(`\n🔧 NEW ABILITY TO BUILD: ${detection.newAbility}`);
            console.log('\n⚡ Time to expand the system, not fight it!\n');

            this.solutionsSuggested.push({
                timestamp: new Date().toISOString(),
                pattern: detection.pattern,
                solution: detection.solution,
                ability: detection.newAbility
            });

            return detection;
        }

        return null;
    }

    // Log when we actually build the new ability
    abilityBuilt(abilityName, description) {
        this.abilitiesBuilt.push({
            timestamp: new Date().toISOString(),
            name: abilityName,
            description: description,
            timeStuck: Date.now() - this.startTime
        });

        console.log(`\n✅ NEW ABILITY UNLOCKED: ${abilityName}`);
        console.log(`Description: ${description}`);
        console.log(`Time stuck before breakthrough: ${(this.abilitiesBuilt[this.abilitiesBuilt.length - 1].timeStuck / 60000).toFixed(1)} minutes\n`);
    }

    // Get stuck report
    getReport() {
        return {
            totalTimeInSession: Date.now() - this.startTime,
            solutionsSuggested: this.solutionsSuggested.length,
            abilitiesBuilt: this.abilitiesBuilt.length,
            evolutionRate: this.abilitiesBuilt.length / (Date.now() - this.startTime) * 3600000, // abilities per hour
            details: {
                suggested: this.solutionsSuggested,
                built: this.abilitiesBuilt
            }
        };
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StuckDetector;
}

// Example usage:
/*
const detector = new StuckDetector();

// When you're stuck, ask:
detector.suggestAbility("We're stuck with SSL certificate errors for 3 hours");
// Output: Build new ability → "Passwordless auth system"

// When you build it:
detector.abilityBuilt("Invite Code Authentication", "Genesis keys replace passwords entirely");

// Get report:
console.log(detector.getReport());
*/
