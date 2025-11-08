"""
MODULE #24: BLOCKCHAIN INTEGRATION SUITE
Instance 3: Module Developer
Built: 2025-11-08

Immutable record-keeping and decentralized consensus for the Consciousness Revolution.
No corporate control. No manipulation. Pure truth.
"""

import json
import hashlib
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TransactionType(Enum):
    """Types of blockchain transactions"""
    CONTRIBUTION = "contribution"
    ACHIEVEMENT = "achievement"
    CERTIFICATION = "certification"
    VOTE = "vote"
    MESSAGE = "message"
    CONTRACT = "contract"
    TRANSFER = "transfer"


@dataclass
class Transaction:
    """Represents a blockchain transaction"""
    type: TransactionType
    sender: str
    data: Dict[str, Any]
    timestamp: float
    signature: Optional[str] = None


@dataclass
class Block:
    """Represents a block in the blockchain"""
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: Optional[str] = None


class SmartContract:
    """
    Simple smart contract system

    Contracts are Python functions stored on the blockchain
    that execute automatically when conditions are met.
    """

    def __init__(self, name: str, code: str, creator: str):
        self.name = name
        self.code = code
        self.creator = creator
        self.created_at = time.time()
        self.execution_count = 0
        self.state: Dict[str, Any] = {}

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute contract code

        WARNING: In production, use a sandboxed environment!
        This demo uses eval() for simplicity.
        """
        try:
            # Create execution context
            exec_context = {
                'state': self.state,
                'context': context,
                'result': {}
            }

            # Execute contract code
            exec(self.code, exec_context)

            self.execution_count += 1

            return {
                'success': True,
                'result': exec_context.get('result', {}),
                'state': self.state
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize contract"""
        return {
            'name': self.name,
            'code': self.code,
            'creator': self.creator,
            'created_at': self.created_at,
            'execution_count': self.execution_count,
            'state': self.state
        }


class Blockchain:
    """
    Immutable blockchain for the Consciousness Revolution

    Features:
    - Proof of work consensus
    - Transaction validation
    - Smart contracts
    - Immutable records
    - Decentralized verification
    """

    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty  # Number of leading zeros in hash
        self.smart_contracts: Dict[str, SmartContract] = {}
        self.mining_reward = 1.0
        self.balances: Dict[str, float] = {}

        # Create genesis block
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
            nonce=0
        )
        genesis.hash = self._calculate_hash(genesis)
        self.chain.append(genesis)

    def _calculate_hash(self, block: Block) -> str:
        """Calculate SHA-256 hash of a block"""
        block_data = {
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': [asdict(t) for t in block.transactions],
            'previous_hash': block.previous_hash,
            'nonce': block.nonce
        }

        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_transaction(
        self,
        transaction_type: TransactionType,
        sender: str,
        data: Dict[str, Any],
        signature: Optional[str] = None
    ) -> Transaction:
        """
        Add a transaction to pending transactions

        Args:
            transaction_type: Type of transaction
            sender: Who is sending
            data: Transaction data
            signature: Optional cryptographic signature

        Returns:
            Transaction object
        """

        transaction = Transaction(
            type=transaction_type,
            sender=sender,
            data=data,
            timestamp=time.time(),
            signature=signature
        )

        # Validate transaction
        if self._validate_transaction(transaction):
            self.pending_transactions.append(transaction)
            return transaction
        else:
            raise ValueError("Invalid transaction")

    def _validate_transaction(self, transaction: Transaction) -> bool:
        """Validate a transaction"""

        # Basic validation
        if not transaction.sender:
            return False

        if not transaction.data:
            return False

        # Type-specific validation
        if transaction.type == TransactionType.TRANSFER:
            amount = transaction.data.get('amount', 0)
            recipient = transaction.data.get('recipient')

            if amount <= 0 or not recipient:
                return False

            # Check sender has sufficient balance
            if self.get_balance(transaction.sender) < amount:
                return False

        return True

    def mine_block(self, miner_address: str) -> Block:
        """
        Mine a new block using proof of work

        Args:
            miner_address: Address to send mining reward

        Returns:
            Mined block
        """

        # Add mining reward transaction
        reward_tx = Transaction(
            type=TransactionType.TRANSFER,
            sender="SYSTEM",
            data={
                'amount': self.mining_reward,
                'recipient': miner_address,
                'reason': 'mining_reward'
            },
            timestamp=time.time()
        )
        self.pending_transactions.append(reward_tx)

        # Create new block
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.chain[-1].hash
        )

        # Proof of work
        print(f"Mining block {new_block.index}...", end=" ")
        while True:
            block_hash = self._calculate_hash(new_block)

            # Check if hash meets difficulty
            if block_hash.startswith('0' * self.difficulty):
                new_block.hash = block_hash
                break

            new_block.nonce += 1

        print(f"Mined! (nonce: {new_block.nonce}, hash: {new_block.hash[:16]}...)")

        # Add block to chain
        self.chain.append(new_block)

        # Update balances
        self._update_balances(new_block.transactions)

        # Clear pending transactions
        self.pending_transactions = []

        return new_block

    def _update_balances(self, transactions: List[Transaction]):
        """Update balances based on transactions"""

        for tx in transactions:
            if tx.type == TransactionType.TRANSFER:
                amount = tx.data.get('amount', 0)
                recipient = tx.data.get('recipient')

                if tx.sender != "SYSTEM":
                    self.balances[tx.sender] = self.balances.get(tx.sender, 0) - amount

                if recipient:
                    self.balances[recipient] = self.balances.get(recipient, 0) + amount

    def get_balance(self, address: str) -> float:
        """Get balance of an address"""
        return self.balances.get(address, 0)

    def deploy_contract(self, name: str, code: str, creator: str) -> SmartContract:
        """
        Deploy a smart contract to the blockchain

        Args:
            name: Contract name
            code: Python code
            creator: Who deployed it

        Returns:
            SmartContract
        """

        contract = SmartContract(name, code, creator)
        self.smart_contracts[name] = contract

        # Record deployment on blockchain
        self.add_transaction(
            TransactionType.CONTRACT,
            creator,
            {
                'action': 'deploy',
                'contract_name': name,
                'code_hash': hashlib.sha256(code.encode()).hexdigest()
            }
        )

        return contract

    def execute_contract(
        self,
        contract_name: str,
        context: Dict[str, Any],
        caller: str
    ) -> Dict[str, Any]:
        """
        Execute a smart contract

        Args:
            contract_name: Name of contract
            context: Execution context
            caller: Who is calling

        Returns:
            Execution result
        """

        if contract_name not in self.smart_contracts:
            return {'success': False, 'error': 'Contract not found'}

        contract = self.smart_contracts[contract_name]
        result = contract.execute(context)

        # Record execution on blockchain
        self.add_transaction(
            TransactionType.CONTRACT,
            caller,
            {
                'action': 'execute',
                'contract_name': contract_name,
                'success': result['success'],
                'context': context
            }
        )

        return result

    def verify_chain(self) -> bool:
        """
        Verify the integrity of the blockchain

        Returns:
            True if chain is valid, False otherwise
        """

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify hash
            if current.hash != self._calculate_hash(current):
                print(f"Invalid hash at block {i}")
                return False

            # Verify previous hash link
            if current.previous_hash != previous.hash:
                print(f"Invalid previous hash at block {i}")
                return False

            # Verify proof of work
            if not current.hash.startswith('0' * self.difficulty):
                print(f"Invalid proof of work at block {i}")
                return False

        return True

    def get_transaction_history(self, address: str) -> List[Transaction]:
        """Get all transactions involving an address"""

        history = []

        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    history.append(tx)
                elif tx.type == TransactionType.TRANSFER and tx.data.get('recipient') == address:
                    history.append(tx)

        return history

    def record_contribution(self, contributor: str, contribution_data: Dict[str, Any]):
        """Record a contribution on the blockchain (immutable proof of work)"""

        self.add_transaction(
            TransactionType.CONTRIBUTION,
            contributor,
            contribution_data
        )

    def record_achievement(self, user: str, achievement_data: Dict[str, Any]):
        """Record an achievement on the blockchain (immutable credential)"""

        self.add_transaction(
            TransactionType.ACHIEVEMENT,
            user,
            achievement_data
        )

    def vote(self, voter: str, vote_data: Dict[str, Any]):
        """Record a vote on the blockchain (transparent governance)"""

        self.add_transaction(
            TransactionType.VOTE,
            voter,
            vote_data
        )

    def generate_report(self) -> str:
        """Generate human-readable blockchain report"""

        report = "=" * 60 + "\n"
        report += "BLOCKCHAIN INTEGRATION SUITE - REPORT\n"
        report += "=" * 60 + "\n\n"

        report += f"Chain Length: {len(self.chain)} blocks\n"
        report += f"Total Transactions: {sum(len(b.transactions) for b in self.chain)}\n"
        report += f"Difficulty: {self.difficulty}\n"
        report += f"Smart Contracts: {len(self.smart_contracts)}\n"
        report += f"Active Addresses: {len(self.balances)}\n\n"

        report += "CHAIN VALIDITY: "
        if self.verify_chain():
            report += "✅ VALID\n\n"
        else:
            report += "❌ INVALID\n\n"

        report += "RECENT BLOCKS:\n"
        for block in self.chain[-5:]:
            report += f"  Block {block.index}: {len(block.transactions)} tx, "
            report += f"hash: {block.hash[:16]}...\n"
        report += "\n"

        report += "BALANCES:\n"
        for address, balance in sorted(self.balances.items(), key=lambda x: x[1], reverse=True):
            report += f"  {address}: {balance:.2f}\n"

        if not self.balances:
            report += "  (no balances yet)\n"

        report += "\n" + "=" * 60 + "\n"

        return report


def demo():
    """Demonstrate the blockchain integration suite"""

    print("=" * 60)
    print("BLOCKCHAIN INTEGRATION SUITE - DEMO")
    print("=" * 60)
    print()

    # Create blockchain
    blockchain = Blockchain(difficulty=2)
    print("Blockchain initialized\n")

    # Record contributions
    print("Recording contributions...")
    blockchain.record_contribution(
        "alice",
        {
            "project": "Module #24",
            "lines_of_code": 500,
            "impact": "high"
        }
    )

    blockchain.record_contribution(
        "bob",
        {
            "project": "Module #23",
            "lines_of_code": 300,
            "impact": "medium"
        }
    )
    print()

    # Mine block
    print("Mining block with contributions...")
    blockchain.mine_block("alice")
    print()

    # Record achievements
    print("Recording achievements...")
    blockchain.record_achievement(
        "alice",
        {
            "achievement": "Built 3 modules",
            "date": "2025-11-08",
            "verified": True
        }
    )
    print()

    # Deploy smart contract
    print("Deploying smart contract...")
    contract_code = """
# Voting contract
if 'votes' not in state:
    state['votes'] = {}

vote_for = context.get('vote_for')
if vote_for:
    state['votes'][vote_for] = state['votes'].get(vote_for, 0) + 1
    result['vote_recorded'] = True
    result['current_votes'] = state['votes'].copy()
"""

    contract = blockchain.deploy_contract(
        name="voting_contract",
        code=contract_code,
        creator="alice"
    )
    print(f"Contract '{contract.name}' deployed")
    print()

    # Mine block
    blockchain.mine_block("bob")
    print()

    # Execute contract
    print("Executing voting contract...")
    result1 = blockchain.execute_contract(
        "voting_contract",
        {"vote_for": "proposal_A"},
        "alice"
    )
    print(f"Vote 1: {result1['result']}")

    result2 = blockchain.execute_contract(
        "voting_contract",
        {"vote_for": "proposal_A"},
        "bob"
    )
    print(f"Vote 2: {result2['result']}")

    result3 = blockchain.execute_contract(
        "voting_contract",
        {"vote_for": "proposal_B"},
        "charlie"
    )
    print(f"Vote 3: {result3['result']}")
    print()

    # Mine block
    blockchain.mine_block("alice")
    print()

    # Show report
    print(blockchain.generate_report())

    # Verify chain
    print("Verifying blockchain integrity...")
    is_valid = blockchain.verify_chain()
    print(f"Chain valid: {is_valid}")
    print()

    # Show transaction history
    print("Alice's transaction history:")
    alice_history = blockchain.get_transaction_history("alice")
    for tx in alice_history:
        print(f"  - {tx.type.value}: {tx.data}")
    print()

    print("=" * 60)
    print("Demo complete. Blockchain operational!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
