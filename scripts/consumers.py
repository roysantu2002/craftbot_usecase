import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
from django.conf import settings
from channels.db import database_sync_to_async
import asyncio
from scripts.models import NetworkKeyword
from fuzzywuzzy import fuzz
import httpx  # Make sure to install this library


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

        await self.send(json.dumps({
            "message": "Wait let me check",
        }))
      
    
        
        # Perform any necessary actions with the received message data here
        await self.process_message(message, channel_name)
    
    # def find_matching_script(self, message):
    #     # Query the NetworkKeyword model to find a match in the message
    #     # Assuming your NetworkKeyword model has fields "keyword" and "script_name"
    #     keywords = NetworkKeyword.objects.all()

    #     for keyword in keywords:
    #         if keyword.keyword in message:
    #             return keyword.script_name

    #     return None


    async def process_message(self, message, channel_name):
        # Use the REDIS_HOST setting variable
        redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        redis_client.publish(channel_name, json.dumps(message))
        # await self.send(json.dumps({
        #     "message": "Wait let me check",
        # }))
        # Wait for a response on the Redis channel before sending a WebSocket message
        # response = await self.wait_for_response(channel_name)
        # await self.send(json.dumps({
        #     "message": "Wait let me check",
        #     "response": response
        # }))

        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:8000/api/scripts/keyword-lists/')
        
            if response.status_code == 200:
                network_keywords = json.loads(response.text)
               # Extract the "keyword" values from the list of dictionaries
                network_keywords = [item["keyword"] for item in network_keywords]
   

        script_name = "I don't have"  # Default message
        print(network_keywords)

        for keyword in network_keywords:
            if keyword.lower() in message:
            # Calculate a matching score for the keyword and the message
            # score = fuzz.token_sort_ratio(keyword.lower(), message)

            # if score >= 80:  # Adjust the threshold as needed
                await self.send_script_name(keyword)
                return  # Stop searching if a keyword is found

        # if matched_keywords:
        #     # Sort the matched keywords by score in descending order
        #     matched_keywords.sort(key=lambda x: x[1], reverse=True)

            # Send the script name with the highest score to the WebSocket client
            # self.send_script_name(matched_keywords[0][0])
        else:
            # If no matching keyword is found, send the default message
         await self.send(text_data=json.dumps({
            "message": f"sorry did not find any scripts related to {message}",
        }))

        self.send_script_name(script_name)

    @database_sync_to_async
    def get_keywords_from_db(self):
            # Perform your database query here
            return NetworkKeyword.objects.all()

    async def send_script_name(self, script_name):
        print(script_name)
        await self.send(text_data=json.dumps({
            "message": f"I found something related to {script_name}",
        }))
    

    async def wait_for_response(self, channel_name, timeout=30):
        print(channel_name)
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
