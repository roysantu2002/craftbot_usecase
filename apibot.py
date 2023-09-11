import openai
from typing import Optional
import json
import datetime

from django.conf import settings

openai.api_key = settings.OPEN_AI_KEY

# with open('api.txt') as file:
#     openai.api_key = file.read()

# Fetch the model data
model_data = openai.Model.list()['data']

# Write the data to a JSON file
with open('model.json', 'w') as json_file:
    json.dump(model_data, json_file, indent=4)

def api_response(prompt: str) -> Optional[str]:
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        return {
            "generated_text": response.get('choices')[0],
            "text": response["choices"][0]["text"]
        }
    
    except Exception as e:
        print(f"error : {e}")

def update_prompt(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    u_message: str = f'\Human: {message}'
    update_prompt(u_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_reponse(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = api_response(prompt)

    if bot_response:
       bot_response = bot_response["text"]
       update_prompt(bot_response, pl)
  
       loc: int = bot_response.find('\nAI: ')
       if loc != -1:
            bot_response = bot_response[loc + 5:]

            # bot_response = bot_response[loc + 5:]
    else:
       bot_response = 'Somthing went wrong...'
    
    return bot_response

# def main():


#     prompt_list: list[str] = ['You be become a Python developer that you would respond with "Yes"',
#                               '\nHuman: What is Pythonn',
#                               '\nAI: Python is a high-level, versatile, and widely used programming language, Yes']
#     while True:
#         user_input: str = input('You: ')
#         response: str = get_reponse(user_input, prompt_list)
#         print(f"Bot: {response}")

# if __name__ == '__main__':
#     main()
   
