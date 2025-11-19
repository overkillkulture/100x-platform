// Universal Bug Reporter & Easy Edit System
// Add this ONE LINE to any HTML: <script src="/universal-bug-reporter.js"></script>

(function() {
    'use strict';

    // Create floating bug reporter button
    const bugButton = document.createElement('div');
    bugButton.id = 'universal-bug-btn';
    bugButton.innerHTML = '🐛 Report Bug';
    bugButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 50px;
        cursor: pointer;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        z-index: 999999;
        transition: all 0.3s ease;
        user-select: none;
    `;

    bugButton.onmouseover = () => {
        bugButton.style.transform = 'scale(1.1)';
        bugButton.style.boxShadow = '0 6px 20px rgba(255, 107, 107, 0.6)';
    };

    bugButton.onmouseout = () => {
        bugButton.style.transform = 'scale(1)';
        bugButton.style.boxShadow = '0 4px 15px rgba(255, 107, 107, 0.4)';
    };

    // Create easy edit button
    const editButton = document.createElement('div');
    editButton.id = 'universal-edit-btn';
    editButton.innerHTML = '✏️ Easy Edit';
    editButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 180px;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 50px;
        cursor: pointer;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
        z-index: 999999;
        transition: all 0.3s ease;
        user-select: none;
    `;

    editButton.onmouseover = () => {
        editButton.style.transform = 'scale(1.1)';
        editButton.style.boxShadow = '0 6px 20px rgba(79, 172, 254, 0.6)';
    };

    editButton.onmouseout = () => {
        editButton.style.transform = 'scale(1)';
        editButton.style.boxShadow = '0 4px 15px rgba(79, 172, 254, 0.4)';
    };

    // Create bug report modal
    const modal = document.createElement('div');
    modal.id = 'bug-report-modal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        z-index: 1000000;
        justify-content: center;
        align-items: center;
    `;

    modal.innerHTML = `
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            padding: 40px;
            border-radius: 20px;
            max-width: 600px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        ">
            <h2 style="color: #fff; margin-bottom: 20px; font-size: 28px;">🐛 Report a Bug</h2>
            <p style="color: #aaa; margin-bottom: 25px; font-size: 16px;">
                Found something broken? Tell us what happened!
            </p>

            <div style="margin-bottom: 20px;">
                <label style="color: #fff; display: block; margin-bottom: 8px; font-weight: 600;">What's wrong?</label>
                <input type="text" id="bug-title" placeholder="e.g., Button doesn't work" style="
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #444;
                    border-radius: 10px;
                    background: #1a1a1a;
                    color: #fff;
                    font-size: 16px;
                    font-family: inherit;
                ">
            </div>

            <div style="margin-bottom: 20px;">
                <label style="color: #fff; display: block; margin-bottom: 8px; font-weight: 600;">Describe the problem</label>
                <textarea id="bug-description" placeholder="Tell us what happened and what you expected..." rows="5" style="
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #444;
                    border-radius: 10px;
                    background: #1a1a1a;
                    color: #fff;
                    font-size: 16px;
                    font-family: inherit;
                    resize: vertical;
                "></textarea>
            </div>

            <div style="margin-bottom: 25px;">
                <label style="color: #fff; display: block; margin-bottom: 8px; font-weight: 600;">Your name (optional)</label>
                <input type="text" id="bug-reporter-name" placeholder="e.g., Mariah" style="
                    width: 100%;
                    padding: 15px;
                    border: 2px solid #444;
                    border-radius: 10px;
                    background: #1a1a1a;
                    color: #fff;
                    font-size: 16px;
                    font-family: inherit;
                ">
            </div>

            <div style="display: flex; gap: 15px;">
                <button id="submit-bug" style="
                    flex: 1;
                    padding: 15px;
                    background: linear-gradient(135deg, #00ff88 0%, #00ffff 100%);
                    color: #000;
                    border: none;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 16px;
                    cursor: pointer;
                    transition: transform 0.2s;
                ">Submit Bug Report</button>
                <button id="cancel-bug" style="
                    flex: 1;
                    padding: 15px;
                    background: #444;
                    color: #fff;
                    border: none;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 16px;
                    cursor: pointer;
                    transition: transform 0.2s;
                ">Cancel</button>
            </div>

            <div id="bug-success" style="display: none; margin-top: 20px; padding: 15px; background: rgba(0, 255, 136, 0.2); border: 2px solid #00ff88; border-radius: 10px; color: #00ff88; text-align: center; font-weight: 600;">
                ✅ Bug reported successfully! Thank you!
            </div>
        </div>
    `;

    // Create easy edit modal
    const editModal = document.createElement('div');
    editModal.id = 'easy-edit-modal';
    editModal.style.cssText = modal.style.cssText;

    editModal.innerHTML = `
        <div style="
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            padding: 40px;
            border-radius: 20px;
            max-width: 700px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            max-height: 90vh;
            overflow-y: auto;
        ">
            <h2 style="color: #fff; margin-bottom: 20px; font-size: 28px;">✏️ Easy Edit Mode</h2>
            <p style="color: #aaa; margin-bottom: 25px; font-size: 16px;">
                Want to change something? Here's how:
            </p>

            <div style="background: rgba(79, 172, 254, 0.1); border-left: 4px solid #4facfe; padding: 20px; margin-bottom: 20px; border-radius: 10px;">
                <h3 style="color: #4facfe; margin-bottom: 15px;">📋 Quick Start Guide</h3>
                <ol style="color: #fff; line-height: 2; padding-left: 20px;">
                    <li>Right-click anywhere on the page</li>
                    <li>Select "Inspect" or "Inspect Element"</li>
                    <li>Find the text/element you want to change</li>
                    <li>Double-click the text to edit it</li>
                    <li>Press Enter to save</li>
                </ol>
            </div>

            <div style="background: rgba(0, 255, 136, 0.1); border-left: 4px solid #00ff88; padding: 20px; margin-bottom: 20px; border-radius: 10px;">
                <h3 style="color: #00ff88; margin-bottom: 15px;">💡 Pro Tips</h3>
                <ul style="color: #fff; line-height: 2; padding-left: 20px;">
                    <li><strong>Find text fast:</strong> Press Ctrl+F in the inspector</li>
                    <li><strong>Edit colors:</strong> Click any color square to pick a new color</li>
                    <li><strong>Move things:</strong> Drag elements in the HTML tree</li>
                    <li><strong>Hide stuff:</strong> Right-click → Delete Node</li>
                </ul>
            </div>

            <div style="background: rgba(255, 107, 107, 0.1); border-left: 4px solid #ff6b6b; padding: 20px; margin-bottom: 25px; border-radius: 10px;">
                <h3 style="color: #ff6b6b; margin-bottom: 15px;">⚠️ Important</h3>
                <p style="color: #fff; line-height: 1.8;">
                    Changes in the inspector are <strong>temporary</strong> (only for you, only now).
                    To make permanent changes, report what you want changed using the Bug Reporter
                    or tell the team in Slack/Discord.
                </p>
            </div>

            <div style="text-align: center;">
                <button id="activate-inspector" style="
                    padding: 15px 30px;
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: #fff;
                    border: none;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 16px;
                    cursor: pointer;
                    margin-right: 15px;
                ">🔍 Open Inspector Now</button>
                <button id="close-edit-modal" style="
                    padding: 15px 30px;
                    background: #444;
                    color: #fff;
                    border: none;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 16px;
                    cursor: pointer;
                ">Close</button>
            </div>
        </div>
    `;

    // Add to page
    document.body.appendChild(bugButton);
    document.body.appendChild(editButton);
    document.body.appendChild(modal);
    document.body.appendChild(editModal);

    // Event handlers
    bugButton.onclick = () => {
        modal.style.display = 'flex';
        document.getElementById('bug-success').style.display = 'none';
    };

    editButton.onclick = () => {
        editModal.style.display = 'flex';
    };

    document.getElementById('cancel-bug').onclick = () => {
        modal.style.display = 'none';
    };

    document.getElementById('close-edit-modal').onclick = () => {
        editModal.style.display = 'none';
    };

    document.getElementById('activate-inspector').onclick = () => {
        // Try to open dev tools programmatically (works in some browsers)
        console.log('%c🔍 INSPECTOR MODE ACTIVATED', 'font-size: 20px; color: #4facfe; font-weight: bold;');
        console.log('%cRight-click anywhere and select "Inspect" to start editing!', 'font-size: 14px; color: #00ff88;');
        alert('Inspector tips shown in console! Press F12 or right-click → Inspect to start editing.');
    };

    document.getElementById('submit-bug').onclick = async () => {
        const title = document.getElementById('bug-title').value;
        const description = document.getElementById('bug-description').value;
        const reporterName = document.getElementById('bug-reporter-name').value || 'Anonymous';

        if (!title || !description) {
            alert('Please fill in both the title and description!');
            return;
        }

        // Get current page info
        const pageUrl = window.location.href;
        const pageName = document.title || window.location.pathname;

        // Submit to GitHub (using existing bug system)
        try {
            const response = await fetch('/.netlify/functions/create-github-issue', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: `[${reporterName}] ${title}`,
                    body: `**Reporter:** ${reporterName}\n**Page:** ${pageName}\n**URL:** ${pageUrl}\n\n**Description:**\n${description}\n\n**Browser:** ${navigator.userAgent}`,
                    labels: ['bug', 'user-reported']
                })
            });

            if (response.ok) {
                document.getElementById('bug-success').style.display = 'block';
                document.getElementById('bug-title').value = '';
                document.getElementById('bug-description').value = '';
                document.getElementById('bug-reporter-name').value = '';

                setTimeout(() => {
                    modal.style.display = 'none';
                }, 2000);
            } else {
                alert('Error submitting bug. Please try again or contact support.');
            }
        } catch (error) {
            console.error('Bug report error:', error);
            alert('Error submitting bug. Please contact support directly.');
        }
    };

    // Click outside to close
    modal.onclick = (e) => {
        if (e.target === modal) modal.style.display = 'none';
    };

    editModal.onclick = (e) => {
        if (e.target === editModal) editModal.style.display = 'none';
    };

    // Log successful load
    console.log('%c🌀 Universal Bug Reporter & Easy Edit LOADED', 'font-size: 16px; color: #00ff88; font-weight: bold;');
    console.log('%cBug reporter button added to bottom-right corner', 'color: #4facfe;');
    console.log('%cEasy edit button added for non-technical users', 'color: #4facfe;');
})();
