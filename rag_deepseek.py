import os

import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)

client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
MODEL_NAME = "o1"

# open hybrid.csv in the same directory as this script and send to model
with open("hybrid.csv") as file:
    rows = file.readlines()
csv_data = "\n".join(rows)

# Not supported: temperature, top_p, tools
# max_tokens is supported BUT that may end up cutting off a thought process!
# stop is also supported
completion = client.chat.completions.create(
    model=MODEL_NAME,
    n=1,
    messages=[
        {"role": "user",
        "content": f"What is the fastest hybrid car? Here is a CSV with data: {csv_data}"},
    ],
    #stream=True
)

print("Response: ")
print(completion.choices[0].message.content)
exit()
is_thinking = False
for event in completion:
    if event.choices:
        content = event.choices[0].delta.content
        if content == "<think>":
            is_thinking = True
            # note: this is sometimes followed ONLY by a new line
            print("🧠 Thinking...", end="", flush=True)
        elif content == "</think>":
            is_thinking = False
            print("🛑\n\n")
        elif content:
            print(content, end="", flush=True)
