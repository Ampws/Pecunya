from web3 import Web3

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('https://weathered-multi-sky.bsc.discover.quiknode.pro/fe83dcbbff5d28b5c5f5623093e8330dfcca9960/'))

# 交易哈希
tx_hash = '0x182227bccbc79099cfc25ad700c6864e238c9376d6b47688cce01e41adb53754'

# 使用 JSON-RPC 查询交易详情
try:
    tx_details = w3.eth.get_transaction_receipt(tx_hash)
    print(tx_details)
except Exception as e:
    print(f"查询交易详情时出错：{e}")
