/**
 * SIMPLE BUG REPORTER WIDGET
 *
 * Add to any page: <script src="bug-reporter-widget.js"></script>
 *
 * Creates floating "Report Bug" button that opens simple text form.
 * Submits to Airtable (or your chosen backend).
 * No AI, no chatbot, no confusion - just honest bug reporting.
 */

(function() {
    // Only run once
    if (window.BugReporterLoaded) return;
    window.BugReporterLoaded = true;

    // Configuration
    const CONFIG = {
        // Bug report endpoint (same tunnel as terminal, just different port)
        submitURL: 'http://localhost:5001/api/bug-report', // For local testing
        // submitURL: 'https://YOUR_NGROK_URL/api/bug-report', // For production
        position: 'bottom-right' // bottom-right, bottom-left, top-right, top-left
    };

    // Create styles
    const styles = `
        #bug-reporter-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #ff4757;
            color: white;
            border: none;
            border-radius: 50px;
            padding: 15px 25px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
            z-index: 9998;
            transition: all 0.3s ease;
        }

        #bug-reporter-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 71, 87, 0.6);
        }

        #bug-reporter-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 9999;
            justify-content: center;
            align-items: center;
        }

        #bug-reporter-modal.active {
            display: flex;
        }

        .bug-reporter-content {
            background: #1a1a2e;
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
        }

        .bug-reporter-header {
            color: #00ff41;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            margin-bottom: 20px;
            text-shadow: 0 0 10px #00ff41;
        }

        .bug-reporter-label {
            color: #00d4ff;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin-bottom: 5px;
            display: block;
        }

        .bug-reporter-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            border-radius: 5px;
            padding: 10px;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin-bottom: 15px;
            outline: none;
        }

        .bug-reporter-textarea {
            min-height: 120px;
            resize: vertical;
        }

        .bug-reporter-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }

        .bug-reporter-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .bug-reporter-btn-submit {
            background: #00ff41;
            color: #1a1a2e;
        }

        .bug-reporter-btn-submit:hover {
            background: #00d435;
        }

        .bug-reporter-btn-cancel {
            background: transparent;
            color: #00ff41;
            border: 1px solid #00ff41;
        }

        .bug-reporter-btn-cancel:hover {
            background: rgba(0, 255, 65, 0.1);
        }

        .bug-reporter-status {
            margin-top: 15px;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            text-align: center;
        }

        .bug-reporter-status.success {
            background: rgba(0, 255, 65, 0.2);
            border: 1px solid #00ff41;
            color: #00ff41;
        }

        .bug-reporter-status.error {
            background: rgba(255, 71, 87, 0.2);
            border: 1px solid #ff4757;
            color: #ff4757;
        }
    `;

    // Inject styles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Create HTML
    const html = `
        <button id="bug-reporter-button">🐛 Report Bug</button>

        <div id="bug-reporter-modal">
            <div class="bug-reporter-content">
                <div class="bug-reporter-header">🐛 Report a Bug</div>

                <label class="bug-reporter-label">What page are you on?</label>
                <input type="text" id="bug-page" class="bug-reporter-input" readonly>

                <label class="bug-reporter-label">What happened? (Be specific!)</label>
                <textarea id="bug-description" class="bug-reporter-input bug-reporter-textarea" placeholder="Example: Clicked the 'Start' button but nothing happened. Expected to see dashboard."></textarea>

                <label class="bug-reporter-label">Your email (optional - only if you want updates)</label>
                <input type="email" id="bug-email" class="bug-reporter-input" placeholder="your@email.com">

                <div class="bug-reporter-buttons">
                    <button class="bug-reporter-btn bug-reporter-btn-cancel" id="bug-cancel">Cancel</button>
                    <button class="bug-reporter-btn bug-reporter-btn-submit" id="bug-submit">Submit Bug Report</button>
                </div>

                <div id="bug-status"></div>
            </div>
        </div>
    `;

    // Inject HTML
    document.body.insertAdjacentHTML('beforeend', html);

    // Get elements
    const button = document.getElementById('bug-reporter-button');
    const modal = document.getElementById('bug-reporter-modal');
    const cancelBtn = document.getElementById('bug-cancel');
    const submitBtn = document.getElementById('bug-submit');
    const pageInput = document.getElementById('bug-page');
    const descriptionInput = document.getElementById('bug-description');
    const emailInput = document.getElementById('bug-email');
    const statusDiv = document.getElementById('bug-status');

    // Set current page
    pageInput.value = window.location.href;

    // Open modal
    button.addEventListener('click', () => {
        modal.classList.add('active');
        descriptionInput.focus();
    });

    // Close modal
    cancelBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    function closeModal() {
        modal.classList.remove('active');
        descriptionInput.value = '';
        emailInput.value = '';
        statusDiv.innerHTML = '';
    }

    // Submit bug
    submitBtn.addEventListener('click', async () => {
        const description = descriptionInput.value.trim();

        if (!description) {
            showStatus('Please describe what happened!', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';

        try {
            const response = await fetch(CONFIG.submitURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    page: pageInput.value,
                    description: description,
                    email: emailInput.value || 'Not provided',
                    timestamp: new Date().toISOString(),
                    userAgent: navigator.userAgent
                })
            });

            if (response.ok) {
                showStatus('✅ Bug reported! Thank you!', 'success');
                setTimeout(closeModal, 2000);
            } else {
                throw new Error('Submission failed');
            }
        } catch (error) {
            showStatus('❌ Could not submit. Please email bugs to support@conciousnessrevolution.io', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Bug Report';
        }
    });

    function showStatus(message, type) {
        statusDiv.innerHTML = message;
        statusDiv.className = `bug-reporter-status ${type}`;
    }

    // Keyboard shortcut: Ctrl+Shift+B
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key === 'B') {
            button.click();
        }
    });

    console.log('🐛 Bug Reporter loaded - Press Ctrl+Shift+B or click button to report bugs');
})();
