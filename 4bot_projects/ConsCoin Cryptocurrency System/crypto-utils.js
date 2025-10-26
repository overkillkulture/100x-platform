/**
 * ConsCoin Cryptocurrency System - Cryptographic Utilities
 * Provides secure cryptographic functions for hashing, digital signatures, and key generation
 */

class CryptoUtils {
    constructor() {
        this.encoder = new TextEncoder();
        this.decoder = new TextDecoder();
    }

    /**
     * Generate SHA-256 hash of input data
     * @param {string} data - Data to hash
     * @returns {Promise<string>} - Hex string of hash
     */
    async sha256(data) {
        const msgBuffer = this.encoder.encode(data);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Generate double SHA-256 hash (common in blockchain applications)
     * @param {string} data - Data to hash
     * @returns {Promise<string>} - Hex string of double hash
     */
    async doubleSha256(data) {
        const firstHash = await this.sha256(data);
        return await this.sha256(firstHash);
    }

    /**
     * Generate ECDSA key pair for wallet addresses and signatures
     * @returns {Promise<Object>} - Object containing public and private keys
     */
    async generateKeyPair() {
        const keyPair = await crypto.subtle.generateKey(
            {
                name: 'ECDSA',
                namedCurve: 'P-256'
            },
            true, // extractable
            ['sign', 'verify']
        );

        return keyPair;
    }

    /**
     * Export public key to hex string format
     * @param {CryptoKey} publicKey - Public key to export
     * @returns {Promise<string>} - Hex string of public key
     */
    async exportPublicKey(publicKey) {
        const exported = await crypto.subtle.exportKey('raw', publicKey);
        const exportedKeyBuffer = new Uint8Array(exported);
        return Array.from(exportedKeyBuffer)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    /**
     * Export private key to hex string format
     * @param {CryptoKey} privateKey - Private key to export
     * @returns {Promise<string>} - Hex string of private key
     */
    async exportPrivateKey(privateKey) {
        const exported = await crypto.subtle.exportKey('pkcs8', privateKey);
        const exportedKeyBuffer = new Uint8Array(exported);
        return Array.from(exportedKeyBuffer)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    /**
     * Import public key from hex string
     * @param {string} keyHex - Hex string of public key
     * @returns {Promise<CryptoKey>} - Imported public key
     */
    async importPublicKey(keyHex) {
        const keyBuffer = new Uint8Array(
            keyHex.match(/.{1,2}/g).map(byte => parseInt(byte, 16))
        );

        return await crypto.subtle.importKey(
            'raw',
            keyBuffer,
            {
                name: 'ECDSA',
                namedCurve: 'P-256'
            },
            true,
            ['verify']
        );
    }

    /**
     * Import private key from hex string
     * @param {string} keyHex - Hex string of private key
     * @returns {Promise<CryptoKey>} - Imported private key
     */
    async importPrivateKey(keyHex) {
        const keyBuffer = new Uint8Array(
            keyHex.match(/.{1,2}/g).map(byte => parseInt(byte, 16))
        );

        return await crypto.subtle.importKey(
            'pkcs8',
            keyBuffer,
            {
                name: 'ECDSA',
                namedCurve: 'P-256'
            },
            true,
            ['sign']
        );
    }

    /**
     * Sign data with private key
     * @param {string} data - Data to sign
     * @param {CryptoKey} privateKey - Private key for signing
     * @returns {Promise<string>} - Hex string of signature
     */
    async sign(data, privateKey) {
        const dataBuffer = this.encoder.encode(data);
        const signature = await crypto.subtle.sign(
            {
                name: 'ECDSA',
                hash: 'SHA-256'
            },
            privateKey,
            dataBuffer
        );

        const signatureArray = Array.from(new Uint8Array(signature));
        return signatureArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Verify signature with public key
     * @param {string} data - Original data
     * @param {string} signatureHex - Signature in hex format
     * @param {CryptoKey} publicKey - Public key for verification
     * @returns {Promise<boolean>} - True if signature is valid
     */
    async verify(data, signatureHex, publicKey) {
        try {
            const dataBuffer = this.encoder.encode(data);
            const signatureBuffer = new Uint8Array(
                signatureHex.match(/.{1,2}/g).map(byte => parseInt(byte, 16))
            );

            return await crypto.subtle.verify(
                {
                    name: 'ECDSA',
                    hash: 'SHA-256'
                },
                publicKey,
                signatureBuffer,
                dataBuffer
            );
        } catch (error) {
            console.error('Signature verification failed:', error);
            return false;
        }
    }

    /**
     * Generate wallet address from public key
     * @param {string} publicKeyHex - Public key in hex format
     * @returns {Promise<string>} - Wallet address
     */
    async generateAddress(publicKeyHex) {
        // Hash the public key
        const hash1 = await this.sha256(publicKeyHex);
        const hash2 = await this.sha256(hash1);
        
        // Take first 40 characters and add prefix
        const address = 'CC' + hash2.substring(0, 40);
        return address.toUpperCase();
    }

    /**
     * Generate random nonce for mining
     * @returns {string} - Random hex string
     */
    generateNonce() {
        const array = new Uint32Array(1);
        crypto.getRandomValues(array);
        return array[0].toString(16);
    }

    /**
     * Generate secure random bytes
     * @param {number} length - Number of bytes to generate
     * @returns {string} - Random hex string
     */
    generateRandomBytes(length = 32) {
        const array = new Uint8Array(length);
        crypto.getRandomValues(array);
        return Array.from(array)
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    /**
     * Validate hash meets difficulty requirement
     * @param {string} hash - Hash to validate
     * @param {number} difficulty - Required number of leading zeros
     * @returns {boolean} - True if hash meets difficulty
     */
    validateHashDifficulty(hash, difficulty) {
        const prefix = '0'.repeat(difficulty);
        return hash.substring(0, difficulty) === prefix;
    }

    /**
     * Create merkle root from array of transaction hashes
     * @param {string[]} hashes - Array of transaction hashes
     * @returns {Promise<string>} - Merkle root hash
     */
    async createMerkleRoot(hashes) {
        if (hashes.length === 0) {
            return await this.sha256('');
        }

        if (hashes.length === 1) {
            return hashes[0];
        }

        const newLevel = [];
        
        // Process pairs of hashes
        for (let i = 0; i < hashes.length; i += 2) {
            const left = hashes[i];
            const right = i + 1 < hashes.length ? hashes[i + 1] : left;
            const combined = left + right;
            const hash = await this.sha256(combined);
            newLevel.push(hash);
        }

        // Recursively process until single root remains
        return await this.createMerkleRoot(newLevel);
    }

    /**
     * Validate transaction signature
     * @param {Object} transaction - Transaction object
     * @returns {Promise<boolean>} - True if signature is valid
     */
    async validateTransactionSignature(transaction) {
        try {
            if (!transaction.signature || !transaction.fromAddress) {
                return false;
            }

            // Create transaction data without signature
            const transactionData = {
                fromAddress: transaction.fromAddress,
                toAddress: transaction.toAddress,
                amount: transaction.amount,
                timestamp: transaction.timestamp
            };

            const dataString = JSON.stringify(transactionData);
            
            // Import public key from address (simplified - in real implementation, 
            // you'd need to derive public key from address or store it separately)
            const publicKey = await this.importPublicKey(transaction.publicKey);
            
            return await this.verify(dataString, transaction.signature, publicKey);
        } catch (error) {
            console.error('Transaction signature validation failed:', error);
            return false;
        }
    }

    /**
     * Generate transaction ID from transaction data
     * @param {Object} transaction - Transaction object
     * @returns {Promise<string>} - Transaction ID hash
     */
    async generateTransactionId(transaction) {
        const transactionString = JSON.stringify({
            fromAddress: transaction.fromAddress,
            toAddress: transaction.toAddress,
            amount: transaction.amount,
            timestamp: transaction.timestamp
        });
        
        return await this.sha256(transactionString);
    }

    /**
     * Encrypt data using AES-GCM
     * @param {string} data - Data to encrypt
     * @param {string} password - Password for encryption
     * @returns {Promise<Object>} - Encrypted data with IV
     */
    async encrypt(data, password) {
        const passwordKey = await this.deriveKey(password);
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const dataBuffer = this.encoder.encode(data);

        const encrypted = await crypto.subtle.encrypt(
            {
                name: 'AES-GCM',
                iv: iv
            },
            passwordKey,
            dataBuffer
        );

        return {
            encrypted: Array.from(new Uint8Array(encrypted))
                .map(b => b.toString(16).padStart(2, '0'))
                .join(''),
            iv: Array.from(iv)
                .map(b => b.toString(16).padStart(2, '0'))
                .join('')
        };
    }

    /**
     * Decrypt data using AES-GCM
     * @param {Object} encryptedData - Encrypted data object with IV
     * @param {string} password - Password for decryption
     * @returns {Promise<string>} - Decrypted data
     */
    async decrypt(encryptedData, password) {
        const passwordKey = await this.deriveKey(password);
        const iv = new Uint8Array(
            encryptedData.iv.match(/.{1,2}/g).map(byte => parseInt(byte, 16))
        );
        const encrypted = new Uint8Array(
            encryptedData.encrypted.match(/.{1,2}/g).map(byte => parseInt