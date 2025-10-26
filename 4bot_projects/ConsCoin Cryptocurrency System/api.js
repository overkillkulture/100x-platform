const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class ConsCoinAPI {
    constructor() {
        this.app = express();
        this.dataDir = path.join(__dirname, 'data');
        this.blockchainFile = path.join(this.dataDir, 'blockchain.json');
        this.walletsFile = path.join(this.dataDir, 'wallets.json');
        this.mempoolFile = path.join(this.dataDir, 'mempool.json');
        
        this.setupMiddleware();
        this.setupRoutes();
        this.initializeData();
    }

    setupMiddleware() {
        this.app.use(cors());
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.static('public'));
        
        // Request logging
        this.app.use((req, res, next) => {
            console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }

    setupRoutes() {
        // Blockchain endpoints
        this.app.get('/api/blockchain', this.getBlockchain.bind(this));
        this.app.get('/api/blockchain/latest', this.getLatestBlock.bind(this));
        this.app.get('/api/blockchain/block/:hash', this.getBlockByHash.bind(this));
        this.app.get('/api/blockchain/height/:height', this.getBlockByHeight.bind(this));
        this.app.post('/api/blockchain/validate', this.validateBlockchain.bind(this));

        // Transaction endpoints
        this.app.get('/api/transactions', this.getAllTransactions.bind(this));
        this.app.get('/api/transactions/:txId', this.getTransaction.bind(this));
        this.app.post('/api/transactions', this.createTransaction.bind(this));
        this.app.post('/api/transactions/broadcast', this.broadcastTransaction.bind(this));
        this.app.get('/api/mempool', this.getMempool.bind(this));

        // Wallet endpoints
        this.app.post('/api/wallets', this.createWallet.bind(this));
        this.app.get('/api/wallets/:address/balance', this.getBalance.bind(this));
        this.app.get('/api/wallets/:address/transactions', this.getWalletTransactions.bind(this));
        this.app.get('/api/wallets/:address/utxos', this.getUTXOs.bind(this));

        // Mining endpoints
        this.app.get('/api/mining/difficulty', this.getDifficulty.bind(this));
        this.app.post('/api/mining/block', this.submitMinedBlock.bind(this));
        this.app.get('/api/mining/template', this.getMiningTemplate.bind(this));
        this.app.post('/api/mining/start', this.startMining.bind(this));
        this.app.post('/api/mining/stop', this.stopMining.bind(this));

        // Network endpoints
        this.app.get('/api/network/peers', this.getPeers.bind(this));
        this.app.post('/api/network/peers', this.addPeer.bind(this));
        this.app.get('/api/network/stats', this.getNetworkStats.bind(this));

        // Utility endpoints
        this.app.get('/api/stats', this.getStats.bind(this));
        this.app.get('/api/health', this.healthCheck.bind(this));
        this.app.post('/api/reset', this.resetBlockchain.bind(this));

        // Error handling
        this.app.use(this.errorHandler.bind(this));
    }

    async initializeData() {
        try {
            await fs.mkdir(this.dataDir, { recursive: true });
            
            // Initialize blockchain if it doesn't exist
            try {
                await fs.access(this.blockchainFile);
            } catch {
                const genesisBlock = this.createGenesisBlock();
                await this.saveBlockchain([genesisBlock]);
            }

            // Initialize empty files if they don't exist
            await this.ensureFileExists(this.walletsFile, []);
            await this.ensureFileExists(this.mempoolFile, []);
            
        } catch (error) {
            console.error('Failed to initialize data:', error);
        }
    }

    async ensureFileExists(filePath, defaultData) {
        try {
            await fs.access(filePath);
        } catch {
            await fs.writeFile(filePath, JSON.stringify(defaultData, null, 2));
        }
    }

    createGenesisBlock() {
        const timestamp = Date.now();
        const data = {
            transactions: [],
            reward: 50,
            miner: 'genesis'
        };
        
        const block = {
            index: 0,
            timestamp,
            data,
            previousHash: '0',
            nonce: 0,
            difficulty: 2
        };

        block.hash = this.calculateHash(block);
        return block;
    }

    calculateHash(block) {
        const blockString = JSON.stringify({
            index: block.index,
            timestamp: block.timestamp,
            data: block.data,
            previousHash: block.previousHash,
            nonce: block.nonce
        });
        return crypto.createHash('sha256').update(blockString).digest('hex');
    }

    // Blockchain endpoints
    async getBlockchain(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const limit = parseInt(req.query.limit) || blockchain.length;
            const offset = parseInt(req.query.offset) || 0;
            
            const paginatedBlocks = blockchain.slice(offset, offset + limit);
            
            res.json({
                blocks: paginatedBlocks,
                total: blockchain.length,
                offset,
                limit
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getLatestBlock(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const latestBlock = blockchain[blockchain.length - 1];
            res.json(latestBlock);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getBlockByHash(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const block = blockchain.find(b => b.hash === req.params.hash);
            
            if (!block) {
                return res.status(404).json({ error: 'Block not found' });
            }
            
            res.json(block);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getBlockByHeight(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const height = parseInt(req.params.height);
            
            if (height < 0 || height >= blockchain.length) {
                return res.status(404).json({ error: 'Block not found' });
            }
            
            res.json(blockchain[height]);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async validateBlockchain(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const isValid = await this.isValidChain(blockchain);
            
            res.json({
                valid: isValid,
                length: blockchain.length,
                lastBlock: blockchain[blockchain.length - 1]?.hash
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    // Transaction endpoints
    async getAllTransactions(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const transactions = [];
            
            blockchain.forEach(block => {
                if (block.data.transactions) {
                    block.data.transactions.forEach(tx => {
                        transactions.push({
                            ...tx,
                            blockHash: block.hash,
                            blockIndex: block.index,
                            timestamp: block.timestamp
                        });
                    });
                }
            });
            
            const limit = parseInt(req.query.limit) || transactions.length;
            const offset = parseInt(req.query.offset) || 0;
            
            res.json({
                transactions: transactions.slice(offset, offset + limit),
                total: transactions.length,
                offset,
                limit
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getTransaction(req, res) {
        try {
            const blockchain = await this.loadBlockchain();
            const txId = req.params.txId;
            
            for (const block of blockchain) {
                if (block.data.transactions) {
                    const transaction = block.data.transactions.find(tx => tx.id === txId);
                    if (transaction) {
                        return res.json({
                            ...transaction,
                            blockHash: block.hash,
                            blockIndex: block.index,
                            timestamp: block.timestamp
                        });
                    }
                }
            }
            
            res.status(404).json({ error: 'Transaction not found' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async createTransaction(req, res) {
        try {
            const { from, to, amount, privateKey } = req.body;
            
            if (!from || !to || !amount || !privateKey) {
                return res.status(400).json({ error: 'Missing required fields' });
            }
            
            // Verify balance
            const balance = await this.calculateBalance(from);
            if (balance < amount) {
                return res.status(400).json({ error: 'Insufficient balance' });
            }
            
            // Create transaction
            const transaction = {
                id: crypto.randomUUID(),
                from,
                to,
                amount: parseFloat(amount),
                timestamp: Date.now(),
                signature: this.signTransaction(from, to, amount, privateKey)
            };
            
            // Add to mempool
            const mempool = await this.loadMempool();
            mempool.push(transaction);
            await this.saveMempool(mempool);
            
            res.json(transaction);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async broadcastTransaction(req, res) {
        try {
            const transaction = req.body;
            
            // Validate transaction
            if (!this.isValidTransaction(transaction)) {
                return res.status(400).json({ error: 'Invalid transaction' });
            }
            
            // Add to mempool
            const mempool = await this.loadMempool();
            mempool.push(transaction);
            await this.saveMempool(mempool);
            
            res.json({ message: 'Transaction broadcasted successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getMempool(req, res) {
        try {
            const mempool = await this.loadMempool();
            res.json(mempool);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    // Wallet endpoints
    async createWallet(req, res) {
        try {
            const keyPair = crypto.generateKeyPairSync('rsa', {