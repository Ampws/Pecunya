from django.apps import AppConfig

from BlockchainListener.blockchain_listener import BlockchainListener

class BlockchainlistenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BlockchainListener'

    def ready(self):
        BlockchainListener().start()