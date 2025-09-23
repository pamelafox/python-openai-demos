import json
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


def lookup_weather(city_name=None, zip_code=None):
    """Busca el clima según nombre de ciudad o código postal."""
    return {
        "city_name": city_name,
        "zip_code": zip_code,
        "weather": "soleado",
        "temperature": 75,
    }


tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_weather",
            "description": "Lookup the weather for a given city name or zip code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "The city name",
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "The zip code",
                    },
                },
                "strict": True,
                "additionalProperties": False,
            },
        },
    }
]

messages = [
    {"role": "system", "content": "Eres un chatbot de clima."},
    {"role": "user", "content": "Está soleado en Berkeley CA?"},
]
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

print(f"Respuesta de {MODEL_NAME} en {API_HOST}: \n")

# Ahora llama a la función indicada

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    if function_name == "lookup_weather":
        messages.append(response.choices[0].message)
        result = lookup_weather(**arguments)
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
        response = client.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
        print(response.choices[0].message.content)
