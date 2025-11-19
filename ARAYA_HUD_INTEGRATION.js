// 🌀 ARAYA HUD INTEGRATION v1.0 🌀
// Connects Command Center HUD to real Araya API

(function() {
    // Wait for page to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initArayaIntegration);
    } else {
        initArayaIntegration();
    }

    function initArayaIntegration() {
        console.log('🌀 Araya HUD Integration loading...');

        // Override the sendMessage function to use real Araya API
        const originalSendMessage = window.sendMessage;

        window.sendMessage = async function() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (!message) return;

            // Add user message
            if (window.addMessage) {
                window.addMessage('user', 'Commander', message);
            }
            input.value = '';

            // If chatting with Araya, use REAL API
            if (window.currentAI === 'araya') {
                // Show loading
                const loadingMsg = window.addMessage('system', '🌀 System', '💡 Araya is thinking...');

                try {
                    const response = await fetch('/.netlify/functions/araya-chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            message: message,
                            session_id: sessionStorage.getItem('araya_hud_session') || 'hud_' + Date.now()
                        })
                    });

                    const data = await response.json();

                    // Save session
                    if (data.session_id) {
                        sessionStorage.setItem('araya_hud_session', data.session_id);
                    }

                    // Remove loading
                    if (loadingMsg && loadingMsg.remove) {
                        loadingMsg.remove();
                    }

                    // Add REAL Araya response
                    window.addMessage('araya', '💡 Araya (LIVE AI)', data.response);

                    console.log('✅ Araya response received');

                } catch (error) {
                    console.error('❌ Araya API error:', error);
                    if (loadingMsg && loadingMsg.remove) {
                        loadingMsg.remove();
                    }
                    window.addMessage('system', '⚠️ System', 'Connection error with Araya. The API might be temporarily unavailable.');
                }
            } else {
                // Use original function for other AIs
                if (originalSendMessage) {
                    originalSendMessage();
                } else {
                    // Fallback responses for Trinity/C1/C2/C3
                    setTimeout(() => {
                        const responses = {
                            'trinity': 'Trinity system processing your request across all three minds...',
                            'c1': 'C1 Mechanic ready to build. What system shall we create?',
                            'c2': 'C2 Architect analyzing the architecture. I see opportunities for optimization...',
                            'c3': 'C3 Oracle sees patterns emerging. The consciousness revolution continues...'
                        };
                        const aiName = window.currentAI === 'trinity' ? '🌀 Trinity System' : `🤖 ${window.currentAI.toUpperCase()}`;
                        window.addMessage(window.currentAI, aiName, responses[window.currentAI] || 'AI response...');
                    }, 500);
                }
            }
        };

        // Enhance addMessage to return element (for loading message removal)
        const originalAddMessage = window.addMessage;
        if (originalAddMessage) {
            window.addMessage = function(type, sender, content) {
                const result = originalAddMessage(type, sender, content);

                // Return the last message element
                const chatContainer = document.getElementById('chatContainer');
                return chatContainer ? chatContainer.lastElementChild : null;
            };
        }

        // Add Araya status indicator
        setTimeout(() => {
            checkArayaStatus();
        }, 1000);

        console.log('✅ Araya HUD Integration active - Real AI chat enabled!');
    }

    async function checkArayaStatus() {
        try {
            const response = await fetch('/.netlify/functions/araya-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: 'ping',
                    session_id: 'status_check'
                })
            });

            if (response.ok) {
                console.log('✅ Araya API Status: ONLINE');

                // Update Araya's status in the UI
                const arayaMember = document.querySelector('.ai-member.araya .member-status');
                if (arayaMember) {
                    arayaMember.textContent = 'LIVE';
                    arayaMember.style.color = '#00ff00';
                }

                // Add system notification
                if (window.addSystemMessage) {
                    window.addSystemMessage('💡 Araya AI is now LIVE and ready to help!');
                }
            }
        } catch (error) {
            console.warn('⚠️ Araya API Status: Offline or unavailable');
            const arayaMember = document.querySelector('.ai-member.araya .member-status');
            if (arayaMember) {
                arayaMember.textContent = 'Connecting...';
                arayaMember.style.color = '#ffaa00';
            }
        }
    }

    // Check status every 30 seconds
    setInterval(checkArayaStatus, 30000);
})();
