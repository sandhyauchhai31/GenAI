import tkinter as tk
from tkinter import scrolledtext
import json
from dotenv import load_dotenv
from collections import Counter
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

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
def run_self_consistent_prompt(query, output_box,model="gpt-3.5-turbo",runs=5):
    final_results = []

    output_box.delete(1.0,tk.END) #clear output box

    for i in range(runs):
        steps = []
        messages = [        
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": query }        
        ]

        while True:
            try:

                response = client.chat.completions.create(
                    model=model,
                    response_format={"type": "json_object"},
                    messages=messages
                )
            except Exception as e:
                output_box.insert(tk.END, f"❌ API Error: {e}\n")
                return

            print(f"[Debug] Sending request to OpenAI: {messages}")

            parsed = json.loads(response.choices[0].message.content)
            print(f"[Debug] Received response: {response.choices[0].message.content}")

            messages.append({ "role": "assistant", "content": json.dumps(parsed) })
            steps.append(parsed)

            if parsed["step"] == "result":
                final_results.append(parsed["content"])
                output_box.insert(tk.END,f"\n--- Run {i+1} ---\n")
                for s in steps:
                    output_box.insert(tk.END,f'{s["step"].capitalize()}: {s["content"]}\n')
                    break

    majority = Counter(final_results).most_common(1)[0]
    output_box.insert(tk.END, f"\n✅ Final Self-Consistent Answer: {majority[0]} ({majority[1]} out of {runs})\n")

#---- GUI SETUP ----

window = tk.Tk()
window.title("🧠 Math Solver (Self-Consistency)")

tk.Label(window, text="Enter your math query:").pack(pady=5)
query_input = tk.Entry(window, width=60)
query_input.pack(pady=5)

output_box = scrolledtext.ScrolledText(window, width=80, height=25)
output_box.pack(padx=10,pady=10)

def on_submit():
    query = query_input.get()
    if query:
        run_self_consistent_prompt(query, output_box)

tk.Button(window, text="Solve", command=on_submit).pack(pady=10)

window.mainloop()

