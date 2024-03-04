import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis
from django.conf import settings
from channels.db import database_sync_to_async
import asyncio
from scripts.models import NetworkKeyword
from fuzzywuzzy import fuzz
import httpx  # Make sure to install this library
import os

import json
from difflib import get_close_matches
from typing import List, Optional
from apibot import get_reponse


def load_knowledge_data(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_data(file_path: str, data: dict):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
     matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
     return matches[0] if matches else None

def get_best_possible_answer(question: str, knowledge_data: dict) -> Optional[str]:
    for q in knowledge_data['keywords']:
         if q["keyword"] == question:
              return q["category"]
         

class ScriptConsumer(AsyncWebsocketConsumer):
   

    async def connect(self):
        self.previous_message = None  # Initialize the previous_message variable

        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:8000/api/scripts/keyword-lists/')

            # Extract keywords and categories
            data = response.json()
            # print(data)
            keywords = [{"id": entry["id"], "keyword": entry["keyword"], "category": entry["category"]} for entry in data]
            # Create a JSON object with the "keywords" list
            keywords_json = {"keywords": keywords}
            # print(keywords_json)

            # Read the existing JSON data from the "keywords.json" file, if it exists
            try:
                with open("keywords.json", "r") as infile:
                    existing_data = json.load(infile)
                    existing_keywords = existing_data.get("keywords", [])
            except FileNotFoundError:
                existing_keywords = []

            # Merge the new keywords with the existing data, avoiding duplicates
            for keyword in keywords:
                if keyword not in existing_keywords:
                    existing_keywords.append(keyword)

            # Create a JSON object with the merged "keywords" list
            merged_keywords_json = {"keywords": existing_keywords}

            # Write the merged JSON data to "keywords.json" in the current working directory with proper indentation
            with open("keywords.json", "w") as outfile:
                json.dump(merged_keywords_json, outfile, indent=4)

            # print("Merged JSON data saved to 'keywords.json'")

            # if response.status_code == 200:
            #     network_keywords = json.loads(response.text)
            #     # Extract the "keyword" values from the list of dictionaries
            #     network_keywords = [item["keyword"] for item in network_keywords]

        # async with httpx.AsyncClient() as client:
        #     response = await client.get('http://localhost:8000/api/scripts/keyword-lists/')

        #     # Extract keywords and categories
        #     data = response.json()
        #     # print(data)
        #     keywords = [{"id": entry["id"], "keyword": entry["keyword"], "category": entry["category"]} for entry in data]
        #     # Create a JSON object with the "keywords" list
        #     keywords_json = {"keywords": keywords}
        #     print(keywords_json)

        #     # Write the JSON data to "keywords.json" in the current working directory with proper indentation
        #     with open("keywords.json", "w") as outfile:
        #         json.dump(keywords_json, outfile, indent=4)

        #     print("New JSON data saved to 'keywords.json'")
        
        #     if response.status_code == 200:
        #         network_keywords = json.loads(response.text)
        #        # Extract the "keyword" values from the list of dictionaries
        #         network_keywords = [item["keyword"] for item in network_keywords]
                
        # Get the channel name from the URL path, e.g., /ws/run_script/ or /ws/other_channel/
        channel_name = self.scope['url_route']['kwargs']['channel_name']
        print('line105')
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
        self.previous_message = text_data  # Store the previous message
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

        # await self.send(json.dumps({
        #     "message": "Wait let me check",
        # }))
      
    
        
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
        # print('insdie process_message')
        knowledge_data: dict = load_knowledge_data('keywords.json')
        # print(knowledge_data)

        best_match: Optional[str] = find_best_match(message, [q['keyword'] for q in knowledge_data['keywords']])

        if best_match:
               answer: str = get_best_possible_answer(best_match, knowledge_data)
               await self.send_script_name(f'AI: {answer}')
            #    print(f'NetGeni: {answer}')
        else:
            prompt_list: list[str] = ['You be become a Python developer that you would respond with "Yes"',
                '\nHuman: What is Python',
                '\nAI: Python is a high-level, versatile, and widely used programming language, Yes']
            # while True:
            #     user_input: str = input('You: ')
            response: str = get_reponse(message, prompt_list)
            print(f"Bot: {response}")
            await self.send_script_name(f'AI: {response}')
            # print('NetGeni: I don\'t have the script, shall I learn from you?')
            new_answer: str = message
            if message.lower() != 'ask':
                 message_dict = json.loads(self.previous_message)  # Parse the JSON string into a dictionary
                 hello_text = message_dict.get("message", "")  # Get t
    
                #  message_str = str(self.previous_message.message)
                 knowledge_data["keywords"].append({"keyword": hello_text, "category": response})
                 save_knowledge_data('keywords.json', knowledge_data)
                 await self.send_script_name("AI: Thank you! I learned from you to help others!")

        
        # await self.send(json.dumps({
        #     "message": "Wait let me check",
        # }))
        # Wait for a response on the Redis channel before sending a WebSocket message
        # response = await self.wait_for_response(channel_name)
        # await self.send(json.dumps({
        #     "message": "Wait let me check",
        #     "response": response
        # }))

        # async with httpx.AsyncClient() as client:
        #     response = await client.get('http://localhost:8000/api/scripts/keyword-lists/')

        #     # Extract keywords and categories
        #     data = response.json()
        #     # print(data)
        #     keywords = [{"id": entry["id"], "keyword": entry["keyword"], "category": entry["category"]} for entry in data]
        #     # Create a JSON object with the "keywords" list
        #     keywords_json = {"keywords": keywords}
        #     print(keywords_json)

        #     # Write the JSON data to "keywords.json" in the current working directory with proper indentation
        #     with open("keywords.json", "w") as outfile:
        #         json.dump(keywords_json, outfile, indent=4)

        #     print("New JSON data saved to 'keywords.json'")
        
        #     if response.status_code == 200:
        #         network_keywords = json.loads(response.text)
        #        # Extract the "keyword" values from the list of dictionaries
        #         network_keywords = [item["keyword"] for item in network_keywords]
   

        # script_name = "I don't have"  # Default message
        # print(network_keywords)

        # for keyword in network_keywords:
        #     if keyword.lower() in message:
        #     # Calculate a matching score for the keyword and the message
        #     # score = fuzz.token_sort_ratio(keyword.lower(), message)

        #     # if score >= 80:  # Adjust the threshold as needed
        #         await self.send_script_name(keyword)
        #         return  # Stop searching if a keyword is found

        # if matched_keywords:
        #     # Sort the matched keywords by score in descending order
        #     matched_keywords.sort(key=lambda x: x[1], reverse=True)

            # Send the script name with the highest score to the WebSocket client
            # self.send_script_name(matched_keywords[0][0])
        # else:
        #     # If no matching keyword is found, send the default message
        #  await self.send(text_data=json.dumps({
        #     "message": f"sorry did not find any scripts related to {message}",
        # }))

        # self.send_script_name(script_name)

    # @database_sync_to_async
    # def get_keywords_from_db(self):
    #         # Perform your database query here
    #         return NetworkKeyword.objects.all()

    async def send_script_name(self, script_name):
        print(script_name)
        await self.send(text_data=json.dumps({
            "message": script_name,
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
