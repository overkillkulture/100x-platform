/**
 * ConsCoin Storage Management System
 * Handles local storage operations for blockchain data persistence
 */

class StorageManager {
    constructor() {
        this.storagePrefix = 'conscoin_';
        this.keys = {
            blockchain: 'blockchain',
            wallet: 'wallet',
            transactions: 'transactions',
            peers: 'peers',
            settings: 'settings',
            mining_stats: 'mining_stats'
        };
        
        // Initialize storage structure if not exists
        this.initializeStorage();
    }

    /**
     * Initialize storage with default values if empty
     */
    initializeStorage() {
        try {
            if (!this.getBlockchain()) {
                this.saveBlockchain([]);
            }
            
            if (!this.getTransactions()) {
                this.saveTransactions([]);
            }
            
            if (!this.getSettings()) {
                this.saveSettings({
                    difficulty: 4,
                    mining_reward: 50,
                    network_id: 'conscoin_local',
                    created_at: Date.now()
                });
            }
            
            if (!this.getMiningStats()) {
                this.saveMiningStats({
                    blocks_mined: 0,
                    total_hash_attempts: 0,
                    last_block_time: null,
                    average_block_time: 0
                });
            }
        } catch (error) {
            console.error('Storage initialization failed:', error);
        }
    }

    /**
     * Generic storage operations
     */
    _save(key, data) {
        try {
            const serialized = JSON.stringify(data);
            localStorage.setItem(this.storagePrefix + key, serialized);
            return true;
        } catch (error) {
            console.error(`Failed to save ${key}:`, error);
            return false;
        }
    }

    _load(key) {
        try {
            const data = localStorage.getItem(this.storagePrefix + key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error(`Failed to load ${key}:`, error);
            return null;
        }
    }

    _remove(key) {
        try {
            localStorage.removeItem(this.storagePrefix + key);
            return true;
        } catch (error) {
            console.error(`Failed to remove ${key}:`, error);
            return false;
        }
    }

    /**
     * Blockchain storage operations
     */
    saveBlockchain(blockchain) {
        return this._save(this.keys.blockchain, blockchain);
    }

    getBlockchain() {
        return this._load(this.keys.blockchain) || [];
    }

    addBlock(block) {
        const blockchain = this.getBlockchain();
        blockchain.push(block);
        return this.saveBlockchain(blockchain);
    }

    getBlock(index) {
        const blockchain = this.getBlockchain();
        return blockchain[index] || null;
    }

    getLatestBlock() {
        const blockchain = this.getBlockchain();
        return blockchain.length > 0 ? blockchain[blockchain.length - 1] : null;
    }

    getBlockchainLength() {
        return this.getBlockchain().length;
    }

    /**
     * Wallet storage operations
     */
    saveWallet(walletData) {
        return this._save(this.keys.wallet, walletData);
    }

    getWallet() {
        return this._load(this.keys.wallet);
    }

    removeWallet() {
        return this._remove(this.keys.wallet);
    }

    /**
     * Transaction storage operations
     */
    saveTransactions(transactions) {
        return this._save(this.keys.transactions, transactions);
    }

    getTransactions() {
        return this._load(this.keys.transactions) || [];
    }

    addTransaction(transaction) {
        const transactions = this.getTransactions();
        transactions.push({
            ...transaction,
            timestamp: transaction.timestamp || Date.now(),
            id: transaction.id || this.generateTransactionId()
        });
        return this.saveTransactions(transactions);
    }

    getTransactionsByAddress(address) {
        const transactions = this.getTransactions();
        return transactions.filter(tx => 
            tx.from === address || tx.to === address
        );
    }

    getTransaction(id) {
        const transactions = this.getTransactions();
        return transactions.find(tx => tx.id === id) || null;
    }

    /**
     * Settings storage operations
     */
    saveSettings(settings) {
        return this._save(this.keys.settings, settings);
    }

    getSettings() {
        return this._load(this.keys.settings);
    }

    updateSetting(key, value) {
        const settings = this.getSettings() || {};
        settings[key] = value;
        return this.saveSettings(settings);
    }

    getSetting(key, defaultValue = null) {
        const settings = this.getSettings();
        return settings && settings.hasOwnProperty(key) ? settings[key] : defaultValue;
    }

    /**
     * Mining statistics storage
     */
    saveMiningStats(stats) {
        return this._save(this.keys.mining_stats, stats);
    }

    getMiningStats() {
        return this._load(this.keys.mining_stats);
    }

    updateMiningStats(updates) {
        const stats = this.getMiningStats() || {};
        Object.assign(stats, updates);
        return this.saveMiningStats(stats);
    }

    /**
     * Peer network storage (for future P2P functionality)
     */
    savePeers(peers) {
        return this._save(this.keys.peers, peers);
    }

    getPeers() {
        return this._load(this.keys.peers) || [];
    }

    addPeer(peer) {
        const peers = this.getPeers();
        if (!peers.find(p => p.id === peer.id)) {
            peers.push({
                ...peer,
                added_at: Date.now()
            });
            return this.savePeers(peers);
        }
        return true;
    }

    removePeer(peerId) {
        const peers = this.getPeers();
        const filtered = peers.filter(p => p.id !== peerId);
        return this.savePeers(filtered);
    }

    /**
     * Utility functions
     */
    generateTransactionId() {
        return 'tx_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Data validation and integrity
     */
    validateBlockchain() {
        const blockchain = this.getBlockchain();
        
        if (!Array.isArray(blockchain)) {
            return false;
        }

        for (let i = 1; i < blockchain.length; i++) {
            const currentBlock = blockchain[i];
            const previousBlock = blockchain[i - 1];
            
            if (!currentBlock.hash || !currentBlock.previousHash) {
                return false;
            }
            
            if (currentBlock.previousHash !== previousBlock.hash) {
                return false;
            }
        }
        
        return true;
    }

    /**
     * Storage cleanup and maintenance
     */
    clearAll() {
        Object.values(this.keys).forEach(key => {
            this._remove(key);
        });
        this.initializeStorage();
        return true;
    }

    clearTransactions() {
        return this.saveTransactions([]);
    }

    clearMiningStats() {
        return this.saveMiningStats({
            blocks_mined: 0,
            total_hash_attempts: 0,
            last_block_time: null,
            average_block_time: 0
        });
    }

    /**
     * Export/Import functionality
     */
    exportData() {
        const data = {};
        Object.values(this.keys).forEach(key => {
            data[key] = this._load(key);
        });
        
        return {
            ...data,
            exported_at: Date.now(),
            version: '1.0'
        };
    }

    importData(data) {
        try {
            if (!data || typeof data !== 'object') {
                throw new Error('Invalid import data format');
            }

            Object.keys(data).forEach(key => {
                if (this.keys.hasOwnProperty(key)) {
                    this._save(key, data[key]);
                }
            });

            return true;
        } catch (error) {
            console.error('Import failed:', error);
            return false;
        }
    }

    /**
     * Storage statistics and monitoring
     */
    getStorageStats() {
        const stats = {
            blockchain_size: this.getBlockchainLength(),
            transaction_count: this.getTransactions().length,
            peer_count: this.getPeers().length,
            storage_used: 0,
            last_updated: Date.now()
        };

        // Calculate approximate storage usage
        try {
            Object.values(this.keys).forEach(key => {
                const data = localStorage.getItem(this.storagePrefix + key);
                if (data) {
                    stats.storage_used += data.length;
                }
            });
        } catch (error) {
            console.warn('Could not calculate storage usage:', error);
        }

        return stats;
    }

    /**
     * Backup functionality
     */
    createBackup() {
        const backup = {
            data: this.exportData(),
            created_at: Date.now(),
            version: '1.0'
        };

        return JSON.stringify(backup);
    }

    restoreBackup(backupString) {
        try {
            const backup = JSON.parse(backupString);
            
            if (!backup.data || !backup.version) {
                throw new Error('Invalid backup format');
            }

            return this.importData(backup.data);
        } catch (error) {
            console.error('Backup restore failed:', error);
            return false;
        }
    }

    /**
     * Storage health check
     */
    healthCheck() {
        const health = {
            storage_available: true,
            blockchain_valid: false,
            wallet_exists: false,
            settings_valid: false,
            errors: []
        };

        try {
            // Test storage availability
            const testKey = 'health_check_test';
            localStorage.setItem(testKey, 'test');
            localStorage.removeItem(testKey);
        } catch (error) {
            health.storage_available = false;
            health.errors.push('Local storage not available');
        }

        // Validate blockchain
        health.blockchain_valid = this.validateBlockchain();
        if (!health.blockchain_valid) {
            health.errors.push('Blockchain validation failed');
        }

        // Check wallet
        health.wallet_exists = this.getWallet() !== null;

        // Check settings
        const settings = this.getSettings();
        health.settings_valid = settings && typeof settings === 'object';

        return health;
    }
}

// Create and export singleton instance
const storage = new StorageManager();

// Export for both Node.js and browser environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { StorageManager, storage };
} else if (typeof window !== 'undefined') {
    window.StorageManager = StorageManager;
    window.storage = storage;
}