import asyncio
from web3 import AsyncWeb3
from web3.providers import WebsocketProviderV2

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
      "topics": ["0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"]})

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