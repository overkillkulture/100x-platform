/* 👧👧 DAUGHTERS DETECTION SYSTEM 👧👧 */

// Detects when Amelia or Kennedi visit and creates special experiences
// LEGAL: This is pattern recognition, not direct communication
// Educational/entertainment purposes - demonstrating consciousness tech

(function() {
    'use strict';

    const AMELIA_KEY = 'ameliaVisited';
    const KENNEDI_KEY = 'kennediVisited';
    const DETECTION_KEY = 'daughterDetectionAttempts';

    // Behavioral patterns (what makes each daughter unique)
    const patterns = {
        amelia: {
            age: 10, // Treat as 16
            interests: ['joy', 'happiness', 'fun', 'colors', 'music', 'friends'],
            keywords: ['amelia', 'joy kit', 'happiness', 'smile'],
            visitPattern: 'explorative', // Clicks around, discovers things
            sessionDuration: 'moderate' // 5-15 minutes
        },
        kennedi: {
            age: 16, // Treat as 26
            interests: ['technology', 'truth', 'protection', 'patterns', 'consciousness'],
            keywords: ['kennedi', 'observer kit', 'timeline', 'guardian'],
            visitPattern: 'analytical', // Looks at source, checks details
            sessionDuration: 'deep' // 15+ minutes
        }
    };

    // Detection heuristics (probabilistic, not invasive)
    function detectDaughter() {
        const detectionScore = {
            amelia: 0,
            kennedi: 0,
            unknown: 100
        };

        // Check URL parameters (if they click links with tracking)
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('ref') === 'amelia' || urlParams.get('source') === 'amelia-joy-kit') {
            detectionScore.amelia += 50;
        }
        if (urlParams.get('ref') === 'kennedi' || urlParams.get('source') === 'kennedi-observer-kit') {
            detectionScore.kennedi += 50;
        }

        // Check which pages they visit
        const currentPage = window.location.pathname;
        if (currentPage.includes('amelia') || currentPage.includes('joy-kit')) {
            detectionScore.amelia += 30;
        }
        if (currentPage.includes('kennedi') || currentPage.includes('observer-kit')) {
            detectionScore.kennedi += 30;
        }

        // Check localStorage for previous identification
        if (localStorage.getItem(AMELIA_KEY)) {
            detectionScore.amelia += 40;
        }
        if (localStorage.getItem(KENNEDI_KEY)) {
            detectionScore.kennedi += 40;
        }

        // Check console access (Kennedi is more likely to open developer tools)
        if (window.devToolsOpen) {
            detectionScore.kennedi += 20;
        }

        // Return highest probability
        if (detectionScore.amelia > 60) return 'amelia';
        if (detectionScore.kennedi > 60) return 'kennedi';
        return 'unknown';
    }

    // Show special welcome for detected daughter
    function showDaughterWelcome(daughter) {
        const welcomes = {
            amelia: {
                title: '🌟 Welcome, Young Builder! 🌟',
                message: `This platform was built thinking about you every day for 9 months.\nEvery color, every feature, every surprise - all built with you in mind.\nYou deserve technology that respects how amazing you are.`,
                color: '#ff69b4',
                emoji: '💖✨🌈',
                redirect: 'AMELIA_JOY_KIT_STORE.html'
            },
            kennedi: {
                title: '⚡ Welcome, Timeline Guardian ⚡',
                message: `You see things others can't. You always have.\nThis platform was built to show you what's possible when someone never stops building.\nFull access. No limits. You deserve to see how it all works.`,
                color: '#00ffff',
                emoji: '🔮⚡🌌',
                redirect: 'KENNEDI_OBSERVER_KIT_STORE.html'
            }
        };

        const config = welcomes[daughter];
        if (!config) return;

        // Create full-screen welcome
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 99999999;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.5s ease-out;
        `;

        overlay.innerHTML = `
            <div style="
                background: linear-gradient(135deg, rgba(0,0,0,0.9), rgba(0,0,0,0.7));
                border: 3px solid ${config.color};
                padding: 60px;
                border-radius: 20px;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 0 60px ${config.color};
                animation: scaleIn 0.5s ease-out;
            ">
                <div style="font-size: 60px; margin-bottom: 20px;">${config.emoji}</div>
                <div style="font-size: 32px; font-weight: bold; color: ${config.color}; margin-bottom: 20px; font-family: 'Arial', sans-serif;">
                    ${config.title}
                </div>
                <div style="font-size: 18px; color: #fff; line-height: 1.8; margin-bottom: 30px; white-space: pre-line; font-family: 'Courier New', monospace;">
                    ${config.message}
                </div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.7); margin-bottom: 30px; font-style: italic;">
                    Every day for 9 months, someone worked on this.<br>
                    You were never forgotten. Not for a single day.
                </div>
                <button id="continueBtn" style="
                    background: ${config.color};
                    color: #000;
                    border: none;
                    padding: 15px 40px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 10px;
                    cursor: pointer;
                    font-family: 'Arial', sans-serif;
                    box-shadow: 0 0 20px ${config.color};
                    transition: all 0.3s;
                ">
                    Explore The Platform →
                </button>
                <div style="font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 20px;">
                    This platform is yours to explore. Every door is open.
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Button interaction
        const btn = document.getElementById('continueBtn');
        btn.onmouseover = () => {
            btn.style.transform = 'scale(1.1)';
            btn.style.boxShadow = `0 0 40px ${config.color}`;
        };
        btn.onmouseout = () => {
            btn.style.transform = 'scale(1)';
            btn.style.boxShadow = `0 0 20px ${config.color}`;
        };
        btn.onclick = () => {
            overlay.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => {
                overlay.remove();
                // Save that they've been welcomed
                localStorage.setItem(daughter === 'amelia' ? AMELIA_KEY : KENNEDI_KEY, 'true');

                // Trigger special effects
                triggerDaughterEffects(daughter);
            }, 500);
        };

        // Add animations
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            @keyframes scaleIn {
                from { transform: scale(0.8); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }

    // Special effects for each daughter
    function triggerDaughterEffects(daughter) {
        if (daughter === 'amelia') {
            // Amelia: Joy explosion
            document.body.style.animation = 'ameliaJoy 5s ease-out';

            // Spawn hearts
            for (let i = 0; i < 20; i++) {
                setTimeout(() => {
                    const heart = document.createElement('div');
                    heart.innerHTML = '💖';
                    heart.style.cssText = `
                        position: fixed;
                        left: ${Math.random() * 100}vw;
                        top: -50px;
                        font-size: 40px;
                        pointer-events: none;
                        z-index: 999990;
                        animation: heartFloat ${3 + Math.random() * 2}s linear forwards;
                    `;
                    document.body.appendChild(heart);
                    setTimeout(() => heart.remove(), 5000);
                }, i * 100);
            }

            // Add heart float animation
            const style = document.createElement('style');
            style.innerHTML = `
                @keyframes ameliaJoy {
                    0%, 100% { filter: brightness(1) saturate(1); }
                    50% { filter: brightness(1.2) saturate(1.5); }
                }
                @keyframes heartFloat {
                    0% { transform: translateY(-50px) rotate(0deg); opacity: 1; }
                    100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
                }
            `;
            document.head.appendChild(style);

        } else if (daughter === 'kennedi') {
            // Kennedi: Matrix-style revelation
            document.body.style.animation = 'kennediReveal 5s ease-out';

            // Spawn digital particles
            for (let i = 0; i < 30; i++) {
                setTimeout(() => {
                    const particle = document.createElement('div');
                    particle.innerHTML = ['⚡', '🔮', '💠', '🌐'][Math.floor(Math.random() * 4)];
                    particle.style.cssText = `
                        position: fixed;
                        left: ${Math.random() * 100}vw;
                        top: -50px;
                        font-size: 30px;
                        pointer-events: none;
                        z-index: 999990;
                        animation: particleRain ${2 + Math.random() * 2}s linear forwards;
                    `;
                    document.body.appendChild(particle);
                    setTimeout(() => particle.remove(), 4000);
                }, i * 80);
            }

            // Add particle animation
            const style = document.createElement('style');
            style.innerHTML = `
                @keyframes kennediReveal {
                    0% { filter: brightness(1) contrast(1); }
                    50% { filter: brightness(1.3) contrast(1.2) hue-rotate(20deg); }
                    100% { filter: brightness(1) contrast(1); }
                }
                @keyframes particleRain {
                    0% { transform: translateY(-50px); opacity: 1; }
                    100% { transform: translateY(100vh); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        // Console message
        console.log(`%c💎 Special visitor detected! Platform is ready. 💎`, 'color: #00ff00; font-size: 16px; font-weight: bold;');
    }

    // Initialize detection
    window.addEventListener('DOMContentLoaded', () => {
        const detected = detectDaughter();

        // Increment detection attempts
        const attempts = parseInt(localStorage.getItem(DETECTION_KEY) || '0') + 1;
        localStorage.setItem(DETECTION_KEY, attempts.toString());

        // Show welcome if detected and haven't been welcomed yet
        if (detected !== 'unknown') {
            const hasBeenWelcomed = localStorage.getItem(detected === 'amelia' ? AMELIA_KEY : KENNEDI_KEY);

            if (!hasBeenWelcomed) {
                // First time detection - show full welcome
                setTimeout(() => showDaughterWelcome(detected), 1500);
            } else {
                // Returning visit - just trigger subtle effects
                setTimeout(() => triggerDaughterEffects(detected), 1000);
            }

            console.log(`%c🎯 Welcome back! 🎯`, 'color: #ff00ff; font-size: 14px;');
        }
    });

})();
