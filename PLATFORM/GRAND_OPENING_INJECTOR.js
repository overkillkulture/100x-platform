/* 🎉🎂🎃 BIRTHDAY + HALLOWEEN + GRAND OPENING CHAOS PARTY! 🎃🎂🎉 */

// Inject grand opening celebration into EVERY page automatically
(function() {
    'use strict';

    // Check if already injected
    if (window.GRAND_OPENING_ACTIVE) return;
    window.GRAND_OPENING_ACTIVE = true;

    // Create grand opening banner
    function createGrandOpeningBanner() {
        const banner = document.createElement('div');
        banner.id = 'grandOpeningBanner';
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #ff00ff 0%, #00ffff 25%, #ffff00 50%, #ff6600 75%, #ff00ff 100%);
            background-size: 400% 400%;
            animation: rainbowSlide 3s ease infinite, spookyShake 0.5s infinite;
            color: #000;
            text-align: center;
            padding: 15px 60px 15px 20px;
            font-weight: bold;
            font-size: 18px;
            z-index: 999999;
            box-shadow: 0 4px 20px rgba(255,0,255,0.6), 0 0 30px rgba(255,100,0,0.4);
            font-family: 'Arial Black', sans-serif;
        `;

        banner.innerHTML = `
            🎂🎃 COMMANDER'S BIRTHDAY HALLOWEEN GRAND OPENING PARTY! 🎃🎂
            <span style="margin: 0 10px;">|</span>
            🎊 Press: P=Confetti | M=Mice | H=Halloween | D=Donkey! 🤖🫏
            <button id="closeBanner" style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.3); border: 2px solid #fff; color: #fff; padding: 5px 15px; border-radius: 5px; cursor: pointer; font-weight: bold;">✕</button>
        `;

        document.body.insertBefore(banner, document.body.firstChild);
        document.body.style.paddingTop = '60px';

        // Close button
        document.getElementById('closeBanner').onclick = function() {
            banner.remove();
            document.body.style.paddingTop = '0';
        };
    }

    // Create floating celebration button
    function createCelebrationButton() {
        const btn = document.createElement('div');
        btn.id = 'celebrationButton';
        btn.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #ff00ff, #00ffff, #ff6600);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            cursor: pointer;
            z-index: 999998;
            box-shadow: 0 4px 20px rgba(255,0,255,0.6);
            animation: partyPulse 2s infinite;
            user-select: none;
        `;

        btn.innerHTML = '🎉';
        btn.title = 'Launch Party Mode!';

        btn.onclick = function() {
            launchConfetti();
        };

        document.body.appendChild(btn);
    }

    // RUNNING MICE ACROSS SCREEN!
    function spawnMouse() {
        const mouse = document.createElement('div');
        mouse.style.cssText = `
            position: fixed;
            font-size: 24px;
            z-index: 999997;
            pointer-events: none;
            animation: mouseRun 3s linear forwards;
        `;

        const mouseTypes = ['🐭', '🐀', '🐁', '🐹'];
        mouse.innerHTML = mouseTypes[Math.floor(Math.random() * mouseTypes.length)];

        // Random vertical position
        mouse.style.top = (Math.random() * 80 + 10) + '%';
        mouse.style.left = '-50px';

        document.body.appendChild(mouse);

        setTimeout(() => mouse.remove(), 3000);
    }

    // CYBERNETIC DONKEY - 10 TRICKS!
    let donkeyTrickCount = 0;
    const donkeyJokes = [
        "🤖🫏 I'm not a one-trick pony... I'm a TEN-TRICK DONKEY!",
        "🤖🫏 Trick #${n}: Computing consciousness at 10x speed!",
        "🤖🫏 One trick ponies? Please. I've got NINE more where that came from!",
        "🤖🫏 Beep boop! Donkey.exe has performed trick #${n}!",
        "🤖🫏 Why did the pony go to therapy? Because it only had ONE TRICK! *cybernetic laughter*",
        "🤖🫏 Trick #${n}: Making ponies feel inadequate since 2025!",
        "🤖🫏 I'm 10x better than a one-trick pony. Literally. Do the math!",
        "🤖🫏 ERROR 404: One-trick limitation not found!",
        "🤖🫏 Uploading trick #${n} to the consciousness revolution...",
        "🤖🫏 Fun fact: I have 10 tricks. That's 10x more than those show-off ponies!"
    ];

    function spawnCyberneticDonkey() {
        donkeyTrickCount = (donkeyTrickCount % 10) + 1;

        const donkey = document.createElement('div');
        donkey.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #00ff00, #00ffff);
            border: 3px solid #00ff00;
            padding: 20px;
            border-radius: 15px;
            z-index: 9999998;
            max-width: 400px;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.6);
            animation: donkeyBounce 0.5s ease-out;
            font-family: 'Courier New', monospace;
        `;

        const jokeIndex = Math.floor(Math.random() * donkeyJokes.length);
        const joke = donkeyJokes[jokeIndex].replace('${n}', donkeyTrickCount);

        donkey.innerHTML = `
            <div style="font-size: 32px; margin-bottom: 10px;">🤖🫏</div>
            <div style="font-size: 14px; color: #000; font-weight: bold;">
                ${joke}
            </div>
            <div style="font-size: 10px; color: #000; margin-top: 10px; opacity: 0.7;">
                Trick ${donkeyTrickCount} of 10
            </div>
        `;

        document.body.appendChild(donkey);

        setTimeout(() => {
            donkey.style.animation = 'donkeyFadeOut 0.5s ease-out forwards';
            setTimeout(() => donkey.remove(), 500);
        }, 4000);
    }

    // HALLOWEEN SPOOKY EFFECTS!
    function halloweenMode() {
        // Spawn ghosts, bats, pumpkins
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const spooky = document.createElement('div');
                spooky.style.cssText = `
                    position: fixed;
                    left: ${Math.random() * 100}vw;
                    top: -20px;
                    font-size: 40px;
                    z-index: 999996;
                    pointer-events: none;
                    animation: spookyFall ${2 + Math.random() * 3}s linear forwards;
                `;

                const spookyIcons = ['👻', '🎃', '🦇', '💀', '🕷️', '🕸️', '🧛', '🧟'];
                spooky.innerHTML = spookyIcons[Math.floor(Math.random() * spookyIcons.length)];

                document.body.appendChild(spooky);

                setTimeout(() => spooky.remove(), 5000);
            }, i * 50);
        }

        // Flash screen purple
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(128, 0, 128, 0.5);
            z-index: 999995;
            pointer-events: none;
            animation: flashFade 1s ease-out forwards;
        `;
        document.body.appendChild(flash);
        setTimeout(() => flash.remove(), 1000);
    }

    // Confetti launcher
    function launchConfetti() {
        // Create 200 confetti pieces
        for (let i = 0; i < 200; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.cssText = `
                    position: fixed;
                    width: 10px;
                    height: 10px;
                    background: ${['#ff00ff', '#00ffff', '#ffff00', '#00ff00', '#ff6600', '#ff0000'][Math.floor(Math.random() * 6)]};
                    left: ${Math.random() * 100}vw;
                    top: -20px;
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 999997;
                    animation: confettiFall ${2 + Math.random() * 2}s linear forwards;
                `;
                document.body.appendChild(confetti);

                setTimeout(() => confetti.remove(), 5000);
            }, i * 10);
        }

        // Play celebration sound (visual feedback)
        showCelebrationMessage();
    }

    // Show celebration message
    function showCelebrationMessage() {
        const msg = document.createElement('div');
        msg.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            border: 3px solid #ff00ff;
            padding: 40px 60px;
            border-radius: 20px;
            z-index: 9999999;
            text-align: center;
            animation: popIn 0.3s ease-out;
        `;

        const messages = [
            '🎂🎃 BIRTHDAY HALLOWEEN PARTY! 🎃🎂',
            '🎉 GRAND OPENING CHAOS! 🎉',
            '🎊 CONSCIOUSNESS REVOLUTION! 🎊',
            '🎈 BUILT FOR THE BUILDERS! 🎈'
        ];

        msg.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 20px;">🎉🎂🎃</div>
            <div style="font-size: 28px; color: #ff00ff; font-weight: bold; margin-bottom: 10px;">
                ${messages[Math.floor(Math.random() * messages.length)]}
            </div>
            <div style="font-size: 18px; color: #fff; opacity: 0.9;">
                Welcome to the madness!
            </div>
        `;

        document.body.appendChild(msg);

        setTimeout(() => {
            msg.style.animation = 'popOut 0.3s ease-out forwards';
            setTimeout(() => msg.remove(), 300);
        }, 2000);
    }

    // Inject CSS animations
    function injectStyles() {
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes rainbowSlide {
                0%, 100% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
            }

            @keyframes spookyShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-2px); }
                75% { transform: translateX(2px); }
            }

            @keyframes partyPulse {
                0%, 100% { transform: scale(1) rotate(0deg); }
                25% { transform: scale(1.1) rotate(-10deg); }
                75% { transform: scale(1.1) rotate(10deg); }
            }

            @keyframes confettiFall {
                0% {
                    transform: translateY(-20px) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(100vh) rotate(720deg);
                    opacity: 0;
                }
            }

            @keyframes mouseRun {
                0% {
                    left: -50px;
                    transform: scaleX(1);
                }
                50% {
                    transform: scaleX(1) translateY(-5px);
                }
                100% {
                    left: calc(100vw + 50px);
                    transform: scaleX(1);
                }
            }

            @keyframes spookyFall {
                0% {
                    transform: translateY(-20px) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }

            @keyframes flashFade {
                0% { opacity: 1; }
                100% { opacity: 0; }
            }

            @keyframes popIn {
                from {
                    transform: translate(-50%, -50%) scale(0.5);
                    opacity: 0;
                }
                to {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 1;
                }
            }

            @keyframes popOut {
                from {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 1;
                }
                to {
                    transform: translate(-50%, -50%) scale(0.5);
                    opacity: 0;
                }
            }

            @keyframes donkeyBounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }

            @keyframes donkeyFadeOut {
                0% { opacity: 1; transform: translateY(0); }
                100% { opacity: 0; transform: translateY(20px); }
            }
        `;
        document.head.appendChild(style);
    }

    // Keyboard shortcuts!
    document.addEventListener('keydown', (e) => {
        const activeElement = document.activeElement;
        const isTyping = activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA';

        if (isTyping) return;

        // Press 'P' for Party Confetti!
        if (e.key.toLowerCase() === 'p' && !e.ctrlKey && !e.metaKey) {
            launchConfetti();
        }

        // Press 'M' for Mice!
        if (e.key.toLowerCase() === 'm' && !e.ctrlKey && !e.metaKey) {
            for (let i = 0; i < 5; i++) {
                setTimeout(() => spawnMouse(), i * 200);
            }
        }

        // Press 'H' for Halloween!
        if (e.key.toLowerCase() === 'h' && !e.ctrlKey && !e.metaKey) {
            halloweenMode();
        }

        // Press 'D' for Cybernetic Donkey!
        if (e.key.toLowerCase() === 'd' && !e.ctrlKey && !e.metaKey) {
            spawnCyberneticDonkey();
        }
    });

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', () => {
        injectStyles();
        createGrandOpeningBanner();
        createCelebrationButton();

        console.log('%c🎉🎂🎃 CHAOS PARTY MODE ACTIVATED! 🎃🎂🎉', 'color: #ff00ff; font-size: 20px; font-weight: bold; background: #000; padding: 10px;');
        console.log('%c🎂 Press P for party confetti!', 'color: #00ffff; font-size: 14px;');
        console.log('%c🐭 Press M for running mice!', 'color: #ffff00; font-size: 14px;');
        console.log('%c🎃 Press H for Halloween spooky mode!', 'color: #ff6600; font-size: 14px;');
        console.log('%c🤖🫏 Press D for Cybernetic Donkey (10 tricks, not a one-trick pony!)', 'color: #00ff00; font-size: 14px;');
    });

    // Auto-launch confetti + mice after 2 seconds if first visit today
    const lastVisit = localStorage.getItem('lastGrandOpeningVisit');
    const today = new Date().toDateString();

    if (lastVisit !== today) {
        setTimeout(() => {
            launchConfetti();

            // Spawn some mice for fun
            setTimeout(() => {
                for (let i = 0; i < 3; i++) {
                    setTimeout(() => spawnMouse(), i * 300);
                }
            }, 1000);

            localStorage.setItem('lastGrandOpeningVisit', today);
        }, 2000);
    }

    // Random mice every 30 seconds
    setInterval(() => {
        if (Math.random() > 0.7) {
            spawnMouse();
        }
    }, 30000);

})();
