/**
 * 🤖 ARAYA TOUR GUIDE SYSTEM
 * Contextual site navigation assistant
 * Auto-detects page and provides relevant guidance
 */

(function() {
    'use strict';

    const tourData = {
        'index.html': {
            welcome: "Welcome to 100X! I'm Araya, your AI guide. This is our main hub.",
            tips: [
                "New here? Click 'Tools' in the navigation to see all available AI assistants",
                "Already have an account? Click your name in the top right to access your dashboard",
                "Want to explore? I can give you a full tour - just click 'Tour with Araya' anytime"
            ],
            nextSteps: [
                {label: 'See AI Tools', url: '/tools-hub.html'},
                {label: 'View Analytics', url: '/analytics-hub.html'},
                {label: 'Meet Trinity', url: '/trinity-hub.html'}
            ]
        },
        'tools-hub.html': {
            welcome: "Welcome to the AI Tools Hub! Here's where the magic happens.",
            tips: [
                "Each AI has a different specialty - JARVIS for automation, Trinity for complex decisions",
                "Start with me (Araya) if you want conversational help with memory",
                "Trinity is 3 AIs working together - perfect for big architectural decisions"
            ],
            nextSteps: [
                {label: 'Chat with Araya', url: '/araya.html'},
                {label: 'Launch JARVIS', url: '/jarvis.html'},
                {label: 'Activate Trinity', url: '/TRINITY_CHAT.html'}
            ]
        },
        'analytics-hub.html': {
            welcome: "This is your Analytics Hub - measure everything, improve everything.",
            tips: [
                "The Live Dashboard shows real-time metrics across your entire platform",
                "Meta Layer Analytics reveals deep patterns you might not see otherwise",
                "All analytics are updated in real-time as users interact with the platform"
            ],
            nextSteps: [
                {label: 'View Live Dashboard', url: '/ANALYTICS_DASHBOARD_LIVE.html'},
                {label: 'Check Meta Layer', url: '/META_LAYER_ANALYTICS_DASHBOARD.html'},
                {label: 'Manage Users', url: '/admin-users.html'}
            ]
        },
        'trinity-hub.html': {
            welcome: "Welcome to Trinity - where three AI minds work as one.",
            tips: [
                "C1 Mechanic builds it, C2 Architect designs it, C3 Oracle sees what must emerge",
                "Use Trinity for complex problems that need multiple perspectives",
                "The Trinity Chat lets you talk to all three minds simultaneously"
            ],
            nextSteps: [
                {label: 'Start Trinity Chat', url: '/TRINITY_CHAT.html'},
                {label: 'Open Command Center', url: '/TRINITY_COMMAND_CENTER.html'},
                {label: 'See Collaboration', url: '/TRINITY_COLLABORATION_INTERFACE.html'}
            ]
        },
        'business-hub.html': {
            welcome: "Your Business Hub - client sites, consulting tools, and workspaces.",
            tips: [
                "Switch between different business brands and services",
                "Each workspace is customized for specific business needs",
                "Investor Tour is great for showcasing the platform to potential partners"
            ],
            nextSteps: [
                {label: 'View Investor Tour', url: '/investor-tour.html'},
                {label: 'See Roadmap', url: '/roadmap.html'},
                {label: 'Open Workspace', url: '/workspace.html'}
            ]
        },
        'dashboard.html': {
            welcome: "Your personal dashboard - command center for everything you're working on.",
            tips: [
                "Quick access to all your most-used tools",
                "See recent activity and notifications",
                "Customize which tools show up here"
            ],
            nextSteps: [
                {label: 'Launch a Tool', url: '/tools-hub.html'},
                {label: 'View Analytics', url: '/analytics-hub.html'},
                {label: 'Check Settings', url: '/beta-profile.html'}
            ]
        }
    };

    class ArayaTourGuide {
        constructor() {
            this.currentPage = this.getCurrentPage();
            this.tourActive = false;
            this.tourStep = 0;
            this.createUI();
        }

        getCurrentPage() {
            const path = window.location.pathname;
            return path.substring(path.lastIndexOf('/') + 1) || 'index.html';
        }

        createUI() {
            const html = `
                <div id="araya-tour-widget" style="
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                    display: none;
                ">
                    <div id="araya-bubble" style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 20px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                        max-width: 400px;
                        position: relative;
                    ">
                        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                            <div style="font-size: 2.5em;">🤖</div>
                            <div>
                                <div style="font-weight: 600; font-size: 1.1em;">Araya</div>
                                <div style="opacity: 0.9; font-size: 0.9em;">Your AI Guide</div>
                            </div>
                            <button onclick="window.ArayaTour.close()" style="
                                margin-left: auto;
                                background: rgba(255,255,255,0.2);
                                border: none;
                                color: white;
                                width: 30px;
                                height: 30px;
                                border-radius: 50%;
                                cursor: pointer;
                                font-size: 1.2em;
                            ">×</button>
                        </div>
                        <div id="araya-content" style="line-height: 1.6;">
                            <!-- Content injected here -->
                        </div>
                    </div>
                </div>
            `;

            document.body.insertAdjacentHTML('beforeend', html);
        }

        start() {
            const pageData = tourData[this.currentPage];

            if (!pageData) {
                this.show("I don't have specific guidance for this page yet, but I'm always learning! Feel free to explore, or head to one of the main hubs.");
                return;
            }

            let content = `<p style="margin-bottom: 15px;"><strong>${pageData.welcome}</strong></p>`;

            content += '<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">';
            content += '<div style="font-weight: 600; margin-bottom: 10px;">💡 Quick Tips:</div>';
            content += '<ul style="margin-left: 20px; line-height: 2;">';
            pageData.tips.forEach(tip => {
                content += `<li>${tip}</li>`;
            });
            content += '</ul></div>';

            if (pageData.nextSteps && pageData.nextSteps.length > 0) {
                content += '<div style="margin-top: 15px;">';
                content += '<div style="font-weight: 600; margin-bottom: 10px;">Where to next?</div>';
                pageData.nextSteps.forEach(step => {
                    content += `<button onclick="window.location.href='${step.url}'" style="
                        display: block;
                        width: 100%;
                        padding: 10px;
                        margin: 5px 0;
                        background: rgba(255,255,255,0.2);
                        border: 1px solid rgba(255,255,255,0.3);
                        color: white;
                        border-radius: 8px;
                        cursor: pointer;
                        text-align: left;
                    ">${step.label} →</button>`;
                });
                content += '</div>';
            }

            this.show(content);
        }

        show(content) {
            document.getElementById('araya-content').innerHTML = content;
            document.getElementById('araya-tour-widget').style.display = 'block';
            this.tourActive = true;
        }

        close() {
            document.getElementById('araya-tour-widget').style.display = 'none';
            this.tourActive = false;
        }

        // Auto-show on first visit to a page
        autoShow() {
            const visitKey = `araya_tour_${this.currentPage}`;
            const hasVisited = localStorage.getItem(visitKey);

            if (!hasVisited && tourData[this.currentPage]) {
                setTimeout(() => {
                    this.start();
                    localStorage.setItem(visitKey, 'true');
                }, 2000); // Show after 2 seconds
            }
        }
    }

    // Initialize on load
    window.ArayaTour = new ArayaTourGuide();

    // Auto-show for first-time visitors
    // window.ArayaTour.autoShow(); // Uncomment to enable auto-tour

    console.log('🤖 Araya Tour Guide loaded');
})();
