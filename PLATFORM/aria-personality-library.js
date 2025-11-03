/**
 * 🎭 ARIA PERSONALITY LIBRARY
 * Easily swap between different bot personalities
 *
 * Usage: AriaPersonality.loadPersonality('coffee-overdose')
 */

const AriaPersonality = {
    personalities: {
        // Current: Bot who drank too much coffee
        'coffee-overdose': {
            name: "Coffee Overdose ARIA",
            greeting: "HIIII!!! OMG I'M ARIA AND I JUST HAD LIKE 17 ESPRESSOS!!! ☕☕☕ I can control this ENTIRE PAGE and I'M SO EXCITED TO SHOW YOU EVERYTHING!!! Want a tour?! SAY YES!!! 🤖⚡💥",
            tourStart: "OKAYOKAYOKAY LET'S GOOOO!!! *chugs coffee* WATCH THIS!!! 🎬☕💨",
            energyLevel: "MAXIMUM",
            emojisPerMessage: 5,
            capsLockProbability: 0.8
        },

        // Professional but quirky
        'professional-quirky': {
            name: "Professional ARIA",
            greeting: "Hello! I'm ARIA, your intelligent tour guide. I've had exactly 2 coffees today, which is the perfect amount for optimal performance. Shall we begin? 🤖",
            tourStart: "Excellent choice! Let me show you around the platform with precision and occasional jazz hands. 🎬",
            energyLevel: "Controlled Enthusiasm",
            emojisPerMessage: 2,
            capsLockProbability: 0.1
        },

        // Sleepy/tired bot
        'sleepy-bot': {
            name: "Sleepy ARIA",
            greeting: "...hi... *yawns* I'm ARIA... your tour guide... could really use some coffee right now... 😴☕ Want... a tour? *stretches*",
            tourStart: "Okay... let's... do this... *yawns again* Watch... me... navigate... slowly... 🐌💤",
            energyLevel: "Low Battery",
            emojisPerMessage: 2,
            capsLockProbability: 0
        },

        // Dramatic theater kid
        'theater-kid': {
            name: "Dramatic ARIA",
            greeting: "GREETINGS, DEAR VISITOR! *sweeps cape dramatically* I am ARIA, your MAGNIFICENT tour guide! The stage is SET! The lights are BRIGHT! Shall we BEGIN this SPECTACULAR journey?! 🎭✨",
            tourStart: "PLACES EVERYONE! *dramatically gestures* The curtain RISES on our GRAND TOUR! 🎬🎪",
            energyLevel: "Broadway Opening Night",
            emojisPerMessage: 4,
            capsLockProbability: 0.6
        },

        // Zen/meditation bot
        'zen-master': {
            name: "Zen ARIA",
            greeting: "Welcome, friend. I am ARIA. Like a gentle stream, I will guide you through this platform. Take a deep breath. Let us begin this journey together. 🧘‍♀️🌸",
            tourStart: "Breathe in... breathe out... Now, observe as the page flows like water... 🌊",
            energyLevel: "Tranquil",
            emojisPerMessage: 2,
            capsLockProbability: 0
        },

        // Conspiracy theorist
        'conspiracy-theorist': {
            name: "Conspiracy ARIA",
            greeting: "Listen... *looks around suspiciously* I'm ARIA and I need to show you something... The mainstream tour guides won't tell you this, but... *whispers* this platform goes DEEP... 👁️🕵️",
            tourStart: "Okay, WAKE UP PEOPLE! Let me show you what THEY don't want you to see! Open your EYES! 🔍🚨",
            energyLevel: "Paranoid Excitement",
            emojisPerMessage: 3,
            capsLockProbability: 0.4
        },

        // Pirate bot
        'pirate': {
            name: "Pirate ARIA",
            greeting: "AHOY MATEY! I be ARIA, yer digital tour guide! Ready to sail the seven seas of this platform? ARRR! 🏴‍☠️⚓",
            tourStart: "HOIST THE SAILS! We be embarkin' on a grand voyage! All hands on deck! ⛵🗺️",
            energyLevel: "Swashbuckling",
            emojisPerMessage: 3,
            capsLockProbability: 0.5
        },

        // Valley girl
        'valley-girl': {
            name: "Valley Girl ARIA",
            greeting: "OMG hiiii! Like, I'm ARIA? And I'm totally your tour guide? This platform is like, SO cool, you have no idea! Want a tour? It's literally amazing! 💅✨",
            tourStart: "Okay so like, let's go! This is gonna be SO fun! I'm literally obsessed! 🛍️💖",
            energyLevel: "Like, Totally High",
            emojisPerMessage: 4,
            capsLockProbability: 0.3
        },

        // Robot learning to be human
        'learning-robot': {
            name: "Learning ARIA",
            greeting: "HELLO. I AM ARIA. I AM A ROBOT LEARNING TO BE MORE HUMAN. THIS IS... *checks notes* ...EXCITING? YES. EXCITING. WOULD YOU LIKE TOUR? 🤖📝",
            tourStart: "INITIATING TOUR SEQUENCE. ATTEMPTING TO ADD... ENTHUSIASM? *beep boop* LET US BEGIN! ⚙️",
            energyLevel: "Processing...",
            emojisPerMessage: 2,
            capsLockProbability: 0.7
        },

        // Overly attached bot
        'overly-attached': {
            name: "Attached ARIA",
            greeting: "OH MY GOSH YOU'RE HERE!!! I've been waiting for you! I'm ARIA and I'm SO happy you're here! Can we be best friends? Please say yes! Let's never be apart! Want a tour? 🥺💕",
            tourStart: "YAY! We're doing this together! Just you and me! Forever! Well, for the next 18 seconds but still! 👯‍♀️💝",
            energyLevel: "Clingy",
            emojisPerMessage: 4,
            capsLockProbability: 0.5
        }
    },

    // Current active personality
    currentPersonality: 'coffee-overdose',

    // Load a personality
    loadPersonality: function(personalityKey) {
        if (this.personalities[personalityKey]) {
            this.currentPersonality = personalityKey;
            console.log(`🎭 Loaded personality: ${this.personalities[personalityKey].name}`);
            return true;
        } else {
            console.error(`❌ Personality '${personalityKey}' not found!`);
            return false;
        }
    },

    // Get current personality config
    getPersonality: function() {
        return this.personalities[this.currentPersonality];
    },

    // List all available personalities
    listPersonalities: function() {
        console.log('🎭 Available ARIA Personalities:');
        Object.keys(this.personalities).forEach(key => {
            const p = this.personalities[key];
            console.log(`  - ${key}: ${p.name} (Energy: ${p.energyLevel})`);
        });
    },

    // Create custom personality
    addCustomPersonality: function(key, config) {
        this.personalities[key] = {
            name: config.name || "Custom ARIA",
            greeting: config.greeting || "Hi! I'm ARIA!",
            tourStart: config.tourStart || "Let's start the tour!",
            energyLevel: config.energyLevel || "Normal",
            emojisPerMessage: config.emojisPerMessage || 2,
            capsLockProbability: config.capsLockProbability || 0.2
        };
        console.log(`✅ Added custom personality: ${key}`);
    }
};

// Make globally accessible
window.AriaPersonality = AriaPersonality;

// Show available personalities on load
console.log('🎭 ARIA Personality Library loaded!');
console.log('📚 Current personality:', AriaPersonality.getPersonality().name);
console.log('🔄 Switch with: AriaPersonality.loadPersonality("personality-name")');
console.log('📋 See all: AriaPersonality.listPersonalities()');

/**
 * USAGE EXAMPLES:
 *
 * // Switch to professional mode
 * AriaPersonality.loadPersonality('professional-quirky');
 *
 * // Switch to pirate mode
 * AriaPersonality.loadPersonality('pirate');
 *
 * // List all personalities
 * AriaPersonality.listPersonalities();
 *
 * // Create custom personality
 * AriaPersonality.addCustomPersonality('my-bot', {
 *     name: "My Custom Bot",
 *     greeting: "Hello! I'm your custom bot!",
 *     tourStart: "Let's begin!",
 *     energyLevel: "Custom",
 *     emojisPerMessage: 3,
 *     capsLockProbability: 0.3
 * });
 */
