from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from core.consumers import BaseConsumer

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Auth Bearer b14asj4r2od... { "name": "Bob" }
            path('ws_connect', BaseConsumer.as_asgi()),
        ]),
    ),
})
