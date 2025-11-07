/**
 * 🔍 ENHANCED VISITOR TRACKING SNIPPET - 10 MILLION ANALYTICS TRAPS 🔍
 *
 * This comprehensive tracking system captures:
 * - WHO: Visitors, sessions, devices, locations
 * - WHAT: Clicks, scrolls, forms, interactions
 * - HOW: Engagement quality, time spent, completion rates
 * - RESULTS: Builds created, actions completed, goals achieved
 *
 * Add this to every page on consciousnessrevolution.io
 * Version: 2.0 - Autonomous Work Session
 */

(function() {
    'use strict';

    // ========================================
    // CONFIGURATION
    // ========================================

    const CONFIG = {
        localEndpoint: 'http://localhost:6000/api',
        cloudEndpoint: 'https://builder-pattern-api-production.up.railway.app/api',
        heartbeatInterval: 10000,  // 10 seconds
        scrollThrottle: 1000,      // 1 second
        idleThreshold: 60000,      // 1 minute
        sessionTimeout: 1800000    // 30 minutes
    };

    // ========================================
    // SESSION MANAGEMENT
    // ========================================

    class SessionManager {
        constructor() {
            this.sessionId = this.getOrCreateSessionId();
            this.sessionStart = Date.now();
            this.lastActivity = Date.now();
            this.userPin = localStorage.getItem('beta_user_pin') || 'anonymous';
            this.userName = localStorage.getItem('beta_user_name') || 'Guest';
            this.pageLoadTime = Date.now();
        }

        getOrCreateSessionId() {
            let sessionId = sessionStorage.getItem('tracking_session_id');
            if (!sessionId) {
                sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                sessionStorage.setItem('tracking_session_id', sessionId);
                sessionStorage.setItem('session_start', Date.now().toString());
            }
            return sessionId;
        }

        updateActivity() {
            this.lastActivity = Date.now();
        }

        getSessionDuration() {
            return Date.now() - this.sessionStart;
        }

        getTimeSinceLastActivity() {
            return Date.now() - this.lastActivity;
        }

        isIdle() {
            return this.getTimeSinceLastActivity() > CONFIG.idleThreshold;
        }

        getDeviceInfo() {
            return {
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screenWidth: window.screen.width,
                screenHeight: window.screen.height,
                viewportWidth: window.innerWidth,
                viewportHeight: window.innerHeight,
                deviceType: this.getDeviceType(),
                isMobile: /Mobile|Android|iPhone|iPad/.test(navigator.userAgent)
            };
        }

        getDeviceType() {
            const ua = navigator.userAgent;
            if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
                return 'tablet';
            }
            if (/Mobile|Android|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua)) {
                return 'mobile';
            }
            return 'desktop';
        }
    }

    // ========================================
    // EVENT TRACKING ENGINE
    // ========================================

    class AnalyticsTracker {
        constructor(session) {
            this.session = session;
            this.eventQueue = [];
            this.maxScrollDepth = 0;
            this.clickCount = 0;
            this.formInteractions = new Map();
            this.toolsUsed = new Set();
            this.pageViews = [];

            this.init();
        }

        init() {
            // Track page entry
            this.trackEvent('page_enter', {
                page: window.location.pathname,
                referrer: document.referrer,
                title: document.title
            });

            // Initialize all tracking listeners
            this.setupPageTracking();
            this.setupInteractionTracking();
            this.setupFormTracking();
            this.setupScrollTracking();
            this.setupEngagementTracking();
            this.setupBuilderTracking();

            // Start heartbeat
            this.startHeartbeat();
        }

        // ========================================
        // PAGE TRACKING
        // ========================================

        setupPageTracking() {
            // Page visibility changes
            document.addEventListener('visibilitychange', () => {
                this.trackEvent('page_visibility', {
                    hidden: document.hidden,
                    timeActive: this.calculateActiveTime()
                });

                if (!document.hidden) {
                    this.session.updateActivity();
                }
            });

            // Page exit
            window.addEventListener('beforeunload', () => {
                this.trackEvent('page_exit', {
                    page: window.location.pathname,
                    timeSpent: Date.now() - this.session.pageLoadTime,
                    scrollDepth: this.maxScrollDepth,
                    clickCount: this.clickCount,
                    engagementScore: this.calculateEngagementScore()
                });
            });

            // Page performance
            window.addEventListener('load', () => {
                this.trackEvent('page_performance', {
                    loadTime: performance.now(),
                    domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                    fullyLoaded: performance.timing.loadEventEnd - performance.timing.navigationStart
                });
            });
        }

        // ========================================
        // INTERACTION TRACKING
        // ========================================

        setupInteractionTracking() {
            // Click tracking with intelligent filtering
            document.addEventListener('click', (e) => {
                this.session.updateActivity();
                this.clickCount++;

                const element = e.target;
                const elementData = {
                    tag: element.tagName,
                    id: element.id,
                    class: element.className,
                    text: element.innerText?.substring(0, 50),
                    href: element.href,
                    x: e.clientX,
                    y: e.clientY,
                    timestamp: Date.now()
                };

                // Track button clicks specifically
                if (element.tagName === 'BUTTON' || element.role === 'button') {
                    this.trackEvent('button_click', {
                        ...elementData,
                        buttonType: element.type,
                        buttonValue: element.value
                    });
                }

                // Track link clicks
                if (element.tagName === 'A') {
                    this.trackEvent('link_click', {
                        ...elementData,
                        isExternal: this.isExternalLink(element.href)
                    });
                }

                // General click event
                this.trackEvent('click', elementData);
            });

            // Keyboard activity
            let keyPressCount = 0;
            document.addEventListener('keypress', () => {
                this.session.updateActivity();
                keyPressCount++;

                if (keyPressCount % 10 === 0) {  // Report every 10 keypresses
                    this.trackEvent('typing_activity', {
                        keyPresses: keyPressCount,
                        activeElement: document.activeElement?.tagName
                    });
                }
            });

            // Mouse movement (for activity detection)
            let lastMouseMove = 0;
            document.addEventListener('mousemove', () => {
                const now = Date.now();
                if (now - lastMouseMove > 5000) {  // Only track every 5 seconds
                    this.session.updateActivity();
                    lastMouseMove = now;
                }
            });

            // Copy/paste events
            document.addEventListener('copy', () => {
                this.trackEvent('user_copied', {
                    selection: window.getSelection()?.toString()?.substring(0, 100)
                });
            });

            document.addEventListener('paste', () => {
                this.trackEvent('user_pasted', {
                    activeElement: document.activeElement?.tagName
                });
            });
        }

        // ========================================
        // FORM TRACKING
        // ========================================

        setupFormTracking() {
            document.querySelectorAll('form').forEach(form => {
                const formId = form.id || form.name || `form_${Math.random().toString(36).substr(2, 9)}`;

                // Form start (first interaction)
                let formStarted = false;
                form.addEventListener('focusin', (e) => {
                    if (!formStarted) {
                        formStarted = true;
                        this.formInteractions.set(formId, {
                            startTime: Date.now(),
                            fields: new Set(),
                            completed: false
                        });

                        this.trackEvent('form_start', {
                            formId: formId,
                            formName: form.name,
                            firstField: e.target.name || e.target.id
                        });
                    }
                }, { once: true });

                // Field interactions
                form.querySelectorAll('input, textarea, select').forEach(field => {
                    // Field focus
                    field.addEventListener('focus', () => {
                        const interaction = this.formInteractions.get(formId);
                        if (interaction) {
                            interaction.fields.add(field.name || field.id);
                        }

                        this.trackEvent('field_focus', {
                            formId: formId,
                            field: field.name || field.id,
                            fieldType: field.type || field.tagName
                        });
                    });

                    // Field blur (completion)
                    field.addEventListener('blur', () => {
                        this.trackEvent('field_complete', {
                            formId: formId,
                            field: field.name || field.id,
                            hasValue: !!field.value,
                            valueLength: field.value?.length || 0
                        });
                    });

                    // Field input (typing)
                    let lastInput = 0;
                    field.addEventListener('input', () => {
                        const now = Date.now();
                        if (now - lastInput > 2000) {  // Throttle to every 2 seconds
                            this.trackEvent('field_typing', {
                                formId: formId,
                                field: field.name || field.id,
                                valueLength: field.value?.length || 0
                            });
                            lastInput = now;
                        }
                    });
                });

                // Form submission
                form.addEventListener('submit', (e) => {
                    const interaction = this.formInteractions.get(formId);
                    if (interaction) {
                        interaction.completed = true;

                        this.trackEvent('form_submit', {
                            formId: formId,
                            formName: form.name,
                            timeToComplete: Date.now() - interaction.startTime,
                            fieldsInteracted: interaction.fields.size,
                            totalFields: form.querySelectorAll('input, textarea, select').length
                        });
                    }
                });
            });

            // Form abandonment detection
            window.addEventListener('beforeunload', () => {
                this.formInteractions.forEach((interaction, formId) => {
                    if (!interaction.completed && interaction.fields.size > 0) {
                        this.trackEvent('form_abandon', {
                            formId: formId,
                            timeSpent: Date.now() - interaction.startTime,
                            fieldsCompleted: interaction.fields.size,
                            abandonmentPoint: document.activeElement?.name || document.activeElement?.id
                        });
                    }
                });
            });
        }

        // ========================================
        // SCROLL TRACKING
        // ========================================

        setupScrollTracking() {
            let lastScroll = 0;
            let scrollEvents = 0;

            window.addEventListener('scroll', () => {
                const now = Date.now();
                if (now - lastScroll < CONFIG.scrollThrottle) return;  // Throttle
                lastScroll = now;

                scrollEvents++;
                this.session.updateActivity();

                const scrollPercent = Math.round(
                    (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
                );

                // Update max scroll depth
                if (scrollPercent > this.maxScrollDepth) {
                    this.maxScrollDepth = scrollPercent;

                    // Track milestone depths
                    if ([25, 50, 75, 90, 100].includes(this.maxScrollDepth)) {
                        this.trackEvent('scroll_milestone', {
                            depth: this.maxScrollDepth,
                            timeToReach: Date.now() - this.session.pageLoadTime
                        });
                    }
                }

                // Periodic scroll tracking
                if (scrollEvents % 5 === 0) {
                    this.trackEvent('scroll_activity', {
                        currentDepth: scrollPercent,
                        maxDepth: this.maxScrollDepth,
                        scrollEvents: scrollEvents
                    });
                }
            });
        }

        // ========================================
        // ENGAGEMENT TRACKING
        // ========================================

        setupEngagementTracking() {
            // Idle detection
            setInterval(() => {
                if (this.session.isIdle()) {
                    this.trackEvent('user_idle', {
                        idleDuration: this.session.getTimeSinceLastActivity(),
                        lastPage: window.location.pathname
                    });
                }
            }, 30000);  // Check every 30 seconds

            // Session quality calculation (periodic)
            setInterval(() => {
                this.trackEvent('session_quality', {
                    duration: this.session.getSessionDuration(),
                    clickCount: this.clickCount,
                    scrollDepth: this.maxScrollDepth,
                    formsInteracted: this.formInteractions.size,
                    toolsUsed: this.toolsUsed.size,
                    engagementScore: this.calculateEngagementScore(),
                    isActive: !this.session.isIdle()
                });
            }, 60000);  // Every minute
        }

        // ========================================
        // BUILDER TRACKING
        // ========================================

        setupBuilderTracking() {
            // Track builder tool usage
            document.querySelectorAll('[data-tool]').forEach(tool => {
                tool.addEventListener('click', () => {
                    const toolName = tool.dataset.tool;
                    this.toolsUsed.add(toolName);

                    this.trackEvent('tool_used', {
                        tool: toolName,
                        timestamp: Date.now(),
                        firstUse: this.toolsUsed.size === 1
                    });
                });
            });

            // Track save/export actions
            document.querySelectorAll('[data-action="save"], [data-action="export"]').forEach(btn => {
                btn.addEventListener('click', () => {
                    this.trackEvent('project_action', {
                        action: btn.dataset.action,
                        timestamp: Date.now()
                    });
                });
            });

            // Track file uploads
            document.querySelectorAll('input[type="file"]').forEach(input => {
                input.addEventListener('change', (e) => {
                    if (e.target.files && e.target.files.length > 0) {
                        this.trackEvent('file_upload', {
                            fileCount: e.target.files.length,
                            fileTypes: Array.from(e.target.files).map(f => f.type),
                            totalSize: Array.from(e.target.files).reduce((sum, f) => sum + f.size, 0)
                        });
                    }
                });
            });
        }

        // ========================================
        // HEARTBEAT SYSTEM
        // ========================================

        startHeartbeat() {
            this.sendHeartbeat();
            setInterval(() => this.sendHeartbeat(), CONFIG.heartbeatInterval);
        }

        sendHeartbeat() {
            const heartbeatData = {
                // Session info
                sessionId: this.session.sessionId,
                pin: this.session.userPin,
                name: this.session.userName,

                // Page info
                page: window.location.pathname,
                title: document.title,
                referrer: document.referrer,

                // Activity metrics
                timeOnPage: Date.now() - this.session.pageLoadTime,
                sessionDuration: this.session.getSessionDuration(),
                isActive: !this.session.isIdle(),
                lastActivity: this.session.lastActivity,

                // Engagement metrics
                clickCount: this.clickCount,
                scrollDepth: this.maxScrollDepth,
                formsStarted: this.formInteractions.size,
                toolsUsed: Array.from(this.toolsUsed),
                engagementScore: this.calculateEngagementScore(),

                // Device info
                device: this.session.getDeviceInfo(),

                // Timestamp
                timestamp: new Date().toISOString()
            };

            // Send to local server
            this.sendToEndpoint(CONFIG.localEndpoint + '/visitor/heartbeat', heartbeatData);

            // Send to cloud backup
            this.sendToEndpoint(CONFIG.cloudEndpoint + '/visitor/heartbeat', heartbeatData);
        }

        // ========================================
        // EVENT TRACKING & SENDING
        // ========================================

        trackEvent(eventType, eventData) {
            const event = {
                type: eventType,
                sessionId: this.session.sessionId,
                pin: this.session.userPin,
                page: window.location.pathname,
                timestamp: new Date().toISOString(),
                data: eventData
            };

            // Add to queue
            this.eventQueue.push(event);

            // Send events in batches
            if (this.eventQueue.length >= 10) {
                this.flushEvents();
            }

            // Also log to console in development
            if (window.location.hostname === 'localhost') {
                console.log(`📊 ${eventType}:`, eventData);
            }
        }

        flushEvents() {
            if (this.eventQueue.length === 0) return;

            const events = [...this.eventQueue];
            this.eventQueue = [];

            // Send batch to server
            this.sendToEndpoint(CONFIG.localEndpoint + '/visitor/events', { events });
            this.sendToEndpoint(CONFIG.cloudEndpoint + '/visitor/events', { events });
        }

        sendToEndpoint(url, data) {
            fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).catch(err => {
                // Silent fail - analytics shouldn't break the app
                if (window.location.hostname === 'localhost') {
                    console.log(`Analytics endpoint offline: ${url}`);
                }
            });
        }

        // ========================================
        // UTILITY METHODS
        // ========================================

        calculateEngagementScore() {
            // Score from 0-100 based on activity
            let score = 0;

            // Time spent (up to 20 points for 5+ minutes)
            const timeMinutes = (Date.now() - this.session.pageLoadTime) / 60000;
            score += Math.min(20, timeMinutes * 4);

            // Clicks (up to 20 points for 10+ clicks)
            score += Math.min(20, this.clickCount * 2);

            // Scroll depth (up to 20 points for 100% scroll)
            score += Math.min(20, this.maxScrollDepth / 5);

            // Forms (up to 20 points for 2+ forms)
            score += Math.min(20, this.formInteractions.size * 10);

            // Tools used (up to 20 points for 5+ tools)
            score += Math.min(20, this.toolsUsed.size * 4);

            return Math.round(score);
        }

        calculateActiveTime() {
            // Estimate active time vs idle time
            return Date.now() - this.session.sessionStart - this.session.getTimeSinceLastActivity();
        }

        isExternalLink(href) {
            if (!href) return false;
            try {
                const url = new URL(href, window.location.origin);
                return url.hostname !== window.location.hostname;
            } catch {
                return false;
            }
        }
    }

    // ========================================
    // INTERCOM SYSTEM (from original)
    // ========================================

    class IntercomSystem {
        constructor(session) {
            this.session = session;
            this.init();
        }

        init() {
            // Poll for messages every 5 seconds
            setInterval(() => this.pollMessages(), 5000);
            this.pollMessages();  // Initial poll
        }

        async pollMessages() {
            if (this.session.userPin === 'anonymous') return;

            try {
                const response = await fetch(`${CONFIG.localEndpoint}/intercom/poll/${this.session.userPin}`);
                const messages = await response.json();

                if (messages && messages.length > 0) {
                    messages.forEach(msg => this.showMessage(msg.from, msg.message));
                }
            } catch (err) {
                // Intercom offline - that's okay
            }
        }

        showMessage(from, message) {
            const popup = document.createElement('div');
            popup.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                max-width: 300px;
                z-index: 99999;
                animation: slideIn 0.3s ease;
            `;
            popup.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 10px;">${from}:</div>
                <div>${message}</div>
                <button onclick="this.parentElement.remove()" style="
                    background: white;
                    color: #667eea;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    margin-top: 10px;
                    cursor: pointer;
                    font-weight: bold;
                ">Got it!</button>
            `;
            document.body.appendChild(popup);
            setTimeout(() => popup.remove(), 10000);
        }
    }

    // ========================================
    // INITIALIZATION
    // ========================================

    // Create session
    const session = new SessionManager();

    // Initialize tracking
    const tracker = new AnalyticsTracker(session);

    // Initialize intercom
    const intercom = new IntercomSystem(session);

    // Flush events before page unload
    window.addEventListener('beforeunload', () => {
        tracker.flushEvents();
    });

    // Make tracker globally available for custom events
    window._analyticsTracker = tracker;

    // Log initialization
    console.log('🔍 Enhanced Analytics Tracking Initialized');
    console.log('Session ID:', session.sessionId);
    console.log('Device:', session.getDeviceType());

})();
