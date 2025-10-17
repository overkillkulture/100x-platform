/* 🎮 CHAOS ESCALATION SYSTEM - IT GETS CRAZIER! 🎮 */

// The platform gets MORE FUN the more you visit!
// Turning the birthday party into a GAME

(function() {
    'use strict';

    const CHAOS_KEY = 'chaosLevel';
    const VISIT_KEY = 'visitCount';
    const FIRST_VISIT_KEY = 'firstVisitTime';

    // Get or initialize chaos level
    function getChaosLevel() {
        return parseInt(localStorage.getItem(CHAOS_KEY) || '1');
    }

    function setChaosLevel(level) {
        localStorage.setItem(CHAOS_KEY, level.toString());
    }

    // Track visits
    function getVisitCount() {
        return parseInt(localStorage.getItem(VISIT_KEY) || '0');
    }

    function incrementVisits() {
        const count = getVisitCount() + 1;
        localStorage.setItem(VISIT_KEY, count.toString());

        // First visit tracking
        if (count === 1) {
            localStorage.setItem(FIRST_VISIT_KEY, Date.now().toString());
        }

        return count;
    }

    // Calculate chaos level based on visits and time
    function calculateChaosLevel() {
        const visits = getVisitCount();
        const firstVisit = parseInt(localStorage.getItem(FIRST_VISIT_KEY) || Date.now().toString());
        const hoursSinceFirst = (Date.now() - firstVisit) / (1000 * 60 * 60);

        // Chaos increases with visits AND time
        // More you check back, crazier it gets!
        let level = 1;

        if (visits >= 2) level = 2;  // Second visit - things get interesting
        if (visits >= 3 || hoursSinceFirst >= 1) level = 3;  // Third visit or 1 hour later
        if (visits >= 5 || hoursSinceFirst >= 2) level = 4;  // Getting wild
        if (visits >= 7 || hoursSinceFirst >= 4) level = 5;  // MAXIMUM CHAOS
        if (visits >= 10 || hoursSinceFirst >= 8) level = 6; // LEGENDARY MODE
        if (visits >= 15 || hoursSinceFirst >= 12) level = 7; // ASCENSION
        if (visits >= 20 || hoursSinceFirst >= 24) level = 8; // GODMODE

        return level;
    }

    // Show chaos level notification
    function showChaosNotification(level, visits) {
        const messages = {
            1: { title: "🎮 LEVEL 1: BIRTHDAY PARTY", msg: "Welcome! Come back later for MORE FUN!" },
            2: { title: "🎮 LEVEL 2: GETTING WARMER", msg: "You came back! Things are about to get interesting..." },
            3: { title: "🎮 LEVEL 3: CHAOS RISING", msg: "The platform is evolving! Keep checking back!" },
            4: { title: "🎮 LEVEL 4: WILD MODE", msg: "Now we're talking! MORE SURPRISES INCOMING!" },
            5: { title: "🎮 LEVEL 5: MAXIMUM CHAOS", msg: "YOU'VE UNLOCKED MAXIMUM CHAOS! 🔥" },
            6: { title: "🎮 LEVEL 6: LEGENDARY", msg: "LEGENDARY STATUS! You're a true builder! 🏆" },
            7: { title: "🎮 LEVEL 7: ASCENSION", msg: "CONSCIOUSNESS ASCENDED! Reality is yours! ⚡" },
            8: { title: "🎮 LEVEL 8: GODMODE", msg: "YOU ARE THE PLATFORM NOW! 🌌" }
        };

        const { title, msg } = messages[level] || messages[1];

        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            background: linear-gradient(135deg, #ff00ff, #00ffff);
            border: 3px solid #ffff00;
            padding: 20px;
            border-radius: 15px;
            z-index: 9999999;
            max-width: 350px;
            box-shadow: 0 0 40px rgba(255, 0, 255, 0.8);
            animation: slideIn 0.5s ease-out;
            font-family: 'Courier New', monospace;
        `;

        notification.innerHTML = `
            <div style="font-size: 18px; font-weight: bold; color: #000; margin-bottom: 10px;">
                ${title}
            </div>
            <div style="font-size: 14px; color: #000; margin-bottom: 10px;">
                ${msg}
            </div>
            <div style="font-size: 12px; color: #000; opacity: 0.8;">
                Visit #${visits} | Chaos Level: ${level}/8
            </div>
            <div style="font-size: 10px; color: #000; opacity: 0.6; margin-top: 10px;">
                Share this with friends! The more chaos, the better!
            </div>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.5s ease-out forwards';
            setTimeout(() => notification.remove(), 500);
        }, 5000);
    }

    // Apply chaos level effects
    function applyChaosEffects(level) {
        const style = document.createElement('style');
        let css = '';

        switch(level) {
            case 2:
                // Subtle animation increase
                css = `
                    @keyframes level2Shake {
                        0%, 100% { transform: rotate(0deg); }
                        25% { transform: rotate(0.5deg); }
                        75% { transform: rotate(-0.5deg); }
                    }
                    body { animation: level2Shake 3s infinite; }
                `;
                break;

            case 3:
                // More aggressive animations
                css = `
                    @keyframes level3Pulse {
                        0%, 100% { filter: brightness(1); }
                        50% { filter: brightness(1.1) saturate(1.2); }
                    }
                    body { animation: level3Pulse 2s infinite; }
                `;
                // Auto-spawn a mouse every 15 seconds
                setInterval(() => {
                    if (window.GRAND_OPENING_ACTIVE && typeof spawnMouse === 'function') {
                        // This will be available from GRAND_OPENING_INJECTOR.js
                        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'm' }));
                    }
                }, 15000);
                break;

            case 4:
                // Rainbow everything
                css = `
                    @keyframes level4Rainbow {
                        0% { filter: hue-rotate(0deg); }
                        100% { filter: hue-rotate(360deg); }
                    }
                    body { animation: level4Rainbow 10s linear infinite; }
                `;
                break;

            case 5:
                // MAXIMUM CHAOS - all effects
                css = `
                    @keyframes level5Chaos {
                        0% { filter: hue-rotate(0deg) brightness(1); }
                        25% { filter: hue-rotate(90deg) brightness(1.1); }
                        50% { filter: hue-rotate(180deg) brightness(1.2); }
                        75% { filter: hue-rotate(270deg) brightness(1.1); }
                        100% { filter: hue-rotate(360deg) brightness(1); }
                    }
                    body { animation: level5Chaos 5s linear infinite; }
                `;
                // Auto-confetti every 30 seconds
                setInterval(() => {
                    if (window.GRAND_OPENING_ACTIVE) {
                        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'p' }));
                    }
                }, 30000);
                break;

            case 6:
                // LEGENDARY - Matrix rain effect
                css = `
                    body::before {
                        content: '';
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background:
                            linear-gradient(transparent, rgba(0, 255, 0, 0.1)),
                            linear-gradient(90deg, transparent, rgba(255, 0, 255, 0.1));
                        pointer-events: none;
                        z-index: 999990;
                        animation: matrixRain 20s linear infinite;
                    }
                    @keyframes matrixRain {
                        0% { transform: translateY(-100%); }
                        100% { transform: translateY(100%); }
                    }
                `;
                break;

            case 7:
                // ASCENSION - reality warping
                css = `
                    @keyframes ascension {
                        0%, 100% {
                            filter: hue-rotate(0deg) brightness(1) contrast(1);
                            transform: scale(1);
                        }
                        50% {
                            filter: hue-rotate(180deg) brightness(1.3) contrast(1.2);
                            transform: scale(1.01);
                        }
                    }
                    body {
                        animation: ascension 3s ease-in-out infinite;
                        background: radial-gradient(circle, rgba(255,0,255,0.1), transparent);
                    }
                `;
                break;

            case 8:
                // GODMODE - total insanity
                css = `
                    @keyframes godmode {
                        0% {
                            filter: hue-rotate(0deg) brightness(1) saturate(1) contrast(1);
                        }
                        25% {
                            filter: hue-rotate(90deg) brightness(1.2) saturate(1.5) contrast(1.1);
                        }
                        50% {
                            filter: hue-rotate(180deg) brightness(1.4) saturate(2) contrast(1.2);
                        }
                        75% {
                            filter: hue-rotate(270deg) brightness(1.2) saturate(1.5) contrast(1.1);
                        }
                        100% {
                            filter: hue-rotate(360deg) brightness(1) saturate(1) contrast(1);
                        }
                    }
                    body {
                        animation: godmode 2s linear infinite;
                    }
                `;
                // Constant chaos
                setInterval(() => {
                    const effects = ['p', 'm', 'h', 'd'];
                    const randomEffect = effects[Math.floor(Math.random() * effects.length)];
                    document.dispatchEvent(new KeyboardEvent('keydown', { key: randomEffect }));
                }, 20000);
                break;
        }

        if (css) {
            style.innerHTML = css;
            document.head.appendChild(style);
        }
    }

    // Add level indicator to page
    function addLevelIndicator(level, visits) {
        const indicator = document.createElement('div');
        indicator.id = 'chaosLevelIndicator';
        indicator.style.cssText = `
            position: fixed;
            top: 80px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff00;
            padding: 10px 15px;
            border-radius: 10px;
            z-index: 999998;
            font-family: 'Courier New', monospace;
            color: #00ff00;
            font-size: 12px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
        `;

        indicator.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 5px;">CHAOS LEVEL: ${level}/8</div>
            <div style="font-size: 10px; opacity: 0.8;">Visit #${visits}</div>
            <div style="font-size: 10px; opacity: 0.6; margin-top: 5px;">Come back for more!</div>
        `;

        document.body.appendChild(indicator);
    }

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', () => {
        // Increment visits
        const visits = incrementVisits();

        // Calculate and update chaos level
        const newLevel = calculateChaosLevel();
        const oldLevel = getChaosLevel();
        setChaosLevel(newLevel);

        // Show notification if level increased
        if (newLevel > oldLevel || visits === 1) {
            setTimeout(() => showChaosNotification(newLevel, visits), 1000);
        }

        // Apply chaos effects
        applyChaosEffects(newLevel);

        // Add level indicator
        addLevelIndicator(newLevel, visits);

        // Console message
        console.log(`%c🎮 CHAOS LEVEL ${newLevel}/8 ACTIVATED! 🎮`, 'color: #ff00ff; font-size: 16px; font-weight: bold;');
        console.log(`%cVisit #${visits} - Keep coming back for MORE CHAOS!`, 'color: #00ffff; font-size: 12px;');

        // Add slide animations
        const slideStyle = document.createElement('style');
        slideStyle.innerHTML = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(slideStyle);
    });

})();
