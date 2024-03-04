from openai import OpenAI

from typing import Optional
import json
import datetime

from django.conf import settings

client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPEN_AI_KEY,
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )

# client = OpenAI()
# client.api_key = settings.OPEN_AI_KEY
# # client = OpenAI(api_key=settings.OPEN_AI_KEY)

# Fetch the model data
response = client.models.list()
model_data = response.data
# model_data = client.Model.list()
# print('------')
# print(model_data)
# Write the data to a JSON file
with open('model.json', 'w') as json_file:
    # json.dump(model_data, json_file, indent=4)
    # Assuming 'data' is the key containing the list of models in the response

    json.dump(model_data, json_file, default=lambda x: x.__dict__, indent=4)

def api_response(prompt: str) -> Optional[str]:
    try:
        response = client.completions.create(model="davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        # temperature=0.9,
        # max_tokens=150,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0.6,
        stop=[' Human:', ' AI:'])

        return {
            "generated_text": response.choices[0],
            "text": response.choices[0].text
        }
    
    except Exception as e:
        print(f"error : {e}")


def create_prompt(message: str, pl: list[str]) -> str:
    u_message: str = f'\Human: {message}'
    update_prompt(u_message, pl)
    prompt: str = ''.join(pl)
    return prompt

# def create_messages(first_name_placeholder='{first_name}', last_name_placeholder='{last_name}', name_analysis_placeholder='{name_analysis}'):
#     messages = [
#         {
#             'role': 'system',
#             'content': f'You being a chaldean numerology expert, I provide a few alphabet combination for a first and last name, you need to use chaldean numerology table and provide a name analysis , you need to explain more about Positive, Negative, Career, relation compatibility, show the alphabet count, color, good days and more use this data, do not use Chaldean anywhere : {name_analysis_placeholder}.',
#         },
#         {
#             'role': 'user',
#             'content': f'Write a long and detailed SEO-friendly analysis blog post about {first_name_placeholder}, that targets the following comma-separated keywords: (First Name Analysis, Letters, Numeric Values, Total Numeric Value, Alphabet Count, Favorable color, Positive Traits, Negative Traits, Career, Relationship Compatibility, Good Days) {last_name_placeholder} same as {first_name_placeholder}, and then {name_analysis_placeholder} Summary . The response should be formatted in SEO-friendly HTML, limited to the following HTML tags: p, h1, h2, h3, h4, h5, h6, strong, i, ul, li, ol.',
#         },
#     ]
#     return messages

# # Example usage:
# placeholders = {
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'name_analysis': 'Name'
# }

# formatted_messages = create_messages(placeholders['first_name'], placeholders['last_name'], placeholders['name_analysis'])
# print(formatted_messages)

# Rewritten function
# def create_prompt(name: str, topic: str, keywords: str, pl: list[str]) -> str:
#     messages = [
#     {
#         'role': 'system',
#         'content': 'You being a chaldean numerology expert, I provide a few alphabet combination for a first and last name, you need to use chaldean numerology table and provide a name analysis , you need to explain more about Positive, Negative, Career, relation compatibility, show the alphabet count, color, good days and more use this data, do not use Chaldean anywhere : .',
#     },
#     {
#         'role': 'user',
#         'content': 'Write a long and detailed SEO-friendly analysis blog post about {name}, that targets the following comma-separated keywords: (First Name Analysis, Letters, Numeric Values, Total Numeric Value, Alphabet Count, Favorable color, Positive Traits, Negative Traits, Career, Relationship Compatibility, Good Days) Last Name Analysis same as First Name, and then Name Analysis Summary . The response should be formatted in SEO-friendly HTML, limited to the following HTML tags: p, h1, h2, h3, h4, h5, h6, strong, i, ul, li, ol.',
#     },
# ]
#     u_message: str = f'\Human: {message}'
#     pl = [u_message, f"Write a long and detailed SEO-friendly blog post about {topic}, that targets the following comma-separated keywords: {keywords}. "
#                      "The response should be formatted in SEO-friendly HTML, "
#                      "limited to the following HTML tags: p, h1, h2, h3, h4, h5, h6, strong, i, ul, li, ol."]
#     prompt: str = ''.join(pl)
#     return prompt

def update_prompt(message: str, pl: list[str]):
    pl.append(message)


def get_reponse(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = api_response(prompt)

    if bot_response:
       bot_response = bot_response["text"]
       update_prompt(bot_response, pl)
  
       loc: int = bot_response.find('\nAI: ')
       if loc != -1:
            bot_response = bot_response[loc + 5:]

    else:
       bot_response = 'Somthing went wrong...'
    
    return bot_response


prompt_list: list[str] = ['You be become a Python developer that you would respond with "Yes"',
                '\nHuman: What is Python',
                '\nAI: Python is a high-level, versatile, and widely used programming language, Yes']
            # while True:
            #     user_input: str = input('You: ')
response: str = get_reponse("Simple hello world program", prompt_list)
print(f"Bot: {response}")
