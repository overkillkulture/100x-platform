/**
 * ConsCoin Mining Interface and Worker Coordination
 * Handles mining operations, difficulty adjustment, and worker management
 */

class MiningManager {
    constructor() {
        this.isMining = false;
        this.workers = [];
        this.maxWorkers = navigator.hardwareConcurrency || 4;
        this.currentDifficulty = 4;
        this.miningStats = {
            hashesPerSecond: 0,
            totalHashes: 0,
            blocksFound: 0,
            startTime: null
        };
        this.hashRateInterval = null;
        this.onBlockFound = null;
        this.onStatsUpdate = null;
        this.pendingTransactions = [];
        this.minerAddress = null;
    }

    /**
     * Initialize mining system
     */
    async initialize(minerAddress) {
        this.minerAddress = minerAddress;
        this.loadMiningStats();
        
        // Check for Web Worker support
        if (typeof Worker === 'undefined') {
            console.warn('Web Workers not supported, using single-threaded mining');
        }
    }

    /**
     * Start mining process
     */
    async startMining(blockchain, pendingTransactions = []) {
        if (this.isMining) {
            console.log('Mining already in progress');
            return;
        }

        if (!this.minerAddress) {
            throw new Error('Miner address not set');
        }

        this.isMining = true;
        this.pendingTransactions = pendingTransactions;
        this.miningStats.startTime = Date.now();
        this.miningStats.totalHashes = 0;

        console.log(`Starting mining with ${this.maxWorkers} workers`);

        // Start hash rate monitoring
        this.startHashRateMonitoring();

        // Create mining workers
        if (typeof Worker !== 'undefined') {
            await this.startWorkerMining(blockchain);
        } else {
            await this.startSingleThreadMining(blockchain);
        }
    }

    /**
     * Stop mining process
     */
    stopMining() {
        this.isMining = false;
        
        // Terminate all workers
        this.workers.forEach(worker => {
            worker.terminate();
        });
        this.workers = [];

        // Stop hash rate monitoring
        if (this.hashRateInterval) {
            clearInterval(this.hashRateInterval);
            this.hashRateInterval = null;
        }

        this.saveMiningStats();
        console.log('Mining stopped');
    }

    /**
     * Start worker-based mining
     */
    async startWorkerMining(blockchain) {
        const lastBlock = blockchain.getLatestBlock();
        const newBlock = this.createNewBlock(lastBlock, blockchain.chain.length);

        // Divide nonce range among workers
        const nonceRange = Math.floor(0xFFFFFFFF / this.maxWorkers);

        for (let i = 0; i < this.maxWorkers; i++) {
            const worker = this.createMiningWorker(
                newBlock,
                i * nonceRange,
                (i + 1) * nonceRange,
                this.currentDifficulty
            );
            this.workers.push(worker);
        }
    }

    /**
     * Create a mining worker
     */
    createMiningWorker(block, startNonce, endNonce, difficulty) {
        // Create worker from inline code since we can't assume external files
        const workerCode = `
            // Import crypto utilities (simplified for worker)
            function sha256(message) {
                const msgBuffer = new TextEncoder().encode(message);
                return crypto.subtle.digest('SHA-256', msgBuffer).then(hashBuffer => {
                    const hashArray = Array.from(new Uint8Array(hashBuffer));
                    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
                });
            }

            async function mineBlock(block, startNonce, endNonce, difficulty) {
                const target = '0'.repeat(difficulty);
                
                for (let nonce = startNonce; nonce < endNonce; nonce++) {
                    const blockData = JSON.stringify({
                        ...block,
                        nonce: nonce
                    });
                    
                    const hash = await sha256(blockData);
                    
                    // Report progress every 1000 hashes
                    if (nonce % 1000 === 0) {
                        postMessage({
                            type: 'progress',
                            hashes: 1000,
                            nonce: nonce
                        });
                    }
                    
                    if (hash.startsWith(target)) {
                        postMessage({
                            type: 'found',
                            block: { ...block, nonce: nonce },
                            hash: hash
                        });
                        return;
                    }
                }
                
                postMessage({
                    type: 'complete',
                    message: 'Nonce range exhausted'
                });
            }

            onmessage = function(e) {
                const { block, startNonce, endNonce, difficulty } = e.data;
                mineBlock(block, startNonce, endNonce, difficulty);
            };
        `;

        const blob = new Blob([workerCode], { type: 'application/javascript' });
        const worker = new Worker(URL.createObjectURL(blob));

        worker.onmessage = (e) => {
            const { type, block, hash, hashes } = e.data;

            if (type === 'progress') {
                this.miningStats.totalHashes += hashes;
            } else if (type === 'found') {
                this.onBlockMined(block, hash);
            } else if (type === 'complete') {
                console.log('Worker completed nonce range');
            }
        };

        worker.onerror = (error) => {
            console.error('Mining worker error:', error);
        };

        // Start the worker
        worker.postMessage({
            block,
            startNonce,
            endNonce,
            difficulty
        });

        return worker;
    }

    /**
     * Single-threaded mining fallback
     */
    async startSingleThreadMining(blockchain) {
        const lastBlock = blockchain.getLatestBlock();
        const newBlock = this.createNewBlock(lastBlock, blockchain.chain.length);

        let nonce = 0;
        const target = '0'.repeat(this.currentDifficulty);

        while (this.isMining) {
            const blockData = JSON.stringify({
                ...newBlock,
                nonce: nonce
            });

            const hash = await this.hashBlock(blockData);
            this.miningStats.totalHashes++;

            if (hash.startsWith(target)) {
                newBlock.nonce = nonce;
                this.onBlockMined(newBlock, hash);
                break;
            }

            nonce++;

            // Yield control periodically to prevent UI blocking
            if (nonce % 100 === 0) {
                await new Promise(resolve => setTimeout(resolve, 1));
            }
        }
    }

    /**
     * Create a new block for mining
     */
    createNewBlock(previousBlock, index) {
        const timestamp = Date.now();
        
        // Create coinbase transaction (mining reward)
        const coinbaseTransaction = {
            id: this.generateTransactionId(),
            from: null, // Coinbase has no sender
            to: this.minerAddress,
            amount: this.getMiningReward(index),
            timestamp: timestamp,
            type: 'coinbase'
        };

        // Include pending transactions
        const transactions = [coinbaseTransaction, ...this.pendingTransactions];

        return {
            index: index,
            timestamp: timestamp,
            transactions: transactions,
            previousHash: previousBlock.hash,
            nonce: 0
        };
    }

    /**
     * Handle successful block mining
     */
    async onBlockMined(block, hash) {
        if (!this.isMining) return;

        this.stopMining();
        this.miningStats.blocksFound++;

        console.log(`Block mined! Hash: ${hash}`);
        console.log(`Nonce: ${block.nonce}`);
        console.log(`Total hashes: ${this.miningStats.totalHashes}`);

        // Add hash to block
        block.hash = hash;

        // Notify callback
        if (this.onBlockFound) {
            this.onBlockFound(block);
        }

        // Adjust difficulty
        this.adjustDifficulty();
    }

    /**
     * Calculate mining reward based on block height
     */
    getMiningReward(blockHeight) {
        const baseReward = 50;
        const halvingInterval = 210000; // Halve reward every 210,000 blocks
        const halvings = Math.floor(blockHeight / halvingInterval);
        return baseReward / Math.pow(2, halvings);
    }

    /**
     * Adjust mining difficulty
     */
    adjustDifficulty() {
        // Simple difficulty adjustment - increase if blocks found quickly
        const miningTime = Date.now() - this.miningStats.startTime;
        const targetTime = 60000; // Target 1 minute per block

        if (miningTime < targetTime * 0.5) {
            this.currentDifficulty++;
            console.log(`Difficulty increased to ${this.currentDifficulty}`);
        } else if (miningTime > targetTime * 2 && this.currentDifficulty > 1) {
            this.currentDifficulty--;
            console.log(`Difficulty decreased to ${this.currentDifficulty}`);
        }
    }

    /**
     * Start hash rate monitoring
     */
    startHashRateMonitoring() {
        let lastHashCount = 0;
        let lastTime = Date.now();

        this.hashRateInterval = setInterval(() => {
            const currentTime = Date.now();
            const timeDiff = (currentTime - lastTime) / 1000; // seconds
            const hashDiff = this.miningStats.totalHashes - lastHashCount;
            
            this.miningStats.hashesPerSecond = Math.round(hashDiff / timeDiff);
            
            lastHashCount = this.miningStats.totalHashes;
            lastTime = currentTime;

            // Notify UI of stats update
            if (this.onStatsUpdate) {
                this.onStatsUpdate(this.miningStats);
            }
        }, 1000);
    }

    /**
     * Hash block data
     */
    async hashBlock(blockData) {
        const encoder = new TextEncoder();
        const data = encoder.encode(blockData);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Generate transaction ID
     */
    generateTransactionId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    /**
     * Get current mining statistics
     */
    getStats() {
        return {
            ...this.miningStats,
            isMining: this.isMining,
            difficulty: this.currentDifficulty,
            workers: this.workers.length
        };
    }

    /**
     * Set mining callbacks
     */
    setCallbacks(onBlockFound, onStatsUpdate) {
        this.onBlockFound = onBlockFound;
        this.onStatsUpdate = onStatsUpdate;
    }

    /**
     * Save mining statistics to localStorage
     */
    saveMiningStats() {
        try {
            const stats = {
                ...this.miningStats,