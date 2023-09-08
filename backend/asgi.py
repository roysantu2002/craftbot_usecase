import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from scripts.consumers import ScriptConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# Define a list of allowed channel names
allowed_channels = ["scripts", "booking", "writing"]

# WSGI application
wsgi_application = get_asgi_application()

# WebSocket (ASGI) routing
def custom_ws_routing(application):
    async def application_scope(scope, receive, send):
        # Get the channel name from the scope
        channel_name = scope['url_route']['kwargs']['channel_name']
        
        # Check if the requested channel is in the list of allowed channels
        if channel_name in allowed_channels:
            # If the channel is allowed, continue with the consumer
            return await application(scope, receive, send)
        else:
            # If the channel is not allowed, reject the connection
            await send({
                'type': 'websocket.close',
                'code': 403,  # Forbidden
            })

    return application_scope


# WebSocket (ASGI) routing
ws_patterns = [
      path("ws/netgeni/<str:channel_name>/", ScriptConsumer.as_asgi()),
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

