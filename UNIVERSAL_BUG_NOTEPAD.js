// UNIVERSAL BUG SUBMISSION NOTEPAD
// Automatically appears on every page - minimalist, always accessible

(function() {
    'use strict';

    // Create bug notepad HTML
    const bugNotepadHTML = `
        <div id="bug-notepad-widget" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999999;
            font-family: 'Courier New', monospace;
        ">
            <!-- Minimized State: Just a button -->
            <div id="bug-notepad-minimized" style="
                background: linear-gradient(135deg, #ff4444, #cc0000);
                color: white;
                padding: 15px 20px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(255, 68, 68, 0.5);
                font-size: 1rem;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s;
            ">
                🐛 REPORT BUG
            </div>

            <!-- Expanded State: Full notepad -->
            <div id="bug-notepad-expanded" style="
                display: none;
                background: rgba(0, 0, 0, 0.95);
                border: 3px solid #ff4444;
                border-radius: 15px;
                padding: 20px;
                width: 400px;
                box-shadow: 0 10px 40px rgba(255, 68, 68, 0.5);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="color: #ff4444; margin: 0; font-size: 1.3rem;">🐛 Bug Report</h3>
                    <button id="bug-notepad-close" style="
                        background: transparent;
                        border: 2px solid #ff4444;
                        color: #ff4444;
                        padding: 5px 12px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 1rem;
                        font-weight: bold;
                    ">✕</button>
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="color: #00ff41; display: block; margin-bottom: 5px; font-size: 0.9rem;">
                        What page are you on?
                    </label>
                    <input type="text" id="bug-page" readonly style="
                        width: 100%;
                        padding: 10px;
                        background: rgba(0, 255, 65, 0.1);
                        border: 2px solid #00ff41;
                        border-radius: 8px;
                        color: #00ff41;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9rem;
                    ">
                </div>

                <div style="margin-bottom: 15px;">
                    <label style="color: #00ff41; display: block; margin-bottom: 5px; font-size: 0.9rem;">
                        What's broken? (describe the issue)
                    </label>
                    <textarea id="bug-description" placeholder="e.g., Voice recording not working, button doesn't click, page won't load..." style="
                        width: 100%;
                        height: 120px;
                        padding: 10px;
                        background: rgba(0, 255, 65, 0.1);
                        border: 2px solid #00ff41;
                        border-radius: 8px;
                        color: #00ff41;
                        font-family: 'Courier New', monospace;
                        font-size: 0.9rem;
                        resize: vertical;
                    "></textarea>
                </div>

                <button id="bug-submit" style="
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(135deg, #ff4444, #cc0000);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-size: 1.1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s;
                    font-family: 'Courier New', monospace;
                ">
                    📤 SUBMIT BUG REPORT
                </button>

                <div id="bug-status" style="
                    margin-top: 15px;
                    padding: 10px;
                    background: rgba(0, 255, 65, 0.1);
                    border: 2px solid #00ff41;
                    border-radius: 8px;
                    color: #00ff41;
                    font-size: 0.9rem;
                    text-align: center;
                    display: none;
                "></div>
            </div>
        </div>
    `;

    // Inject into page
    document.body.insertAdjacentHTML('beforeend', bugNotepadHTML);

    // Get elements
    const minimized = document.getElementById('bug-notepad-minimized');
    const expanded = document.getElementById('bug-notepad-expanded');
    const closeBtn = document.getElementById('bug-notepad-close');
    const submitBtn = document.getElementById('bug-submit');
    const pageInput = document.getElementById('bug-page');
    const descriptionInput = document.getElementById('bug-description');
    const statusDiv = document.getElementById('bug-status');

    // Set current page URL
    pageInput.value = window.location.href;

    // Show/Hide notepad
    minimized.addEventListener('click', () => {
        minimized.style.display = 'none';
        expanded.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        expanded.style.display = 'none';
        minimized.style.display = 'flex';
    });

    // Hover effect for minimized button
    minimized.addEventListener('mouseenter', () => {
        minimized.style.transform = 'scale(1.1)';
        minimized.style.boxShadow = '0 6px 30px rgba(255, 68, 68, 0.7)';
    });

    minimized.addEventListener('mouseleave', () => {
        minimized.style.transform = 'scale(1)';
        minimized.style.boxShadow = '0 4px 20px rgba(255, 68, 68, 0.5)';
    });

    // Submit bug report
    submitBtn.addEventListener('click', async () => {
        const page = pageInput.value;
        const description = descriptionInput.value.trim();

        if (!description) {
            statusDiv.style.display = 'block';
            statusDiv.style.borderColor = '#ff4444';
            statusDiv.style.color = '#ff4444';
            statusDiv.textContent = '❌ Please describe the bug first!';
            return;
        }

        // Save to localStorage
        const bugReport = {
            timestamp: new Date().toISOString(),
            page: page,
            description: description,
            userAgent: navigator.userAgent,
            screenResolution: `${window.screen.width}x${window.screen.height}`
        };

        // Get existing bug reports
        let bugReports = [];
        try {
            const existing = localStorage.getItem('bug_reports');
            if (existing) {
                bugReports = JSON.parse(existing);
            }
        } catch (e) {
            bugReports = [];
        }

        // Add new report
        bugReports.push(bugReport);
        localStorage.setItem('bug_reports', JSON.stringify(bugReports));

        // Show success message
        statusDiv.style.display = 'block';
        statusDiv.style.borderColor = '#00ff41';
        statusDiv.style.color = '#00ff41';
        statusDiv.textContent = '✅ Bug report saved! Commander will review it.';

        // Clear the description
        descriptionInput.value = '';

        // Auto-close after 2 seconds
        setTimeout(() => {
            expanded.style.display = 'none';
            minimized.style.display = 'flex';
            statusDiv.style.display = 'none';
        }, 2000);

        // Log to console for debugging
        console.log('🐛 BUG REPORT SUBMITTED:', bugReport);
    });

    // ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && expanded.style.display === 'block') {
            expanded.style.display = 'none';
            minimized.style.display = 'flex';
        }
    });

    console.log('🐛 Universal Bug Notepad Active - Press button in bottom-right to report issues');
})();
