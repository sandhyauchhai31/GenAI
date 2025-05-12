from collections import Counter
from openai import OpenAI
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI()

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

query = input("> ")

final_results = []

#Run multiple completions for self-consistency
for i in range(5): # try 5 times
    messages = [
        { "role": "system", "content": system_prompt },
        { "role":"user", "content": query }
    ]

    result_value = None
    steps = []

    while True:
        response = client.chat.completions.create(
            model = "gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append( { "role": "assistant", "content": json.dumps(parsed_response) })
        steps.append(parsed_response)

        # This is the step-by-step thinking loop.

        # Each API call gives only one reasoning step (controlled via system prompt).

        # Once the step is "result", we stop.

        if parsed_response["step"] == "result":
            result_value = parsed_response["content"]
            break

    final_results.append(result_value)
    print(f"\n--- Run {i+1} ---")
    for s in steps:
        print(f'{s["step"]}: {s["content"]}')

# Majority Vote
majority = Counter(final_results).most_common(1)[0]
print("\n✅ Final Answer (self consistency):", majority[0])
print("🗳️ Count:", majority[1], "out of", len(final_results))

        
