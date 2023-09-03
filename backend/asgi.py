import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from scripts.consumers import ScriptConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# WSGI application
wsgi_application = get_asgi_application()

# WebSocket (ASGI) routing
ws_patterns = [
    path("ws/scriptchat/run_script/", ScriptConsumer.as_asgi()),
]

# ASGI application
asgi_application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})

# Combined ASGI and WSGI application
application = ProtocolTypeRouter({
    'http': wsgi_application,
    'websocket': asgi_application
})

