#!/usr/bin/env python3
"""
Test script for decentralized mining functionality
"""

import requests
import time
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"


def test_blockchain_api():
    """Test the blockchain API endpoints"""

    print("🚀 Testing MGH Blockchain API")
    print("=" * 50)

    # Test 1: Get root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 2: Get initial status
    print("\n2. Getting initial blockchain status...")
    response = requests.get(f"{BASE_URL}/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test 3: Add transactions
    print("\n3. Adding transactions...")
    transactions = [
        "Alice sends 10 MGH to Bob",
        "Bob sends 5 MGH to Charlie",
        "Charlie sends 3 MGH to David",
        "David sends 1 MGH to Alice",
    ]

    for transaction in transactions:
        response = requests.post(
            f"{BASE_URL}/transactions", json={"transaction": transaction}
        )
        print(f"Added transaction: {transaction}")
        print(f"Response: {response.json()}")

    # Test 4: Get pending transactions
    print("\n4. Getting pending transactions...")
    response = requests.get(f"{BASE_URL}/transactions/pending")
    print(f"Pending transactions: {response.json()}")

    # Test 5: Get mining info
    print("\n5. Getting mining information...")
    response = requests.get(f"{BASE_URL}/mining/info")
    print(f"Mining info: {response.json()}")

    # Test 6: Mine a block (Miner A)
    print("\n6. Mining block with Miner A...")
    response = requests.post(f"{BASE_URL}/mine", json={"miner_address": "miner_A"})
    print(f"Mining result: {response.json()}")

    # Test 7: Add more transactions
    print("\n7. Adding more transactions...")
    more_transactions = ["Eve sends 8 MGH to Frank", "Frank sends 2 MGH to Grace"]

    for transaction in more_transactions:
        response = requests.post(
            f"{BASE_URL}/transactions", json={"transaction": transaction}
        )
        print(f"Added transaction: {transaction}")

    # Test 8: Mine another block (Miner B)
    print("\n8. Mining block with Miner B...")
    response = requests.post(f"{BASE_URL}/mine", json={"miner_address": "miner_B"})
    print(f"Mining result: {response.json()}")

    # Test 9: Get all blocks
    print("\n9. Getting all blocks...")
    response = requests.get(f"{BASE_URL}/blocks")
    blocks = response.json()["blocks"]
    print(f"Total blocks: {len(blocks)}")

    for i, block in enumerate(blocks):
        print(
            f"Block {i}: Hash={block['hash'][:10]}..., Miner={block['miner']}, Transactions={len(block['transactions'])}"
        )

    # Test 10: Validate chain
    print("\n10. Validating blockchain...")
    response = requests.get(f"{BASE_URL}/validate")
    print(f"Validation result: {response.json()}")

    # Test 11: Get statistics
    print("\n11. Getting blockchain statistics...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Statistics: {response.json()}")

    print("\n✅ Testing completed!")


if __name__ == "__main__":
    try:
        test_blockchain_api()
    except requests.exceptions.ConnectionError:
        print(
            "❌ Error: Could not connect to the API. Make sure the server is running on http://localhost:8000"
        )
        print("To start the server, run: uvicorn app:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


