from daphne.server import ProtocolTypeRouter, get_asgi_application

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),  # WSGI application
        "websocket": get_asgi_application(),  # ASGI application
    }
)

