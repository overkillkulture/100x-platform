/**
 * ConsCoin Transaction System
 * Handles transaction creation, validation, and management
 */

class Transaction {
    constructor(fromAddress, toAddress, amount, timestamp = Date.now()) {
        this.fromAddress = fromAddress;
        this.toAddress = toAddress;
        this.amount = amount;
        this.timestamp = timestamp;
        this.signature = null;
        this.transactionId = this.calculateHash();
    }

    /**
     * Calculate hash of transaction data
     * @returns {Promise<string>} Transaction hash
     */
    async calculateHash() {
        const data = this.fromAddress + this.toAddress + this.amount + this.timestamp;
        
        if (typeof window !== 'undefined' && window.crypto && window.crypto.subtle) {
            // Browser environment - use Web Crypto API
            const encoder = new TextEncoder();
            const dataBuffer = encoder.encode(data);
            const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        } else {
            // Node.js environment
            const crypto = require('crypto');
            return crypto.createHash('sha256').update(data).digest('hex');
        }
    }

    /**
     * Sign transaction with private key
     * @param {CryptoKey|string} privateKey - Private key for signing
     */
    async signTransaction(privateKey) {
        if (this.fromAddress === null) {
            throw new Error('Cannot sign mining reward transactions');
        }

        const hashToSign = await this.calculateHash();
        
        try {
            if (typeof window !== 'undefined' && window.crypto && window.crypto.subtle) {
                // Browser environment
                const encoder = new TextEncoder();
                const dataToSign = encoder.encode(hashToSign);
                
                const signature = await crypto.subtle.sign(
                    {
                        name: 'ECDSA',
                        hash: { name: 'SHA-256' }
                    },
                    privateKey,
                    dataToSign
                );
                
                this.signature = Array.from(new Uint8Array(signature))
                    .map(b => b.toString(16).padStart(2, '0')).join('');
            } else {
                // Node.js environment - simplified signing
                const crypto = require('crypto');
                const sign = crypto.createSign('SHA256');
                sign.update(hashToSign);
                this.signature = sign.sign(privateKey, 'hex');
            }
        } catch (error) {
            throw new Error('Failed to sign transaction: ' + error.message);
        }
    }

    /**
     * Verify transaction signature
     * @param {CryptoKey|string} publicKey - Public key for verification
     * @returns {Promise<boolean>} True if signature is valid
     */
    async isValid(publicKey) {
        // Mining reward transactions don't need signatures
        if (this.fromAddress === null) return true;

        if (!this.signature || this.signature.length === 0) {
            throw new Error('No signature in this transaction');
        }

        try {
            const hashToVerify = await this.calculateHash();
            
            if (typeof window !== 'undefined' && window.crypto && window.crypto.subtle) {
                // Browser environment
                const encoder = new TextEncoder();
                const dataToVerify = encoder.encode(hashToVerify);
                
                // Convert hex signature back to ArrayBuffer
                const signatureBytes = new Uint8Array(
                    this.signature.match(/.{2}/g).map(byte => parseInt(byte, 16))
                );
                
                return await crypto.subtle.verify(
                    {
                        name: 'ECDSA',
                        hash: { name: 'SHA-256' }
                    },
                    publicKey,
                    signatureBytes,
                    dataToVerify
                );
            } else {
                // Node.js environment
                const crypto = require('crypto');
                const verify = crypto.createVerify('SHA256');
                verify.update(hashToVerify);
                return verify.verify(publicKey, this.signature, 'hex');
            }
        } catch (error) {
            console.error('Transaction validation error:', error);
            return false;
        }
    }

    /**
     * Convert transaction to JSON
     * @returns {Object} Transaction as plain object
     */
    toJSON() {
        return {
            fromAddress: this.fromAddress,
            toAddress: this.toAddress,
            amount: this.amount,
            timestamp: this.timestamp,
            signature: this.signature,
            transactionId: this.transactionId
        };
    }

    /**
     * Create transaction from JSON object
     * @param {Object} data - Transaction data
     * @returns {Transaction} New transaction instance
     */
    static fromJSON(data) {
        const transaction = new Transaction(
            data.fromAddress,
            data.toAddress,
            data.amount,
            data.timestamp
        );
        transaction.signature = data.signature;
        transaction.transactionId = data.transactionId;
        return transaction;
    }
}

class TransactionPool {
    constructor() {
        this.pendingTransactions = [];
        this.maxPoolSize = 1000;
    }

    /**
     * Add transaction to pending pool
     * @param {Transaction} transaction - Transaction to add
     */
    addTransaction(transaction) {
        // Validate transaction before adding
        if (!this.isValidTransaction(transaction)) {
            throw new Error('Invalid transaction cannot be added to pool');
        }

        // Check if transaction already exists
        const exists = this.pendingTransactions.some(tx => 
            tx.transactionId === transaction.transactionId
        );

        if (exists) {
            throw new Error('Transaction already exists in pool');
        }

        // Remove oldest transactions if pool is full
        if (this.pendingTransactions.length >= this.maxPoolSize) {
            this.pendingTransactions.shift();
        }

        this.pendingTransactions.push(transaction);
    }

    /**
     * Get transactions for mining (up to specified limit)
     * @param {number} limit - Maximum number of transactions
     * @returns {Transaction[]} Array of transactions
     */
    getTransactionsForMining(limit = 10) {
        // Sort by timestamp (oldest first) and return up to limit
        return this.pendingTransactions
            .sort((a, b) => a.timestamp - b.timestamp)
            .slice(0, limit);
    }

    /**
     * Remove transactions that have been mined
     * @param {Transaction[]} minedTransactions - Transactions to remove
     */
    removeMinedTransactions(minedTransactions) {
        const minedIds = minedTransactions.map(tx => tx.transactionId);
        this.pendingTransactions = this.pendingTransactions.filter(
            tx => !minedIds.includes(tx.transactionId)
        );
    }

    /**
     * Basic transaction validation
     * @param {Transaction} transaction - Transaction to validate
     * @returns {boolean} True if valid
     */
    isValidTransaction(transaction) {
        // Check required fields
        if (!transaction.toAddress || transaction.amount <= 0) {
            return false;
        }

        // Check amount is a valid number
        if (typeof transaction.amount !== 'number' || isNaN(transaction.amount)) {
            return false;
        }

        // Check timestamp is reasonable (not too far in future)
        const now = Date.now();
        if (transaction.timestamp > now + 60000) { // 1 minute tolerance
            return false;
        }

        return true;
    }

    /**
     * Get pending transaction count
     * @returns {number} Number of pending transactions
     */
    getPendingCount() {
        return this.pendingTransactions.length;
    }

    /**
     * Clear all pending transactions
     */
    clear() {
        this.pendingTransactions = [];
    }

    /**
     * Get all pending transactions
     * @returns {Transaction[]} Array of pending transactions
     */
    getAllPending() {
        return [...this.pendingTransactions];
    }
}

class TransactionValidator {
    /**
     * Validate transaction against blockchain state
     * @param {Transaction} transaction - Transaction to validate
     * @param {Blockchain} blockchain - Blockchain instance
     * @returns {Promise<Object>} Validation result
     */
    static async validateTransaction(transaction, blockchain) {
        const result = {
            isValid: false,
            errors: []
        };

        try {
            // Basic structure validation
            if (!transaction.toAddress) {
                result.errors.push('Missing recipient address');
            }

            if (!transaction.amount || transaction.amount <= 0) {
                result.errors.push('Invalid transaction amount');
            }

            if (typeof transaction.amount !== 'number') {
                result.errors.push('Amount must be a number');
            }

            // Skip balance check for mining rewards
            if (transaction.fromAddress !== null) {
                // Check sender has sufficient balance
                const senderBalance = blockchain.getBalance(transaction.fromAddress);
                if (senderBalance < transaction.amount) {
                    result.errors.push('Insufficient balance');
                }

                // Verify signature if not a mining reward
                try {
                    const publicKey = blockchain.getPublicKey(transaction.fromAddress);
                    if (publicKey) {
                        const signatureValid = await transaction.isValid(publicKey);
                        if (!signatureValid) {
                            result.errors.push('Invalid transaction signature');
                        }
                    } else {
                        result.errors.push('Cannot verify signature - public key not found');
                    }
                } catch (error) {
                    result.errors.push('Signature verification failed: ' + error.message);
                }
            }

            // Check for double spending
            if (this.checkDoubleSpending(transaction, blockchain)) {
                result.errors.push('Double spending detected');
            }

            result.isValid = result.errors.length === 0;
            return result;

        } catch (error) {
            result.errors.push('Validation error: ' + error.message);
            return result;
        }
    }

    /**
     * Check for double spending attempts
     * @param {Transaction} transaction - Transaction to check
     * @param {Blockchain} blockchain - Blockchain instance
     * @returns {boolean} True if double spending detected
     */
    static checkDoubleSpending(transaction, blockchain) {
        if (transaction.fromAddress === null) return false;

        // This is a simplified check - in a real implementation,
        // you'd check UTXO (Unspent Transaction Outputs)
        const recentTransactions = blockchain.getAllTransactions()
            .filter(tx => 
                tx.fromAddress === transaction.fromAddress &&
                tx.timestamp > Date.now() - 60000 && // Last minute
                tx.transactionId !== transaction.transactionId
            );

        // Check if recent transactions would exceed balance
        const totalSpent = recentTransactions.reduce((sum, tx) => sum + tx.amount, 0);
        const currentBalance = blockchain.getBalance(transaction.fromAddress);
        
        return (totalSpent + transaction.amount) > currentBalance;
    }
}

// Export for both browser and Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Transaction, TransactionPool, TransactionValidator };
} else if (typeof window !== 'undefined') {
    window.Transaction = Transaction;
    window.TransactionPool = TransactionPool;
    window.TransactionValidator = TransactionValidator;
}