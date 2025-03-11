import json
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
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.environ["GITHUB_MODEL"]

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


def lookup_weather(city_name=None, zip_code=None):
    """Buscar el clima para un nombre de ciudad o código postal dado."""
    print(f"Buscando el clima para {city_name or zip_code}...")
    return "¡Está soleado!"


tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_weather",
            "description": "Buscar el clima para un nombre de ciudad o código postal dado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "El nombre de la ciudad",
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "El código postal",
                    },
                },
                "strict": True,
                "additionalProperties": False,
            },
        },
    }
]

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "Eres un chatbot del clima."},
        {"role": "user", "content": "¿está soleado en esa pequeña ciudad cerca de Sydney donde vive Anthony?"},
    ],
    tools=tools,
    tool_choice="auto",
)

print(f"Respuesta de {API_HOST}: \n")
print(response.choices[0].message.tool_calls[0].function.name)
print(response.choices[0].message.tool_calls[0].function.arguments)


if response.choices[0].message.tool_calls:
    function_name = response.choices[0].message.tool_calls[0].function.name
    arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    if function_name == "lookup_weather":
        lookup_weather(**arguments)
