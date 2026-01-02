import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Number of leading zeros required

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return computed_hash

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

def main():
    print("--- PyChain v1.0 ---")
    blockchain = Blockchain()
    
    print("Mining block 1...")
    blockchain.add_block(Block(1, "", time.time(), {"amount": 4}))
    
    print("Mining block 2...")
    blockchain.add_block(Block(2, "", time.time(), {"amount": 10}))
    
    print("\nBlockchain Valid?", blockchain.is_chain_valid())
    
    print("\n[Chain Details]")
    for block in blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Hash: {block.hash}")
        print(f"Prev: {block.previous_hash}")
        print(f"Data: {block.data}")
        print("-" * 30)

if __name__ == "__main__":
    main()
