import asyncio
import os
from Home.celery import app as celery_app
from BlockchainListener.blockchain_listener import BlockchainListener

import logging
logger = logging.getLogger(__name__)

@celery_app.task()
def listen_to_blockchain_task():
    if os.name == 'nt':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    
    listener = BlockchainListener()
    loop.run_until_complete(listener.listen_to_blockchain())
