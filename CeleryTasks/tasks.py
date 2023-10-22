import asyncio
from Home.celery import app as celery_app
from BlockchainListener.blockchain_listener import BlockchainListener

@celery_app.task(bind=True)
def listen_to_blockchain_task():
    listener = BlockchainListener()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listener.listen_to_blockchain())
