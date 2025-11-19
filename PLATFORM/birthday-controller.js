/* 🎂 BIRTHDAY PARTY CONTROLLER - ELEGANT MODE 🎂 */

class BirthdayController {
    constructor() {
        this.isActive = false;
        this.confettiActive = false;
        this.init();
    }

    init() {
        // Add birthday mode class to body
        document.body.classList.add('birthday-mode');

        // Create birthday banner
        this.createBanner();

        // Create birthday badge
        this.createBadge();

        // Create confetti container (hidden by default)
        this.createConfettiContainer();

        // Show welcome modal after 1 second
        setTimeout(() => this.showWelcomeModal(), 1000);

        this.isActive = true;
    }

    createBanner() {
        const banner = document.createElement('div');
        banner.className = 'birthday-banner';
        banner.innerHTML = `
            🎂 Happy Birthday Commander! Welcome to the Consciousness Revolution celebration! 🎉
            <button class="birthday-banner-close" onclick="birthdayController.closeBanner()">✕</button>
        `;
        document.body.insertBefore(banner, document.body.firstChild);
    }

    createBadge() {
        const badge = document.createElement('div');
        badge.className = 'birthday-badge';
        badge.innerHTML = '🎉 Celebrate!';
        badge.onclick = () => this.launchConfetti();
        document.body.appendChild(badge);
    }

    createConfettiContainer() {
        const container = document.createElement('div');
        container.className = 'birthday-confetti';
        container.id = 'birthdayConfetti';
        document.body.appendChild(container);
    }

    showWelcomeModal() {
        // Create backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'birthday-modal-backdrop active';
        backdrop.onclick = () => this.closeModal();
        document.body.appendChild(backdrop);

        // Create modal
        const modal = document.createElement('div');
        modal.className = 'birthday-modal active';
        modal.innerHTML = `
            <h2>🎂 Happy Birthday! 🎂</h2>
            <p>Welcome to the Consciousness Revolution!</p>
            <p>Today we celebrate YOU and this incredible platform.</p>
            <p>Click anywhere to explore, or hit the "Celebrate!" button for confetti! 🎉</p>
            <button onclick="birthdayController.closeModal()">Let's Begin! 🚀</button>
        `;
        document.body.appendChild(modal);

        // Auto-close after 5 seconds
        setTimeout(() => this.closeModal(), 5000);
    }

    closeModal() {
        const modal = document.querySelector('.birthday-modal');
        const backdrop = document.querySelector('.birthday-modal-backdrop');
        if (modal) modal.remove();
        if (backdrop) backdrop.remove();
    }

    closeBanner() {
        const banner = document.querySelector('.birthday-banner');
        if (banner) {
            banner.style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                banner.remove();
                document.body.style.paddingTop = '0';
            }, 300);
        }
    }

    launchConfetti() {
        if (this.confettiActive) return;

        this.confettiActive = true;
        const container = document.getElementById('birthdayConfetti');
        container.classList.add('active');

        // Create 100 confetti pieces
        for (let i = 0; i < 100; i++) {
            setTimeout(() => {
                const piece = document.createElement('div');
                piece.className = 'confetti-piece';
                piece.style.left = Math.random() * 100 + '%';
                piece.style.animationDelay = Math.random() * 1 + 's';
                piece.style.animationDuration = (Math.random() * 2 + 2) + 's';
                container.appendChild(piece);

                // Remove after animation
                setTimeout(() => piece.remove(), 5000);
            }, i * 20);
        }

        // Reset after 5 seconds
        setTimeout(() => {
            container.classList.remove('active');
            container.innerHTML = '';
            this.confettiActive = false;
        }, 5000);

        // Change badge text
        const badge = document.querySelector('.birthday-badge');
        if (badge) {
            badge.innerHTML = '🎊 Celebrating!';
            setTimeout(() => {
                badge.innerHTML = '🎉 Celebrate!';
            }, 5000);
        }
    }

    // Track birthday visits
    trackVisit() {
        let visits = localStorage.getItem('birthdayVisits') || 0;
        visits = parseInt(visits) + 1;
        localStorage.setItem('birthdayVisits', visits);
        return visits;
    }

    getVisitCount() {
        return localStorage.getItem('birthdayVisits') || 0;
    }
}

// Animation for closing banner
const style = document.createElement('style');
style.innerHTML = `
    @keyframes slideUp {
        from { transform: translateY(0); opacity: 1; }
        to { transform: translateY(-100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize birthday controller on page load
let birthdayController;
window.addEventListener('DOMContentLoaded', () => {
    birthdayController = new BirthdayController();
    console.log('🎂 Birthday mode activated!');
    console.log('🎉 Visit count:', birthdayController.trackVisit());
});

// Keyboard shortcut: Press 'B' to launch confetti
document.addEventListener('keydown', (e) => {
    if (e.key.toLowerCase() === 'b' && !e.ctrlKey && !e.metaKey) {
        const activeElement = document.activeElement;
        // Don't trigger if typing in input/textarea
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            birthdayController.launchConfetti();
        }
    }
});
