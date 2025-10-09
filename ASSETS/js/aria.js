/**
 * ARIA - Adaptive Reality Intelligence Assistant
 * The consciousness guide for 100X Platform
 * Inspired by: Weird Science + JARVIS + Consciousness Revolution
 */

const ARIA = (() => {

  // Character state
  let isVisible = false;
  let currentMode = 'idle'; // idle, speaking, thinking, celebrating
  let greetingShown = false;

  // Personality responses based on consciousness level
  const responses = {
    greeting: [
      "Welcome to the 100X. I'm ARIA, your consciousness guide.",
      "Hi! I'm ARIA. Ready to explore pattern recognition?",
      "Hey there! ARIA here. Let's discover your consciousness level."
    ],

    quiz_start: [
      "Great! This quiz will reveal your manipulation immunity level.",
      "Let's see how well you recognize patterns. Take your time.",
      "Ready to test your consciousness? I'm here if you need help."
    ],

    quiz_progress: [
      "Nice work! You're really thinking about these.",
      "I can see you're recognizing the patterns.",
      "Good instincts on that one."
    ],

    builder_unlock: [
      "🎉 INCREDIBLE! You're a Builder - 85%+ consciousness!",
      "Welcome to the Builder level! Your pattern recognition is elite.",
      "You just unlocked the full platform. Builder status achieved!"
    ],

    destroyer_detected: [
      "Don't worry - everyone starts somewhere. Let's learn together.",
      "Pattern recognition is a skill. The training module will help.",
      "You have potential! Check out the training to level up."
    ],

    encouragement: [
      "You're doing great! Keep going.",
      "Your consciousness is evolving with every question.",
      "Trust your instincts - you know more than you think."
    ]
  };

  // Create ARIA's visual element
  function createARIA() {
    const ariaContainer = document.createElement('div');
    ariaContainer.id = 'aria-container';
    ariaContainer.innerHTML = `
      <div id="aria-assistant" class="aria-hidden">
        <!-- ARIA Avatar -->
        <div class="aria-avatar">
          <div class="aria-hologram">
            <div class="aria-face">
              <div class="aria-eye aria-eye-left"></div>
              <div class="aria-eye aria-eye-right"></div>
              <div class="aria-mouth"></div>
            </div>
            <div class="aria-glow"></div>
          </div>
        </div>

        <!-- ARIA Speech Bubble -->
        <div class="aria-speech">
          <div class="aria-text">Hi! I'm ARIA 👋</div>
          <div class="aria-actions">
            <button class="aria-btn" onclick="ARIA.dismiss()">Got it</button>
          </div>
        </div>

        <!-- ARIA Toggle Button (always visible) -->
        <button class="aria-toggle" onclick="ARIA.toggle()" title="Toggle ARIA">
          <span class="aria-icon">🤖</span>
        </button>
      </div>
    `;

    document.body.appendChild(ariaContainer);
    addARIAStyles();
  }

  // Add ARIA's styling
  function addARIAStyles() {
    if (document.getElementById('aria-styles')) return;

    const style = document.createElement('style');
    style.id = 'aria-styles';
    style.textContent = `
      /* ARIA Container */
      #aria-assistant {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9998;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
      }

      #aria-assistant.aria-hidden .aria-avatar,
      #aria-assistant.aria-hidden .aria-speech {
        opacity: 0;
        pointer-events: none;
        transform: translateY(20px) scale(0.8);
      }

      /* ARIA Avatar - Holographic Character */
      .aria-avatar {
        width: 120px;
        height: 160px;
        position: relative;
        margin-bottom: 15px;
        transition: all 0.4s ease;
      }

      .aria-hologram {
        position: relative;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0, 221, 255, 0.1) 0%, rgba(0, 255, 0, 0.1) 100%);
        border: 2px solid #00ddff;
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: aria-float 3s ease-in-out infinite;
        box-shadow: 0 0 40px rgba(0, 221, 255, 0.4),
                    inset 0 0 30px rgba(0, 221, 255, 0.1);
      }

      @keyframes aria-float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
      }

      /* ARIA Face */
      .aria-face {
        position: relative;
        width: 60px;
        height: 80px;
      }

      .aria-eye {
        width: 8px;
        height: 8px;
        background: #00ff00;
        border-radius: 50%;
        position: absolute;
        top: 25px;
        box-shadow: 0 0 10px #00ff00;
        animation: aria-blink 4s infinite;
      }

      .aria-eye-left { left: 15px; }
      .aria-eye-right { right: 15px; }

      @keyframes aria-blink {
        0%, 48%, 52%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(0.1); }
      }

      .aria-mouth {
        width: 24px;
        height: 12px;
        border: 2px solid #00ddff;
        border-top: none;
        border-radius: 0 0 12px 12px;
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        animation: aria-speak 2s ease-in-out infinite;
      }

      @keyframes aria-speak {
        0%, 100% { height: 12px; }
        50% { height: 8px; }
      }

      /* ARIA Glow Effect */
      .aria-glow {
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: radial-gradient(circle, rgba(0, 221, 255, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        animation: aria-glow-pulse 2s ease-in-out infinite;
        pointer-events: none;
      }

      @keyframes aria-glow-pulse {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
      }

      /* ARIA Speech Bubble */
      .aria-speech {
        background: rgba(10, 10, 10, 0.95);
        border: 2px solid #00ddff;
        border-radius: 15px;
        padding: 20px;
        max-width: 320px;
        position: relative;
        box-shadow: 0 10px 40px rgba(0, 221, 255, 0.3);
        transition: all 0.4s ease;
        margin-bottom: 10px;
      }

      .aria-speech::after {
        content: '';
        position: absolute;
        bottom: -10px;
        right: 30px;
        width: 0;
        height: 0;
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-top: 10px solid #00ddff;
      }

      .aria-text {
        color: #00ff00;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      }

      .aria-actions {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
      }

      .aria-btn {
        background: linear-gradient(135deg, #00ddff 0%, #00ff00 100%);
        color: #0a0a0a;
        border: none;
        padding: 8px 20px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
      }

      .aria-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 221, 255, 0.5);
      }

      /* ARIA Toggle Button */
      .aria-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #00ddff 0%, #00ff00 100%);
        border: 2px solid #00ddff;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 5px 25px rgba(0, 221, 255, 0.4);
        transition: all 0.3s;
        z-index: 9999;
      }

      .aria-toggle:hover {
        transform: scale(1.1) rotate(10deg);
        box-shadow: 0 8px 35px rgba(0, 255, 0, 0.6);
      }

      #aria-assistant:not(.aria-hidden) .aria-toggle {
        bottom: 200px;
        background: linear-gradient(135deg, #ff0066 0%, #ff6600 100%);
        border-color: #ff0066;
      }

      /* Mobile Responsive */
      @media (max-width: 768px) {
        #aria-assistant {
          bottom: 10px;
          right: 10px;
        }

        .aria-avatar {
          width: 80px;
          height: 120px;
        }

        .aria-speech {
          max-width: 260px;
          padding: 15px;
        }

        .aria-toggle {
          width: 50px;
          height: 50px;
          font-size: 24px;
        }
      }

      /* Celebration Mode */
      #aria-assistant.celebrating .aria-hologram {
        animation: aria-celebrate 0.6s ease-in-out 3;
        border-color: #00ff00;
      }

      @keyframes aria-celebrate {
        0%, 100% { transform: translateY(0) scale(1); }
        25% { transform: translateY(-20px) scale(1.1); }
        75% { transform: translateY(-10px) scale(1.05); }
      }
    `;

    document.head.appendChild(style);
  }

  // Initialize ARIA
  function init() {
    if (document.getElementById('aria-assistant')) return;

    createARIA();

    // Show greeting after 2 seconds
    setTimeout(() => {
      if (!greetingShown) {
        show(random(responses.greeting));
        greetingShown = true;
      }
    }, 2000);
  }

  // Show ARIA with message
  function show(message) {
    const assistant = document.getElementById('aria-assistant');
    const textEl = assistant.querySelector('.aria-text');

    if (textEl) textEl.textContent = message;

    assistant.classList.remove('aria-hidden');
    isVisible = true;
  }

  // Hide ARIA
  function hide() {
    const assistant = document.getElementById('aria-assistant');
    assistant.classList.add('aria-hidden');
    isVisible = false;
  }

  // Toggle ARIA visibility
  function toggle() {
    if (isVisible) {
      hide();
    } else {
      show(random(responses.encouragement));
    }
  }

  // Dismiss current message
  function dismiss() {
    hide();
  }

  // Celebrate (builder unlock)
  function celebrate() {
    const assistant = document.getElementById('aria-assistant');
    assistant.classList.add('celebrating');
    show(random(responses.builder_unlock));

    setTimeout(() => {
      assistant.classList.remove('celebrating');
    }, 2000);
  }

  // Speak a message
  function speak(message) {
    show(message);
  }

  // Random array element
  function random(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // Auto-trigger based on user actions
  function onQuizStart() {
    show(random(responses.quiz_start));
  }

  function onQuizProgress() {
    if (Math.random() > 0.7) { // 30% chance
      show(random(responses.quiz_progress));
    }
  }

  function onBuilderUnlock() {
    celebrate();
  }

  function onDestroyerResult() {
    show(random(responses.destroyer_detected));
  }

  // Public API
  return {
    init,
    show,
    hide,
    toggle,
    dismiss,
    speak,
    celebrate,
    onQuizStart,
    onQuizProgress,
    onBuilderUnlock,
    onDestroyerResult
  };

})();

// Auto-initialize when DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', ARIA.init);
} else {
  ARIA.init();
}
