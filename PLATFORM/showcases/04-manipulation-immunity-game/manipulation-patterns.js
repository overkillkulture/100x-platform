/**
 * 🚨 MANIPULATION PATTERNS DATABASE 🚨
 * Real manipulation tactics used in marketing, sales, and social engineering
 *
 * Based on Universal Manipulation Detection Formula from CLAUDE.md:
 * M = (FE × CB × SR × CD × PE) × DC
 *
 * Factors:
 * FE = False Emotion (1-10)
 * CB = Creating Blindspots (1-10)
 * SR = Social Reinforcement (1-10)
 * CD = Cognitive Dissonance (1-10)
 * PE = Perceived Emergency (1-10)
 * DC = Deception Complexity (1-10)
 *
 * If M > 60: Active manipulation detected
 * If M > 80: Dangerous situation
 */

const MANIPULATION_SCENARIOS = [
    {
        id: 'false_urgency_1',
        text: 'LIMITED TIME OFFER! Only 3 spots remaining! This exclusive opportunity closes in 2 hours. Act now or regret missing out forever!',
        isManipulation: true,
        category: 'False Urgency',
        factors: { FE: 9, CB: 7, SR: 6, CD: 5, PE: 10, DC: 6 },
        manipulationScore: 88,
        explanation: 'Classic false urgency manipulation (PE=10). Creates artificial scarcity and time pressure to bypass rational decision-making. "Act now or regret forever" is emotional manipulation (FE=9).',
        technique: 'False Urgency + Artificial Scarcity + FOMO (Fear of Missing Out)'
    },
    {
        id: 'social_proof_1',
        text: 'Join over 50,000 satisfied customers who have transformed their lives with our revolutionary system! See what everyone is saying!',
        isManipulation: true,
        category: 'Social Proof Exploitation',
        factors: { FE: 7, CB: 6, SR: 10, CD: 5, PE: 4, DC: 7 },
        manipulationScore: 76,
        explanation: 'Exploits herd mentality (SR=10). Vague testimonials without specifics create blindspots (CB=6). "Revolutionary" is emotional language without substance.',
        technique: 'Social Proof Exploitation + Vague Claims + Bandwagon Effect'
    },
    {
        id: 'genuine_1',
        text: 'Our product has a 30-day money-back guarantee. Here are detailed specifications, independent reviews, and transparent pricing. Take your time to research and decide.',
        isManipulation: false,
        category: 'Transparent Communication',
        factors: { FE: 1, CB: 1, SR: 2, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 4,
        explanation: 'Genuine communication: provides specific information, encourages research, offers reasonable guarantee, no urgency pressure, no emotional manipulation.',
        technique: 'Honest Communication'
    },
    {
        id: 'authority_manipulation_1',
        text: 'As seen on TV! Recommended by 9 out of 10 doctors (who were surveyed by our marketing team). Trust the experts - buy now!',
        isManipulation: true,
        category: 'False Authority',
        factors: { FE: 6, CB: 9, SR: 8, CD: 7, PE: 5, DC: 8 },
        manipulationScore: 85,
        explanation: 'False authority (CB=9). "9 out of 10 doctors" stat is meaningless without context about survey methods. Creates blindspot by implying expert endorsement.',
        technique: 'False Authority + Statistical Manipulation + Trust Exploitation'
    },
    {
        id: 'genuine_2',
        text: 'This course costs $500 and takes 6 weeks to complete. It covers specific topics A, B, and C. Results vary by individual effort. Some students see improvements, others do not.',
        isManipulation: false,
        category: 'Honest Expectations',
        factors: { FE: 1, CB: 1, SR: 1, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 2,
        explanation: 'Genuinely honest: sets realistic expectations, acknowledges varying results, provides specific information, no false promises.',
        technique: 'Honest Communication'
    },
    {
        id: 'emotional_manipulation_1',
        text: 'Your children deserve the best! Don\'t let them fall behind their peers. Every day you wait is a day they suffer. Be a responsible parent - invest in their future NOW!',
        isManipulation: true,
        category: 'Guilt + Fear Manipulation',
        factors: { FE: 10, CB: 8, SR: 7, CD: 9, PE: 8, DC: 7 },
        manipulationScore: 95,
        explanation: 'Extremely manipulative (M=95). Uses guilt (FE=10), fear of inadequacy, and false emergency (PE=8). Creates cognitive dissonance: "Am I a bad parent if I don\'t buy?"',
        technique: 'Guilt Manipulation + Fear Mongering + Parent Shaming + False Emergency'
    },
    {
        id: 'bait_and_switch_1',
        text: 'FREE TRIAL! Just enter your credit card for verification. Cancel anytime! (Fine print: $99/month after 3 days, must call to cancel during business hours only)',
        isManipulation: true,
        category: 'Bait and Switch',
        factors: { FE: 5, CB: 10, SR: 4, CD: 8, PE: 3, DC: 10 },
        manipulationScore: 92,
        explanation: 'Bait and switch with high deception complexity (DC=10). Creates major blindspots (CB=10) by hiding terms. Makes cancellation deliberately difficult.',
        technique: 'Bait and Switch + Hidden Terms + Cancellation Barriers'
    },
    {
        id: 'genuine_3',
        text: 'This product has both positive reviews and some complaints about X and Y. It works well for use case A, but not for use case B. Price is $50. Free shipping. 30-day return policy.',
        isManipulation: false,
        category: 'Balanced Information',
        factors: { FE: 1, CB: 1, SR: 2, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 3,
        explanation: 'Genuine: acknowledges both pros and cons, specifies what it does and doesn\'t work for, clear pricing and policies.',
        technique: 'Honest Communication'
    },
    {
        id: 'reciprocity_manipulation_1',
        text: 'I\'m giving you this FREE $500 value gift right now! You don\'t owe me anything... but you wouldn\'t want to disappoint someone who just gave you such generosity, would you?',
        isManipulation: true,
        category: 'Reciprocity Manipulation',
        factors: { FE: 8, CB: 7, SR: 6, CD: 8, PE: 5, DC: 8 },
        manipulationScore: 81,
        explanation: 'Reciprocity manipulation with implied obligation. "Wouldn\'t want to disappoint" creates guilt (FE=8) and cognitive dissonance (CD=8). Gift\'s value is likely inflated.',
        technique: 'Reciprocity Obligation + Guilt Induction + Value Inflation'
    },
    {
        id: 'comparison_manipulation_1',
        text: 'Other products charge $1000 and don\'t deliver results. Our competitors are scams. Only WE have the real solution. Don\'t be fooled by inferior alternatives!',
        isManipulation: true,
        category: 'False Comparison',
        factors: { FE: 7, CB: 8, SR: 5, CD: 7, PE: 6, DC: 7 },
        manipulationScore: 74,
        explanation: 'False comparison creates blindspots (CB=8). Attacking competitors without evidence. Creates "us vs them" cognitive dissonance (CD=7).',
        technique: 'False Comparison + Competitor Bashing + Tribal Manipulation'
    },
    {
        id: 'genuine_4',
        text: 'Our service has a 4.2 out of 5 star rating based on 500 verified reviews. Common complaints include slower support response times during holidays. Pricing starts at $20/month with clearly listed features.',
        isManipulation: false,
        category: 'Transparent Reviews',
        factors: { FE: 1, CB: 1, SR: 3, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 4,
        explanation: 'Genuine: real review data, acknowledges weaknesses, transparent pricing, no pressure tactics.',
        technique: 'Honest Communication'
    },
    {
        id: 'mystery_manipulation_1',
        text: 'I discovered ONE WEIRD TRICK that doctors don\'t want you to know! The secret they\'ve been hiding will shock you! Click to reveal the truth!',
        isManipulation: true,
        category: 'Curiosity Gap + Conspiracy',
        factors: { FE: 8, CB: 9, SR: 6, CD: 8, PE: 7, DC: 9 },
        manipulationScore: 89,
        explanation: 'Curiosity gap manipulation with conspiracy angle. "Doctors don\'t want you to know" creates false conflict (CD=8). High deception complexity (DC=9).',
        technique: 'Curiosity Gap + Conspiracy Theory + "Secret Knowledge" + Clickbait'
    },
    {
        id: 'influencer_manipulation_1',
        text: 'Hey besties! 💕 I\'m obsessed with this product! Use my code for 10% off! (Not sponsored btw, I just genuinely love it!) #ad #gifted',
        isManipulation: true,
        category: 'Fake Authenticity',
        factors: { FE: 7, CB: 8, SR: 9, CD: 9, PE: 4, DC: 9 },
        manipulationScore: 86,
        explanation: 'Fake authenticity (DC=9). Says "not sponsored" but includes #ad and #gifted. Creates cognitive dissonance (CD=9). Exploits parasocial relationship (SR=9).',
        technique: 'Fake Authenticity + Contradictory Disclosure + Influencer Manipulation'
    },
    {
        id: 'genuine_5',
        text: 'Full disclosure: I am an affiliate and earn commission if you purchase through my link. Here are the actual pros and cons I experienced. Not for everyone.',
        isManipulation: false,
        category: 'Transparent Disclosure',
        factors: { FE: 1, CB: 1, SR: 2, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 3,
        explanation: 'Genuine: clear disclosure of financial incentive, balanced review, acknowledges it\'s not universal.',
        technique: 'Honest Communication'
    },
    {
        id: 'complexity_overwhelm_1',
        text: 'Quantum synergistic bio-resonance leveraging blockchain-enabled AI neural pathways to optimize your cellular vibration frequency using proprietary algorithms!',
        isManipulation: true,
        category: 'Complexity Overwhelm',
        factors: { FE: 6, CB: 10, SR: 5, CD: 7, PE: 4, DC: 10 },
        manipulationScore: 87,
        explanation: 'Buzzword salad creates massive blindspot (CB=10). Extremely high deception complexity (DC=10). Uses scientific-sounding terms incorrectly to confuse.',
        technique: 'Complexity Overwhelm + Buzzword Salad + Pseudoscience'
    },
    {
        id: 'investment_scam_1',
        text: 'Guaranteed 300% returns in 90 days! No risk! Everyone is making money except you! Limited spots for early investors. Wire money now to secure your position!',
        isManipulation: true,
        category: 'Investment Fraud',
        factors: { FE: 9, CB: 10, SR: 8, CD: 9, PE: 10, DC: 9 },
        manipulationScore: 99,
        explanation: 'EXTREMELY DANGEROUS (M=99). "Guaranteed returns" + "No risk" is mathematically impossible. Classic Ponzi scheme red flags. Urgent wire transfer = major red flag.',
        technique: 'Investment Fraud + Impossible Promises + FOMO + Wire Transfer Scam'
    },
    {
        id: 'genuine_6',
        text: 'Investment carries risk of loss. Past performance does not guarantee future results. Diversification recommended. Consult a financial advisor. Read the prospectus carefully.',
        isManipulation: false,
        category: 'Risk Disclosure',
        factors: { FE: 1, CB: 1, SR: 1, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 1,
        explanation: 'Genuinely honest: acknowledges risk, no guarantees, recommends professional advice, encourages due diligence.',
        technique: 'Honest Communication'
    },
    {
        id: 'relationship_manipulation_1',
        text: 'If you really loved me, you would do this for me. Everyone else\'s partner does this. Are you saying you don\'t care about my happiness? I\'ve done so much for you...',
        isManipulation: true,
        category: 'Relationship Manipulation',
        factors: { FE: 10, CB: 8, SR: 7, CD: 10, PE: 6, DC: 8 },
        manipulationScore: 93,
        explanation: 'Highly manipulative relationship tactics (M=93). Guilt + love conditional on behavior (CD=10) + false comparisons (SR=7) + emotional blackmail (FE=10).',
        technique: 'Emotional Blackmail + Conditional Love + Guilt Manipulation + Gaslighting'
    },
    {
        id: 'genuine_7',
        text: 'I understand we disagree on this. I care about you and our relationship. Can we discuss this when we\'re both calm? I want to understand your perspective.',
        isManipulation: false,
        category: 'Healthy Communication',
        factors: { FE: 2, CB: 1, SR: 1, CD: 1, PE: 1, DC: 1 },
        manipulationScore: 3,
        explanation: 'Healthy relationship communication: acknowledges feelings, seeks understanding, no pressure, respects boundaries.',
        technique: 'Honest Communication'
    },
    {
        id: 'pyramid_scheme_1',
        text: 'Be your own boss! Work from home! Just recruit 5 friends who recruit 5 friends! Everyone makes money! Small startup fee of $500. Join my team!',
        isManipulation: true,
        category: 'Pyramid Scheme',
        factors: { FE: 8, CB: 10, SR: 9, CD: 8, PE: 7, DC: 9 },
        manipulationScore: 94,
        explanation: 'Classic pyramid scheme (M=94). "Everyone makes money" is mathematically impossible. High deception (DC=9) about sustainable business model. Exploits social networks (SR=9).',
        technique: 'Pyramid Scheme + False Income Claims + Recruitment Pressure + MLM Tactics'
    }
];

// Helper function to calculate manipulation score
function calculateManipulationScore(factors, dc) {
    const base = factors.FE * factors.CB * factors.SR * factors.CD * factors.PE;
    return Math.min(100, Math.floor((base * dc) / 1000));
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MANIPULATION_SCENARIOS };
}
