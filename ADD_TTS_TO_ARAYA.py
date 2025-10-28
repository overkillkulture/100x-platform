"""
Add Text-to-Speech to Araya chat so she can talk back
"""

file_path = r'C:\Users\dwrek\100X_DEPLOYMENT\araya-chat.html'

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the sendMessage function and add TTS
# We'll add a speaker button and auto-speak feature

# Add TTS button HTML (after the message input)
old_input = '''<input type="text" id="messageInput" placeholder="Type your message...">
                    <button onclick="sendMessage()">Send</button>'''

new_input = '''<input type="text" id="messageInput" placeholder="Type your message or click mic...">
                    <button onclick="sendMessage()">Send</button>
                    <button onclick="toggleAutoSpeak()" id="tts-btn" style="background: #9f3; color: #000;">🔊 Speak: ON</button>
                    <button onclick="startVoiceInput()" style="background: #f0f; color: #fff;">🎤 Voice</button>'''

if old_input in content:
    content = content.replace(old_input, new_input)

# Add TTS JavaScript functionality
# Find the closing script tag and add before it
old_script_end = '''    </script>
</body>'''

new_script_end = '''        // TEXT-TO-SPEECH FUNCTIONALITY
        let autoSpeak = true;
        let speechSynthesis = window.speechSynthesis;

        function toggleAutoSpeak() {
            autoSpeak = !autoSpeak;
            const btn = document.getElementById('tts-btn');
            if (autoSpeak) {
                btn.textContent = '🔊 Speak: ON';
                btn.style.background = '#9f3';
            } else {
                btn.textContent = '🔇 Speak: OFF';
                btn.style.background = '#666';
            }
        }

        function speakText(text) {
            if (!autoSpeak) return;

            // Cancel any ongoing speech
            speechSynthesis.cancel();

            // Create utterance
            const utterance = new SpeechSynthesisUtterance(text);

            // Configure voice (female, slower pace)
            utterance.pitch = 1.2;
            utterance.rate = 0.9;
            utterance.volume = 1.0;

            // Try to use a female voice
            const voices = speechSynthesis.getVoices();
            const femaleVoice = voices.find(v => v.name.includes('Female') || v.name.includes('Zira') || v.name.includes('Samantha'));
            if (femaleVoice) {
                utterance.voice = femaleVoice;
            }

            speechSynthesis.speak(utterance);
        }

        // VOICE INPUT FUNCTIONALITY
        function startVoiceInput() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('🎤 Voice input not supported. Please use Chrome, Edge, or Safari.');
                return;
            }

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();

            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            const input = document.getElementById('messageInput');
            input.placeholder = '🔴 Listening...';

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                input.value = transcript;
                input.placeholder = 'Type your message or click mic...';

                // Auto-send after voice input
                setTimeout(() => sendMessage(), 500);
            };

            recognition.onerror = function(event) {
                input.placeholder = 'Voice error - try again';
                setTimeout(() => {
                    input.placeholder = 'Type your message or click mic...';
                }, 2000);
            };

            recognition.start();
        }

        // Modify existing chat response to include TTS
        // Store original sendMessage if it exists, then enhance it
        const originalAddMessage = window.addArayaMessage || function(text) {
            const messages = document.getElementById('messages');
            if (messages) {
                const div = document.createElement('div');
                div.className = 'araya-message';
                div.textContent = text;
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
            }
        };

        window.addArayaMessage = function(text) {
            originalAddMessage(text);
            speakText(text);  // Speak Araya's response
        };

        // Load voices when available
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = function() {
                const voices = speechSynthesis.getVoices();
                console.log('Available voices:', voices.map(v => v.name));
            };
        }

    </script>
</body>'''

content = content.replace(old_script_end, new_script_end)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Text-to-Speech added to Araya chat!')
print('🔊 Araya will now speak her responses out loud')
print('🎤 Voice input button also added')
print('📍 Features:')
print('   - Auto-speak toggle (ON by default)')
print('   - Voice input button')
print('   - Female voice selection')
print('   - Auto-send after voice input')
