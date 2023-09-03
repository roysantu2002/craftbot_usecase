"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from scripts.consumers import ScriptConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = get_asgi_application()

ws_patterns= [

         path("ws/scriptchat/run_script/", ScriptConsumer.as_asgi()),
]

application= ProtocolTypeRouter({

    'websocket' : URLRouter(ws_patterns)


})
