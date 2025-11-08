# CHAPTER 13: Blockchain Architecture Deep Dive

**Word Count:** ~8,000 words

---

## Introduction: For the 1% Who Need This

**This chapter is for the rare builders who actually need to build a blockchain.**

If you read Chapter 12 and determined you DON'T need a blockchain (99% of projects), you can skip this chapter. Go build your dApp on Ethereum.

**If you're still here, you're either:**
1. Building genuinely novel consensus mechanism
2. Researching blockchain architecture (student, researcher)
3. Contributing to existing blockchain projects
4. Curious about how blockchains work under the hood

**This is the technical deep dive.**

We'll cover:
- Core blockchain components
- Consensus mechanisms in detail
- State management approaches
- Virtual machine architectures
- Network layer design
- Storage strategies
- Performance optimizations

**Warning: This gets technical. Code snippets in Go, Rust, and pseudocode.**

---

## Core Blockchain Components

Every blockchain, regardless of implementation, has these fundamental components:

### 1. Blocks and Blockchain Data Structure

**At its core, a blockchain is a linked list of blocks.**

**Block structure (simplified):**
```go
type Block struct {
    Header    BlockHeader
    Transactions []Transaction
}

type BlockHeader struct {
    Version       uint32
    PrevBlockHash [32]byte    // Links to previous block
    MerkleRoot    [32]byte    // Root of transaction Merkle tree
    Timestamp     uint64
    Nonce         uint32      // For Proof of Work
    Difficulty    uint32      // Current mining difficulty
}

type Transaction struct {
    From      Address
    To        Address
    Value     uint64
    Nonce     uint64
    Signature []byte
    Data      []byte     // Optional: smart contract calls
}
```

**Why Merkle trees?**

Transactions in a block aren't stored as a simple list. They're organized in a Merkle tree (binary hash tree):

```
         MerkleRoot
        /          \
     Hash01       Hash23
     /    \       /    \
  Hash0 Hash1 Hash2  Hash3
    |     |     |      |
   Tx0   Tx1   Tx2    Tx3
```

**Benefits:**
- Efficient proof of inclusion (log n proofs)
- SPV (Simplified Payment Verification) clients can verify transactions without downloading full blockchain
- Tamper-proof: Changing any transaction changes Merkle root

**Bitcoin's actual block:**
- Max size: 1 MB (though SegWit increases effective size)
- Average: 1,500-2,500 transactions per block
- Block time: ~10 minutes

**Ethereum's actual block:**
- Gas limit: ~30M gas per block
- Average: 150-300 transactions per block (simple transfers)
- Block time: ~12 seconds

### 2. Cryptographic Hashing

**SHA-256** (Bitcoin) or **Keccak-256** (Ethereum) provide:

**Properties needed:**
- **Deterministic:** Same input always produces same output
- **Fast to compute:** Hash in milliseconds
- **Avalanche effect:** Tiny input change = completely different hash
- **One-way:** Can't reverse hash to get input
- **Collision-resistant:** Nearly impossible to find two inputs with same hash

**Example:**
```
Input: "Hello"
SHA-256: 185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969

Input: "Hello!" (one character difference)
SHA-256: 334d016f755cd6dc58c53a86e183882f8ec14f52fb05345887c8a5edd42c87b7
```

**Completely different hashes. This is why blockchains are tamper-proof.**

### 3. Digital Signatures (Public Key Cryptography)

**ECDSA** (Elliptic Curve Digital Signature Algorithm) used by Bitcoin and Ethereum:

**Key pair generation:**
```python
# Simplified
private_key = random_256_bit_number()  # Keep secret!
public_key = elliptic_curve_multiply(private_key, G)  # G = generator point
address = hash(public_key)  # Ethereum uses Keccak-256
```

**Signing transaction:**
```python
message_hash = hash(transaction_data)
signature = sign(message_hash, private_key)
```

**Verifying signature:**
```python
is_valid = verify(message_hash, signature, public_key)
# Returns true only if signature was created by corresponding private key
```

**Security:**
- Breaking ECDSA requires solving discrete logarithm problem (computationally infeasible)
- 256-bit private key = 2^256 possible keys (more than atoms in universe)

**Ethereum uses secp256k1 curve (same as Bitcoin)**
**Some newer chains use Ed25519 (faster, simpler)**

### 4. Peer-to-Peer (P2P) Network

**Blockchains are decentralized. No single server.**

**Network topology:**
```
     Node A
    /  |  \
Node B Node C Node D
    \  |  /  \
     Node E  Node F
```

**Each node:**
- Maintains list of peer connections
- Propagates transactions and blocks
- Validates received data
- Stores blockchain state

**Discovery mechanisms:**

**DNS seeds (Bitcoin):**
- Hard-coded DNS names
- Return IP addresses of nodes
- Bootstrap initial connections

**Bootnodes (Ethereum):**
- Hard-coded known nodes
- Kademlia DHT for peer discovery

**Gossip protocol:**
- Node receives new transaction
- Validates it
- Forwards to peers
- Peers forward to their peers
- Exponential propagation across network

**Example (Go, simplified):**
```go
func (n *Node) BroadcastTransaction(tx *Transaction) {
    // Validate transaction
    if !n.ValidateTransaction(tx) {
        return
    }

    // Add to mempool
    n.mempool.Add(tx)

    // Broadcast to peers
    for _, peer := range n.peers {
        peer.Send(&Message{
            Type: MsgTypeTx,
            Data: tx,
        })
    }
}
```

### 5. Transaction Pool (Mempool)

**Mempool** = Memory pool of unconfirmed transactions

**Purpose:**
- Store pending transactions
- Validators/miners select transactions for next block
- Priority based on fees (usually)

**Implementation:**
```go
type Mempool struct {
    transactions map[Hash]*Transaction
    priorityQueue *PriorityQueue  // Ordered by gas price
    mu sync.RWMutex
}

func (m *Mempool) Add(tx *Transaction) error {
    m.mu.Lock()
    defer m.mu.Unlock()

    // Validate transaction
    if err := m.validate(tx); err != nil {
        return err
    }

    // Check if already exists
    txHash := tx.Hash()
    if _, exists := m.transactions[txHash]; exists {
        return ErrDuplicateTx
    }

    // Add to pool
    m.transactions[txHash] = tx
    m.priorityQueue.Push(tx, tx.GasPrice)

    return nil
}

func (m *Mempool) SelectTransactions(maxGas uint64) []*Transaction {
    var selected []*Transaction
    totalGas := uint64(0)

    // Select highest-fee transactions that fit in block
    for totalGas < maxGas {
        tx := m.priorityQueue.Pop()
        if tx == nil {
            break
        }
        if totalGas + tx.GasLimit <= maxGas {
            selected = append(selected, tx)
            totalGas += tx.GasLimit
        }
    }

    return selected
}
```

**Mempool challenges:**
- DoS attacks (spam transactions)
- MEV (Miner Extractable Value) - front-running
- Transaction replacement (higher fee)

---

## Consensus Mechanisms: Deep Dive

**Consensus** = How nodes agree on state of blockchain

### Proof of Work (PoW)

**Used by:** Bitcoin, Ethereum (pre-Merge), Litecoin, Monero

**Core idea:** Make block production computationally expensive

**Mining process:**
```python
def mine_block(block, difficulty):
    target = 2**256 / difficulty
    nonce = 0

    while True:
        block.nonce = nonce
        block_hash = sha256(sha256(block.serialize()))

        if int(block_hash, 16) < target:
            # Found valid block!
            return block

        nonce += 1
        # Bitcoin miners try ~100+ trillion hashes/second
```

**Why it works:**
- Finding valid nonce = random guessing (no shortcut)
- More computational power = more likely to find block first
- Changing transaction = must re-mine (tamper-resistance)

**Bitcoin difficulty adjustment:**
```
New Difficulty = Old Difficulty * (Actual Time / Target Time)

Target: 10 minutes per block
If last 2016 blocks took 12 days instead of 14:
New Difficulty = Old * (12/14) = 14% harder
```

**Pros:**
✅ Proven security (Bitcoin: 15+ years, no successful attack)
✅ Simple to understand
✅ Decentralized (anyone can mine)

**Cons:**
❌ Energy inefficient (Bitcoin: ~150 TWh/year)
❌ Slow (10 min blocks)
❌ Centralization of mining pools

### Proof of Stake (PoS)

**Used by:** Ethereum (post-Merge), Cardano, Polkadot

**Core idea:** Validators stake capital, selected to propose blocks

**Ethereum 2.0 PoS (simplified):**
```python
class Validator:
    def __init__(self, pubkey, stake):
        self.pubkey = pubkey
        self.stake = stake  # 32 ETH minimum
        self.is_active = True

def select_proposer(validators, slot, randomness):
    # Weighted random selection
    total_stake = sum(v.stake for v in validators if v.is_active)
    weights = [v.stake / total_stake for v in validators]

    # Pseudorandom selection using VDF (Verifiable Delay Function)
    seed = hash(randomness + slot)
    return weighted_random(validators, weights, seed)

def propose_block(validator, transactions):
    block = Block(
        proposer=validator.pubkey,
        transactions=transactions,
        slot=current_slot,
        parent=latest_block_hash
    )

    # Sign block
    signature = validator.sign(block.hash())

    return block, signature
```

**Slashing (punishment for misbehavior):**
```python
def slash_validator(validator, violation_type):
    if violation_type == "double_proposal":
        # Proposed two different blocks for same slot
        penalty = validator.stake * 0.5  # Lose 50%
    elif violation_type == "surround_vote":
        # Conflicting attestations
        penalty = validator.stake * 0.25

    validator.stake -= penalty
    burned_eth += penalty  # ETH destroyed
```

**Why it works:**
- Economic security: Attack costs you staked capital
- Nothing-at-stake problem solved by slashing
- More energy efficient than PoW

**Pros:**
✅ Energy efficient (99.95% less than PoW)
✅ Faster finality
✅ Economic security scales with value

**Cons:**
❌ "Rich get richer" (more stake = more rewards)
❌ Complexity (slashing, finality rules)
❌ Less proven than PoW

### Delegated Proof of Stake (DPoS)

**Used by:** EOS, Tron, Cosmos (Tendermint variant)

**Core idea:** Token holders vote for validators

```python
class DPoSChain:
    def __init__(self):
        self.validators = []  # Top 21 voted validators
        self.votes = {}       # Token holder votes

    def vote(self, voter, validator, amount):
        self.votes[(voter, validator)] = amount

    def elect_validators(self):
        # Tally votes
        validator_votes = {}
        for (voter, validator), amount in self.votes.items():
            validator_votes[validator] = validator_votes.get(validator, 0) + amount

        # Top 21 become validators
        sorted_validators = sorted(validator_votes.items(), key=lambda x: x[1], reverse=True)
        self.validators = [v for v, votes in sorted_validators[:21]]

    def produce_blocks(self):
        # Validators take turns producing blocks (round-robin)
        while True:
            for validator in self.validators:
                block = validator.produce_block()
                self.add_block(block)
                sleep(block_time)  # e.g., 0.5 seconds
```

**Pros:**
✅ Very fast (0.5s block times)
✅ High throughput
✅ Low fees

**Cons:**
❌ More centralized (only 21 validators)
❌ Vulnerable to cartel formation
❌ Vote buying potential

### Proof of History + Proof of Stake (Solana)

**Unique to Solana**

**Proof of History:**
```python
# Simplified
def proof_of_history_sequence():
    state = initial_hash
    sequence = []

    for i in range(iterations):
        state = sha256(state)
        sequence.append((i, state))

    return sequence

# Properties:
# - Verifiable: Anyone can recompute sequence
# - Time-stamped: Number of hashes = time elapsed
# - Ordered: Events inserted into sequence prove ordering
```

**Why it matters:**
- Eliminates need for validators to communicate about time
- Parallel transaction processing (know order beforehand)
- Enables 50,000+ TPS

**Combined with PoS:**
- Validators stake SOL
- PoH provides clock
- Faster consensus because time is proven, not agreed upon

**Pros:**
✅ Extremely fast (400ms blocks)
✅ High throughput (50K+ TPS)
✅ Novel approach

**Cons:**
❌ More complex
❌ Network outages (2021, 2022)
❌ Less decentralized (high hardware requirements)

### Byzantine Fault Tolerance (BFT) Variants

**Used by:** Cosmos (Tendermint), Algorand, Hedera

**Core idea:** Classic distributed systems consensus adapted for blockchain

**Tendermint consensus (simplified):**
```
Round-based voting:

1. PROPOSE: Selected proposer broadcasts block
2. PREVOTE: Validators vote on proposed block
3. PRECOMMIT: If >2/3 prevoted, validators precommit
4. COMMIT: If >2/3 precommitted, block is final

Finality: Immediate (no forks possible with >2/3 honest validators)
```

**Implementation (pseudocode):**
```python
def tendermint_consensus(validators, proposed_block):
    # Round 1: Prevote
    prevotes = collect_votes(validators, proposed_block)

    if count(prevotes) > (2/3 * len(validators)):
        # Round 2: Precommit
        precommits = collect_votes(validators, proposed_block)

        if count(precommits) > (2/3 * len(validators)):
            # Finalize block
            finalize(proposed_block)
            return SUCCESS

    # If not enough votes, try next round with different proposer
    return RETRY
```

**Pros:**
✅ Instant finality
✅ Provably secure with >2/3 honest validators
✅ Predictable performance

**Cons:**
❌ Requires known validator set
❌ Doesn't scale to thousands of validators (voting overhead)
❌ Liveness depends on >2/3 participation

---

## State Management

**How blockchains track account balances and contract storage:**

### UTXO Model (Bitcoin)

**UTXO** = Unspent Transaction Output

**Concept:**
- No account balances
- Only unspent outputs from previous transactions
- Transaction consumes UTXOs and creates new ones

**Example:**
```
Alice has:
- UTXO #1: 3 BTC (from Bob)
- UTXO #2: 2 BTC (from Carol)
Total: 5 BTC

Alice sends 4 BTC to Dave:

Transaction:
Inputs:
  - UTXO #1 (3 BTC) [consumed]
  - UTXO #2 (2 BTC) [consumed]
Outputs:
  - New UTXO: 4 BTC (to Dave)
  - New UTXO: 0.999 BTC (change to Alice)
  - Fee: 0.001 BTC (to miner)
```

**Implementation:**
```go
type UTXO struct {
    TxHash  [32]byte
    Index   uint32
    Value   uint64
    ScriptPubKey []byte  // Locking script
}

type UTXOSet struct {
    unspent map[string]*UTXO  // Key: TxHash + Index
}

func (u *UTXOSet) GetUTXOs(address Address) []*UTXO {
    var utxos []*UTXO
    for _, utxo := range u.unspent {
        if utxo.BelongsTo(address) {
            utxos = append(utxos, utxo)
        }
    }
    return utxos
}

func (u *UTXOSet) ApplyTransaction(tx *Transaction) {
    // Remove consumed UTXOs
    for _, input := range tx.Inputs {
        key := input.PrevTxHash.String() + fmt.Sprint(input.OutputIndex)
        delete(u.unspent, key)
    }

    // Add new UTXOs
    for i, output := range tx.Outputs {
        key := tx.Hash().String() + fmt.Sprint(i)
        u.unspent[key] = &UTXO{
            TxHash: tx.Hash(),
            Index: uint32(i),
            Value: output.Value,
            ScriptPubKey: output.ScriptPubKey,
        }
    }
}
```

**Pros:**
✅ Simple
✅ Parallel transaction processing (different UTXOs = no conflict)
✅ Privacy-friendly (no account tracking)

**Cons:**
❌ More complex for users (wallet must track UTXOs)
❌ Difficult for smart contracts
❌ Transaction size grows with number of inputs

### Account Model (Ethereum)

**Account** = Balance stored in account state

**Two account types:**
1. **EOA (Externally Owned Account):** Controlled by private key
2. **Contract Account:** Controlled by code

**State structure:**
```go
type Account struct {
    Nonce    uint64  // Transaction count (prevents replay)
    Balance  *big.Int
    StorageRoot [32]byte  // Merkle root of contract storage
    CodeHash [32]byte  // Hash of contract code (empty for EOA)
}

type WorldState struct {
    accounts map[Address]*Account
}

func (w *WorldState) Transfer(from, to Address, amount *big.Int) error {
    fromAccount := w.accounts[from]
    toAccount := w.accounts[to]

    if fromAccount.Balance.Cmp(amount) < 0 {
        return ErrInsufficientBalance
    }

    fromAccount.Balance.Sub(fromAccount.Balance, amount)
    toAccount.Balance.Add(toAccount.Balance, amount)

    return nil
}
```

**Patricia Merkle Trie (Ethereum's state storage):**
```
             StateRoot
              /     \
         Hash(A)   Hash(B)
         /   \       /   \
    Acc1  Acc2  Acc3  Acc4
```

**Each account's storage is also a Merkle trie:**
```
Account 0x123...
  Balance: 10 ETH
  Nonce: 5
  StorageRoot → Merkle trie of contract storage
    Slot 0: Value 100
    Slot 1: Value 200
```

**Pros:**
✅ Simple balance tracking
✅ Easy smart contracts
✅ Global state view

**Cons:**
❌ Sequential nonces (transactions must be ordered)
❌ Harder to parallelize
❌ State bloat (storing all account data)

---

## Virtual Machines and Execution

### EVM (Ethereum Virtual Machine)

**Stack-based virtual machine**

**Opcodes:**
```
PUSH1 0x60  // Push 96 onto stack
PUSH1 0x40  // Push 64 onto stack
MSTORE      // Store 96 at memory position 64

ADD         // Pop two values, push sum
MUL         // Pop two values, push product
SSTORE      // Store value in contract storage (expensive!)
SLOAD       // Load value from contract storage
```

**Gas model:**
```
Operation      Gas Cost
--------------------------
ADD            3 gas
MUL            5 gas
SSTORE         20,000 gas (first write)
SLOAD          200 gas
CALL           700 gas
CREATE         32,000 gas
```

**EVM execution:**
```python
class EVM:
    def __init__(self):
        self.stack = []
        self.memory = bytearray(1024)
        self.storage = {}
        self.pc = 0  # Program counter
        self.gas = 0

    def execute(self, bytecode, gas_limit):
        self.gas = gas_limit

        while self.pc < len(bytecode):
            opcode = bytecode[self.pc]

            if opcode == 0x01:  # ADD
                if self.gas < 3:
                    raise OutOfGasError
                self.gas -= 3

                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append((a + b) % 2**256)

            elif opcode == 0x55:  # SSTORE
                if self.gas < 20000:
                    raise OutOfGasError
                self.gas -= 20000

                key = self.stack.pop()
                value = self.stack.pop()
                self.storage[key] = value

            # ... 100+ other opcodes

            self.pc += 1

        return self.storage, self.gas  # Return state and remaining gas
```

**Determinism:**
- Same bytecode + same inputs = same outputs (always)
- Critical for consensus

**Pros:**
✅ Turing-complete
✅ Well-tested (10+ years)
✅ Large ecosystem

**Cons:**
❌ Slow (interpreted, not compiled)
❌ Limited parallelization
❌ High gas costs

### WASM (WebAssembly)

**Used by:** Polkadot, NEAR, Cosmos (CosmWasm)

**Compiled, not interpreted:**
```
Solidity → Compile → EVM Bytecode → Interpret → Execute

Rust → Compile → WASM → Execute (much faster)
```

**Benefits:**
- 10-100x faster than EVM
- Can use Rust, C++, AssemblyScript
- Better tooling

**Example WASM contract (Rust):**
```rust
#[no_mangle]
pub extern "C" fn transfer(to: *const u8, amount: u64) -> u32 {
    let caller = get_caller();
    let balance = get_balance(caller);

    if balance < amount {
        return 1;  // Error: Insufficient balance
    }

    set_balance(caller, balance - amount);

    let recipient = unsafe { Address::from_ptr(to) };
    let recipient_balance = get_balance(recipient);
    set_balance(recipient, recipient_balance + amount);

    0  // Success
}
```

**Compiled to WASM, runs in blockchain VM**

### Move (Sui, Aptos)

**Resource-oriented language**

**Key innovation: Linear types**
```rust
// Move code
module MyToken {
    struct Coin has key { value: u64 }

    public fun transfer(coin: Coin, recipient: address) {
        move_to(recipient, coin);
        // coin can't be used again - prevented at compile time!
    }
}
```

**Prevents:**
- Double-spending (can't copy resources)
- Lost assets (must explicitly destroy or move)

**Benefits for blockchain:**
- Assets are first-class citizens
- Security by design
- Formal verification easier

---

## Network Architecture

### Node Types

**Full Node:**
- Stores entire blockchain
- Validates all blocks and transactions
- Serves data to light clients
- Participates in consensus (if validator)

**Light Client (SPV):**
- Stores only block headers
- Requests Merkle proofs for transactions
- Can't validate full chain
- Trusts full nodes

**Archive Node:**
- Full node + all historical state
- Ethereum: ~14 TB (growing)
- Needed for blockchain explorers

**Validator Node:**
- Full node that participates in consensus
- Stakes capital (PoS) or mines (PoW)
- Proposes and votes on blocks

### Communication Protocols

**libp2p (IPFS, Ethereum 2.0, Polkadot):**
```go
// Create libp2p host
host, _ := libp2p.New(
    libp2p.ListenAddrStrings("/ip4/0.0.0.0/tcp/4001"),
    libp2p.Identity(privateKey),
)

// Set up stream handler
host.SetStreamHandler("/blockchain/1.0.0", handleStream)

// Connect to peer
peerInfo := peer.AddrInfo{
    ID: peerID,
    Addrs: multiaddrs,
}
host.Connect(context.Background(), peerInfo)
```

**DevP2P (Ethereum 1.0):**
- RLPx for encoding
- Custom discovery protocol
- Sub-protocols (eth, snap, wit)

**Message types:**
```go
const (
    MsgStatusCode       = 0x00
    MsgNewBlockHashesCode = 0x01
    MsgTransactionsCode  = 0x02
    MsgGetBlockHeadersCode = 0x03
    MsgBlockHeadersCode  = 0x04
    MsgGetBlockBodiesCode = 0x05
    MsgBlockBodiesCode   = 0x06
    MsgNewBlockCode      = 0x07
)
```

---

## Storage and Data Management

### State Storage

**LevelDB (Bitcoin, older Ethereum):**
- Key-value store
- Fast reads/writes
- No SQL needed

**RocksDB (Newer Ethereum, Cosmos):**
- Fork of LevelDB
- Better performance
- More tunable

**Patricia Merkle Trie (Ethereum state):**
```
Pros:
- Cryptographic proof of inclusion
- Efficient state root computation
- Prunable old states

Cons:
- Slow (many DB lookups per value)
- State bloat
```

**Verkle Trees (Ethereum future):**
- Smaller proofs (kilobytes vs megabytes)
- Enable stateless clients

### Pruning and Archival

**Full node can prune old state:**
```go
func PruneState(db Database, beforeBlock uint64) {
    // Keep only state after specific block
    // Reduces storage from ~14 TB to ~500 GB

    for block := 0; block < beforeBlock; block++ {
        stateRoot := GetStateRoot(block)
        DeleteState(db, stateRoot)
    }
}
```

**Archive nodes keep everything:**
- Needed for blockchain explorers
- Historical queries
- Re-executing old transactions

---

## Summary: Architecture Choices

**Building a blockchain requires decisions:**

**Consensus:**
- PoW (secure, slow, wasteful)
- PoS (efficient, complex)
- BFT (fast finality, known validators)
- Novel (PoH, etc.)

**State model:**
- UTXO (simple, parallel)
- Account (easy smart contracts)

**VM:**
- EVM (compatible, slow)
- WASM (fast, flexible)
- Custom (Move, etc.)

**Networking:**
- libp2p (modern, flexible)
- Custom (optimized for specific use)

**Storage:**
- LevelDB/RocksDB (proven)
- Custom (optimized tries)

**Each choice has trade-offs. Study existing chains. Learn from their designs.**

---

**Next Chapter:** Launching and Growing a Blockchain Network - From genesis block to thriving ecosystem.

⚡🏗️🔨
