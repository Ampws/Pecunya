import asyncio
import os
from Home.celery import app as celery_app
from BlockchainListener.blockchain_listener import BlockchainListener

import logging
logger = logging.getLogger(__name__)

@celery_app.task()
def listen_to_blockchain_task():
    logger.info("test0")
    if os.name == 'nt':
        logger.info('test1')
        loop = asyncio.new_event_loop()
        logger.info('test2')
        asyncio.set_event_loop(loop)
        logger.info('test3')
    else:
        loop = asyncio.get_event_loop()
    
    logger.info("test4")
    listener = BlockchainListener()
    logger.info("test5")
    loop.run_until_complete(listener.listen_to_blockchain())
    logger.info("test6")
