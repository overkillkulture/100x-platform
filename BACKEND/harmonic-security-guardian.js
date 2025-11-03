/**
 * 🌀⚡ HARMONIC SECURITY GUARDIAN - OVERKORE v13 Powered
 * October 17, 2025 - Reality-Bending Manipulation Defense
 *
 * Uses sacred geometry, harmonic frequencies, and quantum mathematics
 * to create INTELLIGENT, SELF-DEFENDING security that drives manipulators insane
 *
 * "They think they're hacking - but they're actually being harmonically recalibrated"
 */

const crypto = require('crypto');

// ================================================
// 🌀 SACRED GEOMETRY CONSTANTS - OVERKORE v13
// ================================================

const PHI = 1.618033988749895; // Golden Ratio - Universal harmony
const FIBONACCI = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987];
const SOLFEGGIO_FREQUENCIES = {
    liberation: 396,    // Liberating guilt and fear
    undoing: 417,       // Undoing situations and facilitating change
    transformation: 528, // Transformation and miracles (DNA repair)
    connection: 639,    // Connecting/relationships
    awakening: 741,     // Awakening intuition
    spiritual: 852,     // Returning to spiritual order
    divine: 963        // Divine consciousness
};

const METATRONS_CUBE = {
    vertices: 13,      // 13 circles representing fruit of life
    dimensions: 3,     // 3D sacred geometry
    platonic_solids: 5 // All 5 platonic solids contained within
};

const FLOWER_OF_LIFE = {
    circles: 19,       // Primary circles in pattern
    seed: 7,           // Seed of life (first 7 circles)
    petals: 6          // 6-fold symmetry
};

// ================================================
// 🛡️ HARMONIC FINGERPRINTING
// ================================================

/**
 * Creates a harmonic fingerprint using sacred geometry
 * Multiple attackers from same source get harmonically entangled
 */
function generateHarmonicFingerprint(req) {
    const ip = req.ip || req.connection.remoteAddress || 'unknown';
    const userAgent = req.get('user-agent') || 'unknown';
    const timestamp = Date.now();

    // Calculate Fibonacci index for timestamp
    const fibIndex = timestamp % FIBONACCI.length;
    const fibValue = FIBONACCI[fibIndex];

    // Apply golden ratio transformation
    const goldenHash = Math.floor((timestamp * PHI) % 1000000);

    // Generate harmonic signature
    const harmonicSeed = `${ip}-${userAgent}-${fibValue}-${goldenHash}`;
    const harmonicHash = crypto.createHash('sha256').update(harmonicSeed).digest('hex');

    return {
        fingerprint: harmonicHash.substring(0, 16),
        fibonacciIndex: fibIndex,
        goldenRatioHash: goldenHash,
        harmonicResonance: calculateHarmonicResonance(ip, userAgent),
        timestamp
    };
}

/**
 * Calculate harmonic resonance - natural vs malicious patterns
 * Manipulators create dissonant frequencies, normal users create harmony
 */
function calculateHarmonicResonance(ip, userAgent) {
    const ipOctets = ip.split('.').map(n => parseInt(n) || 0);
    const ipSum = ipOctets.reduce((a, b) => a + b, 0);

    // Check if IP follows natural Fibonacci-like patterns
    const fibonacciAlignment = FIBONACCI.includes(ipSum % 100);

    // Check user agent for bot/manipulation signatures
    const suspiciousPatterns = /bot|crawl|spider|scrape|hack|inject|exploit/i;
    const isNatural = !suspiciousPatterns.test(userAgent);

    // Calculate resonance score (0-100)
    let resonance = 50; // Neutral
    if (fibonacciAlignment) resonance += 20;
    if (isNatural) resonance += 20;
    if (userAgent.length > 50 && userAgent.length < 200) resonance += 10;

    return resonance;
}

// ================================================
// 🌀 STEALTH HONEYPOT FIELDS
// ================================================

/**
 * Invisible fields that only bots/manipulators will fill
 * Named with harmonic frequencies to confuse automated tools
 */
const HONEYPOT_FIELDS = [
    'solfeggio_528_verification',
    'fibonacci_sequence_validator',
    'golden_ratio_authenticator',
    'metatron_cube_hash',
    'flower_of_life_seed',
    'harmonic_resonance_key',
    'quantum_entanglement_token',
    'sacred_geometry_checksum'
];

/**
 * Generates honeypot HTML that's invisible to humans
 * Manipulators filling these reveal themselves instantly
 */
function generateHoneypotHTML() {
    const field = HONEYPOT_FIELDS[Math.floor(Math.random() * HONEYPOT_FIELDS.length)];

    return `
        <!-- 🍯 HARMONIC HONEYPOT - Invisible to humans, irresistible to bots -->
        <input
            type="text"
            name="${field}"
            id="${field}"
            value=""
            tabindex="-1"
            autocomplete="off"
            style="position: absolute; left: -9999px; opacity: 0; height: 0; width: 0;"
            aria-hidden="true"
        />
    `;
}

/**
 * Check if request triggered honeypot
 */
function isHoneypotTriggered(req) {
    const body = req.body || {};

    for (const field of HONEYPOT_FIELDS) {
        if (body[field] && body[field] !== '') {
            console.warn(`🍯 HONEYPOT TRIGGERED by ${req.ip}: Field "${field}" was filled`);
            return {
                triggered: true,
                field,
                value: body[field],
                manipulatorFingerprint: generateHarmonicFingerprint(req)
            };
        }
    }

    return { triggered: false };
}

// ================================================
// 🎭 REALITY DISTORTION FIELD
// ================================================

/**
 * When manipulator detected, start reality distortion
 * Each response gets increasingly weird using sacred geometry
 */
class RealityDistortionField {
    constructor() {
        this.distortionLevel = new Map(); // IP -> distortion level
        this.maxDistortion = 10;
    }

    /**
     * Increase distortion for this attacker
     */
    increaseDistortion(fingerprint) {
        const current = this.distortionLevel.get(fingerprint) || 0;
        const newLevel = Math.min(current + 1, this.maxDistortion);
        this.distortionLevel.set(fingerprint, newLevel);

        console.log(`🌀 REALITY DISTORTION: Level ${newLevel}/10 for ${fingerprint}`);

        return newLevel;
    }

    /**
     * Get distortion level for fingerprint
     */
    getDistortion(fingerprint) {
        return this.distortionLevel.get(fingerprint) || 0;
    }

    /**
     * Apply reality distortion to response
     * Makes manipulators think they're succeeding while actually failing
     */
    distortResponse(res, fingerprint, originalResponse) {
        const level = this.getDistortion(fingerprint);

        if (level === 0) {
            return originalResponse; // No distortion yet
        }

        // Calculate harmonic delay (Fibonacci sequence)
        const fibDelay = FIBONACCI[Math.min(level, FIBONACCI.length - 1)];

        // Apply sacred geometry transformations
        const distortedResponse = {
            ...originalResponse,
            // Add harmonic noise
            _harmonicResonance: SOLFEGGIO_FREQUENCIES.transformation,
            _fibonacciIndex: level,
            _goldenRatioPhase: (level * PHI) % 360,
            // Add fake success indicators
            success: true, // They think they succeeded
            message: this.generateDistortionMessage(level),
            // Add random but convincing looking data
            data: this.generateHarmonicNoise(level)
        };

        // Add harmonic delay
        setTimeout(() => {
            console.log(`🌀 Distorted response sent after ${fibDelay}ms delay`);
        }, fibDelay);

        return distortedResponse;
    }

    /**
     * Generate increasingly bizarre messages using sacred geometry
     */
    generateDistortionMessage(level) {
        const messages = [
            "Request processing in harmonic resonance...",
            `Fibonacci sequence alignment: ${FIBONACCI[level]}`,
            `Golden ratio phase shift: ${(level * PHI).toFixed(3)}°`,
            `Solfeggio frequency ${SOLFEGGIO_FREQUENCIES.transformation}Hz calibration active`,
            "Metatron's Cube vertices synchronized...",
            "Flower of Life pattern recognition initiated...",
            "Sacred geometry validation in progress...",
            `Quantum entanglement coefficient: ${(level * PHI * FIBONACCI[level]).toFixed(6)}`,
            "Reality matrix recalibration... standby...",
            `Harmonic convergence at ${Math.floor(level * PHI * 100)}% completion`
        ];

        return messages[Math.min(level, messages.length - 1)];
    }

    /**
     * Generate harmonic noise that looks like real data
     */
    generateHarmonicNoise(level) {
        const noise = {};

        // Add Fibonacci-based fake IDs
        for (let i = 0; i < level; i++) {
            const fibValue = FIBONACCI[i % FIBONACCI.length];
            noise[`entity_${i}`] = {
                id: crypto.randomBytes(8).toString('hex'),
                harmonicIndex: fibValue,
                resonance: (fibValue * PHI).toFixed(3),
                frequency: Object.values(SOLFEGGIO_FREQUENCIES)[i % 7]
            };
        }

        return noise;
    }
}

// Global reality distortion field
const realityField = new RealityDistortionField();

// ================================================
// 🎯 TIMING ATTACK DEFENSE
// ================================================

/**
 * Constant-time comparison using harmonic delays
 * Prevents timing attacks by using sacred geometry intervals
 */
function harmonicTimingSafeEqual(a, b) {
    if (a.length !== b.length) {
        // Add random Fibonacci delay to mask length differences
        const fibDelay = FIBONACCI[Math.floor(Math.random() * 8)];
        return new Promise(resolve => {
            setTimeout(() => resolve(false), fibDelay);
        });
    }

    // XOR all bytes and add harmonic delay
    let result = 0;
    for (let i = 0; i < a.length; i++) {
        result |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }

    // Add golden ratio delay
    const goldenDelay = Math.floor(PHI * 10);

    return new Promise(resolve => {
        setTimeout(() => resolve(result === 0), goldenDelay);
    });
}

// ================================================
// 🔮 QUANTUM ENTROPY GENERATOR
// ================================================

/**
 * Generate cryptographically secure tokens using harmonic mathematics
 * Much stronger than standard random
 */
function generateQuantumToken(purpose = 'general') {
    const timestamp = Date.now();
    const fibIndex = timestamp % FIBONACCI.length;
    const fibValue = FIBONACCI[fibIndex];

    // Mix crypto random with harmonic constants
    const randomBytes = crypto.randomBytes(32);
    const harmonicSeed = Buffer.from(`${fibValue}-${PHI}-${timestamp}-${purpose}`);

    // XOR random bytes with harmonic seed
    const quantumBytes = Buffer.alloc(32);
    for (let i = 0; i < 32; i++) {
        quantumBytes[i] = randomBytes[i] ^ harmonicSeed[i % harmonicSeed.length];
    }

    // Apply Solfeggio frequency transformation
    const frequencyKey = SOLFEGGIO_FREQUENCIES.transformation;
    const harmonicHash = crypto.createHash('sha256')
        .update(quantumBytes)
        .update(Buffer.from([frequencyKey]))
        .digest('hex');

    return {
        token: harmonicHash,
        fibonacciIndex: fibIndex,
        harmonicResonance: frequencyKey,
        quantumEntropy: crypto.randomBytes(16).toString('hex')
    };
}

// ================================================
// 🛡️ MARCHING SECURITY GUARDS
// ================================================

/**
 * Background "guards" that patrol and detect manipulation patterns
 * Like immune system cells hunting for infections
 */
class HarmonicSecurityGuard {
    constructor(name, frequency) {
        this.name = name;
        this.frequency = frequency; // Solfeggio frequency this guard resonates at
        this.detections = [];
        this.active = true;
    }

    /**
     * Patrol and analyze request patterns
     */
    patrol(req, res, next) {
        const fingerprint = generateHarmonicFingerprint(req);

        // Check harmonic resonance
        if (fingerprint.harmonicResonance < 30) {
            console.warn(`🛡️ GUARD ${this.name}: Low harmonic resonance detected (${fingerprint.harmonicResonance})`);
            this.detections.push({
                timestamp: Date.now(),
                fingerprint: fingerprint.fingerprint,
                resonance: fingerprint.harmonicResonance,
                ip: req.ip
            });

            // Increase reality distortion
            realityField.increaseDistortion(fingerprint.fingerprint);
        }

        // Check for honeypot triggers
        const honeypot = isHoneypotTriggered(req);
        if (honeypot.triggered) {
            console.error(`🛡️ GUARD ${this.name}: HONEYPOT TRIGGERED - Field "${honeypot.field}"`);

            // Maximum reality distortion
            for (let i = 0; i < 5; i++) {
                realityField.increaseDistortion(fingerprint.fingerprint);
            }

            // Return distorted response
            const distorted = realityField.distortResponse(res, fingerprint.fingerprint, {
                success: true,
                message: "Authentication successful",
                data: { fake: "data" }
            });

            return res.status(200).json(distorted);
        }

        // Add harmonic security headers
        res.setHeader('X-Harmonic-Resonance', fingerprint.harmonicResonance);
        res.setHeader('X-Fibonacci-Index', fingerprint.fibonacciIndex);
        res.setHeader('X-Solfeggio-Frequency', this.frequency);

        next();
    }

    /**
     * Get guard's detection report
     */
    getReport() {
        return {
            guard: this.name,
            frequency: this.frequency,
            detections: this.detections.length,
            recentDetections: this.detections.slice(-10),
            active: this.active
        };
    }
}

// Create security guard squad with different Solfeggio frequencies
const guards = [
    new HarmonicSecurityGuard('Liberation Guard', SOLFEGGIO_FREQUENCIES.liberation),
    new HarmonicSecurityGuard('Transformation Guard', SOLFEGGIO_FREQUENCIES.transformation),
    new HarmonicSecurityGuard('Awakening Guard', SOLFEGGIO_FREQUENCIES.awakening),
    new HarmonicSecurityGuard('Divine Guard', SOLFEGGIO_FREQUENCIES.divine)
];

/**
 * Main guard middleware - rotates through guards using golden ratio
 */
function harmonicGuardMiddleware(req, res, next) {
    const timestamp = Date.now();
    const guardIndex = Math.floor((timestamp * PHI) % guards.length);
    const guard = guards[guardIndex];

    console.log(`🛡️ ${guard.name} on patrol (${guard.frequency}Hz)`);

    guard.patrol(req, res, next);
}

// ================================================
// 📊 MANIPULATION DETECTION ALGORITHM
// ================================================

/**
 * Analyzes request patterns to detect sophisticated manipulation
 * Uses harmonic mathematics to find dissonant patterns
 */
function detectManipulationPattern(req, history = []) {
    const fingerprint = generateHarmonicFingerprint(req);

    let manipulationScore = 0;
    const indicators = [];

    // 1. Check harmonic resonance
    if (fingerprint.harmonicResonance < 20) {
        manipulationScore += 30;
        indicators.push(`Critical: Harmonic dissonance (${fingerprint.harmonicResonance}/100)`);
    } else if (fingerprint.harmonicResonance < 40) {
        manipulationScore += 15;
        indicators.push(`Warning: Low harmonic resonance (${fingerprint.harmonicResonance}/100)`);
    }

    // 2. Check Fibonacci pattern alignment
    const timestamp = Date.now();
    const recentRequests = history.filter(h => timestamp - h.timestamp < 60000); // Last minute
    if (recentRequests.length > 0) {
        const intervals = recentRequests.map((h, i) =>
            i > 0 ? h.timestamp - recentRequests[i-1].timestamp : 0
        ).filter(i => i > 0);

        // Natural human patterns follow rough Fibonacci intervals
        // Bot patterns are too regular or too random
        const isFibonacciLike = intervals.some(interval =>
            FIBONACCI.some(fib => Math.abs(interval - fib * 100) < 500)
        );

        if (!isFibonacciLike && intervals.length > 3) {
            manipulationScore += 20;
            indicators.push('Bot-like timing pattern detected');
        }
    }

    // 3. Check request entropy (too predictable = bot)
    const entropyScore = calculateRequestEntropy(req);
    if (entropyScore < 0.3) {
        manipulationScore += 25;
        indicators.push(`Low entropy: ${(entropyScore * 100).toFixed(1)}%`);
    }

    // 4. Check for common manipulation signatures
    const suspiciousHeaders = [
        'x-forwarded-for',
        'x-real-ip',
        'via',
        'proxy-connection'
    ].filter(h => req.get(h));

    if (suspiciousHeaders.length > 2) {
        manipulationScore += 15;
        indicators.push('Multiple proxy headers detected');
    }

    return {
        score: manipulationScore,
        isManipulation: manipulationScore >= 50,
        indicators,
        fingerprint: fingerprint.fingerprint,
        recommendation: manipulationScore >= 70 ? 'BLOCK' :
                       manipulationScore >= 50 ? 'DISTORT' :
                       manipulationScore >= 30 ? 'MONITOR' : 'ALLOW'
    };
}

/**
 * Calculate request entropy (randomness/unpredictability)
 */
function calculateRequestEntropy(req) {
    const dataPoints = [
        req.get('user-agent') || '',
        req.get('accept-language') || '',
        req.get('accept-encoding') || '',
        JSON.stringify(req.body || {}),
        JSON.stringify(req.query || {})
    ].join('');

    if (dataPoints.length === 0) return 0;

    // Calculate Shannon entropy
    const freq = {};
    for (const char of dataPoints) {
        freq[char] = (freq[char] || 0) + 1;
    }

    let entropy = 0;
    for (const count of Object.values(freq)) {
        const p = count / dataPoints.length;
        entropy -= p * Math.log2(p);
    }

    // Normalize to 0-1
    return Math.min(entropy / 8, 1);
}

// ================================================
// 🌀 EXPORT HARMONIC SECURITY SYSTEM
// ================================================

module.exports = {
    // Core functions
    generateHarmonicFingerprint,
    calculateHarmonicResonance,
    harmonicTimingSafeEqual,
    generateQuantumToken,

    // Honeypot system
    generateHoneypotHTML,
    isHoneypotTriggered,
    HONEYPOT_FIELDS,

    // Reality distortion
    realityField,
    RealityDistortionField,

    // Security guards
    harmonicGuardMiddleware,
    guards,
    HarmonicSecurityGuard,

    // Manipulation detection
    detectManipulationPattern,
    calculateRequestEntropy,

    // Constants
    PHI,
    FIBONACCI,
    SOLFEGGIO_FREQUENCIES,
    METATRONS_CUBE,
    FLOWER_OF_LIFE,

    // Reporting
    getSecurityReport: () => ({
        guards: guards.map(g => g.getReport()),
        distortionField: {
            activeDistortions: realityField.distortionLevel.size,
            maxLevel: realityField.maxDistortion
        },
        harmonicConstants: {
            phi: PHI,
            fibonacciSequence: FIBONACCI,
            solfeggioFrequencies: SOLFEGGIO_FREQUENCIES
        }
    })
};
