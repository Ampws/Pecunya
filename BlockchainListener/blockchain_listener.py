import asyncio
import logging

from asgiref.sync import sync_to_async
from django.apps import apps
from django.conf import settings
from tenacity import retry, stop_after_attempt, stop_never, wait_fixed
from web3 import AsyncWeb3, Web3
from web3.providers import WebsocketProviderV2
from web3.providers.async_rpc import AsyncHTTPProvider

from redis_utils import redis_manager

class BlockchainListener(object):
    def __init__(self):
        self.erc_rpc_https = f'https://{settings.RPC_URLS.get("RPC_ERC")}'
        self.erc_rpc_wss = f'wss://{settings.RPC_URLS.get("RPC_ERC")}'
        self.logger = logging.getLogger(__name__)
        self.semaphore = asyncio.Semaphore(3)
        self.subscription_id = None
        self.shutdown = asyncio.Event()
        self.EthereumTransaction = apps.get_model('BlockchainListener', 'EthereumTransaction')
        self.EthereumTransaction_fields = [f.name for f in self.EthereumTransaction._meta.fields]
        self.logger.info(f'filter_fields: {self.EthereumTransaction_fields}')

    @retry(stop=stop_never, wait=wait_fixed(5))
    async def listen_to_blockchain(self):
        self.logger.info("Started listening to the blockchain")
        # await self.fill_missing_blocks()

        async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(self.erc_rpc_wss)) as w3:
            self.subscription_id = await w3.eth.subscribe("newHeads")
            self.logger.info(f"Subscribed to new blocks with ID: {self.subscription_id}")

            # last_block_number = await self.get_last_block_number_from_db()
            # self.logger.info(f"Last block number in DB: {last_block_number}")
            
            unsubscribed = False
            while not unsubscribed:
                try:
                    self.logger.info("Listening to new blocks...")
                    async for response in w3.ws.listen_to_websocket():
                        block_number = response["result"]["number"]
                        self.logger.info(f"Received block number: {block_number}")
                        # if block_number - last_block_number > 1:
                        #     await self.fill_missing_blocks(last_block_number + 1, block_number - 1)
                        # last_block_number = block_number
                        self.logger.info(f'{response}')
                        await asyncio.create_task(self.handle_new_block(response))

                        if self.should_cancel_subscription(response):
                            unsubscribed = await w3.eth.unsubscribe(self.subscription_id)
                            self.logger.info(f"Unsubscribed from blocks with ID: {self.subscription_id}")
                            break
                except Exception as e:
                    self.logger.error(f"WebSocket error: {e}. Trying to reconnect...")
                    raise

        self.logger.info("Ended listening to the blockchain")

    async def fill_missing_blocks(self, start_block=None, end_block=None):
        if not start_block or not end_block:
            min_block, max_block = await self.get_min_max_block_numbers_from_db()
        else:
            min_block, max_block = start_block, end_block
        for block_number in range(min_block, max_block + 1):
            async with self.semaphore:
                block_data = await self.fetch_block_data(block_number)
                await asyncio.create_task(self.handle_new_block(block_data))

    async def fetch_block_data(self, block_number):
        w3 = AsyncWeb3(AsyncHTTPProvider(self.erc_rpc_https))
        return await w3.eth.get_block(block_number, full_transactions=True)

    async def get_min_max_block_numbers_from_db(self):
        min_block = await sync_to_async(self.EthereumTransaction.objects.order_by('blockNumber').first)()
        max_block = await sync_to_async(self.EthereumTransaction.objects.order_by('-blockNumber').first)()
        return min_block.blockNumber if min_block else None, max_block.blockNumber if max_block else None

    async def get_last_block_number_from_db(self):
        _, max_block = await self.get_min_max_block_numbers_from_db()
        return max_block or 0

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    async def handle_new_block(self, event_data):
        try:
            block_hash = event_data['result']['hash']
            transactions_to_create = []

            if block_hash:
                w3 = AsyncWeb3(AsyncHTTPProvider(self.erc_rpc_https))
                block_detail = await w3.eth.get_block(block_hash, full_transactions=True)

                for transaction in block_detail['transactions']:
                    transaction_data = {}

                    for key, value in transaction.items():
                        if key not in self.EthereumTransaction_fields:
                            pass
                        elif key in ['hash', 'blockHash']:
                            transaction_data[key] = self.bytes_to_hex(value)
                        elif key == 'from':
                            transaction_data['tx_from'] = value
                        elif key == 'input':
                            try:
                                transaction_data[key] = value[:10]
                            except:
                                transaction_data[key] = value
                        else:
                            transaction_data[key] = value

                    transactions_to_create.append(self.EthereumTransaction(**transaction_data))

            await sync_to_async(self.EthereumTransaction.objects.bulk_create)(transactions_to_create)
        except Exception as e:
            self.logger.exception("Error in handle_new_block: %s", e)

    @staticmethod
    def bytes_to_hex(b):
        return Web3.to_hex(b)
    
    def should_trigger_token_signal(self, event_data):
        return False

    def should_cancel_subscription(self, event_data):
        return self.shutdown.is_set()

    async def unsubscribe(self):
        if self.subscription_id:
            async with AsyncWeb3(WebsocketProviderV2(self.erc_rpc_wss)) as w3:
                await w3.eth.unsubscribe(self.subscription_id)
