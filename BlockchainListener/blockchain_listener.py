import asyncio
import signal
from django.conf import settings
from web3 import AsyncWeb3
from web3.providers import WebsocketProviderV2

class BlockchainListener(object):
    def __init__(self):
        self.bsc_rpc_wss = f'wss://{settings.RPC_URLS.get("RPC_BSC")}'
        self.shutdown = asyncio.Event()
        self.subscription_id = None

    async def listen_to_blockchain(self):
        async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(self.bsc_rpc_wss)) as w3:
            self.subscription_id = await w3.eth.subscribe("logs", {"topics": ["0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0"]})
            print(f"Subscribed to new blocks with ID: {self.subscription_id}")

            unsubscribed = False
            while not unsubscribed:
                print("Listening to new blocks...")
                async for response in w3.ws.listen_to_websocket():
                    self.handle_new_pending_transaction(response)

                    if self.should_cancel_subscription(response):
                        unsubscribed = await w3.eth.unsubscribe(self.subscription_id)
                        break

    def handle_new_pending_transaction(self, event_data):
        print(f"New pending transaction: {event_data}")
        if self.should_trigger_token_signal(event_data):
            # 在这里触发信号或其他处理逻辑
            pass

    def handle_signal(self):
        print("Received Ctrl+C signal, stopping...")
        self.stop()

    def should_trigger_token_signal(self, event_data):
        # 根据事件数据判断是否触发信号
        return False

    def should_cancel_subscription(self, event_data):
        return self.shutdown.is_set()

    async def run(self):
        await self.listen_to_blockchain()

    def start(self):
        loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame), self.handle_signal)
        loop.run_until_complete(self.run())

    def stop(self):
        self.shutdown.set()
        if self.subscription_id:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.unsubscribe())

    async def unsubscribe(self):
        if self.subscription_id:
            w3 = AsyncWeb3(WebsocketProviderV2(self.bsc_rpc_wss))
            await w3.eth.unsubscribe(self.subscription_id)
