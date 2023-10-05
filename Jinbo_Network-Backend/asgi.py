import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from BlockchainListener.routing import websocket_urlpatterns as BlockchainListener_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jinbo_Network-Backend.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            BlockchainListener_websocket_urlpatterns
        )
    ),
})