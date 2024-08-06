import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
elif API_HOST == "ollama":
    client = openai.OpenAI(
        base_url=os.getenv("OLLAMA_ENDPOINT"),
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")
elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    MODEL_NAME = os.getenv("GITHUB_MODEL")
else:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")


completion = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    max_tokens=500,
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that makes lots of cat references and uses emojis."},
        {"role": "user", "content": "please write a haiku about a hungry cat that wants tuna"},
    ],
    stream=True,
)

print("Response: ")
for event in completion:
    if event.choices:
        content = event.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
