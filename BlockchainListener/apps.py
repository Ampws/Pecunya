# import asyncio
# import threading
from django.apps import AppConfig

# from BlockchainListener.blockchain_listener import BlockchainListener

# def run_async_code():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         loop.run_until_complete(BlockchainListener().listen_to_blockchain())
#     finally:
#         loop.close()

class BlockchainlistenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BlockchainListener'

    # def ready(self):
    #     if not hasattr(self, 'listener_started'):
    #         self.listener_started = True
    #         thread = threading.Thread(target=run_async_code)
    #         thread.daemon = True
    #         thread.start()
    # def ready(self):
    #     BlockchainListener().listen_to_blockchain_task.delay()