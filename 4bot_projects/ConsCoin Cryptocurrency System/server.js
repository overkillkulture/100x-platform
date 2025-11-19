const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs').promises;
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.static(path.join(__dirname)));

// In-memory storage for multi-user blockchain state
let serverBlockchain = null;
let connectedPeers = new Set();
let pendingTransactions = [];

// File paths for persistent storage
const BLOCKCHAIN_FILE = path.join(__dirname, 'server-blockchain.json');
const PEERS_FILE = path.join(__dirname, 'peers.json');

// Initialize server blockchain
async function initializeBlockchain() {
    try {
        const data = await fs.readFile(BLOCKCHAIN_FILE, 'utf8');
        serverBlockchain = JSON.parse(data);
        console.log('Loaded existing blockchain with', serverBlockchain.chain.length, 'blocks');
    } catch (error) {
        // Create genesis block if no blockchain exists
        serverBlockchain = {
            chain: [{
                index: 0,
                timestamp: Date.now(),
                transactions: [],
                previousHash: '0',
                hash: '0000f816a87f806bb0073dcf026a64fb40c946b5abee2573702828694d5b4c43',
                nonce: 0,
                difficulty: 4
            }],
            difficulty: 4,
            miningReward: 100,
            pendingTransactions: []
        };
        await saveBlockchain();
        console.log('Created new blockchain with genesis block');
    }
}

// Save blockchain to file
async function saveBlockchain() {
    try {
        await fs.writeFile(BLOCKCHAIN_FILE, JSON.stringify(serverBlockchain, null, 2));
    } catch (error) {
        console.error('Error saving blockchain:', error);
    }
}

// Validate blockchain integrity
function isValidChain(chain) {
    for (let i = 1; i < chain.length; i++) {
        const currentBlock = chain[i];
        const previousBlock = chain[i - 1];

        // Check if current block's previous hash matches previous block's hash
        if (currentBlock.previousHash !== previousBlock.hash) {
            return false;
        }

        // Validate block hash
        const blockData = currentBlock.index + 
                         currentBlock.timestamp + 
                         JSON.stringify(currentBlock.transactions) + 
                         currentBlock.previousHash + 
                         currentBlock.nonce;
        
        const hash = crypto.createHash('sha256').update(blockData).digest('hex');
        if (hash !== currentBlock.hash) {
            return false;
        }

        // Check proof of work
        if (!currentBlock.hash.startsWith('0'.repeat(currentBlock.difficulty))) {
            return false;
        }
    }
    return true;
}

// API Routes

// Get full blockchain
app.get('/api/blockchain', (req, res) => {
    res.json(serverBlockchain);
});

// Get blockchain info
app.get('/api/blockchain/info', (req, res) => {
    res.json({
        blocks: serverBlockchain.chain.length,
        difficulty: serverBlockchain.difficulty,
        pendingTransactions: serverBlockchain.pendingTransactions.length,
        lastBlock: serverBlockchain.chain[serverBlockchain.chain.length - 1],
        connectedPeers: connectedPeers.size
    });
});

// Get specific block
app.get('/api/block/:index', (req, res) => {
    const index = parseInt(req.params.index);
    if (index >= 0 && index < serverBlockchain.chain.length) {
        res.json(serverBlockchain.chain[index]);
    } else {
        res.status(404).json({ error: 'Block not found' });
    }
});

// Get balance for address
app.get('/api/balance/:address', (req, res) => {
    const address = req.params.address;
    let balance = 0;

    // Calculate balance from all transactions in blockchain
    for (const block of serverBlockchain.chain) {
        for (const transaction of block.transactions) {
            if (transaction.to === address) {
                balance += transaction.amount;
            }
            if (transaction.from === address) {
                balance -= transaction.amount;
            }
        }
    }

    res.json({ address, balance });
});

// Get transaction history for address
app.get('/api/transactions/:address', (req, res) => {
    const address = req.params.address;
    const transactions = [];

    for (const block of serverBlockchain.chain) {
        for (const transaction of block.transactions) {
            if (transaction.from === address || transaction.to === address) {
                transactions.push({
                    ...transaction,
                    blockIndex: block.index,
                    timestamp: block.timestamp
                });
            }
        }
    }

    res.json(transactions.reverse()); // Most recent first
});

// Submit new transaction
app.post('/api/transaction', (req, res) => {
    try {
        const { from, to, amount, signature, publicKey } = req.body;

        // Validate required fields
        if (!from || !to || !amount || !signature || !publicKey) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        // Validate amount
        if (amount <= 0) {
            return res.status(400).json({ error: 'Amount must be positive' });
        }

        // Check if sender has sufficient balance
        let senderBalance = 0;
        for (const block of serverBlockchain.chain) {
            for (const transaction of block.transactions) {
                if (transaction.to === from) {
                    senderBalance += transaction.amount;
                }
                if (transaction.from === from) {
                    senderBalance -= transaction.amount;
                }
            }
        }

        if (senderBalance < amount) {
            return res.status(400).json({ error: 'Insufficient balance' });
        }

        // Add transaction to pending pool
        const transaction = {
            from,
            to,
            amount,
            timestamp: Date.now(),
            signature,
            publicKey
        };

        serverBlockchain.pendingTransactions.push(transaction);
        
        res.json({ 
            message: 'Transaction added to pending pool',
            transaction 
        });

    } catch (error) {
        res.status(500).json({ error: 'Failed to process transaction' });
    }
});

// Submit mined block
app.post('/api/mine', async (req, res) => {
    try {
        const { minerAddress, nonce, hash } = req.body;

        if (!minerAddress || nonce === undefined || !hash) {
            return res.status(400).json({ error: 'Missing required mining fields' });
        }

        // Create new block with pending transactions
        const lastBlock = serverBlockchain.chain[serverBlockchain.chain.length - 1];
        const newBlock = {
            index: lastBlock.index + 1,
            timestamp: Date.now(),
            transactions: [
                // Mining reward transaction
                {
                    from: null,
                    to: minerAddress,
                    amount: serverBlockchain.miningReward,
                    timestamp: Date.now()
                },
                ...serverBlockchain.pendingTransactions
            ],
            previousHash: lastBlock.hash,
            hash: hash,
            nonce: nonce,
            difficulty: serverBlockchain.difficulty
        };

        // Verify the submitted hash
        const blockData = newBlock.index + 
                         newBlock.timestamp + 
                         JSON.stringify(newBlock.transactions) + 
                         newBlock.previousHash + 
                         newBlock.nonce;
        
        const calculatedHash = crypto.createHash('sha256').update(blockData).digest('hex');
        
        if (calculatedHash !== hash) {
            return res.status(400).json({ error: 'Invalid hash' });
        }

        if (!hash.startsWith('0'.repeat(serverBlockchain.difficulty))) {
            return res.status(400).json({ error: 'Hash does not meet difficulty requirement' });
        }

        // Add block to chain
        serverBlockchain.chain.push(newBlock);
        serverBlockchain.pendingTransactions = [];

        // Adjust difficulty every 10 blocks
        if (newBlock.index % 10 === 0 && newBlock.index > 0) {
            const last10Blocks = serverBlockchain.chain.slice(-10);
            const timeSpent = last10Blocks[9].timestamp - last10Blocks[0].timestamp;
            const expectedTime = 10 * 30000; // 30 seconds per block

            if (timeSpent < expectedTime / 2) {
                serverBlockchain.difficulty++;
            } else if (timeSpent > expectedTime * 2) {
                serverBlockchain.difficulty = Math.max(1, serverBlockchain.difficulty - 1);
            }
        }

        await saveBlockchain();

        res.json({ 
            message: 'Block mined successfully',
            block: newBlock,
            reward: serverBlockchain.miningReward
        });

    } catch (error) {
        res.status(500).json({ error: 'Failed to process mined block' });
    }
});

// Get pending transactions for mining
app.get('/api/pending-transactions', (req, res) => {
    res.json(serverBlockchain.pendingTransactions);
});

// Sync blockchain with peer
app.post('/api/sync', async (req, res) => {
    try {
        const { blockchain } = req.body;

        if (!blockchain || !blockchain.chain) {
            return res.status(400).json({ error: 'Invalid blockchain data' });
        }

        // Validate incoming blockchain
        if (!isValidChain(blockchain.chain)) {
            return res.status(400).json({ error: 'Invalid blockchain' });
        }

        // Replace if incoming chain is longer and valid
        if (blockchain.chain.length > serverBlockchain.chain.length) {
            serverBlockchain = blockchain;
            await saveBlockchain();
            
            res.json({ 
                message: 'Blockchain updated',
                blocks: serverBlockchain.chain.length 
            });
        } else {
            res.json({ 
                message: 'Local blockchain is up to date',
                blocks: serverBlockchain.chain.length 
            });
        }

    } catch (error) {
        res.status(500).json({ error: 'Failed to sync blockchain' });
    }
});

// Register as peer
app.post('/api/peers/register', (req, res) => {
    const { address } = req.body;
    if (address) {
        connectedPeers.add(address);
        res.json({ message: 'Peer registered', peers: connectedPeers.size });
    } else {
        res.status(400).json({ error: 'Address required' });
    }
});

// Get connected peers
app.get('/api/peers', (req, res) => {
    res.json(Array.from(connectedPeers));
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'healthy',
        uptime: process.uptime(),
        blocks: serverBlockchain ? serverBlockchain.chain.length : 0,
        timestamp: Date.now()
    });
});

// Serve main application
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({ error: 