from asgiref.sync import sync_to_async
import asyncio
from django.apps import apps
from django.conf import settings
import logging
from web3 import AsyncWeb3
from web3.providers import WebsocketProviderV2
from web3.providers.async_rpc import AsyncHTTPProvider

class BlockchainListener(object):
    def __init__(self):
        self.erc_rpc_https = f'https://{settings.RPC_URLS.get("RPC_ERC")}'
        self.erc_rpc_wss = f'wss://{settings.RPC_URLS.get("RPC_ERC")}'
        self.logger = logging.getLogger(__name__)
        self.ethereum_transaction_keys = []
        self.subscription_id = None
        self.shutdown = asyncio.Event()

    async def listen_to_blockchain(self):
        async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(self.erc_rpc_wss)) as w3:
            # self.subscription_id = await w3.eth.subscribe("logs", {"topics": ["0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0"]})
            self.subscription_id = await w3.eth.subscribe("newHeads")
            self.logger.info(f"Subscribed to new blocks with ID: {self.subscription_id}")

            unsubscribed = False
            while not unsubscribed:
                self.logger.info("Listening to new blocks...")
                async for response in w3.ws.listen_to_websocket():
                    await asyncio.create_task(self.handle_new_block(response))

                    if self.should_cancel_subscription(response):
                        unsubscribed = await w3.eth.unsubscribe(self.subscription_id)
                        break

    async def handle_new_block(self, event_data):

        def bytes_to_hex(b):
            return b.hex()

        try:
            EthereumTransaction = apps.get_model('BlockchainListener', 'EthereumTransaction')
            if not self.ethereum_transaction_keys:
                self.ethereum_transaction_keys = ['from' if field.name == 'tx_from' else field.name for field in EthereumTransaction._meta.get_fields()]
            self.logger.info(self.ethereum_transaction_keys)

            block_hash = event_data['result']['hash']
            transactions_to_create = []

            if block_hash:
                w3 = AsyncWeb3(AsyncHTTPProvider(self.erc_rpc_https))
                block_detail = await w3.eth.get_block(block_hash, full_transactions=True)

                for transaction in block_detail['transactions']:
                    transaction_data = {key: transaction[key] for key in self.ethereum_transaction_keys if key in transaction}
                    transaction_data["tx_from"] = transaction_data.pop("from", None)
                    self.logger.info(f'value: {transaction_data["value"]}')
                    for field in ['hash', 'blockHash', 'r', 's']:
                        if field in transaction_data:
                            transaction_data[field] = bytes_to_hex(transaction_data[field])
                    transactions_to_create.append(EthereumTransaction(**transaction_data))

            await sync_to_async(EthereumTransaction.objects.bulk_create)(transactions_to_create)
        except Exception as e:
            self.logger.exception("Error in handle_new_block: %s", e)

    def should_trigger_token_signal(self, event_data):
        return False

    def should_cancel_subscription(self, event_data):
        return self.shutdown.is_set()

    async def unsubscribe(self):
        if self.subscription_id:
            async with AsyncWeb3(WebsocketProviderV2(self.erc_rpc_wss)) as w3:
                await w3.eth.unsubscribe(self.subscription_id)
