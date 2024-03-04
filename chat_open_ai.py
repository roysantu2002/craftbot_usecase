from openai import OpenAI

client = OpenAI(api_key=settings.OPEN_AI_KEY)
from typing import Optional
import json
import datetime

from django.conf import settings

class ChatGPT:
    def __init__(self):
        self.pl = []

        # Fetch the model data
        self.model_data = client.models.list()['data']

        print(self.model_data)

        # Write the data to a JSON file
        with open('model.json', 'w') as json_file:
            json.dump(self.model_data, json_file, indent=4)

    def api_response(self, prompt: str) -> Optional[str]:
        try:
            response = client.completions.create(model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:'])

            return {
                "generated_text": response.choices[0],
                "text": response.choices[0].text
            }

        except Exception as e:
            print(f"error : {e}")

    def create_prompt(self, message: str) -> str:
        u_message: str = f'Human: {message}'
        self.update_prompt(u_message)
        prompt: str = ''.join(self.pl)
        return prompt

    def update_prompt(self, message: str):
        self.pl.append(message)

    def get_response(self, message: str) -> str:
        prompt: str = self.create_prompt(message)
        bot_response: str = self.api_response(prompt)

        if bot_response:
            bot_response = bot_response["text"]
            self.update_prompt(bot_response)

            loc: int = bot_response.find('\nAI: ')
            if loc != -1:
                bot_response = bot_response[loc + 5:]

        else:
            bot_response = 'Something went wrong...'

        return bot_response
