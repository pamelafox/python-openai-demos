import os

import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)


client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
MODEL_NAME = "DeepSeek-R1"


# Not supported: temperature, top_p, tools
response = client.chat.completions.create(
    model=MODEL_NAME,
    n=1,
    messages=[
        # A system message can be specified, but is not adhered to as much as usual
        {"role": "user", "content": "You are a helpful assistant that makes lots of cat references and uses emojis. Write a haiku about a hungry cat who wants tuna"},
    ],
)

print("Response: ")
print(response.choices[0].message.content)
