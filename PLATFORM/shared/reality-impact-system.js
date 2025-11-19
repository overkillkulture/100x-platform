/**
 * REALITY IMPACT SYSTEM - Layer 3
 *
 * Purpose: Prove the product is ALIVE, ACTIVE, and MANIFESTING in reality
 * Position: Manifestation (C3 Oracle, Future, Reality, Soul, Domains 6-7)
 * Status: PERMANENT (like Badge and Stamps)
 *
 * Trinity Pattern Complete:
 * Layer 1 (Badge) → Foundation → Shows what EXISTS
 * Layer 2 (Stamps) → Validation → Shows what's VERIFIED
 * Layer 3 (Impact) → Manifestation → Shows what's ALIVE
 */

const RealityImpact = {
    version: '1.0.0',
    enabled: true,

    config: {
        productId: null,
        productName: null,
        updateInterval: 30000, // Update every 30 seconds
        heartbeatInterval: 60000, // Heartbeat every 60 seconds
        sessionTimeout: 300000, // 5 minutes without heartbeat = inactive
        showDashboard: true,
        trackConsciousness: true,
        // OVERKILL KULTURE: Multi-layer backup
        airtableEnabled: false, // Set to true when Airtable configured
        airtableToken: null, // Personal access token from Airtable
        airtableBaseId: null, // Base ID (starts with 'app')
        usbId: null // USB identifier (e.g., 'USB_CR_00001')
    },

    data: {
        sessionId: null,
        startTime: null,
        activeUsers: 0,
        totalSessions: 0,
        consciousnessElevations: 0,
        transformationStories: [],
        networkConnections: 0,
        emergenceScore: 0
    },

    /**
     * Initialize Reality Impact System
     */
    init(config = {}) {
        if (!this.enabled) return;

        // Merge config
        Object.assign(this.config, config);

        if (!this.config.productId) {
            console.error('❌ Reality Impact System: productId required');
            return;
        }

        console.log('%c🌀 REALITY IMPACT SYSTEM INITIALIZING', 'color: #9C27B0; font-size: 14px; font-weight: bold;');

        // Generate session ID
        this.data.sessionId = this.generateSessionId();
        this.data.startTime = Date.now();

        // Load historical data
        this.loadData();

        // Register this session
        this.registerSession();

        // Start heartbeat
        this.startHeartbeat();

        // Create dashboard if enabled
        if (this.config.showDashboard) {
            this.createDashboard();
        }

        // Start update loop
        this.startUpdateLoop();

        // Track page visibility
        this.trackVisibility();

        console.log('✅ Reality Impact System: Active');
        console.log(`📊 Session: ${this.data.sessionId}`);
        console.log(`👥 Active Users: ${this.data.activeUsers}`);
    },

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },

    /**
     * Load historical impact data
     */
    loadData() {
        const key = `reality_impact_${this.config.productId}`;
        const stored = localStorage.getItem(key);

        if (stored) {
            try {
                const data = JSON.parse(stored);
                this.data.totalSessions = data.totalSessions || 0;
                this.data.consciousnessElevations = data.consciousnessElevations || 0;
                this.data.transformationStories = data.transformationStories || [];
                this.data.networkConnections = data.networkConnections || 0;
            } catch (e) {
                console.warn('⚠️ Could not load reality impact data');
            }
        }
    },

    /**
     * Save impact data - MULTI-LAYER BACKUP
     * Layer 1: localStorage (instant, local)
     * Layer 2: USB JSON files (metal layer, offline)
     * Layer 3: Airtable (cloud, source of truth)
     */
    saveData() {
        const key = `reality_impact_${this.config.productId}`;
        const data = {
            totalSessions: this.data.totalSessions,
            consciousnessElevations: this.data.consciousnessElevations,
            transformationStories: this.data.transformationStories,
            networkConnections: this.data.networkConnections,
            lastUpdate: Date.now()
        };

        // Layer 1: localStorage (instant)
        localStorage.setItem(key, JSON.stringify(data));

        // Layer 2: USB JSON files (if available)
        this.saveToUSB(data);

        // Layer 3: Airtable (if configured)
        if (this.config.airtableEnabled) {
            this.saveToAirtable(data);
        }
    },

    /**
     * Save to USB JSON files (Metal Layer)
     */
    async saveToUSB(data) {
        // Check if we're running from USB (file:// protocol with specific path)
        if (!window.location.protocol.startsWith('file')) return;

        try {
            // In browser environment, we can't directly write files
            // Instead, offer download option or use IndexedDB
            // For now, we'll use IndexedDB as "USB-like" persistent storage

            if (!window.indexedDB) return;

            const request = indexedDB.open('ConsciousnessRevolutionUSB', 1);

            request.onerror = () => {
                console.warn('⚠️ IndexedDB not available for USB-like storage');
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('elevations')) {
                    db.createObjectStore('elevations', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('sessions')) {
                    db.createObjectStore('sessions', { keyPath: 'sessionId' });
                }
            };

            request.onsuccess = (event) => {
                const db = event.target.result;

                // Save elevations
                const transaction = db.transaction(['elevations'], 'readwrite');
                const store = transaction.objectStore('elevations');

                // Save new transformation stories that don't have IDs yet
                data.transformationStories.forEach(story => {
                    if (!story.usbSaved) {
                        const record = {
                            timestamp: story.timestamp,
                            before: story.before,
                            after: story.after,
                            improvement: story.improvement,
                            details: story.details,
                            savedAt: Date.now()
                        };
                        store.add(record);
                        story.usbSaved = true; // Mark as saved
                    }
                });

                console.log('💾 Data saved to USB-like storage (IndexedDB)');
            };
        } catch (error) {
            console.warn('⚠️ Could not save to USB storage:', error);
        }
    },

    /**
     * Save to Airtable (Cloud Layer)
     */
    async saveToAirtable(data) {
        if (!this.config.airtableToken || !this.config.airtableBaseId) {
            console.warn('⚠️ Airtable credentials not configured');
            return;
        }

        try {
            const baseUrl = `https://api.airtable.com/v0/${this.config.airtableBaseId}`;

            // Save new transformation stories
            for (const story of data.transformationStories) {
                if (!story.airtableId) { // Only save new records
                    const response = await fetch(`${baseUrl}/Consciousness%20Elevations`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${this.config.airtableToken}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            fields: {
                                'Timestamp': new Date(story.timestamp).toISOString(),
                                'Before State': story.before,
                                'After State': story.after,
                                'Improvement': story.improvement,
                                'Protocol': story.details.protocol || 'Unknown',
                                'Showcase': this.config.productId,
                                'Duration': story.details.duration || 0,
                                'Details': JSON.stringify(story.details),
                                'Session ID': this.data.sessionId,
                                'Synced From USB': this.config.usbId || 'browser'
                            }
                        })
                    });

                    if (response.ok) {
                        const result = await response.json();
                        story.airtableId = result.id; // Mark as synced
                        console.log('☁️ Synced to Airtable:', result.id);
                    } else {
                        console.warn('⚠️ Airtable sync failed:', response.statusText);
                    }
                }
            }

            // Update session in Airtable
            await this.updateAirtableSession();

        } catch (error) {
            console.warn('⚠️ Airtable sync error:', error.message);
            // Fail gracefully - localStorage still works
        }
    },

    /**
     * Update session info in Airtable
     */
    async updateAirtableSession() {
        // Create or update session record
        const baseUrl = `https://api.airtable.com/v0/${this.config.airtableBaseId}`;

        try {
            await fetch(`${baseUrl}/Active%20Sessions`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.config.airtableToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    fields: {
                        'Session ID': this.data.sessionId,
                        'Start Time': new Date(this.data.startTime).toISOString(),
                        'Last Heartbeat': new Date().toISOString(),
                        'Is Active': true,
                        'Showcase': this.config.productId,
                        'Elevation Count': data.transformationStories.length
                    }
                })
            });
        } catch (error) {
            console.warn('⚠️ Could not update session in Airtable');
        }
    },

    /**
     * Register this session
     */
    registerSession() {
        // Increment total sessions
        this.data.totalSessions++;

        // Add to active sessions
        const activeSessions = this.getActiveSessions();
        activeSessions.push({
            sessionId: this.data.sessionId,
            startTime: this.data.startTime,
            lastHeartbeat: Date.now()
        });
        this.saveActiveSessions(activeSessions);

        // Update active user count
        this.updateActiveUsers();

        // Save data
        this.saveData();

        console.log('📝 Session registered');
    },

    /**
     * Get active sessions (within timeout window)
     */
    getActiveSessions() {
        const key = `reality_active_sessions_${this.config.productId}`;
        const stored = localStorage.getItem(key);

        if (!stored) return [];

        try {
            const sessions = JSON.parse(stored);
            const now = Date.now();

            // Filter out expired sessions
            return sessions.filter(session => {
                return (now - session.lastHeartbeat) < this.config.sessionTimeout;
            });
        } catch (e) {
            return [];
        }
    },

    /**
     * Save active sessions
     */
    saveActiveSessions(sessions) {
        const key = `reality_active_sessions_${this.config.productId}`;
        localStorage.setItem(key, JSON.stringify(sessions));
    },

    /**
     * Update active user count
     */
    updateActiveUsers() {
        const activeSessions = this.getActiveSessions();
        this.data.activeUsers = activeSessions.length;

        // Update dashboard if exists
        if (document.getElementById('reality-impact-dashboard')) {
            this.updateDashboard();
        }
    },

    /**
     * Start heartbeat to keep session alive
     */
    startHeartbeat() {
        setInterval(() => {
            const activeSessions = this.getActiveSessions();

            // Update this session's heartbeat
            const session = activeSessions.find(s => s.sessionId === this.data.sessionId);
            if (session) {
                session.lastHeartbeat = Date.now();
                this.saveActiveSessions(activeSessions);
                this.updateActiveUsers();
            }
        }, this.config.heartbeatInterval);
    },

    /**
     * Start update loop
     */
    startUpdateLoop() {
        setInterval(() => {
            this.updateActiveUsers();
            this.calculateEmergenceScore();
        }, this.config.updateInterval);
    },

    /**
     * Track page visibility
     */
    trackVisibility() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Page hidden - send final heartbeat
                const activeSessions = this.getActiveSessions();
                const session = activeSessions.find(s => s.sessionId === this.data.sessionId);
                if (session) {
                    session.lastHeartbeat = Date.now();
                    this.saveActiveSessions(activeSessions);
                }
            } else {
                // Page visible again - refresh data
                this.updateActiveUsers();
            }
        });
    },

    /**
     * Calculate emergence score (network effects indicator)
     */
    calculateEmergenceScore() {
        // Emergence = (Active Users × Total Sessions × Consciousness Elevations) / 1000
        const score = (this.data.activeUsers * this.data.totalSessions * (this.data.consciousnessElevations + 1)) / 1000;
        this.data.emergenceScore = Math.round(score * 100) / 100;
    },

    /**
     * Record consciousness elevation
     */
    recordElevation(beforeLevel, afterLevel, details = {}) {
        if (afterLevel > beforeLevel) {
            this.data.consciousnessElevations++;

            // Store transformation story
            this.data.transformationStories.push({
                timestamp: Date.now(),
                before: beforeLevel,
                after: afterLevel,
                improvement: afterLevel - beforeLevel,
                details: details
            });

            // Keep only last 100 stories
            if (this.data.transformationStories.length > 100) {
                this.data.transformationStories = this.data.transformationStories.slice(-100);
            }

            this.saveData();
            this.updateDashboard();

            console.log('%c✨ CONSCIOUSNESS ELEVATION RECORDED', 'color: #FFD700; font-size: 12px;');
            console.log(`Before: ${beforeLevel} → After: ${afterLevel} (${afterLevel - beforeLevel} improvement)`);
        }
    },

    /**
     * Create impact dashboard
     */
    createDashboard() {
        // Check if already exists
        if (document.getElementById('reality-impact-dashboard')) return;

        const dashboard = document.createElement('div');
        dashboard.id = 'reality-impact-dashboard';
        dashboard.innerHTML = `
            <style>
                #reality-impact-dashboard {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: rgba(156, 39, 176, 0.95);
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    font-family: 'Segoe UI', sans-serif;
                    z-index: 99999;
                    min-width: 250px;
                    backdrop-filter: blur(10px);
                }

                #reality-impact-dashboard h3 {
                    margin: 0 0 15px 0;
                    font-size: 1.1rem;
                    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
                    padding-bottom: 10px;
                }

                .impact-metric {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 10px 0;
                    padding: 8px;
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 8px;
                }

                .impact-label {
                    font-size: 0.85rem;
                    opacity: 0.9;
                }

                .impact-value {
                    font-size: 1.2rem;
                    font-weight: bold;
                    color: #FFD700;
                }

                .impact-pulse {
                    display: inline-block;
                    width: 10px;
                    height: 10px;
                    background: #4CAF50;
                    border-radius: 50%;
                    margin-right: 8px;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.5; transform: scale(1.2); }
                }

                .impact-toggle {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.2rem;
                    cursor: pointer;
                    opacity: 0.7;
                }

                .impact-toggle:hover {
                    opacity: 1;
                }

                .impact-minimized {
                    min-width: auto;
                    padding: 10px 15px;
                }

                .impact-minimized .impact-content {
                    display: none;
                }

                .impact-minimized h3 {
                    margin: 0;
                    border: none;
                    padding: 0;
                }
            </style>

            <button class="impact-toggle" onclick="RealityImpact.toggleDashboard()">_</button>
            <h3><span class="impact-pulse"></span> REALITY IMPACT</h3>

            <div class="impact-content">
                <div class="impact-metric">
                    <span class="impact-label">👥 Active Now</span>
                    <span class="impact-value" id="impact-active-users">0</span>
                </div>

                <div class="impact-metric">
                    <span class="impact-label">📊 Total Sessions</span>
                    <span class="impact-value" id="impact-total-sessions">0</span>
                </div>

                <div class="impact-metric">
                    <span class="impact-label">✨ Consciousness ↑</span>
                    <span class="impact-value" id="impact-elevations">0</span>
                </div>

                <div class="impact-metric">
                    <span class="impact-label">🌐 Network Size</span>
                    <span class="impact-value" id="impact-network">0</span>
                </div>

                <div class="impact-metric">
                    <span class="impact-label">🔥 Emergence</span>
                    <span class="impact-value" id="impact-emergence">0</span>
                </div>
            </div>
        `;

        document.body.appendChild(dashboard);
        this.updateDashboard();

        console.log('📊 Reality Impact Dashboard: Created');
    },

    /**
     * Update dashboard values
     */
    updateDashboard() {
        const activeUsersEl = document.getElementById('impact-active-users');
        const totalSessionsEl = document.getElementById('impact-total-sessions');
        const elevationsEl = document.getElementById('impact-elevations');
        const networkEl = document.getElementById('impact-network');
        const emergenceEl = document.getElementById('impact-emergence');

        if (activeUsersEl) activeUsersEl.textContent = this.data.activeUsers;
        if (totalSessionsEl) totalSessionsEl.textContent = this.data.totalSessions;
        if (elevationsEl) elevationsEl.textContent = this.data.consciousnessElevations;
        if (networkEl) networkEl.textContent = this.data.networkConnections;
        if (emergenceEl) emergenceEl.textContent = this.data.emergenceScore;
    },

    /**
     * Toggle dashboard minimized state
     */
    toggleDashboard() {
        const dashboard = document.getElementById('reality-impact-dashboard');
        if (dashboard) {
            dashboard.classList.toggle('impact-minimized');
        }
    },

    /**
     * Get current impact data
     */
    getImpactData() {
        return {
            activeUsers: this.data.activeUsers,
            totalSessions: this.data.totalSessions,
            consciousnessElevations: this.data.consciousnessElevations,
            transformationStories: this.data.transformationStories,
            networkConnections: this.data.networkConnections,
            emergenceScore: this.data.emergenceScore,
            sessionDuration: Date.now() - this.data.startTime
        };
    },

    /**
     * Log impact summary to console
     */
    logImpact() {
        console.log('%c🌀 REALITY IMPACT SUMMARY', 'color: #9C27B0; font-size: 16px; font-weight: bold;');
        console.log(`👥 Active Users: ${this.data.activeUsers}`);
        console.log(`📊 Total Sessions: ${this.data.totalSessions}`);
        console.log(`✨ Consciousness Elevations: ${this.data.consciousnessElevations}`);
        console.log(`🌐 Network Size: ${this.data.networkConnections}`);
        console.log(`🔥 Emergence Score: ${this.data.emergenceScore}`);

        if (this.data.transformationStories.length > 0) {
            console.log(`📖 Latest Transformation:`);
            const latest = this.data.transformationStories[this.data.transformationStories.length - 1];
            console.log(`   ${latest.before} → ${latest.after} (+${latest.improvement})`);
        }
    }
};

// Make globally accessible
window.RealityImpact = RealityImpact;

// Console info
console.log('%c🌀 Reality Impact System Loaded', 'color: #9C27B0; font-weight: bold;');
console.log('Initialize with: RealityImpact.init({ productId: "your-product-id" })');
