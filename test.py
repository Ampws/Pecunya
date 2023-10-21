from web3 import Web3

# 连接到以太坊节点
RPC = 'https://radial-alpha-borough.discover.quiknode.pro/7fe337be1bf0dea3bcd2a91b2fa541de8c6c487f/'
w3 = Web3(Web3.HTTPProvider(RPC))

block_number = 0x118afe4
block_detail = w3.eth.get_block(block_number, full_transactions=True)

for transaction in block_detail['transactions']:
    print(list(transaction.keys()))

# 交易哈希
# tx_hash = '0x182227bccbc79099cfc25ad700c6864e238c9376d6b47688cce01e41adb53754'

# 使用 JSON-RPC 查询交易详情
# try:
#     tx_details = w3.eth.get_transaction_receipt(tx_hash)
#     print(tx_details)
# except Exception as e:
#     print(f"查询交易详情时出错：{e}")

# OwnershipTransferred (index_topic_1 address previousOwner, index_topic_2 address newOwner)View Source
# 0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0
# hash = Web3.keccak(text='transfer(address, uint256)').hex()
# hash = Web3.keccak(text='approve(address,uint256)').hex()
# hash = Web3.keccak(text='Transfer(address,address,uint256)').hex()
# hash = Web3.keccak(text='setMaxTxnAmount(uint256)').hex()
# hash = Web3.keccak(text='OwnershipTransferred(address,address)').hex()
# print(hash)