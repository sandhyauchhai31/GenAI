from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are an AI assistant who is expert in breaking down complex problms and then resolve the user query

For the given user input, analys the input and break down the problem style by step.
Atleast think 5-6 steps on how to solve th problem before solving solving it down.

The steps are you get a user input, you analyse, you think you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1.Follow the strict JSON ouput as per Output schema.
2.Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string"}}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is interested in maths query and he is asking a basic arthermatic operation.}}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}
"""

result = client.chat.completions.create(
    model="gemini-2.0-flash",
    response_format={"type": "json_object"},
    messages=[
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": "what is 3 + 4 * 5?"  },

        #
        { "role": "assistant", "content": json.dumps({"step": "analyse", "content": "The user wants to evaluate the expression>  3 + 4 * 5. This involves addition and multiplication."}) },
        { "role": "assistant", "content": json.dumps({"step": "think", "content": "I need to consider the order of operations (PEMDAS/BODMAS). Multiplication should be done before addition. So, first calculate 4 * 5, then add 3 to the result."}) },
        { "role": "assistant", "content": json.dumps( {"step": "output", "content": "First, calculate 4 * 5 = 20.  Then, calculate 3 + 20 = 23."})},
        { "role": "assistant", "content": json.dumps({"step": "validate","content": "Verified the calculation: 4 * 5 = 20, and 3 + 20 = 23. The order of operations was correctly followed."})}
    ]
)
print(result.choices[0].message.content)