const crypto = require('crypto');

/**
 * Represents a single block in the blockchain
 */
class Block {
    constructor(index, timestamp, data, previousHash, nonce = 0) {
        this.index = index;
        this.timestamp = timestamp;
        this.data = data; // Array of transactions
        this.previousHash = previousHash;
        this.nonce = nonce;
        this.hash = this.calculateHash();
    }

    /**
     * Calculate SHA-256 hash of the block
     */
    calculateHash() {
        return crypto
            .createHash('sha256')
            .update(
                this.index +
                this.previousHash +
                this.timestamp +
                JSON.stringify(this.data) +
                this.nonce
            )
            .digest('hex');
    }

    /**
     * Mine block using proof-of-work algorithm
     * @param {number} difficulty - Number of leading zeros required
     */
    mineBlock(difficulty) {
        const target = Array(difficulty + 1).join('0');
        
        while (this.hash.substring(0, difficulty) !== target) {
            this.nonce++;
            this.hash = this.calculateHash();
        }

        console.log(`Block mined: ${this.hash}`);
    }

    /**
     * Validate block integrity
     */
    isValid() {
        return this.hash === this.calculateHash();
    }
}

/**
 * Main blockchain class
 */
class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
        this.difficulty = 4; // Mining difficulty (number of leading zeros)
        this.pendingTransactions = [];
        this.miningReward = 100; // ConsCoin reward for mining
        this.maxTransactionsPerBlock = 10;
    }

    /**
     * Create the genesis block (first block in chain)
     */
    createGenesisBlock() {
        const genesisBlock = new Block(
            0,
            Date.now(),
            'Genesis Block',
            '0'
        );
        return genesisBlock;
    }

    /**
     * Get the latest block in the chain
     */
    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }

    /**
     * Add a new transaction to pending transactions
     * @param {Object} transaction - Transaction object
     */
    addTransaction(transaction) {
        // Validate transaction
        if (!transaction.fromAddress || !transaction.toAddress) {
            throw new Error('Transaction must include from and to address');
        }

        if (!transaction.isValid()) {
            throw new Error('Cannot add invalid transaction to chain');
        }

        // Check if sender has sufficient balance (except for mining rewards)
        if (transaction.fromAddress !== null) {
            const balance = this.getBalance(transaction.fromAddress);
            if (balance < transaction.amount) {
                throw new Error('Not enough balance');
            }
        }

        this.pendingTransactions.push(transaction);
    }

    /**
     * Mine pending transactions and create new block
     * @param {string} miningRewardAddress - Address to send mining reward
     */
    minePendingTransactions(miningRewardAddress) {
        // Add mining reward transaction
        const rewardTransaction = {
            fromAddress: null,
            toAddress: miningRewardAddress,
            amount: this.miningReward,
            timestamp: Date.now(),
            isValid: () => true
        };

        // Take up to maxTransactionsPerBlock transactions
        const transactionsToMine = this.pendingTransactions
            .splice(0, this.maxTransactionsPerBlock - 1);
        
        transactionsToMine.push(rewardTransaction);

        // Create new block
        const block = new Block(
            this.chain.length,
            Date.now(),
            transactionsToMine,
            this.getLatestBlock().hash
        );

        // Mine the block
        block.mineBlock(this.difficulty);

        // Add to chain
        this.chain.push(block);

        return block;
    }

    /**
     * Get balance for a given address
     * @param {string} address - Wallet address
     */
    getBalance(address) {
        let balance = 0;

        // Go through all blocks and transactions
        for (const block of this.chain) {
            if (!Array.isArray(block.data)) continue;

            for (const trans of block.data) {
                // If sender, subtract amount
                if (trans.fromAddress === address) {
                    balance -= trans.amount;
                }

                // If receiver, add amount
                if (trans.toAddress === address) {
                    balance += trans.amount;
                }
            }
        }

        return balance;
    }

    /**
     * Get all transactions for a given address
     * @param {string} address - Wallet address
     */
    getTransactionsForAddress(address) {
        const transactions = [];

        for (const block of this.chain) {
            if (!Array.isArray(block.data)) continue;

            for (const trans of block.data) {
                if (trans.fromAddress === address || trans.toAddress === address) {
                    transactions.push({
                        ...trans,
                        blockIndex: block.index,
                        blockHash: block.hash,
                        timestamp: block.timestamp
                    });
                }
            }
        }

        return transactions;
    }

    /**
     * Validate the entire blockchain
     */
    isChainValid() {
        // Check genesis block
        const realGenesis = JSON.stringify(this.createGenesisBlock());
        if (realGenesis !== JSON.stringify(this.chain[0])) {
            return false;
        }

        // Check all other blocks
        for (let i = 1; i < this.chain.length; i++) {
            const currentBlock = this.chain[i];
            const previousBlock = this.chain[i - 1];

            // Validate current block
            if (!currentBlock.isValid()) {
                console.log(`Invalid block at index ${i}`);
                return false;
            }

            // Check if current block points to previous block
            if (currentBlock.previousHash !== previousBlock.hash) {
                console.log(`Invalid previous hash at index ${i}`);
                return false;
            }

            // Check proof of work
            if (currentBlock.hash.substring(0, this.difficulty) !== 
                Array(this.difficulty + 1).join('0')) {
                console.log(`Block not properly mined at index ${i}`);
                return false;
            }
        }

        return true;
    }

    /**
     * Get blockchain statistics
     */
    getStats() {
        return {
            totalBlocks: this.chain.length,
            difficulty: this.difficulty,
            pendingTransactions: this.pendingTransactions.length,
            miningReward: this.miningReward,
            isValid: this.isChainValid(),
            totalSupply: this.getTotalSupply()
        };
    }

    /**
     * Calculate total supply of ConsCoin
     */
    getTotalSupply() {
        let supply = 0;
        
        for (const block of this.chain) {
            if (!Array.isArray(block.data)) continue;
            
            for (const trans of block.data) {
                // Mining rewards (from null address) increase supply
                if (trans.fromAddress === null) {
                    supply += trans.amount;
                }
            }
        }
        
        return supply;
    }

    /**
     * Get recent blocks
     * @param {number} count - Number of recent blocks to return
     */
    getRecentBlocks(count = 5) {
        return this.chain
            .slice(-count)
            .reverse()
            .map(block => ({
                index: block.index,
                hash: block.hash,
                previousHash: block.previousHash,
                timestamp: block.timestamp,
                transactionCount: Array.isArray(block.data) ? block.data.length : 0,
                nonce: block.nonce
            }));
    }

    /**
     * Adjust mining difficulty based on block time
     */
    adjustDifficulty() {
        const targetBlockTime = 30000; // 30 seconds
        const recentBlocks = this.chain.slice(-10); // Last 10 blocks
        
        if (recentBlocks.length < 2) return;
        
        const timeSpent = recentBlocks[recentBlocks.length - 1].timestamp - 
                         recentBlocks[0].timestamp;
        const expectedTime = targetBlockTime * (recentBlocks.length - 1);
        
        if (timeSpent < expectedTime / 2) {
            this.difficulty++;
            console.log(`Difficulty increased to ${this.difficulty}`);
        } else if (timeSpent > expectedTime * 2 && this.difficulty > 1) {
            this.difficulty--;
            console.log(`Difficulty decreased to ${this.difficulty}`);
        }
    }

    /**
     * Export blockchain data
     */
    exportChain() {
        return {
            chain: this.chain,
            difficulty: this.difficulty,
            pendingTransactions: this.pendingTransactions,
            miningReward: this.miningReward
        };
    }

    /**
     * Import blockchain data
     * @param {Object} data - Blockchain data to import
     */
    importChain(data) {
        if (!data.chain || !Array.isArray(data.chain)) {
            throw new Error('Invalid blockchain data');
        }

        this.chain = data.chain.map(blockData => {
            const block = new Block(
                blockData.index,
                blockData.timestamp,
                blockData.data,
                blockData.previousHash,
                blockData.nonce
            );
            block.hash = blockData.hash;
            return block;
        });

        this.difficulty = data.difficulty || 4;
        this.pendingTransactions = data.pendingTransactions || [];
        this.miningReward = data.miningReward || 100;

        // Validate imported chain
        if (!this.isChainValid()) {
            throw new Error('Imported blockchain is invalid');
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Block, Blockchain };
}

// Make available globally for browser use
if (typeof window !== 'undefined') {
    window.Block = Block;
    window.Blockchain = Blockchain;
}