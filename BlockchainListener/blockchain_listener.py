import logging
from django.conf import settings
from web3 import AsyncWeb3
from web3.providers.websocket.websocket_v2 import WebsocketProviderV2

class BlockchainListener(object):
    def __init__(self):
        self.bsc_rpc_wss = f'wss://{settings.RPC_URLS.get("RPC_BSC")}'
        self.logger = logging.getLogger(__name__)
        self.subscription_id = None

    async def listen_to_blockchain(self):
        async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(self.bsc_rpc_wss)) as w3:
            self.subscription_id = await w3.eth.subscribe("logs", {"topics": ["0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0"]}) # type: ignore
            print(f"Subscribed to new blocks with ID: {self.subscription_id}")
            self.logger.info(f"Subscribed to new blocks with ID: {self.subscription_id}")

            unsubscribed = False
            while not unsubscribed:
                print("Listening to new blocks...")
                self.logger.info("Listening to new blocks...")
                async for response in w3.ws.listen_to_websocket():
                    self.handle_new_pending_transaction(response)

                    if self.should_cancel_subscription(response):
                        unsubscribed = await w3.eth.unsubscribe(self.subscription_id)
                        break

    def handle_new_pending_transaction(self, event_data):
        print(f"New pending transaction: {event_data}")
        self.logger.info(f"New pending transaction: {event_data}")
        if self.should_trigger_token_signal(event_data):
            pass

    def should_trigger_token_signal(self, event_data):
        return False

    def should_cancel_subscription(self, event_data):
        return self.shutdown.is_set()

    async def unsubscribe(self):
        if self.subscription_id:
            w3 = AsyncWeb3(WebsocketProviderV2(self.bsc_rpc_wss))
            await w3.eth.unsubscribe(self.subscription_id)