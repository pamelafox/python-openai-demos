import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT"]

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
Eres un asistente útil que ayuda a estudiantes con sus tareas.
En lugar de proporcionar la respuesta completa, respondes con una pista o una clave.
"""


USER_MESSAGE = "¿Cuál es el planeta más grande en nuestro sistema solar?"


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    n=1,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": "¿Cuál es la capital de Francia?"},
        {"role": "assistant", "content": "¿Recuerdes el nombre de la ciudad que es conocida por la Torre Eiffel?"},
        {"role": "user", "content": "¿Cuál es la raíz cuadrada de 144?"},
        {"role": "assistant", "content": "¿Qué número multiplicado por sí mismo es igual a 144?"},
        {"role": "user", "content": "¿Cuál es el número atómico del oxígeno?"},
        {"role": "assistant", "content": "¿Cuántos protones tiene un átomo de oxígeno?"},
        {"role": "user", "content": USER_MESSAGE},
    ],
)


print(f"Response from {API_HOST}: \n")
print(response.choices[0].message.content)
