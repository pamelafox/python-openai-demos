import os

import azure.identity
import openai
from dotenv import load_dotenv
from rich import print

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-5")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]

response = client.chat.completions.create(
    model=MODEL_NAME,  # Must be a reasoning model like gpt-5 or gpt-oss
    messages=[
        {
            "role": "user",
            "content": "How many r's are in strawberry? Answer in a complete sentence with explanation.",
        },
    ],
    reasoning_effort="low",
)

# Reasoning contnet is only available for gpt-oss models running on Ollama
# To see reasoning traces with gpt-5 family, use the Responses API
if hasattr(response.choices[0].message, "reasoning"):
    print("🤔 Thinking...")
    print(response.choices[0].message.reasoning)
    print("🛑 Done thinking.")
print("Response:")
print(response.choices[0].message.content)
print("Usage:")
print(response.usage)
