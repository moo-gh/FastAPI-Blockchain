from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from blockchain import BlockchainManager
from wallet import Wallet


app = FastAPI(
    title="MGH Blockchain API",
    description="A decentralized blockchain with mining capabilities",
)

# Initialize blockchain manager
blockchain = BlockchainManager()


class TransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: float
    signature: str


class MiningRequest(BaseModel):
    miner_address: str


@app.get("/")
def read_root():
    """Root endpoint with basic information"""
    return {
        "message": "Welcome to MGH Blockchain API",
        "version": "1.2.0",
        "endpoints": {
            "create_wallet": "GET /wallets/new",
            "get_balance": "GET /wallets/{address}/balance",
            "add_transaction": "POST /transactions",
            "mine_block": "POST /mine",
            "get_status": "GET /status",
            "get_blocks": "GET /blocks",
            "get_mining_info": "GET /mining/info",
            "validate_chain": "GET /validate",
        },
    }


@app.get("/wallets/new")
def create_wallet():
    """Create a new wallet with public/private key pair"""
    wallet = Wallet()
    return {
        "address": wallet.get_public_key(),
        "private_key": wallet.get_private_key(),
        "instruction": "Keep your private_key safe. You need it to sign transactions."
    }


@app.get("/wallets/{address}/balance")
def get_balance(address: str):
    """Get the balance of a specific address"""
    balance = blockchain.get_balance(address)
    return {
        "address": address,
        "balance": balance,
        "currency": "MGH"
    }


@app.post("/transactions")
def add_transaction(request: TransactionRequest):
    """Add a transaction to the pending pool"""
    result = blockchain.add_transaction(
        sender=request.sender,
        recipient=request.recipient,
        amount=request.amount,
        signature=request.signature
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/mine")
def mine_block(request: MiningRequest):
    """Mine a new block - any miner can call this"""
    # Return error message asking users to mine on their end
    return {
        "status": "error",
        "message": "Mining is not allowed on the server. Please mine blocks on your end using the mining information from /mining/info endpoint.",
        "mining_info": blockchain.get_mining_info(),
    }


@app.get("/mining/info")
def get_mining_info():
    """Get current mining information"""
    return blockchain.get_mining_info()


@app.get("/status")
def get_status():
    """Get blockchain status"""
    return blockchain.get_status()


@app.get("/blocks")
def get_blocks():
    """Get all blocks in the blockchain"""
    return {
        "blocks": [
            {
                "index": i,
                "hash": block.block_hash,
                "transactions": block.transaction_list,
                "nonce": block.nonce,
                "miner": block.miner_address,
                "timestamp": block.timestamp,
                "previous_hash": block.previous_block_hash,
            }
            for i, block in enumerate(blockchain.chain)
        ]
    }


@app.get("/blocks/{block_index}")
def get_block(block_index: int):
    """Get a specific block by index"""
    if block_index >= len(blockchain.chain):
        raise HTTPException(status_code=404, detail="Block not found")

    block = blockchain.chain[block_index]
    return {
        "index": block_index,
        "hash": block.block_hash,
        "transactions": block.transaction_list,
        "nonce": block.nonce,
        "miner": block.miner_address,
        "timestamp": block.timestamp,
        "previous_hash": block.previous_block_hash,
    }


@app.get("/transactions/pending")
def get_pending_transactions():
    """Get all pending transactions"""
    return {"pending_transactions": blockchain.pending_transactions}


@app.get("/validate")
def validate_chain():
    """Validate the entire blockchain"""
    return blockchain.validate_chain()


@app.get("/stats")
def get_stats():
    """Get detailed blockchain statistics"""
    if not blockchain.chain:
        return {"message": "No blocks in chain"}

    total_transactions = sum(len(block.transaction_list) for block in blockchain.chain)
    unique_miners = set(
        block.miner_address for block in blockchain.chain if block.miner_address
    )

    return {
        "total_blocks": len(blockchain.chain),
        "total_transactions": total_transactions,
        "unique_miners": len(unique_miners),
        "miners": list(unique_miners),
        "pending_transactions": len(blockchain.pending_transactions),
        "difficulty": blockchain.difficulty,
        "mining_reward": blockchain.mining_reward,
    }
