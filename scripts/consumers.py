# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
from django.conf import settings
from channels.db import database_sync_to_async
import asyncio

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
        print(message)
        await self.channel_layer.group_send(
            "run_script",
            {
                "type": "chat.message",
                "message": message,
            },
        )
        # Perform any necessary actions with the received message data here
        # Use the REDIS_HOST setting variable
        #redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        #redis_client.publish('script_agent', json.dumps(message))
        # Perform any necessary actions with the received message data here
        await self.process_message(message)

    async def process_message(self, message):
        # Use the REDIS_HOST setting variable
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        redis_client.publish('script_agent', json.dumps(message))

        # Wait for a response on the Redis channel before sending a WebSocket message
        response = await self.wait_for_response()
        await self.send(json.dumps({
            "message": "Task completed successfully",
            "response": response
        }))

    async def wait_for_response(self, timeout=30):
        # Use database_sync_to_async to await Redis response
        # Wait for a response on the Redis channel and return it
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        pubsub = redis_client.pubsub()
        pubsub.subscribe('script_agent')  # Subscribe to "script_agent_response" channel
        response_queue = asyncio.Queue()
        
        async def consume_response():
            while True:
                response = pubsub.get_message()
                print(response)
                if response and 'data' in response:
                    try:
                        response_json = json.loads(response['data'].decode('utf-8'))
                        await response_queue.put(response_json)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                    # Handle non-JSON message or any decoding error
                        pass
                await asyncio.sleep(0.1)
        response_queue = asyncio.Queue()
        consume_task = asyncio.ensure_future(consume_response())

        try:
            return await asyncio.wait_for(response_queue.get(), timeout=timeout)
        except asyncio.TimeoutError:
            return {"error": "Timeout: No response received"}
        finally:
            consume_task.cancel()



    #def wait_for_response(self):
        # Use database_sync_to_async to await Redis response
        # Wait for a response on the Redis channel and return it
   #     redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
   #     pubsub = redis_client.pubsub()
   #     pubsub.subscribe('script_agent')
   #     response = pubsub.get_message(timeout=30)  # Adjust the timeout as needed
   #     print(response)
   #     if response:
   #         print(response)
   #         return json.loads(response['data'])
   #     else:
   #         return {"error": "No response received"}

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

