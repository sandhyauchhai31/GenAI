# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI()

# result = client.chat.completions.create(
#     model="gpt-4",
#     messsages=[
#         {"role" : "user", "content" : "Hey there"}
#     ]
# )

# print( result.choices[0].message.content)

from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Hey there"}
    ]
)

print(result.choices[0].message.content)




