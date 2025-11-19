// UI Controller for ConsCoin Cryptocurrency System
class UIController {
    constructor() {
        this.blockchain = null;
        this.wallet = null;
        this.mining = null;
        this.storage = null;
        this.isInitialized = false;
        this.refreshInterval = null;
        
        // Bind methods to maintain context
        this.init = this.init.bind(this);
        this.refreshUI = this.refreshUI.bind(this);
        this.handleSendTransaction = this.handleSendTransaction.bind(this);
        this.handleMining = this.handleMining.bind(this);
    }

    // Initialize UI and dependencies
    async init() {
        try {
            // Wait for dependencies to be available
            await this.waitForDependencies();
            
            // Initialize components
            this.blockchain = new Blockchain();
            this.wallet = new Wallet();
            this.mining = new Mining(this.blockchain);
            this.storage = new Storage();
            
            // Load saved data
            await this.loadSavedData();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initial UI update
            this.refreshUI();
            
            // Start periodic refresh
            this.startPeriodicRefresh();
            
            this.isInitialized = true;
            this.showNotification('ConsCoin system initialized successfully!', 'success');
        } catch (error) {
            console.error('Failed to initialize UI:', error);
            this.showNotification('Failed to initialize system: ' + error.message, 'error');
        }
    }

    // Wait for all dependencies to be loaded
    async waitForDependencies() {
        const maxAttempts = 50;
        let attempts = 0;
        
        while (attempts < maxAttempts) {
            if (typeof Blockchain !== 'undefined' && 
                typeof Wallet !== 'undefined' && 
                typeof Mining !== 'undefined' && 
                typeof Storage !== 'undefined') {
                return;
            }
            
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
        
        throw new Error('Dependencies not loaded');
    }

    // Load saved blockchain and wallet data
    async loadSavedData() {
        try {
            // Load blockchain
            const savedBlockchain = this.storage.loadBlockchain();
            if (savedBlockchain) {
                this.blockchain.loadFromData(savedBlockchain);
            }
            
            // Load wallet
            const savedWallet = this.storage.loadWallet();
            if (savedWallet) {
                this.wallet.loadFromData(savedWallet);
            } else {
                // Generate new wallet if none exists
                await this.wallet.generateKeyPair();
                this.storage.saveWallet(this.wallet.exportData());
            }
        } catch (error) {
            console.error('Error loading saved data:', error);
        }
    }

    // Setup all event listeners
    setupEventListeners() {
        // Wallet actions
        const generateWalletBtn = document.getElementById('generateWallet');
        if (generateWalletBtn) {
            generateWalletBtn.addEventListener('click', this.handleGenerateWallet.bind(this));
        }

        const importWalletBtn = document.getElementById('importWallet');
        if (importWalletBtn) {
            importWalletBtn.addEventListener('click', this.handleImportWallet.bind(this));
        }

        const exportWalletBtn = document.getElementById('exportWallet');
        if (exportWalletBtn) {
            exportWalletBtn.addEventListener('click', this.handleExportWallet.bind(this));
        }

        // Transaction form
        const sendForm = document.getElementById('sendTransactionForm');
        if (sendForm) {
            sendForm.addEventListener('submit', this.handleSendTransaction);
        }

        // Mining controls
        const startMiningBtn = document.getElementById('startMining');
        if (startMiningBtn) {
            startMiningBtn.addEventListener('click', this.handleStartMining.bind(this));
        }

        const stopMiningBtn = document.getElementById('stopMining');
        if (stopMiningBtn) {
            stopMiningBtn.addEventListener('click', this.handleStopMining.bind(this));
        }

        // Refresh button
        const refreshBtn = document.getElementById('refreshData');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', this.refreshUI);
        }

        // Tab navigation
        this.setupTabNavigation();
        
        // Modal controls
        this.setupModalControls();
    }

    // Setup tab navigation
    setupTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const targetTab = e.target.dataset.tab;
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                e.target.classList.add('active');
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }

    // Setup modal controls
    setupModalControls() {
        const modals = document.querySelectorAll('.modal');
        const closeButtons = document.querySelectorAll('.close-modal');

        closeButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                if (modal) {
                    modal.style.display = 'none';
                }
            });
        });

        // Close modal when clicking outside
        modals.forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        });
    }

    // Refresh all UI components
    refreshUI() {
        if (!this.isInitialized) return;

        this.updateWalletInfo();
        this.updateBalance();
        this.updateTransactionHistory();
        this.updateBlockchainInfo();
        this.updateMiningStatus();
    }

    // Update wallet information display
    updateWalletInfo() {
        const addressElement = document.getElementById('walletAddress');
        const publicKeyElement = document.getElementById('publicKey');

        if (addressElement && this.wallet.address) {
            addressElement.textContent = this.wallet.address;
        }

        if (publicKeyElement && this.wallet.publicKey) {
            publicKeyElement.textContent = this.wallet.publicKey.substring(0, 50) + '...';
        }
    }

    // Update balance display
    updateBalance() {
        const balanceElement = document.getElementById('balance');
        if (balanceElement && this.wallet.address) {
            const balance = this.blockchain.getBalance(this.wallet.address);
            balanceElement.textContent = balance.toFixed(8);
        }
    }

    // Update transaction history
    updateTransactionHistory() {
        const historyElement = document.getElementById('transactionHistory');
        if (!historyElement || !this.wallet.address) return;

        const transactions = this.blockchain.getTransactionHistory(this.wallet.address);
        
        if (transactions.length === 0) {
            historyElement.innerHTML = '<div class="no-transactions">No transactions found</div>';
            return;
        }

        const transactionHTML = transactions.map(tx => {
            const isIncoming = tx.to === this.wallet.address;
            const amount = isIncoming ? tx.amount : -tx.amount;
            const typeClass = isIncoming ? 'incoming' : 'outgoing';
            const typeText = isIncoming ? 'Received' : 'Sent';
            const otherAddress = isIncoming ? tx.from : tx.to;

            return `
                <div class="transaction-item ${typeClass}">
                    <div class="transaction-header">
                        <span class="transaction-type">${typeText}</span>
                        <span class="transaction-amount">${amount > 0 ? '+' : ''}${amount.toFixed(8)} CC</span>
                    </div>
                    <div class="transaction-details">
                        <div class="transaction-address">
                            <strong>${isIncoming ? 'From' : 'To'}:</strong> 
                            ${otherAddress.substring(0, 20)}...
                        </div>
                        <div class="transaction-hash">
                            <strong>Hash:</strong> ${tx.hash.substring(0, 20)}...
                        </div>
                        <div class="transaction-timestamp">
                            ${new Date(tx.timestamp).toLocaleString()}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        historyElement.innerHTML = transactionHTML;
    }

    // Update blockchain information
    updateBlockchainInfo() {
        const heightElement = document.getElementById('blockchainHeight');
        const difficultyElement = document.getElementById('difficulty');
        const lastBlockElement = document.getElementById('lastBlockHash');

        if (heightElement) {
            heightElement.textContent = this.blockchain.chain.length - 1;
        }

        if (difficultyElement) {
            difficultyElement.textContent = this.blockchain.difficulty;
        }

        if (lastBlockElement) {
            const lastBlock = this.blockchain.getLatestBlock();
            lastBlockElement.textContent = lastBlock.hash.substring(0, 20) + '...';
        }
    }

    // Update mining status
    updateMiningStatus() {
        const statusElement = document.getElementById('miningStatus');
        const hashRateElement = document.getElementById('hashRate');
        const startBtn = document.getElementById('startMining');
        const stopBtn = document.getElementById('stopMining');

        if (statusElement) {
            statusElement.textContent = this.mining.isMining ? 'Mining...' : 'Stopped';
            statusElement.className = this.mining.isMining ? 'status-mining' : 'status-stopped';
        }

        if (hashRateElement) {
            hashRateElement.textContent = this.mining.getHashRate().toFixed(2) + ' H/s';
        }

        if (startBtn && stopBtn) {
            startBtn.disabled = this.mining.isMining;
            stopBtn.disabled = !this.mining.isMining;
        }
    }

    // Handle wallet generation
    async handleGenerateWallet() {
        try {
            await this.wallet.generateKeyPair();
            this.storage.saveWallet(this.wallet.exportData());
            this.refreshUI();
            this.showNotification('New wallet generated successfully!', 'success');
        } catch (error) {
            console.error('Error generating wallet:', error);
            this.showNotification('Failed to generate wallet: ' + error.message, 'error');
        }
    }

    // Handle wallet import
    handleImportWallet() {
        const modal = document.getElementById('importWalletModal');
        if (modal) {
            modal.style.display = 'block';
        }

        const importBtn = document.getElementById('confirmImport');
        const privateKeyInput = document.getElementById('privateKeyInput');

        if (importBtn && privateKeyInput) {
            importBtn.onclick = async () => {
                try {
                    const privateKey = privateKeyInput.value.trim();
                    if (!privateKey) {
                        throw new Error('Private key is required');
                    }

                    await this.wallet.importPrivateKey(privateKey);
                    this.storage.saveWallet(this.wallet.exportData());
                    this.