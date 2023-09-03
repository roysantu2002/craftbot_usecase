# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
from django.conf import settings

class ScriptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the "run_script" room
        await self.channel_layer.group_add("run_script", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the "run_script" room
        await self.channel_layer.group_discard("run_script", self.channel_name)

    async def receive(self, text_data):
        # Broadcast the received message to the "run_script" room
        message = json.loads(text_data)["message"]
        await self.channel_layer.group_send(
            "run_script",
            {
                "type": "chat.message",
                "message": message,
            },
        )
        # Perform any necessary actions with the received message data here
        # Use the REDIS_HOST setting variable
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        redis_client.publish('script_agent', json.dumps(message))

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

