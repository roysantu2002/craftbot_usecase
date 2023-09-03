from django.urls import re_path
from scripts import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.ScriptConsumer.as_asgi())
]
