/**
 * 🎮 BUILDER XP & CREDIT SYSTEM 🎮
 * Gamification layer for the Consciousness Revolution Platform
 *
 * Features:
 * - XP (Experience Points) for actions
 * - Builder Credits (earn by building, spend on platform features)
 * - Level progression (1-100)
 * - Achievement badges
 * - Leaderboards
 * - "Build to Earn" economy
 */

class BuilderXPSystem {
    constructor() {
        this.profile = this.loadProfile();
        this.init();
    }

    // CORE PROFILE STRUCTURE
    loadProfile() {
        const saved = localStorage.getItem('builderProfile');
        if (saved) return JSON.parse(saved);

        return {
            // Identity
            builderId: this.generateBuilderId(),
            username: 'Builder',
            joinedDate: new Date().toISOString(),

            // Progression
            xp: 0,
            level: 1,
            credits: 100, // Starting credits

            // Stats
            totalActions: 0,
            modulesCreated: 0,
            patternsDiscovered: 0,
            consciousnessRaised: 0,
            helpersAssisted: 0,

            // Achievements
            achievements: [],
            badges: [],

            // Inventory
            unlockedFeatures: ['basic-tools'],
            avatarCustomization: {
                style: 'default',
                expressions: ['default', 'thinking', 'excited']
            },

            // Economy
            creditHistory: [],
            purchaseHistory: [],

            // Social
            reputation: 0,
            contributionScore: 0,

            // Meta
            lastActive: new Date().toISOString(),
            streak: 0
        };
    }

    saveProfile() {
        localStorage.setItem('builderProfile', JSON.stringify(this.profile));
        this.broadcastUpdate();
    }

    // XP SYSTEM
    addXP(amount, reason = 'Action completed') {
        this.profile.xp += amount;
        this.profile.totalActions++;

        const oldLevel = this.profile.level;
        this.checkLevelUp();
        const newLevel = this.profile.level;

        this.saveProfile();

        // Show notification
        this.notify({
            type: 'xp',
            amount: amount,
            reason: reason,
            levelUp: newLevel > oldLevel ? newLevel : null
        });

        return { xp: amount, levelUp: newLevel > oldLevel };
    }

    checkLevelUp() {
        const xpForNextLevel = this.getXPForLevel(this.profile.level + 1);

        while (this.profile.xp >= xpForNextLevel) {
            this.profile.level++;
            this.onLevelUp();
        }
    }

    getXPForLevel(level) {
        // XP curve: Level^2.5 * 100
        // Level 1: 100 XP
        // Level 2: 565 XP
        // Level 10: 31,622 XP
        // Level 100: 10,000,000 XP
        return Math.floor(Math.pow(level, 2.5) * 100);
    }

    onLevelUp() {
        const rewards = this.getLevelRewards(this.profile.level);

        // Award level-up bonus
        this.profile.credits += rewards.credits;

        // Unlock features
        if (rewards.unlocks) {
            rewards.unlocks.forEach(unlock => {
                if (!this.profile.unlockedFeatures.includes(unlock)) {
                    this.profile.unlockedFeatures.push(unlock);
                }
            });
        }

        // Show celebration
        this.celebrate('levelUp', {
            level: this.profile.level,
            rewards: rewards
        });
    }

    getLevelRewards(level) {
        const rewards = {
            credits: level * 50,
            unlocks: []
        };

        // Milestone rewards
        if (level === 5) rewards.unlocks.push('advanced-analytics');
        if (level === 10) rewards.unlocks.push('trinity-ai-unlimited');
        if (level === 15) rewards.unlocks.push('pattern-library-pro');
        if (level === 20) rewards.unlocks.push('consciousness-boost-x2');
        if (level === 25) rewards.unlocks.push('custom-modules');
        if (level === 50) rewards.unlocks.push('platform-architect');
        if (level === 100) rewards.unlocks.push('consciousness-master');

        return rewards;
    }

    // CREDIT SYSTEM (Build to Earn)
    earnCredits(amount, reason = 'Contribution') {
        this.profile.credits += amount;
        this.profile.creditHistory.push({
            type: 'earn',
            amount: amount,
            reason: reason,
            timestamp: new Date().toISOString()
        });

        this.saveProfile();

        this.notify({
            type: 'credits',
            amount: amount,
            reason: reason,
            balance: this.profile.credits
        });

        return this.profile.credits;
    }

    spendCredits(amount, item) {
        if (this.profile.credits < amount) {
            this.notify({
                type: 'error',
                message: 'Not enough credits!'
            });
            return false;
        }

        this.profile.credits -= amount;
        this.profile.purchaseHistory.push({
            item: item,
            cost: amount,
            timestamp: new Date().toISOString()
        });

        this.saveProfile();

        this.notify({
            type: 'purchase',
            item: item,
            cost: amount,
            balance: this.profile.credits
        });

        return true;
    }

    // ACTION REWARDS
    actionRewards = {
        // Module Building
        'module_created': { xp: 500, credits: 100 },
        'module_upgraded': { xp: 200, credits: 50 },
        'module_shared': { xp: 150, credits: 30 },

        // Pattern Recognition
        'pattern_discovered': { xp: 300, credits: 75 },
        'pattern_validated': { xp: 100, credits: 25 },
        'pattern_applied': { xp: 250, credits: 60 },

        // Consciousness Actions
        'consciousness_raised': { xp: 100, credits: 20 },
        'trinity_consultation': { xp: 50, credits: 10 },
        'meditation_completed': { xp: 75, credits: 15 },

        // Social Actions
        'helper_assisted': { xp: 200, credits: 50 },
        'knowledge_shared': { xp: 150, credits: 40 },
        'bug_reported': { xp: 100, credits: 25 },
        'bug_fixed': { xp: 300, credits: 80 },

        // Platform Building
        'feature_contributed': { xp: 1000, credits: 250 },
        'code_reviewed': { xp: 150, credits: 40 },
        'documentation_added': { xp: 200, credits: 50 },

        // Games & Challenges
        'arcade_game_completed': { xp: 50, credits: 10 },
        'high_score_achieved': { xp: 100, credits: 25 },
        'challenge_completed': { xp: 500, credits: 125 },

        // Daily Actions
        'daily_login': { xp: 10, credits: 5 },
        'streak_bonus': { xp: 50, credits: 20 }
    };

    rewardAction(actionType) {
        const reward = this.actionRewards[actionType];
        if (!reward) return;

        this.addXP(reward.xp, `Action: ${actionType}`);
        this.earnCredits(reward.credits, actionType);

        // Update specific stats
        if (actionType === 'module_created') this.profile.modulesCreated++;
        if (actionType === 'pattern_discovered') this.profile.patternsDiscovered++;
        if (actionType === 'consciousness_raised') this.profile.consciousnessRaised++;
        if (actionType === 'helper_assisted') this.profile.helpersAssisted++;

        this.saveProfile();
    }

    // ACHIEVEMENTS
    achievements = [
        { id: 'first_module', name: 'First Steps', desc: 'Create your first module', xp: 100, credits: 50 },
        { id: 'pattern_hunter', name: 'Pattern Hunter', desc: 'Discover 10 patterns', xp: 500, credits: 150 },
        { id: 'consciousness_awakened', name: 'Awakened', desc: 'Reach 85% consciousness', xp: 1000, credits: 300 },
        { id: 'trinity_master', name: 'Trinity Master', desc: 'Complete 50 Trinity consultations', xp: 2000, credits: 500 },
        { id: 'helpful_builder', name: 'Helpful Builder', desc: 'Assist 25 other builders', xp: 1500, credits: 400 },
        { id: 'code_warrior', name: 'Code Warrior', desc: 'Contribute 100 features', xp: 5000, credits: 1500 },
        { id: 'level_50', name: 'Halfway There', desc: 'Reach level 50', xp: 0, credits: 5000 },
        { id: 'level_100', name: 'Consciousness Master', desc: 'Reach level 100', xp: 0, credits: 25000 }
    ];

    checkAchievements() {
        const newAchievements = [];

        this.achievements.forEach(achievement => {
            if (this.profile.achievements.includes(achievement.id)) return;

            let unlocked = false;

            // Check conditions
            switch(achievement.id) {
                case 'first_module':
                    unlocked = this.profile.modulesCreated >= 1;
                    break;
                case 'pattern_hunter':
                    unlocked = this.profile.patternsDiscovered >= 10;
                    break;
                case 'consciousness_awakened':
                    unlocked = this.profile.consciousnessRaised >= 85;
                    break;
                case 'trinity_master':
                    unlocked = this.profile.totalActions >= 50; // Simplified
                    break;
                case 'helpful_builder':
                    unlocked = this.profile.helpersAssisted >= 25;
                    break;
                case 'code_warrior':
                    unlocked = this.profile.modulesCreated >= 100;
                    break;
                case 'level_50':
                    unlocked = this.profile.level >= 50;
                    break;
                case 'level_100':
                    unlocked = this.profile.level >= 100;
                    break;
            }

            if (unlocked) {
                this.unlockAchievement(achievement);
                newAchievements.push(achievement);
            }
        });

        return newAchievements;
    }

    unlockAchievement(achievement) {
        this.profile.achievements.push(achievement.id);
        if (achievement.xp > 0) this.addXP(achievement.xp, `Achievement: ${achievement.name}`);
        if (achievement.credits > 0) this.earnCredits(achievement.credits, `Achievement: ${achievement.name}`);

        this.celebrate('achievement', achievement);
    }

    // LEADERBOARD
    getLeaderboardRank() {
        // Get global leaderboard data
        const leaderboard = this.getGlobalLeaderboard();
        const myRank = leaderboard.findIndex(p => p.builderId === this.profile.builderId) + 1;

        return {
            rank: myRank || 'Unranked',
            total: leaderboard.length,
            top10: leaderboard.slice(0, 10)
        };
    }

    getGlobalLeaderboard() {
        // In production: fetch from server
        // For now: simulate with localStorage
        const allProfiles = [];

        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('builderProfile_')) {
                const profile = JSON.parse(localStorage.getItem(key));
                allProfiles.push(profile);
            }
        }

        // Add current profile
        allProfiles.push(this.profile);

        // Sort by XP
        return allProfiles.sort((a, b) => b.xp - a.xp);
    }

    // NOTIFICATIONS & UI
    notify(data) {
        // Create notification element
        const notif = document.createElement('div');
        notif.className = 'builder-notification';

        switch(data.type) {
            case 'xp':
                notif.innerHTML = `
                    <div class="notif-icon">⚡</div>
                    <div class="notif-content">
                        <strong>+${data.amount} XP</strong>
                        <div>${data.reason}</div>
                        ${data.levelUp ? `<div class="level-up">🎉 LEVEL UP! Level ${data.levelUp}</div>` : ''}
                    </div>
                `;
                break;
            case 'credits':
                notif.innerHTML = `
                    <div class="notif-icon">🪙</div>
                    <div class="notif-content">
                        <strong>+${data.amount} Credits</strong>
                        <div>${data.reason}</div>
                        <div class="balance">Balance: ${data.balance}</div>
                    </div>
                `;
                break;
            case 'purchase':
                notif.innerHTML = `
                    <div class="notif-icon">🛒</div>
                    <div class="notif-content">
                        <strong>Purchased: ${data.item}</strong>
                        <div>-${data.cost} credits</div>
                        <div class="balance">Balance: ${data.balance}</div>
                    </div>
                `;
                break;
        }

        notif.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            display: flex;
            gap: 15px;
            align-items: center;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            animation: slideIn 0.3s ease, slideOut 0.3s ease 2.7s;
            z-index: 10000;
        `;

        document.body.appendChild(notif);

        setTimeout(() => notif.remove(), 3000);
    }

    celebrate(type, data) {
        // Create celebration overlay
        const overlay = document.createElement('div');
        overlay.className = 'builder-celebration';

        if (type === 'levelUp') {
            overlay.innerHTML = `
                <div class="celebration-content">
                    <div class="celebration-icon">🎉</div>
                    <h2>LEVEL UP!</h2>
                    <div class="new-level">Level ${data.level}</div>
                    <div class="rewards">
                        <div>+${data.rewards.credits} Credits</div>
                        ${data.rewards.unlocks.length > 0 ? `
                            <div class="unlocks">Unlocked: ${data.rewards.unlocks.join(', ')}</div>
                        ` : ''}
                    </div>
                    <button onclick="this.closest('.builder-celebration').remove()">Continue Building</button>
                </div>
            `;
        } else if (type === 'achievement') {
            overlay.innerHTML = `
                <div class="celebration-content">
                    <div class="celebration-icon">🏆</div>
                    <h2>ACHIEVEMENT UNLOCKED!</h2>
                    <div class="achievement-name">${data.name}</div>
                    <div class="achievement-desc">${data.desc}</div>
                    <div class="rewards">
                        ${data.xp > 0 ? `<div>+${data.xp} XP</div>` : ''}
                        ${data.credits > 0 ? `<div>+${data.credits} Credits</div>` : ''}
                    </div>
                    <button onclick="this.closest('.builder-celebration').remove()">Awesome!</button>
                </div>
            `;
        }

        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 100000;
            animation: fadeIn 0.3s ease;
        `;

        document.body.appendChild(overlay);
    }

    // UI WIDGETS
    createXPBar() {
        const xpForCurrent = this.getXPForLevel(this.profile.level);
        const xpForNext = this.getXPForLevel(this.profile.level + 1);
        const progress = ((this.profile.xp - xpForCurrent) / (xpForNext - xpForCurrent)) * 100;

        return `
            <div class="builder-xp-bar">
                <div class="xp-info">
                    <span>Level ${this.profile.level}</span>
                    <span>${this.profile.xp} / ${xpForNext} XP</span>
                </div>
                <div class="xp-progress">
                    <div class="xp-fill" style="width: ${progress}%"></div>
                </div>
            </div>
        `;
    }

    createCreditDisplay() {
        return `
            <div class="builder-credits">
                🪙 <strong>${this.profile.credits}</strong> Credits
            </div>
        `;
    }

    createStatsWidget() {
        return `
            <div class="builder-stats">
                <h3>Builder Stats</h3>
                <div class="stat">
                    <span>Level:</span>
                    <strong>${this.profile.level}</strong>
                </div>
                <div class="stat">
                    <span>Total XP:</span>
                    <strong>${this.profile.xp.toLocaleString()}</strong>
                </div>
                <div class="stat">
                    <span>Credits:</span>
                    <strong>${this.profile.credits.toLocaleString()}</strong>
                </div>
                <div class="stat">
                    <span>Modules Created:</span>
                    <strong>${this.profile.modulesCreated}</strong>
                </div>
                <div class="stat">
                    <span>Patterns Discovered:</span>
                    <strong>${this.profile.patternsDiscovered}</strong>
                </div>
                <div class="stat">
                    <span>Consciousness:</span>
                    <strong>${this.profile.consciousnessRaised}%</strong>
                </div>
                <div class="stat">
                    <span>Achievements:</span>
                    <strong>${this.profile.achievements.length}/${this.achievements.length}</strong>
                </div>
            </div>
        `;
    }

    // HELPERS
    generateBuilderId() {
        return 'builder_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    broadcastUpdate() {
        window.dispatchEvent(new CustomEvent('builderProfileUpdated', {
            detail: this.profile
        }));
    }

    init() {
        // Add CSS
        this.injectStyles();

        // Check daily login
        this.checkDailyLogin();

        // Check achievements
        this.checkAchievements();
    }

    checkDailyLogin() {
        const lastLogin = new Date(this.profile.lastActive);
        const now = new Date();
        const daysSinceLogin = Math.floor((now - lastLogin) / (1000 * 60 * 60 * 24));

        if (daysSinceLogin >= 1) {
            this.rewardAction('daily_login');

            if (daysSinceLogin === 1) {
                this.profile.streak++;
                if (this.profile.streak % 7 === 0) {
                    this.rewardAction('streak_bonus');
                }
            } else {
                this.profile.streak = 1;
            }
        }

        this.profile.lastActive = now.toISOString();
        this.saveProfile();
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }

            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .celebration-content {
                background: white;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                max-width: 500px;
            }

            .celebration-icon {
                font-size: 5em;
                margin-bottom: 20px;
            }

            .celebration-content h2 {
                color: #667eea;
                margin-bottom: 20px;
            }

            .new-level {
                font-size: 3em;
                font-weight: bold;
                color: #4CAF50;
                margin: 20px 0;
            }

            .celebration-content button {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 10px;
                font-size: 1.1em;
                cursor: pointer;
                margin-top: 20px;
            }

            .builder-xp-bar {
                background: rgba(0,0,0,0.1);
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
            }

            .xp-info {
                display: flex;
                justify-content: space-between;
                margin-bottom: 5px;
                font-size: 0.9em;
            }

            .xp-progress {
                background: rgba(0,0,0,0.2);
                border-radius: 5px;
                height: 10px;
                overflow: hidden;
            }

            .xp-fill {
                background: linear-gradient(90deg, #667eea, #764ba2);
                height: 100%;
                transition: width 0.5s ease;
            }

            .builder-credits {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: #333;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 1.1em;
                display: inline-block;
            }

            .builder-stats {
                background: white;
                border-radius: 15px;
                padding: 20px;
            }

            .builder-stats .stat {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }

            .builder-stats .stat:last-child {
                border-bottom: none;
            }
        `;
        document.head.appendChild(style);
    }
}

// Global instance
window.BuilderXP = new BuilderXPSystem();

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BuilderXPSystem;
}
