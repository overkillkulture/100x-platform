/**
 * DATA-SAFE UPGRADE SCRIPT
 * Adds new UI elements WITHOUT touching existing localStorage
 * Drop this script into police-accountability.html to upgrade the UI
 */

(function() {
    'use strict';

    console.log('🔄 Police Accountability Upgrade v2.0 Loading...');

    // Step 1: Check for existing data
    function checkExistingData() {
        const transcript = localStorage.getItem('policeAccountabilityTranscript');
        const caseData = localStorage.getItem('policeAccountabilityCase');
        const account = localStorage.getItem('accountabilityAccount');

        const hasData = transcript || caseData || account;

        if (hasData) {
            console.log('✅ Existing data found! Preserving...');
            showDataPreservedBanner();

            // Create backup just in case
            createBackup({ transcript, caseData, account });
        }

        return hasData;
    }

    // Step 2: Create automatic backup
    function createBackup(data) {
        const backup = {
            timestamp: Date.now(),
            data: data,
            version: 'v1_backup'
        };

        const backupKey = `accountabilityBackup_${Date.now()}`;
        localStorage.setItem(backupKey, JSON.stringify(backup));

        console.log(`✅ Backup created: ${backupKey}`);

        // Keep only last 3 backups
        cleanOldBackups();
    }

    // Step 3: Clean old backups (keep last 3)
    function cleanOldBackups() {
        const backups = Object.keys(localStorage)
            .filter(key => key.startsWith('accountabilityBackup_'))
            .sort()
            .reverse();

        // Remove backups older than the 3 most recent
        backups.slice(3).forEach(key => {
            localStorage.removeItem(key);
            console.log(`🗑️  Removed old backup: ${key}`);
        });
    }

    // Step 4: Show "Data Preserved" banner
    function showDataPreservedBanner() {
        // Check if already dismissed
        if (localStorage.getItem('upgradeBannerDismissed') === 'true') {
            return;
        }

        const banner = document.createElement('div');
        banner.id = 'upgradeBanner';
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #00ff00, #00aa00);
            color: #000;
            padding: 1rem 2rem;
            text-align: center;
            font-weight: 700;
            z-index: 99999;
            box-shadow: 0 4px 20px rgba(0,255,0,0.3);
            animation: slideDown 0.5s ease;
        `;

        banner.innerHTML = `
            <div style="max-width: 800px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
                <div style="flex: 1;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.25rem;">
                        ✅ Your Data is Safe!
                    </div>
                    <div style="font-size: 0.9rem; font-weight: 400;">
                        We've upgraded the system. All your case information has been preserved.
                    </div>
                </div>
                <button onclick="dismissUpgradeBanner()" style="
                    background: rgba(0,0,0,0.2);
                    border: 2px solid #000;
                    padding: 0.5rem 1.5rem;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: 700;
                    color: #000;
                ">Got It!</button>
            </div>
        `;

        document.body.prepend(banner);

        // Add slide down animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideDown {
                from {
                    transform: translateY(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);

        // Global function to dismiss banner
        window.dismissUpgradeBanner = function() {
            document.getElementById('upgradeBanner').style.animation = 'slideUp 0.3s ease';
            setTimeout(() => {
                document.getElementById('upgradeBanner').remove();
            }, 300);
            localStorage.setItem('upgradeBannerDismissed', 'true');
        };
    }

    // Step 5: Add professional styling updates
    function applyVisualUpgrades() {
        // Add modern CSS enhancements without breaking existing styles
        const upgradeStyles = document.createElement('style');
        upgradeStyles.textContent = `
            /* Professional UI Enhancements - V2 */
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%) !important;
            }

            .header h1 {
                background: linear-gradient(135deg, #ff4444, #ff6666);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5rem !important;
            }

            .section {
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
            }

            .section:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.4);
            }

            .record-button {
                box-shadow: 0 8px 30px rgba(255,68,68,0.5);
            }

            .form-group input:focus,
            .form-group textarea:focus,
            .form-group select:focus {
                border-color: rgba(0,255,255,0.5);
                box-shadow: 0 0 0 3px rgba(0,255,255,0.1);
            }

            /* Add smooth transitions */
            .form-group input,
            .form-group textarea,
            .form-group select,
            .section,
            .record-button {
                transition: all 0.3s ease !important;
            }

            /* Professional scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
            }

            ::-webkit-scrollbar-track {
                background: rgba(255,255,255,0.05);
            }

            ::-webkit-scrollbar-thumb {
                background: rgba(0,255,255,0.3);
                border-radius: 5px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: rgba(0,255,255,0.5);
            }
        `;

        document.head.appendChild(upgradeStyles);
        console.log('✨ Visual upgrades applied');
    }

    // Step 6: Add version indicator
    function addVersionIndicator() {
        const indicator = document.createElement('div');
        indicator.style.cssText = `
            position: fixed;
            bottom: 1rem;
            right: 1rem;
            background: rgba(0,255,255,0.1);
            border: 1px solid rgba(0,255,255,0.3);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.75rem;
            color: #00ffff;
            z-index: 9999;
        `;
        indicator.textContent = '⚡ System v2.0';
        document.body.appendChild(indicator);
    }

    // Step 7: Initialize upgrade
    function initialize() {
        console.log('🚀 Initializing upgrade...');

        // Check and preserve data
        const hasExistingData = checkExistingData();

        // Apply visual upgrades
        applyVisualUpgrades();

        // Add version indicator
        addVersionIndicator();

        console.log('✅ Upgrade complete! Data preserved:', hasExistingData);
    }

    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

})();
