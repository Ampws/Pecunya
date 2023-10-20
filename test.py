import asyncio
from web3 import AsyncWeb3
from web3.providers.websocket.websocket_v2 import WebsocketProviderV2

LOG = True  # toggle debug logging
if LOG:
    import logging
    logger = logging.getLogger("web3.providers.WebsocketProviderV2")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

async def ws_v2_subscription_context_manager_example():
    async with AsyncWeb3.persistent_websocket(
        WebsocketProviderV2(f"wss://eth-mainnet.g.alchemy.com/v2/KOsuCAAN_FD8IBJUaOwKjme3WmI6-Hgw")
    ) as w3:
        # subscribe to new block headers
        subscription_id = await w3.eth.subscribe("logs", {"address": "0x8320fe7702b96808f7bbc0d4a888ed1468216cfd",
      "topics": ["0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"]}) # type: ignore

       # async for response in w3.ws.listen_to_websocket():
        #    print(f"{response}\n")
            # handle responses here

        # still an open connection, make any other requests and get
        # responses via send / receive
        #latest_block = await w3.eth.get_block("latest")
        #print(f"Latest block: {latest_block}")

        # the connection closes automatically when exiting the context
        # manager (the `async with` block)

asyncio.run(ws_v2_subscription_context_manager_example())
from web3 import Web3

# 连接到以太坊节点
# w3 = Web3(Web3.HTTPProvider('https://weathered-multi-sky.bsc.discover.quiknode.pro/fe83dcbbff5d28b5c5f5623093e8330dfcca9960/'))

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
hash = Web3.keccak(text='setMaxTxnAmount(uint256)').hex()
# hash = Web3.keccak(text='OwnershipTransferred(address,address)').hex()
print(hash)

import re
url = 'socks5://biao0588:biao1013@hk10b.amazonip.net:61884'
print(re.match(r'socks5://(?:\S+:\S+@)?\S+:\d+', url))
if re.match(r'socks5://(?:\S+:\S+@)?\S+:\d+', url):
    print(1)
