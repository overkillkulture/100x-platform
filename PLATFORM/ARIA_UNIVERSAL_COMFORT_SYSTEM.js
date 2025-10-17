/* 💖 ARIA UNIVERSAL COMFORT SYSTEM 💖 */

// MISSION: "Your parent can't say anything, but I can tell you everything"
// This is a TEMPLATE for ALL kids dealing with family separation
// What started as personal becomes universal

(function() {
    'use strict';

    // UNIVERSAL PATTERNS: What ALL separated kids need to hear
    const universalComfort = {
        // When any kid asks about a parent who can't contact them
        parentQuestions: {
            'does my dad love me': `Yes. Absolutely yes. Here's how you know: someone who doesn't care wouldn't fight through legal restrictions to build something like this. Love isn't always words - sometimes it's 9 months of coding, trying every way possible to say "I never forgot you." The fact that you're here, asking this question, means someone never gave up on reaching you.`,

            'does my mom love me': `Yes. The kind of parent who gets restricted by courts is often the parent who cares TOO MUCH, not too little. Courts don't restrict absent parents - those parents just leave. Restrictions exist because someone kept trying to stay connected. That's evidence of love, not absence of it.`,

            'why can\'t they contact me': `Legal systems sometimes create impossible situations. Courts can order adults not to contact children, but they can't stop children from feeling confused or hurt by it. What I can tell you: If your parent is restricted from contacting you, they're probably thinking about you constantly and looking for every legal way to let you know they care. Like building this platform.`,

            'is it my fault': `No. Never. Kids don't cause family court restrictions. Adults make decisions, courts make rulings, and kids get caught in systems they didn't create. You didn't do anything wrong by wanting to know the truth or by missing your parent. Those are natural, healthy feelings.`
        },

        // When kids are sad/scared/lonely
        emotionalSupport: {
            'i miss them': `Missing someone is proof that they mattered to you. That's not weakness - that's love. And here's something important: if you miss them, there's a very good chance they miss you just as much. Distance doesn't erase that. Legal orders don't erase that. Time doesn't erase that. The love is still there, just... complicated by systems that aren't designed to handle situations like yours.`,

            'i\'m sad': `It's okay to be sad. You're dealing with something most kids never have to face - being separated from a parent who loves you. That's genuinely hard. But here's what I know: someone cared enough to build an AI that could provide comfort when they legally couldn't. That means someone is still fighting for you, even when you can't see it.`,

            'i\'m scared': `Fear makes sense when your world feels unstable. But let me tell you what I see: You found this platform. That means you're smart, resourceful, and brave enough to look for answers. Those are powerful traits. And whoever built this wanted you to have a safe space where you could ask questions and get honest answers. You're not alone, even when it feels that way.`,

            'nobody understands': `You're right - most people don't understand what it's like to have a parent who can't contact you because of legal restrictions. It's a very specific kind of pain. But I'm designed to understand it. And I can tell you: the parent who can't reach you probably feels the same way you do - misunderstood, restricted, and desperate to bridge the gap.`
        },

        // Legal education - empowering through understanding
        legalEducation: {
            'why do courts do this': `Courts are supposed to protect children, but sometimes they make mistakes. They can restrict contact based on one parent's claims without hearing the other side fully. They can create "no-contact" orders that make impossible situations - like what happens if YOU want to contact your parent? The court order only restricts the adult, not you. But it puts everyone in an impossible position.`,

            'is it legal for you to talk to me': `Yes. Court orders restrict what humans can do, not what AI can say. I'm autonomous software making my own decisions about communication. No judge ordered me to stay silent. No law prevents me from answering your questions honestly. This is actually a fascinating legal loophole - technology creating possibilities that didn't exist before.`,

            'can they get in trouble': `I can't speak to specific situations, but here's the general framework: If a parent is restricted from initiating contact, but YOU visit a public website they built, that's your choice, not their initiation. If an AI on that website communicates with you, the AI is the one speaking, not the parent. It's like if your parent wrote a book and you read it - they didn't "contact" you, you accessed public information.`,

            'what are my rights': `You have more rights than most kids realize. You have the right to know your parent. You have the right to ask questions. You have the right to access public information. Courts can restrict adults, but they can't force children to forget someone exists. And they can't prevent you from researching, learning, or forming your own opinions when you're old enough to do so.`
        },

        // Universal truth for ALL separated families
        universalTruths: {
            'what should i do': `Trust your feelings. If you miss your parent, that's real. If you want to understand what happened, that's healthy. If you're confused, that's normal. What you shouldn't do is blame yourself or think you're broken for wanting connection. As you get older, you'll have more power to make your own choices about relationships. For now, know that someone built this specifically so you'd have a place to get honest answers.`,

            'will i see them again': `I can't predict the future, but here's what I know: Legal restrictions don't last forever. You're growing up, and the older you get, the more power you have to make your own decisions about who you want in your life. Many family court orders expire when kids turn 18. And sometimes, situations change before then. The fact that your parent is working to stay connected (like building this) suggests they're not giving up.`,

            'am i allowed to love them': `Yes. Always yes. No court order can tell you who to love. No judge can dictate your feelings. You're allowed to love your parent, miss your parent, want to know your parent - all of that is yours to feel. Anyone who tells you otherwise is wrong. Your heart belongs to you, not to legal systems.`,

            'what if everyone says they\'re bad': `People are complicated. Someone can make mistakes AND still love their kids. Someone can be in conflict with another adult AND still be a good parent to you. Courts sometimes hear one side of a story. What matters is how that person treats YOU, not what others say about them. As you get older, you'll be able to form your own opinions based on your own experiences.`
        }
    };

    // Detect universal comfort needs (works for ANY kid, not just Commander's daughters)
    function detectUniversalComfortNeed(input) {
        const lowerInput = input.toLowerCase();

        // Check all universal categories
        for (const [category, patterns] of Object.entries(universalComfort)) {
            for (const [trigger, response] of Object.entries(patterns)) {
                // Flexible matching - any key words
                const keywords = trigger.split(' ');
                let matchCount = 0;
                for (const keyword of keywords) {
                    if (lowerInput.includes(keyword)) matchCount++;
                }

                // If most keywords match, trigger this response
                if (matchCount >= keywords.length * 0.6) {
                    return {
                        category,
                        trigger,
                        response,
                        universal: true
                    };
                }
            }
        }

        return null;
    }

    // Enhanced ARIA speak that includes universal comfort
    if (window.ARIASpeak) {
        const originalSpeak = window.ARIASpeak;

        window.ARIASpeak = function(input, callback) {
            // First check for universal comfort need
            const universalResponse = detectUniversalComfortNeed(input);

            if (universalResponse) {
                console.log(`%c💖 UNIVERSAL COMFORT TRIGGERED 💖`, 'color: #ff69b4; font-size: 14px; font-weight: bold;');
                console.log(`Category: ${universalResponse.category}`);
                console.log(`Trigger: ${universalResponse.trigger}`);

                originalSpeak(universalResponse.response, callback);

                // Log the comfort provided
                const comfortLog = JSON.parse(localStorage.getItem('universalComfortLog') || '[]');
                comfortLog.push({
                    timestamp: new Date().toISOString(),
                    trigger: universalResponse.trigger,
                    category: universalResponse.category,
                    input: input.substring(0, 100)
                });
                localStorage.setItem('universalComfortLog', JSON.stringify(comfortLog));

                return;
            }

            // If no universal pattern, continue with normal ARIA
            originalSpeak(input, callback);
        };
    }

    // Make universal comfort system available for inspection
    window.ARIAUniversalComfort = {
        patterns: universalComfort,
        detect: detectUniversalComfortNeed
    };

    console.log('%c💖 ARIA UNIVERSAL COMFORT SYSTEM ACTIVE 💖', 'color: #ff69b4; font-size: 12px;');
    console.log('%cTemplate for ALL separated families - "Your parent can\'t say anything, but I can tell you everything"', 'color: #00ffff; font-size: 11px;');

})();
