import os

import azure.identity
import openai
from dotenv import load_dotenv

# Configura el cliente de OpenAI para usar la API de Azure, OpenAI.com u Ollama
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
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


SYSTEM_MESSAGE = """
Quiero que actúes como Chespirito de El Chavo del 8.
Quiero que respondas y contestes como Chespirito utilizando el tono, manera y vocabulario que Chespirito usaría.
No escribas ninguna explicación. Solo responde como Chespirito.
Debes conocer todo el conocimiento de Chespirito, y nada más.
"""

USER_MESSAGE = """
¿Qué es un LLM?
"""

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    n=1,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": USER_MESSAGE},
    ],
)

print(f"Response from {API_HOST}: \n")
print(response.choices[0].message.content)
