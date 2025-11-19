/**
 * CONSCIOUSNESS REVOLUTION - Universal Fundraising Widget
 * Embed on every page to collect donations, supporters, and investors
 */

(function() {
  'use strict';

  const FundraisingWidget = {
    config: {
      apiUrl: 'https://conciousnessrevolution.io/api',
      currentRaised: 50000,  // Update this dynamically from API
      goal: 10000000,
      donorCount: 247,
      avgDonation: 202
    },

    init: function() {
      // Inject CSS
      this.injectStyles();

      // Create floating button
      this.createFloatingButton();

      // Create modal (hidden initially)
      this.createModal();

      // Load current stats from API
      this.loadStats();
    },

    injectStyles: function() {
      const style = document.createElement('style');
      style.textContent = `
        /* Floating Donate Button */
        .consciousness-floating-btn {
          position: fixed;
          bottom: 20px;
          right: 20px;
          z-index: 9999;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 15px 25px;
          border-radius: 50px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.3);
          cursor: pointer;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-weight: bold;
          transition: all 0.3s ease;
          max-width: 200px;
        }

        .consciousness-floating-btn:hover {
          transform: translateY(-3px);
          box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }

        .consciousness-floating-btn .btn-text {
          font-size: 14px;
          margin-bottom: 5px;
        }

        .consciousness-floating-btn .progress-mini {
          font-size: 11px;
          opacity: 0.9;
        }

        /* Progress Bar (top of page) */
        .consciousness-progress-bar {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          background: rgba(0,0,0,0.9);
          padding: 10px 20px;
          z-index: 9998;
          display: flex;
          align-items: center;
          justify-content: space-between;
          box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }

        .consciousness-progress-bar .progress-fill {
          flex: 1;
          height: 8px;
          background: #333;
          border-radius: 10px;
          margin: 0 20px;
          overflow: hidden;
          position: relative;
        }

        .consciousness-progress-bar .progress-fill::after {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          height: 100%;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          transition: width 1s ease;
        }

        .consciousness-progress-bar .progress-text {
          color: white;
          font-size: 12px;
          white-space: nowrap;
        }

        .consciousness-progress-bar button {
          background: white;
          color: #667eea;
          border: none;
          padding: 8px 20px;
          border-radius: 20px;
          font-weight: bold;
          cursor: pointer;
          margin-left: 15px;
          transition: all 0.2s ease;
        }

        .consciousness-progress-bar button:hover {
          transform: scale(1.05);
        }

        /* Modal */
        .consciousness-modal {
          display: none;
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.8);
          z-index: 10000;
          align-items: center;
          justify-content: center;
        }

        .consciousness-modal.active {
          display: flex;
        }

        .consciousness-modal-content {
          background: white;
          padding: 40px;
          border-radius: 20px;
          max-width: 600px;
          width: 90%;
          max-height: 90vh;
          overflow-y: auto;
          position: relative;
        }

        .consciousness-modal-content h2 {
          color: #333;
          margin-bottom: 10px;
        }

        .consciousness-modal-content p {
          color: #666;
          margin-bottom: 30px;
        }

        .consciousness-modal-content .close-btn {
          position: absolute;
          top: 15px;
          right: 15px;
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #999;
        }

        .donation-tiers {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 15px;
          margin-bottom: 30px;
        }

        .donation-tier {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
          border-radius: 10px;
          cursor: pointer;
          text-align: center;
          transition: all 0.3s ease;
          border: none;
          font-family: inherit;
        }

        .donation-tier:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .donation-tier .amount {
          font-size: 24px;
          font-weight: bold;
          margin-bottom: 5px;
        }

        .donation-tier .label {
          font-size: 12px;
          opacity: 0.9;
        }

        .other-methods {
          display: flex;
          gap: 10px;
          justify-content: center;
          margin-top: 30px;
        }

        .other-methods a {
          padding: 10px 20px;
          background: #f0f0f0;
          color: #667eea;
          text-decoration: none;
          border-radius: 5px;
          font-size: 14px;
          transition: all 0.2s ease;
        }

        .other-methods a:hover {
          background: #667eea;
          color: white;
        }

        .stats-banner {
          background: #f9f9f9;
          padding: 20px;
          border-radius: 10px;
          margin-bottom: 20px;
          text-align: center;
        }

        .stats-banner .stat {
          display: inline-block;
          margin: 0 20px;
        }

        .stats-banner .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: #667eea;
        }

        .stats-banner .stat-label {
          font-size: 12px;
          color: #999;
        }

        @media (max-width: 768px) {
          .consciousness-progress-bar {
            flex-direction: column;
            align-items: stretch;
          }

          .consciousness-progress-bar .progress-fill {
            margin: 10px 0;
          }

          .donation-tiers {
            grid-template-columns: repeat(2, 1fr);
          }
        }
      `;
      document.head.appendChild(style);
    },

    createFloatingButton: function() {
      const button = document.createElement('div');
      button.className = 'consciousness-floating-btn';
      button.innerHTML = `
        <div class="btn-text">💰 Support the Revolution</div>
        <div class="progress-mini">$${this.formatMoney(this.config.currentRaised)} / $${this.formatMoney(this.config.goal)}</div>
      `;
      button.onclick = () => this.openModal();
      document.body.appendChild(button);
    },

    createModal: function() {
      const modal = document.createElement('div');
      modal.className = 'consciousness-modal';
      modal.id = 'consciousness-fundraising-modal';

      const percentRaised = ((this.config.currentRaised / this.config.goal) * 100).toFixed(2);

      modal.innerHTML = `
        <div class="consciousness-modal-content">
          <button class="close-btn" onclick="FundraisingWidget.closeModal()">×</button>

          <h2>🚀 Support the Consciousness Revolution</h2>
          <p>Help us build 27 AI modules that make manipulation impossible. We're creating tools that elevate human consciousness and expose corruption.</p>

          <div class="stats-banner">
            <div class="stat">
              <div class="stat-value">${this.config.donorCount}</div>
              <div class="stat-label">Supporters</div>
            </div>
            <div class="stat">
              <div class="stat-value">$${this.formatMoney(this.config.currentRaised)}</div>
              <div class="stat-label">Raised</div>
            </div>
            <div class="stat">
              <div class="stat-value">${percentRaised}%</div>
              <div class="stat-label">of $${this.formatMoney(this.config.goal)} Goal</div>
            </div>
          </div>

          <div class="donation-tiers">
            <button class="donation-tier" onclick="FundraisingWidget.donate(10, 'Believer')">
              <div class="amount">$10</div>
              <div class="label">Believer</div>
            </button>
            <button class="donation-tier" onclick="FundraisingWidget.donate(50, 'Supporter')">
              <div class="amount">$50</div>
              <div class="label">Supporter</div>
            </button>
            <button class="donation-tier" onclick="FundraisingWidget.donate(100, 'Builder')">
              <div class="amount">$100</div>
              <div class="label">Builder</div>
            </button>
            <button class="donation-tier" onclick="FundraisingWidget.donate(1000, 'Revolutionary')">
              <div class="amount">$1,000</div>
              <div class="label">Revolutionary</div>
            </button>
          </div>

          <div style="text-align: center; margin: 20px 0;">
            <button class="donation-tier" onclick="FundraisingWidget.invest()" style="width: 100%; max-width: 400px;">
              <div class="amount">$10,000+</div>
              <div class="label">💎 Investor (Get Equity)</div>
            </button>
          </div>

          <div class="other-methods">
            <a href="https://gofundme.com/consciousness-revolution" target="_blank">GoFundMe</a>
            <a href="https://patreon.com/consciousness" target="_blank">Patreon</a>
            <a href="#" onclick="FundraisingWidget.showCrypto(); return false;">Crypto</a>
          </div>

          <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #999;">
            <p>Your support builds tools that expose corruption and elevate consciousness.</p>
            <p>Thank you for believing in the mission. 🙏</p>
          </div>
        </div>
      `;

      document.body.appendChild(modal);

      // Close on background click
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          this.closeModal();
        }
      });
    },

    openModal: function() {
      const modal = document.getElementById('consciousness-fundraising-modal');
      if (modal) {
        modal.classList.add('active');
      }
    },

    closeModal: function() {
      const modal = document.getElementById('consciousness-fundraising-modal');
      if (modal) {
        modal.classList.remove('active');
      }
    },

    donate: function(amount, tier) {
      // Redirect to Stripe checkout or donation page
      const donationUrl = `${this.config.apiUrl}/donate?amount=${amount}&tier=${tier}`;
      window.location.href = donationUrl;
    },

    invest: function() {
      // Redirect to investor portal
      window.location.href = `${this.config.apiUrl}/invest`;
    },

    showCrypto: function() {
      alert(`Crypto Wallet Addresses:

Bitcoin (BTC):
bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

Ethereum (ETH):
0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

USDC:
0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb

Thank you for your support! 🙏`);
    },

    loadStats: function() {
      // TODO: Load real-time stats from API
      // fetch(`${this.config.apiUrl}/fundraising/stats`)
      //   .then(r => r.json())
      //   .then(data => {
      //     this.config.currentRaised = data.raised;
      //     this.config.donorCount = data.donors;
      //     this.updateDisplay();
      //   });
    },

    formatMoney: function(amount) {
      if (amount >= 1000000) {
        return (amount / 1000000).toFixed(1) + 'M';
      } else if (amount >= 1000) {
        return (amount / 1000).toFixed(0) + 'K';
      }
      return amount.toString();
    }
  };

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => FundraisingWidget.init());
  } else {
    FundraisingWidget.init();
  }

  // Expose globally
  window.FundraisingWidget = FundraisingWidget;

})();
