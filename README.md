# MGH Blockchain – Decentralized Mining System

A prototype for MGH COIN😁. A FastAPI-powered blockchain featuring decentralized mining, proof-of-work consensus, and robust transaction management. This project enables multiple miners to compete in real time, ensuring security, transparency, and efficient block creation.

## Features

- 🔗 **Decentralized Mining**: Multiple miners can compete to mine blocks
- ⛏️ **Proof of Work**: Cryptographic puzzle solving with adjustable difficulty
- 💰 **Mining Rewards**: Miners receive MGH coins for successfully mining blocks
- 📊 **Transaction Management**: Add and track pending transactions
- 🔍 **Blockchain Validation**: Verify blockchain integrity
- 📈 **Real-time Statistics**: Monitor blockchain status and metrics

## Architecture

### Core Components

1. **Blockchain Class**: Individual block structure with nonce and miner information
2. **BlockchainManager Class**: Manages the entire blockchain, pending transactions, and mining
3. **FastAPI Endpoints**: RESTful API for blockchain operations

### Mining Process

1. **Transaction Pool**: Transactions are added to a pending pool
2. **Mining Competition**: Multiple miners can attempt to mine the same block
3. **Proof of Work**: Miners try different nonces to find a hash with required leading zeros
4. **Block Creation**: First miner to find a valid hash creates the block
5. **Reward Distribution**: Winning miner receives MGH coins

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd fastapi-blockchain
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
uvicorn app:app --reload
```

The API will be available at `https://fastapi-blockchain.m-gh.com`

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with API information |
| `POST` | `/transactions` | Add a new transaction |
| `POST` | `/mine` | Mine a new block |
| `GET` | `/status` | Get blockchain status |
| `GET` | `/blocks` | Get all blocks |
| `GET` | `/blocks/{index}` | Get specific block |
| `GET` | `/transactions/pending` | Get pending transactions |
| `GET` | `/mining/info` | Get mining information |
| `GET` | `/validate` | Validate blockchain |
| `GET` | `/stats` | Get detailed statistics |

### Usage Examples

#### 1. Create a Wallet
```bash
curl "https://fastapi-blockchain.m-gh.com/wallets/new"
```
Response:
```json
{
  "address": "...",
  "private_key": "...",
  "instruction": "..."
}
```

#### 2. Get Balance
```bash
curl "https://fastapi-blockchain.m-gh.com/wallets/<address>/balance"
```

#### 3. Add a Transaction
```bash
curl -X POST "https://fastapi-blockchain.m-gh.com/transactions" \
     -H "Content-Type: application/json" \
     -d '{
           "sender": "<sender_address>",
           "recipient": "<recipient_address>",
           "amount": 10.5,
           "signature": "<digital_signature>"
         }'
```

#### 2. Mine a Block
```bash
curl -X POST "https://fastapi-blockchain.m-gh.com/mine" \
     -H "Content-Type: application/json" \
     -d '{"miner_address": "miner_A"}'
```

#### 3. Get Blockchain Status
```bash
curl "https://fastapi-blockchain.m-gh.com/status"
```

#### 4. Get All Blocks
```bash
curl "https://fastapi-blockchain.m-gh.com/blocks"
```

### Postman Collection

For easier API testing, you can import the provided Postman collection:

1. **Download the collection**: The `Postman.json` file in the root directory contains all the API endpoints
2. **Import to Postman**: Open Postman and import the `Postman.json` file
3. **Update the base URL**: Make sure to update the base URL variable to `https://fastapi-blockchain.m-gh.com` in your Postman environment

This collection includes all the endpoints with pre-configured requests and example data for easy testing.

## Configuration

### Hard-coded Limits

The system uses the following hard-coded values:

```python
MAX_TRANSACTIONS_PER_BLOCK = 100
MIN_TRANSACTIONS_PER_BLOCK = 1
MINING_DIFFICULTY = 2  # Number of leading zeros required
MINING_REWARD = 10     # MGH coins per block
```

### Mining Difficulty

- **Difficulty 1**: Hash must start with "0"
- **Difficulty 2**: Hash must start with "00" (current setting)
- **Difficulty 3**: Hash must start with "000"
- Higher difficulty = more computational work required

## Testing

Run the test script to verify the implementation:

```bash
python test_decentralized_mining.py
```

This will:
1. Add sample transactions
2. Test mining with different miners
3. Validate the blockchain
4. Display statistics

## How Mining Works

### Step-by-Step Process

1. **Transaction Collection**: Transactions are added to the pending pool
2. **Mining Trigger**: Mining starts when minimum transactions are reached
3. **Nonce Iteration**: Miners try different nonce values (0, 1, 2, ...)
4. **Hash Calculation**: For each nonce, calculate SHA256 hash
5. **Difficulty Check**: Check if hash starts with required zeros
6. **Block Creation**: First valid hash creates the block
7. **Reward**: Miner receives MGH coins

### Example Mining

```python
# Block data: "Alice sends 10 MGH to Bob | previous_hash | 42"
# Nonce: 42
# Hash: "00f8a9..." (starts with "00" - meets difficulty 2)
# Result: Block mined successfully!
```

## Blockchain Structure

### Block Format

```json
{
  "index": 1,
  "hash": "00f8a9b2c3d4e5f6...",
  "transactions": ["Alice sends 10 MGH to Bob"],
  "nonce": 42,
  "miner": "miner_A",
  "timestamp": 1640995200.0,
  "previous_hash": "5edce08c5f27ec457650b62fa85c121de34579a8a9b9d0ecbeb13578f1f4f666"
}
```

### Genesis Block

The first block is automatically created with:
- Previous hash: "Genesis Block"
- Transaction: "Genesis Transaction"
- Miner: "Genesis"

## Security Features

- **Immutable Blocks**: Once mined, blocks cannot be modified
- **Hash Chaining**: Each block references the previous block's hash
- **Proof of Work**: Computational work required for block creation
- **Validation**: Blockchain integrity can be verified

## Future Enhancements

- ✅ Wallet management (Public/Private key pairs)
- ✅ Balance tracking per wallet
- ✅ Digital signatures for transactions
- [ ] Dynamic difficulty adjustment
- [ ] Transaction fees
- [ ] Network consensus
- [ ] Block size limits
- [ ] Mining pools
- [ ] WebSocket support for real-time updates
