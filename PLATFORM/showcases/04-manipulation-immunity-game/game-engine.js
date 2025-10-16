/**
 * 🎯 MANIPULATION IMMUNITY GAME ENGINE 🎯
 * Interactive consciousness training game
 */

class ManipulationImmunityGame {
    constructor() {
        this.currentQuestionIndex = 0;
        this.correctAnswers = 0;
        this.totalQuestions = 5; // SHORTENED: 5 questions instead of 10 (user feedback)
        this.consciousnessLevel = 0;
        this.questions = [];
        this.answered = false;
        this.startTime = null;
        this.questionStartTime = null;
    }

    start() {
        // Select 10 random scenarios (mix of manipulation and genuine)
        this.questions = this.selectQuestions(this.totalQuestions);
        this.startTime = Date.now();
        this.questionStartTime = Date.now();
        this.showQuestion();

        // Track game start
        this.trackEvent('game_start');
    }

    selectQuestions(count) {
        // Get mix of manipulation and genuine scenarios
        const manipulationScenarios = MANIPULATION_SCENARIOS.filter(s => s.isManipulation);
        const genuineScenarios = MANIPULATION_SCENARIOS.filter(s => !s.isManipulation);

        // Aim for 60/40 split (more manipulation to practice spotting)
        const manipCount = Math.ceil(count * 0.6);
        const genuineCount = count - manipCount;

        const selectedManip = this.shuffleArray([...manipulationScenarios]).slice(0, manipCount);
        const selectedGenuine = this.shuffleArray([...genuineScenarios]).slice(0, genuineCount);

        // Combine and shuffle
        return this.shuffleArray([...selectedManip, ...selectedGenuine]);
    }

    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    showQuestion() {
        this.answered = false;
        this.questionStartTime = Date.now();

        const question = this.questions[this.currentQuestionIndex];

        // Update UI
        document.getElementById('questionCounter').textContent =
            `Question ${this.currentQuestionIndex + 1} of ${this.totalQuestions}`;
        document.getElementById('scenario').textContent = question.text;
        document.getElementById('feedback').style.display = 'none';
        document.getElementById('nextBtn').style.display = 'none';

        // Enable buttons
        document.querySelectorAll('.answer-btn').forEach(btn => {
            btn.disabled = false;
        });
    }

    answerQuestion(answer) {
        if (this.answered) return;
        this.answered = true;

        const question = this.questions[this.currentQuestionIndex];
        const correct = (answer === 'manipulation' && question.isManipulation) ||
                       (answer === 'genuine' && !question.isManipulation);

        if (correct) {
            this.correctAnswers++;
        }

        // Calculate time taken
        const timeTaken = Date.now() - this.questionStartTime;

        // Track answer
        this.trackEvent('question_answered', {
            questionId: question.id,
            userAnswer: answer,
            correct: correct,
            timeTaken: timeTaken
        });

        // Update consciousness level
        this.consciousnessLevel = Math.floor((this.correctAnswers / (this.currentQuestionIndex + 1)) * 100);
        this.updateConsciousnessMeter();

        // Show feedback
        this.showFeedback(correct, question);

        // Disable buttons
        document.querySelectorAll('.answer-btn').forEach(btn => {
            btn.disabled = true;
        });

        // Show next button
        document.getElementById('nextBtn').style.display = 'block';
    }

    showFeedback(correct, question) {
        const feedback = document.getElementById('feedback');
        feedback.style.display = 'block';

        if (correct) {
            feedback.className = 'feedback correct';
            feedback.innerHTML = `
                <strong>✅ Correct!</strong><br><br>
                <strong>Explanation:</strong> ${question.explanation}<br><br>
                <strong>Technique:</strong> ${question.technique}
                ${question.isManipulation ? `
                    <div class="manipulation-formula">
                        Manipulation Score: ${question.manipulationScore}/100<br>
                        M = (FE:${question.factors.FE} × CB:${question.factors.CB} × SR:${question.factors.SR} × CD:${question.factors.CD} × PE:${question.factors.PE}) × DC:${question.factors.DC}
                    </div>
                ` : ''}
            `;
        } else {
            feedback.className = 'feedback incorrect';
            feedback.innerHTML = `
                <strong>❌ Incorrect</strong><br><br>
                <strong>Correct Answer:</strong> This is ${question.isManipulation ? 'MANIPULATION' : 'GENUINE'}<br><br>
                <strong>Explanation:</strong> ${question.explanation}<br><br>
                <strong>Technique:</strong> ${question.technique}
                ${question.isManipulation ? `
                    <div class="manipulation-formula">
                        Manipulation Score: ${question.manipulationScore}/100<br>
                        M = (FE:${question.factors.FE} × CB:${question.factors.CB} × SR:${question.factors.SR} × CD:${question.factors.CD} × PE:${question.factors.PE}) × DC:${question.factors.DC}
                    </div>
                ` : ''}
            `;
        }
    }

    updateConsciousnessMeter() {
        document.getElementById('consciousnessLevel').textContent = `${this.consciousnessLevel}%`;
        document.getElementById('progressFill').style.width = `${this.consciousnessLevel}%`;
        document.getElementById('progressText').textContent = `${this.consciousnessLevel}%`;
    }

    nextQuestion() {
        this.currentQuestionIndex++;

        if (this.currentQuestionIndex >= this.totalQuestions) {
            this.endGame();
        } else {
            this.showQuestion();
        }
    }

    endGame() {
        // Calculate final stats
        const totalTime = Date.now() - this.startTime;
        const finalScore = this.consciousnessLevel;

        // Track completion
        this.trackEvent('game_complete', {
            score: finalScore,
            correct: this.correctAnswers,
            total: this.totalQuestions,
            time: totalTime
        });

        // Save high score
        this.saveHighScore(finalScore);

        // Show results
        document.getElementById('gameScreen').style.display = 'none';
        document.getElementById('resultsScreen').style.display = 'block';

        document.getElementById('finalScore').textContent = `${finalScore}%`;
        document.getElementById('correctCount').textContent = `${this.correctAnswers}`;
        document.getElementById('totalQuestions').textContent = `${this.totalQuestions}`;

        // Show achievement badge
        const badge = this.getAchievementBadge(finalScore);
        document.getElementById('achievementBadge').innerHTML = badge.emoji + ' ' + badge.title;

        // Create share buttons
        viralEngine.createShareButtons('manipulation-immunity-game', 'shareButtons', {
            score: finalScore
        });

        // Celebrate if high score
        if (finalScore >= 85) {
            this.celebrateHighScore();
        }
    }

    getAchievementBadge(score) {
        if (score >= 90) {
            return { emoji: '🏆', title: 'Consciousness Master', description: 'Elite manipulation immunity!' };
        } else if (score >= 85) {
            return { emoji: '⚡', title: 'Consciousness Knight', description: 'Achieved immunity threshold!' };
        } else if (score >= 70) {
            return { emoji: '🎯', title: 'Pattern Seeker', description: 'Strong awareness growing!' };
        } else if (score >= 50) {
            return { emoji: '🌱', title: 'Consciousness Awakening', description: 'On the path to immunity!' };
        } else {
            return { emoji: '🔍', title: 'Truth Seeker', description: 'Beginning the journey!' };
        }
    }

    celebrateHighScore() {
        // Add confetti or celebration animation
        const celebration = document.createElement('div');
        celebration.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 5rem;
            z-index: 10000;
            animation: celebrate 2s ease-out;
        `;
        celebration.textContent = '🎉';

        document.body.appendChild(celebration);

        setTimeout(() => celebration.remove(), 2000);
    }

    saveHighScore(score) {
        const highScore = parseInt(localStorage.getItem('manipulationGameHighScore') || '0');

        if (score > highScore) {
            localStorage.setItem('manipulationGameHighScore', score.toString());

            // Show new high score notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(45deg, #FFD700, #FFA500);
                color: #333;
                padding: 20px 30px;
                border-radius: 15px;
                font-size: 1.2rem;
                font-weight: bold;
                z-index: 10000;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            `;
            notification.textContent = `🏆 NEW HIGH SCORE: ${score}%!`;

            document.body.appendChild(notification);

            setTimeout(() => notification.remove(), 5000);
        }
    }

    restart() {
        this.currentQuestionIndex = 0;
        this.correctAnswers = 0;
        this.consciousnessLevel = 0;
        this.answered = false;

        document.getElementById('gameScreen').style.display = 'block';
        document.getElementById('resultsScreen').style.display = 'none';

        this.updateConsciousnessMeter();
        this.start();
    }

    trackEvent(event, data = {}) {
        // Track locally
        const events = JSON.parse(localStorage.getItem('gameEvents') || '[]');
        events.push({
            event: event,
            data: data,
            timestamp: Date.now()
        });

        // Keep last 100 events
        if (events.length > 100) {
            events.shift();
        }

        localStorage.setItem('gameEvents', JSON.stringify(events));

        // Send to viral engine analytics
        if (typeof viralEngine !== 'undefined') {
            viralEngine.sendToAnalytics(event, {
                showcase: 'manipulation-immunity-game',
                ...data
            });
        }
    }
}

// Add celebration animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes celebrate {
        0% {
            transform: translate(-50%, -50%) scale(0) rotate(0deg);
            opacity: 0;
        }
        50% {
            transform: translate(-50%, -50%) scale(2) rotate(180deg);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -50%) scale(0) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
