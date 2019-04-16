import datetime
import hashlib

# This is the block which should essentially store data, pointer to the next block,
# the previous hash and its own hash.
class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    
    # We would use this timestamp to synchronize the blockchain over the network
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data
    # We define the hash function || This should take sometime to avoid intruders
    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()
    # We will return this string to print out our blockchain
    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"

class Blockchain:

    # If we set this to zero, every single block will be accepted
    diff = 20

    # The maximum number you can store in 32 bit number
    maxNonce = 2**32
    target = 2 ** (256-diff)
    
    # The first block is called Genesis
    block = Block("Genesis")

    # We add dummy to avoid changing the head any time block is changed because python pass
    # variable by reference
    dummy = head = block

    # Blockchain is a linkedlist, so will add the new block at the beginning or head
    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        # We point to the new block, and we move the next pointer up, so we can continue to add the list
        self.block.next = block
        self.block = self.block.next

    # To make sure we add a blockhash in our blockchain
    # # We make sure the value of a blockhash is less than a specific target number
    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1

blockchain = Blockchain()

# Generate 10 random block chains
for n in range(10):
    blockchain.mine(Block("Block " + str(n+1)))

while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next
