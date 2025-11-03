/**
 * ConsCoin Wallet Management System
 * Handles wallet creation, key management, and transaction signing
 */

class Wallet {
    constructor() {
        this.publicKey = null;
        this.privateKey = null;
        this.address = null;
        this.balance = 0;
        this.transactions = [];
    }

    /**
     * Generate a new wallet with public/private key pair
     */
    async generateWallet() {
        try {
            // Generate ECDSA key pair using Web Crypto API
            const keyPair = await window.crypto.subtle.generateKey(
                {
                    name: "ECDSA",
                    namedCurve: "P-256"
                },
                true, // extractable
                ["sign", "verify"]
            );

            this.privateKey = keyPair.privateKey;
            this.publicKey = keyPair.publicKey;

            // Generate wallet address from public key
            this.address = await this.generateAddress();
            
            // Save wallet to storage
            await this.saveWallet();
            
            return {
                address: this.address,
                publicKey: await this.exportPublicKey(),
                success: true
            };
        } catch (error) {
            console.error('Error generating wallet:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Generate wallet address from public key
     */
    async generateAddress() {
        try {
            const publicKeyBuffer = await window.crypto.subtle.exportKey(
                "raw",
                this.publicKey
            );
            
            // Hash the public key to create address
            const hashBuffer = await window.crypto.subtle.digest(
                "SHA-256",
                publicKeyBuffer
            );
            
            // Convert to hex and take first 40 characters
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            
            return 'CC' + hashHex.substring(0, 38); // ConsCoin prefix
        } catch (error) {
            console.error('Error generating address:', error);
            throw error;
        }
    }

    /**
     * Export public key for sharing
     */
    async exportPublicKey() {
        try {
            const exported = await window.crypto.subtle.exportKey(
                "raw",
                this.publicKey
            );
            const exportedKeyBuffer = new Uint8Array(exported);
            const exportedAsString = Array.from(exportedKeyBuffer, byte => 
                String.fromCharCode(byte)
            ).join('');
            return btoa(exportedAsString);
        } catch (error) {
            console.error('Error exporting public key:', error);
            throw error;
        }
    }

    /**
     * Import public key from string
     */
    async importPublicKey(keyString) {
        try {
            const keyBuffer = Uint8Array.from(atob(keyString), c => c.charCodeAt(0));
            return await window.crypto.subtle.importKey(
                "raw",
                keyBuffer,
                {
                    name: "ECDSA",
                    namedCurve: "P-256"
                },
                false,
                ["verify"]
            );
        } catch (error) {
            console.error('Error importing public key:', error);
            throw error;
        }
    }

    /**
     * Sign a transaction with private key
     */
    async signTransaction(transaction) {
        try {
            if (!this.privateKey) {
                throw new Error('No private key available for signing');
            }

            // Create transaction hash for signing
            const transactionString = JSON.stringify({
                from: transaction.from,
                to: transaction.to,
                amount: transaction.amount,
                timestamp: transaction.timestamp,
                nonce: transaction.nonce
            });

            const encoder = new TextEncoder();
            const data = encoder.encode(transactionString);

            // Sign the transaction
            const signature = await window.crypto.subtle.sign(
                {
                    name: "ECDSA",
                    hash: { name: "SHA-256" }
                },
                this.privateKey,
                data
            );

            // Convert signature to base64
            const signatureArray = new Uint8Array(signature);
            const signatureString = Array.from(signatureArray, byte => 
                String.fromCharCode(byte)
            ).join('');
            
            return btoa(signatureString);
        } catch (error) {
            console.error('Error signing transaction:', error);
            throw error;
        }
    }

    /**
     * Verify a transaction signature
     */
    async verifyTransaction(transaction, signature, publicKeyString) {
        try {
            // Import the public key
            const publicKey = await this.importPublicKey(publicKeyString);

            // Recreate transaction hash
            const transactionString = JSON.stringify({
                from: transaction.from,
                to: transaction.to,
                amount: transaction.amount,
                timestamp: transaction.timestamp,
                nonce: transaction.nonce
            });

            const encoder = new TextEncoder();
            const data = encoder.encode(transactionString);

            // Convert signature from base64
            const signatureBuffer = Uint8Array.from(atob(signature), c => c.charCodeAt(0));

            // Verify signature
            return await window.crypto.subtle.verify(
                {
                    name: "ECDSA",
                    hash: { name: "SHA-256" }
                },
                publicKey,
                signatureBuffer,
                data
            );
        } catch (error) {
            console.error('Error verifying transaction:', error);
            return false;
        }
    }

    /**
     * Calculate wallet balance from blockchain
     */
    calculateBalance(blockchain) {
        let balance = 0;
        
        if (!blockchain || !blockchain.chain) {
            return 0;
        }

        // Iterate through all blocks and transactions
        for (const block of blockchain.chain) {
            if (block.transactions) {
                for (const transaction of block.transactions) {
                    // Add received amounts
                    if (transaction.to === this.address) {
                        balance += parseFloat(transaction.amount);
                    }
                    // Subtract sent amounts
                    if (transaction.from === this.address) {
                        balance -= parseFloat(transaction.amount);
                    }
                }
            }
            
            // Add mining rewards
            if (block.miner === this.address && block.reward) {
                balance += parseFloat(block.reward);
            }
        }

        this.balance = Math.max(0, balance); // Ensure non-negative balance
        return this.balance;
    }

    /**
     * Get transaction history for this wallet
     */
    getTransactionHistory(blockchain) {
        const transactions = [];
        
        if (!blockchain || !blockchain.chain) {
            return transactions;
        }

        for (const block of blockchain.chain) {
            if (block.transactions) {
                for (const transaction of block.transactions) {
                    if (transaction.from === this.address || transaction.to === this.address) {
                        transactions.push({
                            ...transaction,
                            blockIndex: block.index,
                            blockHash: block.hash,
                            type: transaction.from === this.address ? 'sent' : 'received'
                        });
                    }
                }
            }
            
            // Add mining rewards
            if (block.miner === this.address && block.reward) {
                transactions.push({
                    from: 'MINING_REWARD',
                    to: this.address,
                    amount: block.reward,
                    timestamp: block.timestamp,
                    blockIndex: block.index,
                    blockHash: block.hash,
                    type: 'mining'
                });
            }
        }

        // Sort by timestamp (newest first)
        transactions.sort((a, b) => b.timestamp - a.timestamp);
        
        this.transactions = transactions;
        return transactions;
    }

    /**
     * Save wallet to localStorage
     */
    async saveWallet() {
        try {
            if (!this.privateKey || !this.publicKey) {
                throw new Error('No keys to save');
            }

            // Export private key
            const privateKeyBuffer = await window.crypto.subtle.exportKey(
                "pkcs8",
                this.privateKey
            );
            const privateKeyArray = new Uint8Array(privateKeyBuffer);
            const privateKeyString = Array.from(privateKeyArray, byte => 
                String.fromCharCode(byte)
            ).join('');

            // Export public key
            const publicKeyString = await this.exportPublicKey();

            const walletData = {
                address: this.address,
                privateKey: btoa(privateKeyString),
                publicKey: publicKeyString,
                balance: this.balance,
                created: Date.now()
            };

            localStorage.setItem('conscoin_wallet', JSON.stringify(walletData));
            return true;
        } catch (error) {
            console.error('Error saving wallet:', error);
            return false;
        }
    }

    /**
     * Load wallet from localStorage
     */
    async loadWallet() {
        try {
            const walletData = localStorage.getItem('conscoin_wallet');
            if (!walletData) {
                return false;
            }

            const data = JSON.parse(walletData);
            
            // Import private key
            const privateKeyBuffer = Uint8Array.from(atob(data.privateKey), c => c.charCodeAt(0));
            this.privateKey = await window.crypto.subtle.importKey(
                "pkcs8",
                privateKeyBuffer,
                {
                    name: "ECDSA",
                    namedCurve: "P-256"
                },
                true,
                ["sign"]
            );

            // Import public key
            this.publicKey = await this.importPublicKey(data.publicKey);
            
            this.address = data.address;
            this.balance = data.balance || 0;

            return true;
        } catch (error) {
            console.error('Error loading wallet:', error);
            return false;
        }
    }

    /**
     * Export wallet for backup
     */
    async exportWallet() {
        try {
            if (!this.privateKey || !this.publicKey) {
                throw new Error('No wallet to export');
            }

            const privateKeyBuffer = await window.crypto.subtle.exportKey(
                "pkcs8",
                this.privateKey
            );
            const privateKeyArray = new Uint8Array(privateKeyBuffer);
            const privateKeyString = Array.from(privateKeyArray, byte => 
                String.fromCharCode(byte)
            ).join('');

            const walletBackup = {
                address: this.address,
                privateKey: btoa(privateKeyString),
                publicKey: await this.exportPublicKey(),
                created: Date.now(),
                version: '1.0'
            };

            return JSON.stringify(walletBackup, null, 2);
        } catch (error) {
            console.error('Error exporting wallet:', error);
            throw error;
        }
    }

    /**
     * Import wallet from backup
     */
    async importWallet(backupString) {
        try {
            const backupData = JSON.parse(backupString);
            
            if (!backupData.privateKey || !backupData.publicKey || !backupData.address) {
                throw new Error('Invalid wallet backup format');
            }

            // Import private key
            const privateKeyBuffer = Uint8Array.from(atob(backupData.privateKey), c => c.charCodeAt(0));
            this.privateKey = await window.crypto.subtle.importKey(
                "pkcs8",
                privateKeyBuffer,
                {
                