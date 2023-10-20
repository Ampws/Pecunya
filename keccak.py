from web3 import Web3
hash = Web3.keccak(text="OwnershipTransferred (index_topic_1 address previousOwner,index_topic_2 address newOwner)")
print(hash.hex())