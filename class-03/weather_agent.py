from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
    You are an AI assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode
"""

response = client.chat.completions.create(
    model = "gpt-4o",
    messages=[
        {
            "role": "user", "content": "what is the current weather of pune?"
        }
    ]
)
print(response.choices[0].message.content)