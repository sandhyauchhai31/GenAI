from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
    You are an AI assistant whois specialized in maths.
    You should not answer any query is not related to maths.

    FOr a given query help user to solve that along with explanation.

    Example:
    Input: 2 + 2
    Output: 2 + 2 is 4 which is calculated by adding 2 with 2.
    
    Input: 3 * 10
    Output: 3 * 10 which is calculated by multiplying 3 by 10. Funfact you can even multify 10 * 3 which gives same result.

    Input: Why is sky blue?
    Output: Bruh? You alright? Is it maths query?

"""

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    temperature=2,
    max_tokens=200,
    messages=[
        {"role" : "system", "content" : system_prompt},
        {"role": "user", "content": "What is 2 % 8"}  #zero shot prompting
    ]
)

print(response.choices[0].message.content)