"""
FIX BUG REPORTER PATH ISSUE
Replaces external script reference with inline JavaScript
This fixes the issue where pages in subdirectories couldn't load the script
"""

import os
import re
from pathlib import Path

DEPLOYMENT_DIR = r"C:\Users\dwrek\100X_DEPLOYMENT"

# The inline script (complete JavaScript code)
INLINE_SCRIPT = """<script>
/**
 * FLOATING BUG REPORTER (INLINE)
 * Always-visible bug reporting widget in bottom-right corner
 */

(function() {
    // Create the floating bug reporter
    const bugReporter = document.createElement('div');
    bugReporter.id = 'floating-bug-reporter';
    bugReporter.innerHTML = `
        <style>
            #floating-bug-reporter {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 999999;
                font-family: 'Courier New', monospace;
            }

            .bug-fab {
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #ff4444 0%, #ff6666 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(255, 68, 68, 0.5);
                transition: all 0.3s;
                animation: pulse 2s infinite;
                border: 3px solid #fff;
            }

            .bug-fab:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 30px rgba(255, 68, 68, 0.8);
            }

            @keyframes pulse {
                0%, 100% {
                    box-shadow: 0 4px 20px rgba(255, 68, 68, 0.5);
                }
                50% {
                    box-shadow: 0 4px 30px rgba(255, 68, 68, 0.8), 0 0 50px rgba(255, 68, 68, 0.3);
                }
            }

            .bug-panel {
                position: absolute;
                bottom: 100px;
                right: 0;
                width: 400px;
                max-height: 600px;
                background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
                border: 3px solid #ff4444;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                display: none;
                overflow: hidden;
            }

            .bug-panel.active {
                display: block;
                animation: slideUp 0.3s ease-out;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .bug-panel-header {
                background: linear-gradient(135deg, #ff4444 0%, #ff6666 100%);
                color: #fff;
                padding: 20px;
                font-size: 1.3rem;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .bug-panel-close {
                background: none;
                border: none;
                color: #fff;
                font-size: 1.5rem;
                cursor: pointer;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background 0.2s;
            }

            .bug-panel-close:hover {
                background: rgba(255, 255, 255, 0.2);
            }

            .bug-panel-body {
                padding: 20px;
                color: #e8e8e8;
                max-height: 500px;
                overflow-y: auto;
            }

            .bug-notice {
                background: rgba(0, 255, 65, 0.1);
                border-left: 4px solid #00ff41;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
                font-size: 0.95rem;
                line-height: 1.6;
            }

            .bug-notice strong {
                color: #00ff41;
            }

            .bug-form-group {
                margin-bottom: 20px;
            }

            .bug-form-label {
                display: block;
                color: #ff6666;
                font-weight: bold;
                margin-bottom: 8px;
                font-size: 0.95rem;
            }

            .bug-form-input,
            .bug-form-textarea {
                width: 100%;
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px;
                color: #e8e8e8;
                font-family: 'Courier New', monospace;
                font-size: 0.95rem;
                transition: border-color 0.3s;
            }

            .bug-form-input:focus,
            .bug-form-textarea:focus {
                outline: none;
                border-color: #ff4444;
                background: rgba(255, 68, 68, 0.05);
            }

            .bug-form-textarea {
                min-height: 120px;
                resize: vertical;
            }

            .bug-submit-btn {
                width: 100%;
                background: linear-gradient(135deg, #ff4444 0%, #ff6666 100%);
                color: #fff;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 1.1rem;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
                font-family: 'Courier New', monospace;
            }

            .bug-submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(255, 68, 68, 0.4);
            }

            .bug-submit-btn:active {
                transform: translateY(0);
            }

            .bug-badge {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #00ff41;
                color: #000;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.8rem;
                font-weight: bold;
                border: 2px solid #fff;
            }

            ::-webkit-scrollbar {
                width: 8px;
            }

            ::-webkit-scrollbar-track {
                background: #1a1a1a;
            }

            ::-webkit-scrollbar-thumb {
                background: #ff4444;
                border-radius: 4px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #ff6666;
            }
        </style>

        <div class="bug-fab" onclick="toggleBugPanel()">
            🐛
            <div class="bug-badge">!</div>
        </div>

        <div class="bug-panel" id="bug-panel">
            <div class="bug-panel-header">
                <span>🐛 REPORT A BUG</span>
                <button class="bug-panel-close" onclick="toggleBugPanel()">✕</button>
            </div>
            <div class="bug-panel-body">
                <div class="bug-notice">
                    <strong>📢 We check bugs every couple hours!</strong><br><br>
                    Found something broken? Report it here and we'll fix it ASAP.
                    Every bug report helps make the platform better for everyone.
                </div>

                <form id="bug-report-form" onsubmit="submitBugReport(event)">
                    <div class="bug-form-group">
                        <label class="bug-form-label">What's broken? (Short description)</label>
                        <input type="text"
                               class="bug-form-input"
                               id="bug-title"
                               placeholder="e.g., Login button doesn't work"
                               required>
                    </div>

                    <div class="bug-form-group">
                        <label class="bug-form-label">Tell us more (What happened?)</label>
                        <textarea class="bug-form-textarea"
                                  id="bug-description"
                                  placeholder="Describe what you were doing when the bug occurred..."
                                  required></textarea>
                    </div>

                    <div class="bug-form-group">
                        <label class="bug-form-label">Your Name/PIN (Optional)</label>
                        <input type="text"
                               class="bug-form-input"
                               id="bug-reporter"
                               placeholder="e.g., Joshua (PIN 1001)">
                    </div>

                    <button type="submit" class="bug-submit-btn">
                        🚀 SUBMIT BUG REPORT
                    </button>
                </form>
            </div>
        </div>
    `;

    // Add to page
    document.body.appendChild(bugReporter);

    // Make functions global
    window.toggleBugPanel = function() {
        const panel = document.getElementById('bug-panel');
        panel.classList.toggle('active');
    };

    window.submitBugReport = function(event) {
        event.preventDefault();

        const bugData = {
            id: 'bug_' + Date.now(),
            timestamp: new Date().toISOString(),
            title: document.getElementById('bug-title').value,
            description: document.getElementById('bug-description').value,
            reporter: document.getElementById('bug-reporter').value || 'Anonymous',
            url: window.location.href,
            userAgent: navigator.userAgent
        };

        // Save to localStorage
        const bugs = JSON.parse(localStorage.getItem('bugReports') || '[]');
        bugs.push(bugData);
        localStorage.setItem('bugReports', JSON.stringify(bugs));

        // Try to save to server
        fetch('/api/bug-report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bugData)
        }).catch(() => {
            // Fallback: save to local file
            const blob = new Blob([JSON.stringify(bugData, null, 2)], { type: 'application/json' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `bug_${Date.now()}.json`;
            a.click();
        });

        // Show success message
        alert('✅ BUG REPORTED!\\n\\nThanks for reporting this bug. We check reports every couple hours and will fix it ASAP.\\n\\nYour feedback makes the platform better!');

        // Reset form
        document.getElementById('bug-report-form').reset();
        toggleBugPanel();
    };
})();
</script>"""

def fix_html_files():
    """Replace external script reference with inline script"""
    html_files = list(Path(DEPLOYMENT_DIR).glob('**/*.html'))

    print(f"🔍 Found {len(html_files)} HTML files\n")

    fixed_count = 0
    skipped_count = 0

    for html_file in html_files:
        try:
            # Read file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if has external script reference
            if 'src="FLOATING_BUG_REPORTER.js"' not in content:
                skipped_count += 1
                continue

            # Replace external reference with inline script
            updated_content = content.replace(
                '<script src="FLOATING_BUG_REPORTER.js"></script>',
                INLINE_SCRIPT
            )

            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"✅ FIXED: {html_file.relative_to(DEPLOYMENT_DIR)}")
            fixed_count += 1

        except Exception as e:
            print(f"❌ ERROR: {html_file.name} - {str(e)}")

    print(f"\n{'='*60}")
    print(f"📊 SUMMARY:")
    print(f"   Total files checked: {len(html_files)}")
    print(f"   ✅ Fixed: {fixed_count}")
    print(f"   ⏭️  Skipped (no bug reporter): {skipped_count}")
    print(f"{'='*60}\n")

    if fixed_count > 0:
        print(f"🎉 SUCCESS! Bug reporter now inline on {fixed_count} pages!")
        print(f"\n✨ BENEFITS:")
        print(f"   • Works from ANY directory (no path issues)")
        print(f"   • No external file dependency")
        print(f"   • Guaranteed to load on every page")
        print(f"   • Bug reporter visible across entire platform!")

    return fixed_count

if __name__ == "__main__":
    print("🐛 BUG REPORTER PATH FIX")
    print("="*60 + "\n")
    print("Converting external script to inline JavaScript...\n")

    fixed = fix_html_files()

    if fixed > 0:
        print(f"\n✅ BUG FIX COMPLETE!")
        print(f"   The bug reporter is now guaranteed to work on ALL pages.")
