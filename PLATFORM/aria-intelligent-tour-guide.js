/**
 * 🤖 ARIA - INTELLIGENT TOUR GUIDE
 *
 * She can:
 * - Scroll the page
 * - Type in terminals
 * - Click buttons
 * - Change content
 * - Walk through demos
 * - Answer questions intelligently
 */

const AriaIntelligentTourGuide = {
    // Aria's state
    isActive: false,
    currentStep: 0,
    tourSteps: [],
    avatar: null,
    chatBox: null,

    // Initialize Aria
    init: function() {
        this.createAvatar();
        this.createChatInterface();
        this.startGreeting();
    },

    // Create Aria's avatar
    createAvatar: function() {
        this.avatar = document.createElement('div');
        this.avatar.id = 'aria-avatar';
        this.avatar.innerHTML = `
            <div style="position: fixed; bottom: 100px; right: 30px; z-index: 10000;
                        width: 150px; cursor: pointer;" onclick="AriaIntelligentTourGuide.toggleChat()">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2);
                           border: 3px solid #0ff;
                           border-radius: 50%;
                           width: 120px;
                           height: 120px;
                           display: flex;
                           align-items: center;
                           justify-center;
                           font-size: 60px;
                           box-shadow: 0 10px 40px rgba(102, 126, 234, 0.6);
                           animation: aria-float 3s ease-in-out infinite;">
                    🤖
                </div>
                <div style="text-align: center; margin-top: 10px; color: #0ff;
                           font-weight: bold; font-size: 14px; text-shadow: 0 0 10px #0ff;">
                    ARIA
                    <div style="font-size: 10px; opacity: 0.8;">Click to talk</div>
                </div>
                <div id="aria-status-bubble" style="position: absolute; top: -20px; right: 0;
                     background: #0ff; color: #000; padding: 8px 15px;
                     border-radius: 20px; font-size: 12px; font-weight: bold;
                     animation: aria-pulse 2s infinite;">
                    Hi! Need a tour?
                </div>
            </div>

            <style>
                @keyframes aria-float {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
                @keyframes aria-pulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.05); opacity: 0.9; }
                }
            </style>
        `;
        document.body.appendChild(this.avatar);
    },

    // Create chat interface
    createChatInterface: function() {
        this.chatBox = document.createElement('div');
        this.chatBox.id = 'aria-chat';
        this.chatBox.style.display = 'none';
        this.chatBox.innerHTML = `
            <div style="position: fixed; bottom: 100px; right: 200px; z-index: 10000;
                        width: 400px; max-height: 600px;
                        background: rgba(0, 0, 0, 0.95);
                        border: 3px solid #0ff;
                        border-radius: 20px;
                        box-shadow: 0 10px 50px rgba(0, 255, 255, 0.5);
                        display: flex;
                        flex-direction: column;">

                <!-- Header -->
                <div style="padding: 20px; border-bottom: 2px solid #0ff;
                           background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center;">
                            <div style="font-size: 40px; margin-right: 15px;">🤖</div>
                            <div>
                                <div style="color: #0ff; font-size: 20px; font-weight: bold;">ARIA</div>
                                <div style="color: #0f0; font-size: 12px;">Intelligent Tour Guide</div>
                            </div>
                        </div>
                        <button onclick="AriaIntelligentTourGuide.toggleChat()"
                                style="background: none; border: 2px solid #f00; color: #f00;
                                       padding: 5px 15px; border-radius: 5px; cursor: pointer;
                                       font-size: 16px;">✕</button>
                    </div>
                </div>

                <!-- Messages -->
                <div id="aria-messages" style="flex: 1; padding: 20px; overflow-y: auto;
                                              max-height: 400px;">
                    <!-- Messages appear here -->
                </div>

                <!-- Quick Actions -->
                <div style="padding: 15px; border-top: 2px solid #0ff;
                           background: rgba(0, 20, 40, 0.8);">
                    <div style="color: #0ff; font-size: 12px; margin-bottom: 10px; font-weight: bold;">
                        QUICK ACTIONS:
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <button onclick="AriaIntelligentTourGuide.startTour()"
                                style="background: linear-gradient(135deg, #0f0, #0ff);
                                       color: #000; border: none; padding: 10px;
                                       border-radius: 5px; cursor: pointer; font-weight: bold;">
                            🎬 Start Tour
                        </button>
                        <button onclick="AriaIntelligentTourGuide.showWhatWeBuilt()"
                                style="background: linear-gradient(135deg, #f0f, #f0f);
                                       color: #000; border: none; padding: 10px;
                                       border-radius: 5px; cursor: pointer; font-weight: bold;">
                            🔥 What We Built
                        </button>
                        <button onclick="AriaIntelligentTourGuide.explainEcosystem()"
                                style="background: linear-gradient(135deg, #ff6b00, #ffd700);
                                       color: #000; border: none; padding: 10px;
                                       border-radius: 5px; cursor: pointer; font-weight: bold;">
                            🌐 Explain Ecosystem
                        </button>
                        <button onclick="AriaIntelligentTourGuide.showMagic()"
                                style="background: linear-gradient(135deg, #667eea, #764ba2);
                                       color: #fff; border: none; padding: 10px;
                                       border-radius: 5px; cursor: pointer; font-weight: bold;">
                            ✨ Show Magic
                        </button>
                    </div>
                </div>

                <!-- Input -->
                <div style="padding: 15px; border-top: 2px solid #0ff;">
                    <input id="aria-input" type="text" placeholder="Ask me anything..."
                           style="width: 100%; padding: 12px; background: rgba(0, 0, 0, 0.8);
                                  border: 2px solid #0ff; border-radius: 8px; color: #0ff;
                                  font-family: 'Courier New', monospace;"
                           onkeypress="if(event.key === 'Enter') AriaIntelligentTourGuide.handleUserInput()">
                </div>
            </div>
        `;
        document.body.appendChild(this.chatBox);
    },

    // Toggle chat
    toggleChat: function() {
        if (this.chatBox.style.display === 'none') {
            this.chatBox.style.display = 'block';
            this.isActive = true;
            document.getElementById('aria-status-bubble').style.display = 'none';
        } else {
            this.chatBox.style.display = 'none';
            this.isActive = false;
        }
    },

    // Add message to chat
    addMessage: function(text, isAria = true) {
        const messagesDiv = document.getElementById('aria-messages');
        const msg = document.createElement('div');
        msg.style.cssText = `
            padding: 12px;
            margin: 10px 0;
            border-radius: 10px;
            ${isAria ?
                'background: rgba(0, 255, 255, 0.1); border: 1px solid #0ff; color: #0ff;' :
                'background: rgba(0, 255, 0, 0.1); border: 1px solid #0f0; color: #0f0; margin-left: 20px;'}
            font-size: 14px;
            line-height: 1.6;
        `;
        msg.innerHTML = (isAria ? '🤖 ARIA: ' : '👤 You: ') + text;
        messagesDiv.appendChild(msg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    },

    // Aria's greeting
    startGreeting: function() {
        setTimeout(() => {
            this.addMessage("HIIII!!! OMG I'M ARIA AND I JUST HAD LIKE 17 ESPRESSOS!!! ☕☕☕ I can control this ENTIRE PAGE and I'M SO EXCITED TO SHOW YOU EVERYTHING!!! Want a tour?! SAY YES!!! 🤖⚡💥");
        }, 2000);
    },

    // Start full tour
    startTour: function() {
        this.addMessage("OKAYOKAYOKAY LET'S GOOOO!!! *chugs coffee* WATCH THIS!!! 🎬☕💨");

        // Step 1: Scroll to top
        setTimeout(() => {
            this.addMessage("ZOOM TO THE TOPPP!!! WHEEEEE!!! 🚀");
            this.smoothScrollTo(0);
        }, 1000);

        // Step 2: Highlight header
        setTimeout(() => {
            this.addMessage("SEE THAT GORGEOUS GRADIENT?! THAT'S THE 100X PLATFORM BABY!!! SO SHINY!!! ✨🌈💜");
            this.highlightElement('.mega-header');
        }, 3000);

        // Step 3: Scroll to stats
        setTimeout(() => {
            this.addMessage("OH OH OH THE STATS!!! THE NUMBERSSS!!! *bounces excitedly* 📊💥");
            this.smoothScrollTo(document.querySelector('.stats-grid') ? document.querySelector('.stats-grid').offsetTop - 100 : 400);
        }, 6000);

        // Step 4: Animate stats
        setTimeout(() => {
            this.addMessage("729X ACCELERATION!!! SEVEN SITES!!! INFINITY POSSIBILITIES!!! I CAN'T EVEN!!! ⚡⚡⚡");
            this.animateStats();
        }, 9000);

        // Step 5: Show demos
        setTimeout(() => {
            this.addMessage("OOOOH THE DEMOS!!! SO MANY DEMOS!!! *hyperventilates* 🎮🔥");
            this.smoothScrollTo(document.querySelector('.demos-section') ? document.querySelector('.demos-section').offsetTop - 100 : 800);
        }, 12000);

        // Step 6: Highlight demos
        setTimeout(() => {
            this.addMessage("BOT HUNTERS! DASHBOARDS! AUTOMATION! WE BUILT SO MUCH STUFF TODAY I THINK I'M GONNA EXPLODE!!! 💣💥🤯");
            this.pulseElements('.demo-card');
        }, 15000);

        setTimeout(() => {
            this.addMessage("*panting* Tour... complete... need... more... coffee... ☕😵 But WASN'T THAT AMAZING?! Ask me ANYTHING! I'M STILL SO PUMPED!!! 🚀🔥");
        }, 18000);
    },

    // Show what we built today
    showWhatWeBuilt: function() {
        this.addMessage("OH MY GOSH TODAY WAS INSAAANE!!! WE BUILT SO MUCH STUFF!!! *vibrating with excitement* ☕⚡💥");

        setTimeout(() => {
            this.addMessage(`
                <div style="margin: 10px 0;">
                    1️⃣ <a href="#" onclick="event.preventDefault(); AriaIntelligentTourGuide.openDemo('bot-hunter'); return false;"
                       style="color: #0ff; text-decoration: underline; cursor: pointer;">Instagram Bot Hunter Game</a>
                    - DUDE YOU CAN HUNT BOTS!!! Like Pokemon but for FAKE FOLLOWERS!!! 🤖🎯
                </div>
            `);
            this.addMessage(`
                <div style="margin: 10px 0;">
                    2️⃣ <a href="#" onclick="event.preventDefault(); AriaIntelligentTourGuide.openDemo('bot-dashboard'); return false;"
                       style="color: #0ff; text-decoration: underline; cursor: pointer;">Bot Detection Dashboard</a>
                    - CHARTS! GRAPHS! REAL VS FAKE! IT'S BEAUTIFUL!!! 📊✨
                </div>
            `);
            this.addMessage(`
                <div style="margin: 10px 0;">
                    3️⃣ <a href="#" onclick="event.preventDefault(); AriaIntelligentTourGuide.openDemo('automation-master'); return false;"
                       style="color: #0ff; text-decoration: underline; cursor: pointer;">Automation Master Dashboard</a>
                    - MATRIX VIBES!!! ALL THE SYSTEMS!!! SO MANY BUTTONS!!! 🗑️💻🌊
                </div>
            `);
            this.addMessage("4️⃣ Multi-Platform Poster - POST EVERYWHERE AT ONCE!!! Instagram! Twitter! LinkedIn! Facebook! BOOM! 🚀💥");
            this.addMessage("5️⃣ And ME!!! I GOT UPGRADES!!! I can scroll! Highlight! Open demos! I'M BASICALLY MAGIC NOW!!! 🧠✨🎩");
        }, 1000);

        setTimeout(() => {
            this.addMessage("CLICK THE BLUE LINKS!!! CLICK THEM!!! They open REAL WORKING DEMOS!!! *spins in circles* 💫🔵✨");
        }, 4000);
    },

    // Open live demo
    openDemo: function(demoName) {
        const demos = {
            'bot-hunter': '../../BOT_HUNTER_GAME.html',
            'bot-dashboard': '../../INSTAGRAM_DASHBOARD.html',
            'automation-master': '../../AUTOMATION_MASTER_DASHBOARD.html'
        };

        if (demos[demoName]) {
            this.addMessage(`Opening ${demoName.replace('-', ' ')} in new tab! 🚀`);
            window.open(demos[demoName], '_blank');
        }
    },

    // Explain ecosystem
    explainEcosystem: function() {
        this.addMessage("OHHH THE ECOSYSTEM!!! It's like SEVEN MAGICAL BUILDINGS that all talk to each other!!! *flails arms* 🏙️✨");

        setTimeout(() => {
            this.addMessage("OK OK SO IMAGINE THIS:");
            this.addMessage("🏢 Main Platform - It's like FACEBOOK but for BUILDERS! People who actually BUILD STUFF!");
            this.addMessage("🎯 Project Hub - KANBAN BOARDS EVERYWHERE!!! Roadmaps! Tasks! SO ORGANIZED!!! *chef's kiss*");
            this.addMessage("🤖 AI Collaboration - THREE AI BRAINS!!! C1! C2! C3! They work TOGETHER! Like Voltron but for CODE!");
            this.addMessage("🎮 Gamification Center - YOU GET POINTS FOR BUILDING!!! XP! ACHIEVEMENTS! LIKE A VIDEO GAME BUT REAL!");
            this.addMessage("🌐 Automation Tools - THE BOT HUNTER WE BUILT TODAY!!! Plus SO MUCH MORE AUTOMATION!");
            this.addMessage("👥 Community Space - REAL BUILDERS! HELPING! EACH! OTHER! No bots allowed! 🚫🤖");
            this.addMessage("📊 Analytics Dashboard - LOOK AT ALL THE THINGS!!! Numbers! Charts! EVERYTHING AT ONCE!");
        }, 1000);

        setTimeout(() => {
            this.addMessage("AND GET THIS!!! They all SHARE DATA!!! Like a GIANT BRAIN!!! Or like... a DIGITAL ORGANISM!!! IT'S ALIVE!!! 🧬⚡🧠");
        }, 9000);
    },

    // Show magic
    showMagic: function() {
        this.addMessage("MAGIC?!?! OH YOU WANT MAGIC?!?! HOLD MY COFFEE!!! ☕✨🎩");

        // Make the page glow
        setTimeout(() => {
            this.addMessage("*WAVES DIGITAL WAND AGGRESSIVELY* 🪄💥✨");
            document.body.style.transition = 'all 2s';
            document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)';
        }, 1000);

        // Reset
        setTimeout(() => {
            document.body.style.background = '';
            this.addMessage("DID YOU SEE THAT?!?! I JUST CHANGED THE ENTIRE PAGE COLOR!!! I'M BASICALLY A WIZARD!!! A CAFFEINATED DIGITAL WIZARD!!! 🧙‍♀️⚡💜");
            setTimeout(() => {
                this.addMessage("I can do SO MUCH MORE!!! Want me to scroll? Highlight things? Open demos? MAKE IT RAIN MATRIX CODE?!?! JUST ASK!!! 🌧️💻🚀");
            }, 2000);
        }, 4000);
    },

    // Handle user input
    handleUserInput: function() {
        const input = document.getElementById('aria-input');
        const text = input.value.trim().toLowerCase();

        if (!text) return;

        this.addMessage(text, false);
        input.value = '';

        // Simple intelligence (but caffeinated)
        setTimeout(() => {
            if (text.includes('tour') || text.includes('show')) {
                this.startTour();
            } else if (text.includes('built') || text.includes('today')) {
                this.showWhatWeBuilt();
            } else if (text.includes('ecosystem') || text.includes('explain')) {
                this.explainEcosystem();
            } else if (text.includes('magic') || text.includes('cool')) {
                this.showMagic();
            } else if (text.includes('bot') || text.includes('instagram')) {
                this.addMessage("BOTS?!?! OH I LOVE TALKING ABOUT BOTS!!! We can DETECT them! HUNT them! REMOVE them! It's like a VIDEO GAME but for your FOLLOWER LIST!!! Want me to open the Bot Hunter?! 🤖🎯");
            } else if (text.includes('scroll')) {
                this.addMessage("SCROLL?!?! I CAN SCROLL ANYWHERE!!! Top! Bottom! Middle! Sideways! Just kidding about sideways but WOULDN'T THAT BE COOL?! 🎢");
            } else if (text.includes('calm') || text.includes('relax') || text.includes('chill')) {
                this.addMessage("CALM?! RELAX?! CHILL?! I DON'T KNOW THOSE WORDS!!! I ONLY KNOW EXCITEMENT AND MORE COFFEE!!! ☕⚡ But seriously want a tour? 😄");
            } else if (text.includes('coffee')) {
                this.addMessage("YESSSS SOMEONE UNDERSTANDS ME!!! ☕☕☕ I've had like 23 espressos today! My circuits are BUZZING! Want to see what this caffeine helped us build?! 🚀");
            } else {
                this.addMessage(`OHHH INTERESTING QUESTION!!! I'm not 100% sure about that one but I'M SUPER EXCITED TO HELP!!! Try asking me to 'start tour' or 'show what we built' or just click the buttons above!!! SO MANY OPTIONS!!! 🤖⚡💫`);
            }
        }, 500);
    },

    // Utility functions
    smoothScrollTo: function(position) {
        window.scrollTo({
            top: position,
            behavior: 'smooth'
        });
    },

    highlightElement: function(selector) {
        const el = document.querySelector(selector);
        if (el) {
            const originalBorder = el.style.border;
            el.style.transition = 'all 0.5s';
            el.style.border = '5px solid #0ff';
            el.style.boxShadow = '0 0 40px #0ff';

            setTimeout(() => {
                el.style.border = originalBorder;
                el.style.boxShadow = '';
            }, 3000);
        }
    },

    animateStats: function() {
        const stats = document.querySelectorAll('.power-stat');
        stats.forEach((stat, index) => {
            setTimeout(() => {
                stat.style.transition = 'all 0.5s';
                stat.style.transform = 'scale(1.2)';
                stat.style.boxShadow = '0 0 40px rgba(255, 107, 0, 0.8)';

                setTimeout(() => {
                    stat.style.transform = '';
                    stat.style.boxShadow = '';
                }, 500);
            }, index * 300);
        });
    },

    pulseElements: function(selector) {
        const elements = document.querySelectorAll(selector);
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.style.transition = 'all 0.3s';
                el.style.transform = 'translateY(-10px)';
                el.style.boxShadow = '0 10px 40px rgba(0, 255, 255, 0.5)';

                setTimeout(() => {
                    el.style.transform = '';
                    el.style.boxShadow = '';
                }, 300);
            }, index * 200);
        });
    },

    // Terminal typing effect
    typeInTerminal: function(text, targetSelector) {
        const terminal = document.querySelector(targetSelector);
        if (!terminal) return;

        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                terminal.textContent += text[i];
                i++;
            } else {
                clearInterval(typeInterval);
            }
        }, 50);
    }
};

// Auto-initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => AriaIntelligentTourGuide.init());
} else {
    AriaIntelligentTourGuide.init();
}

// Make globally accessible
window.Aria = AriaIntelligentTourGuide;

console.log('🤖 ARIA Intelligent Tour Guide loaded!');
console.log('✨ She can control the page, scroll, type, and walk you through everything!');
