import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
from django.conf import settings
from channels.db import database_sync_to_async
import asyncio

class ScriptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the channel name from the URL path, e.g., /ws/run_script/ or /ws/other_channel/
        channel_name = self.scope['url_route']['kwargs']['channel_name']
        print(channel_name)
      
        
        # Join the specified room (channel)
        await self.channel_layer.group_add(channel_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Get the channel name from the URL path, e.g., /ws/run_script/ or /ws/other_channel/
        channel_name = self.scope['url_route']['kwargs']['channel_name']
        
        # Leave the specified room (channel)
        await self.channel_layer.group_discard(channel_name, self.channel_name)

    async def receive(self, text_data):
        # Get the channel name from the URL path, e.g., /ws/run_script/ or /ws/other_channel/
        channel_name = self.scope['url_route']['kwargs']['channel_name']
        
        # Broadcast the received message to the specified room (channel)
        message = json.loads(text_data)["message"]
        await self.channel_layer.group_send(
            channel_name,
            {
                "type": "chat.message",
                "message": message,
            },
        )
        
        # Perform any necessary actions with the received message data here
        await self.process_message(message, channel_name)

    async def process_message(self, message, channel_name):
        # Use the REDIS_HOST setting variable
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        redis_client.publish(channel_name, json.dumps(message))
        
        # Wait for a response on the Redis channel before sending a WebSocket message
        response = await self.wait_for_response(channel_name)
        await self.send(json.dumps({
            "message": "Task completed successfully",
            "response": response
        }))

    async def wait_for_response(self, channel_name, timeout=30):
        # Use database_sync_to_async to await Redis response
        # Wait for a response on the Redis channel and return it
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        pubsub = redis_client.pubsub()
        pubsub.subscribe(channel_name)  # Subscribe to the specified channel
        response_queue = asyncio.Queue()
        
        async def consume_response():
            while True:
                response = pubsub.get_message()
                if response and 'data' in response:
                    try:
                        response_json = json.loads(response['data'].decode('utf-8'))
                        await response_queue.put(response_json)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        # Handle non-JSON message or any decoding error
                        pass
                await asyncio.sleep(0.1)
        
        consume_task = asyncio.ensure_future(consume_response())

        try:
            return await asyncio.wait_for(response_queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return {"error": "Timeout: No response received"}
        finally:
            consume_task.cancel()

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
