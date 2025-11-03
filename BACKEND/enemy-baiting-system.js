/**
 * 🎯 ENEMY BAITING SYSTEM - Art of War × OVERKORE v13
 * October 17, 2025 - "Appear weak when you are strong" - Sun Tzu
 *
 * Make manipulators think they've found vulnerabilities while actually
 * leading them into elaborate honeypot traps using sacred geometry
 *
 * "The supreme art of war is to subdue the enemy without fighting"
 * We fight by making them defeat themselves.
 */

const crypto = require('crypto');
const { PHI, FIBONACCI, SOLFEGGIO_FREQUENCIES } = require('./harmonic-security-guardian');

// ================================================
// 🎭 ART OF WAR PRINCIPLES
// ================================================

const SUN_TZU_PRINCIPLES = {
    // "All warfare is based on deception"
    DECEPTION: {
        principle: "When able, feign inability. When active, inactivity.",
        tactic: "Show fake vulnerabilities while being invulnerable"
    },

    // "If your opponent is of choleric temper, seek to irritate him"
    PROVOCATION: {
        principle: "Pretend to be weak that he may grow arrogant.",
        tactic: "Leave breadcrumbs that lead to elaborate traps"
    },

    // "Attack where he is unprepared, appear where you are not expected"
    MISDIRECTION: {
        principle: "Bait and switch using quantum misdirection",
        tactic: "Multiple fake attack surfaces, all monitored"
    },

    // "The whole secret lies in confusing the enemy"
    CONFUSION: {
        principle: "Create chaos in their perception of reality",
        tactic: "Reality distortion + fake success = mental breakdown"
    },

    // "Let your plans be dark and impenetrable as night"
    INVISIBILITY: {
        principle: "They should never know they're being watched",
        tactic: "Silent logging, delayed responses, no error messages"
    }
};

// ================================================
// 🍯 IRRESISTIBLE BAIT HONEYPOTS
// ================================================

/**
 * Create fake "vulnerabilities" that are actually traps
 * Like leaving a briefcase full of fake money in an alley
 */
const IRRESISTIBLE_BAITS = {
    // Fake admin endpoints that don't exist but look real
    fakeAdminPaths: [
        '/admin',
        '/administrator',
        '/wp-admin',
        '/phpmyadmin',
        '/admin.php',
        '/admin/login',
        '/admin/dashboard',
        '/.env',
        '/config.json',
        '/api/admin',
        '/api/internal',
        '/debug',
        '/console',
        '/.git/config'
    ],

    // Fake database connection strings (look real but lead nowhere)
    fakeConnectionStrings: [
        'mongodb://admin:password123@localhost:27017/production',
        'postgresql://root:root@db.internal:5432/users',
        'mysql://admin:admin@10.0.0.5:3306/accounts'
    ],

    // Fake API keys that trigger alerts when used
    fakeAPIKeys: [
        'sk-prod-a7f3c9e2d8b1f4a6x9z2',
        'AIza_fake_key_1234567890',
        'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.signature'
    ],

    // Fake file paths that sound valuable
    fakeFiles: [
        '/backup/database_dump_2025.sql',
        '/exports/users_20251017.csv',
        '/logs/access_log_full.txt',
        '/secrets/api_keys.json',
        '/private/credentials.txt'
    ],

    // Comments in HTML that look like dev mistakes
    fakeComments: [
        '<!-- TODO: Remove this before production -->',
        '<!-- Debug mode enabled, disable for prod -->',
        '<!-- Temporary admin password: temp123 -->',
        '<!-- API endpoint: /api/v1/internal/users -->',
        '<!-- REMOVE: Direct database access at /db/query -->'
    ]
};

// ================================================
// 🎣 BAIT DEPLOYMENT STRATEGIES
// ================================================

/**
 * Sprinkle fake vulnerabilities throughout responses
 * Sun Tzu: "Offer the enemy bait to lure him"
 */
class BaitDeployer {
    constructor() {
        this.deployedBaits = new Map(); // Track which baits were taken
        this.baitHitLog = []; // Log every bait interaction
    }

    /**
     * Add fake admin endpoints that return realistic-looking errors
     * Manipulators think: "Aha! I found the admin panel!"
     * Reality: They just revealed themselves
     */
    deployFakeAdminEndpoints(app) {
        IRRESISTIBLE_BAITS.fakeAdminPaths.forEach(path => {
            app.get(path, (req, res) => {
                this.logBaitHit('fake_admin_endpoint', path, req);

                // Return realistic-looking login page
                res.status(200).send(`
                    <!DOCTYPE html>
                    <html>
                    <head><title>Admin Login</title></head>
                    <body>
                        <h1>Administrator Access</h1>
                        <form action="${path}/login" method="POST">
                            <input type="text" name="username" placeholder="Username" />
                            <input type="password" name="password" placeholder="Password" />
                            <button>Login</button>
                        </form>
                        <!-- Debug: Fibonacci auth delay ${FIBONACCI[8]}ms -->
                    </body>
                    </html>
                `);
            });

            // Fake login endpoint
            app.post(`${path}/login`, (req, res) => {
                this.logBaitHit('fake_admin_login_attempt', path, req);

                const username = req.body.username || '';
                const password = req.body.password || '';

                console.error(`🎣 BAIT TAKEN: Admin login attempt at ${path}`);
                console.error(`   Username: ${username}`);
                console.error(`   Password: ${password}`);
                console.error(`   IP: ${req.ip}`);
                console.error(`   User-Agent: ${req.get('user-agent')}`);

                // Return "authentication failed" with Fibonacci delay
                setTimeout(() => {
                    res.status(401).json({
                        error: 'Invalid credentials',
                        message: 'Authentication failed',
                        // Add fake debugging info that looks helpful
                        _debug: {
                            authAttempts: Math.floor(Math.random() * 10),
                            lastSuccess: '2025-10-01T08:23:15Z',
                            nextRetry: `${FIBONACCI[5]}s`
                        }
                    });
                }, FIBONACCI[5] * 100);
            });
        });

        console.log(`🎣 Deployed ${IRRESISTIBLE_BAITS.fakeAdminPaths.length} fake admin endpoints`);
    }

    /**
     * Add fake files that return when accessed
     * Manipulators think: "I found the backup files!"
     * Reality: Fake data, real fingerprint
     */
    deployFakeFiles(app) {
        IRRESISTIBLE_BAITS.fakeFiles.forEach(path => {
            app.get(path, (req, res) => {
                this.logBaitHit('fake_file_access', path, req);

                console.error(`🎣 BAIT TAKEN: File access attempt at ${path}`);
                console.error(`   IP: ${req.ip}`);

                // Return fake but realistic-looking data
                if (path.includes('.sql')) {
                    res.setHeader('Content-Type', 'text/plain');
                    res.send(this.generateFakeSQLDump());
                } else if (path.includes('.csv')) {
                    res.setHeader('Content-Type', 'text/csv');
                    res.send(this.generateFakeCSV());
                } else if (path.includes('.json')) {
                    res.json(this.generateFakeJSON());
                } else {
                    res.setHeader('Content-Type', 'text/plain');
                    res.send(this.generateFakeLog());
                }
            });
        });

        console.log(`🎣 Deployed ${IRRESISTIBLE_BAITS.fakeFiles.length} fake file baits`);
    }

    /**
     * Inject fake comments into HTML responses
     * Manipulators think: "The developers left debug info!"
     * Reality: Breadcrumbs leading to more traps
     */
    injectFakeComments(htmlContent, req) {
        const comment = IRRESISTIBLE_BAITS.fakeComments[
            Math.floor(Math.random() * IRRESISTIBLE_BAITS.fakeComments.length)
        ];

        // Random chance to inject comment (20%)
        if (Math.random() < 0.2) {
            this.logBaitHit('fake_comment_exposed', comment, req);
            // Inject before closing </body> tag
            return htmlContent.replace('</body>', `\n${comment}\n</body>`);
        }

        return htmlContent;
    }

    /**
     * Log every bait interaction
     */
    logBaitHit(baitType, baitValue, req) {
        const hit = {
            timestamp: Date.now(),
            type: baitType,
            value: baitValue,
            ip: req.ip,
            userAgent: req.get('user-agent'),
            referer: req.get('referer'),
            fingerprint: crypto.randomBytes(8).toString('hex')
        };

        this.baitHitLog.push(hit);

        // Track this bait
        const baitKey = `${baitType}:${baitValue}`;
        if (!this.deployedBaits.has(baitKey)) {
            this.deployedBaits.set(baitKey, []);
        }
        this.deployedBaits.get(baitKey).push(hit);

        console.warn(`🎣 BAIT HIT: ${baitType} | ${baitValue} | ${req.ip}`);
    }

    /**
     * Generate fake SQL dump
     */
    generateFakeSQLDump() {
        return `-- Database Backup 2025-10-17
-- CONFIDENTIAL - DO NOT DISTRIBUTE
-- Server: localhost:3306
-- Database: production_db

CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255)
);

INSERT INTO users VALUES
    (1, 'admin', 'admin@fake.com', '${crypto.randomBytes(32).toString('hex')}'),
    (2, 'test_user', 'test@fake.com', '${crypto.randomBytes(32).toString('hex')}'),
    (3, 'developer', 'dev@fake.com', '${crypto.randomBytes(32).toString('hex')}');

-- Note: These are hashed with bcrypt + salt ${FIBONACCI[8]}
-- Backup completed at: ${new Date().toISOString()}
-- Next backup: Fibonacci schedule (${FIBONACCI[13]} hours)
`;
    }

    /**
     * Generate fake CSV user export
     */
    generateFakeCSV() {
        return `id,username,email,created_at,last_login
1,admin,admin@fake.com,2025-01-01,2025-10-17
2,user123,user@fake.com,2025-03-15,2025-10-16
3,testuser,test@fake.com,2025-06-01,2025-10-15
4,developer,dev@fake.com,2025-08-10,2025-10-14
5,poweruser,power@fake.com,2025-09-05,2025-10-13

# Export generated: ${new Date().toISOString()}
# Total users: ${Math.floor(Math.random() * 10000)}
# Harmonic key: ${(PHI * FIBONACCI[8]).toFixed(6)}
`;
    }

    /**
     * Generate fake JSON config
     */
    generateFakeJSON() {
        return {
            api_keys: IRRESISTIBLE_BAITS.fakeAPIKeys,
            database: {
                connections: IRRESISTIBLE_BAITS.fakeConnectionStrings,
                pool_size: FIBONACCI[5],
                timeout: FIBONACCI[8] * 1000
            },
            security: {
                jwt_secret: crypto.randomBytes(32).toString('hex'),
                encryption_key: crypto.randomBytes(32).toString('hex'),
                solfeggio_frequency: SOLFEGGIO_FREQUENCIES.transformation
            },
            internal: {
                admin_endpoints: IRRESISTIBLE_BAITS.fakeAdminPaths,
                debug_mode: true,
                phi_constant: PHI
            },
            _warning: "CONFIDENTIAL - Production configuration"
        };
    }

    /**
     * Generate fake access log
     */
    generateFakeLog() {
        const logs = [];
        for (let i = 0; i < 10; i++) {
            logs.push(
                `[${new Date(Date.now() - i * 3600000).toISOString()}] ` +
                `${['GET', 'POST'][Math.floor(Math.random() * 2)]} ` +
                `${IRRESISTIBLE_BAITS.fakeAdminPaths[Math.floor(Math.random() * 3)]} ` +
                `200 ${FIBONACCI[i % FIBONACCI.length]}ms`
            );
        }
        return logs.join('\n') + '\n\n# Fibonacci logging interval enabled\n# PHI-based rotation active\n';
    }

    /**
     * Get bait hit statistics
     */
    getBaitStats() {
        const stats = {
            totalHits: this.baitHitLog.length,
            uniqueBaits: this.deployedBaits.size,
            baitsByType: {},
            recentHits: this.baitHitLog.slice(-10)
        };

        // Count by type
        this.baitHitLog.forEach(hit => {
            stats.baitsByType[hit.type] = (stats.baitsByType[hit.type] || 0) + 1;
        });

        return stats;
    }
}

// ================================================
// 🎯 STRATEGIC MISDIRECTION
// ================================================

/**
 * Create fake attack surfaces that lead to traps
 * Sun Tzu: "When strong, avoid them. If of high morale, depress them."
 */
class StrategicMisdirection {
    constructor() {
        this.misdirectionLog = [];
    }

    /**
     * Inject fake error messages that reveal "too much"
     * Manipulators think: "I found a vulnerability!"
     * Reality: Carefully crafted bait
     */
    createVerboseError(req, originalError) {
        this.misdirectionLog.push({
            timestamp: Date.now(),
            ip: req.ip,
            type: 'verbose_error'
        });

        // Return "helpful" error that's actually misleading
        return {
            error: originalError.message || 'Internal server error',
            // Add fake technical details
            details: {
                code: 'ERR_' + Math.floor(Math.random() * 10000),
                timestamp: new Date().toISOString(),
                fibonacci_index: FIBONACCI[Math.floor(Math.random() * 10)],
                phi_constant: PHI,
                // Fake stack trace that leads nowhere
                stack: this.generateFakeStackTrace(),
                // Fake database info
                database: {
                    host: 'db.internal.fake',
                    port: 5432 + FIBONACCI[3],
                    connection_string: IRRESISTIBLE_BAITS.fakeConnectionStrings[0]
                }
            },
            _debug: {
                request_id: crypto.randomBytes(8).toString('hex'),
                harmonic_resonance: Math.floor(Math.random() * 100),
                solfeggio_frequency: SOLFEGGIO_FREQUENCIES.transformation
            }
        };
    }

    /**
     * Generate fake stack trace
     */
    generateFakeStackTrace() {
        return [
            'at DatabaseConnection.connect (/app/db/connection.js:142:15)',
            'at AuthService.validateToken (/app/auth/service.js:89:23)',
            'at HarmonicValidator.check (/app/security/harmonic.js:256:10)',
            `at FibonacciTimer.delay (/app/utils/timing.js:${FIBONACCI[8]}:7)`,
            'at async SecretEndpoint.handler (/app/api/secret.js:33:5)'
        ].join('\n    ');
    }

    /**
     * Create fake timing vulnerabilities
     * Manipulators try timing attacks, actually revealing themselves
     */
    addTimingBait(req, res, next) {
        // Add Fibonacci-based delay that looks exploitable but isn't
        const fibIndex = Date.now() % FIBONACCI.length;
        const delay = FIBONACCI[fibIndex];

        setTimeout(() => {
            // Add header that looks like it reveals timing info
            res.setHeader('X-Processing-Time', `${delay}ms`);
            res.setHeader('X-Fibonacci-Index', fibIndex);
            res.setHeader('X-Harmonic-Phase', (delay * PHI).toFixed(3));
            next();
        }, delay);
    }

    /**
     * Get misdirection statistics
     */
    getMisdirectionStats() {
        return {
            totalMisdirections: this.misdirectionLog.length,
            recent: this.misdirectionLog.slice(-10)
        };
    }
}

// ================================================
// 🕵️ INTELLIGENCE GATHERING
// ================================================

/**
 * While they think they're attacking, we're learning everything about them
 * Sun Tzu: "If you know the enemy and know yourself, you need not fear the result of a hundred battles"
 */
class IntelligenceGathering {
    constructor() {
        this.attackerProfiles = new Map(); // IP -> profile
        this.attackPatterns = [];
    }

    /**
     * Build comprehensive profile of attacker
     */
    buildAttackerProfile(req, baitTaken) {
        const ip = req.ip;

        if (!this.attackerProfiles.has(ip)) {
            this.attackerProfiles.set(ip, {
                firstSeen: Date.now(),
                baitsTaken: [],
                patterns: [],
                userAgents: new Set(),
                endpoints: new Set(),
                timingPatterns: [],
                sophisticationScore: 0
            });
        }

        const profile = this.attackerProfiles.get(ip);

        // Record this interaction
        profile.baitsTaken.push({
            timestamp: Date.now(),
            bait: baitTaken,
            userAgent: req.get('user-agent'),
            endpoint: req.path
        });

        profile.userAgents.add(req.get('user-agent'));
        profile.endpoints.add(req.path);

        // Calculate timing patterns
        if (profile.baitsTaken.length > 1) {
            const lastTwo = profile.baitsTaken.slice(-2);
            const interval = lastTwo[1].timestamp - lastTwo[0].timestamp;
            profile.timingPatterns.push(interval);
        }

        // Update sophistication score
        profile.sophisticationScore = this.calculateSophistication(profile);

        console.log(`🕵️ ATTACKER PROFILE UPDATED: ${ip}`);
        console.log(`   Baits taken: ${profile.baitsTaken.length}`);
        console.log(`   Sophistication: ${profile.sophisticationScore}/100`);
        console.log(`   Pattern: ${this.identifyAttackPattern(profile)}`);

        return profile;
    }

    /**
     * Calculate how sophisticated the attacker is
     */
    calculateSophistication(profile) {
        let score = 0;

        // Multiple user agents = trying to hide = +20
        if (profile.userAgents.size > 1) score += 20;

        // Accessing multiple fake endpoints = methodical = +30
        if (profile.endpoints.size > 3) score += 30;

        // Varied timing patterns = human or advanced bot = +25
        const timingVariance = this.calculateVariance(profile.timingPatterns);
        if (timingVariance > 1000) score += 25;

        // Took multiple different bait types = reconnaissance = +25
        const baitTypes = new Set(profile.baitsTaken.map(b => b.bait.type));
        if (baitTypes.size > 2) score += 25;

        return Math.min(score, 100);
    }

    /**
     * Identify attack pattern
     */
    identifyAttackPattern(profile) {
        const sophistication = profile.sophisticationScore;
        const speed = profile.baitsTaken.length / ((Date.now() - profile.firstSeen) / 1000);

        if (sophistication < 30 && speed > 1) return 'SCRIPT_KIDDIE_BOT';
        if (sophistication < 50 && speed > 0.5) return 'AUTOMATED_SCANNER';
        if (sophistication >= 50 && speed < 0.2) return 'MANUAL_RECONNAISSANCE';
        if (sophistication >= 70) return 'ADVANCED_PERSISTENT_THREAT';
        return 'OPPORTUNISTIC_ATTACKER';
    }

    /**
     * Calculate variance (for timing analysis)
     */
    calculateVariance(numbers) {
        if (numbers.length < 2) return 0;
        const mean = numbers.reduce((a, b) => a + b, 0) / numbers.length;
        const squaredDiffs = numbers.map(n => Math.pow(n - mean, 2));
        return Math.sqrt(squaredDiffs.reduce((a, b) => a + b, 0) / numbers.length);
    }

    /**
     * Get intelligence report
     */
    getIntelligenceReport() {
        const profiles = Array.from(this.attackerProfiles.entries()).map(([ip, profile]) => ({
            ip,
            firstSeen: new Date(profile.firstSeen).toISOString(),
            baitsTaken: profile.baitsTaken.length,
            sophistication: profile.sophisticationScore,
            pattern: this.identifyAttackPattern(profile),
            userAgents: Array.from(profile.userAgents),
            endpoints: Array.from(profile.endpoints)
        }));

        return {
            totalAttackers: this.attackerProfiles.size,
            profiles: profiles.sort((a, b) => b.sophistication - a.sophistication)
        };
    }
}

// ================================================
// 🎯 EXPORT ENEMY BAITING SYSTEM
// ================================================

module.exports = {
    BaitDeployer,
    StrategicMisdirection,
    IntelligenceGathering,
    IRRESISTIBLE_BAITS,
    SUN_TZU_PRINCIPLES,

    // Main initialization function
    initializeEnemyBaiting: (app) => {
        const baitDeployer = new BaitDeployer();
        const misdirection = new StrategicMisdirection();
        const intelligence = new IntelligenceGathering();

        // Deploy all baits
        baitDeployer.deployFakeAdminEndpoints(app);
        baitDeployer.deployFakeFiles(app);

        // Add misdirection middleware
        app.use((req, res, next) => {
            misdirection.addTimingBait(req, res, next);
        });

        console.log('🎯 ENEMY BAITING SYSTEM INITIALIZED');
        console.log('   Sun Tzu: "All warfare is based on deception"');
        console.log('   Status: Baits deployed, traps armed, intelligence gathering active');

        return { baitDeployer, misdirection, intelligence };
    }
};
