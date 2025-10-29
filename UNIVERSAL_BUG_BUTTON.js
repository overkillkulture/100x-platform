// UNIVERSAL BUG BUTTON - Add to every page
(function() {
    // Create floating bug report button
    const bugBtn = document.createElement('div');
    bugBtn.innerHTML = '🐛 Report Bug';
    bugBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #f00;
        color: #fff;
        padding: 15px 25px;
        border-radius: 50px;
        cursor: pointer;
        z-index: 999999;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(255,0,0,0.5);
        transition: transform 0.2s;
    `;

    bugBtn.onmouseover = () => bugBtn.style.transform = 'scale(1.1)';
    bugBtn.onmouseout = () => bugBtn.style.transform = 'scale(1)';

    // Create popup modal
    const modal = document.createElement('div');
    modal.style.cssText = `
        display: none;
        position: fixed;
        bottom: 80px;
        right: 20px;
        background: #1a1a1a;
        border: 2px solid #f00;
        border-radius: 10px;
        padding: 20px;
        z-index: 1000000;
        max-width: 400px;
        box-shadow: 0 8px 32px rgba(255,0,0,0.3);
    `;

    modal.innerHTML = `
        <div style="color: #fff; font-family: monospace;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #f00;">🐛 Report Bug</h3>
                <button id="closeBugModal" style="background: none; border: none; color: #f00; font-size: 24px; cursor: pointer;">×</button>
            </div>
            <textarea id="bugDescription" placeholder="Describe the bug..." style="width: 100%; height: 100px; background: #000; color: #0f0; border: 1px solid #0f0; padding: 10px; font-family: monospace; resize: vertical;"></textarea>
            <button id="submitBug" style="width: 100%; margin-top: 10px; padding: 10px; background: #f00; color: #fff; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Submit Bug</button>
            <div id="bugStatus" style="margin-top: 10px; color: #0f0; text-align: center; font-size: 12px;"></div>
        </div>
    `;

    document.body.appendChild(modal);

    // Toggle modal
    bugBtn.onclick = () => {
        modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
    };

    // Close button
    document.getElementById('closeBugModal').onclick = () => {
        modal.style.display = 'none';
    };

    // Submit bug
    document.getElementById('submitBug').onclick = async () => {
        const description = document.getElementById('bugDescription').value;
        const status = document.getElementById('bugStatus');

        if (!description.trim()) {
            status.style.color = '#f00';
            status.textContent = 'Please describe the bug';
            return;
        }

        status.style.color = '#ff0';
        status.textContent = 'Submitting...';

        try {
            const response = await fetch('/.netlify/functions/web-bug-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: description.substring(0, 50) + (description.length > 50 ? '...' : ''),
                    description: description,
                    reporter: 'Web User',
                    url: window.location.href
                })
            });

            if (response.ok) {
                status.style.color = '#0f0';
                status.textContent = '✅ Bug reported! Thank you!';
                document.getElementById('bugDescription').value = '';
                setTimeout(() => {
                    modal.style.display = 'none';
                    status.textContent = '';
                }, 2000);
            } else {
                throw new Error('Failed to submit');
            }
        } catch (error) {
            status.style.color = '#f00';
            status.textContent = '❌ Error. Text instead: (509) 216-6552';
        }
    };

    document.body.appendChild(bugBtn);

    console.log('🐛 Universal bug reporter button added!');
})();
