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
    client = openai.OpenAI(
        base_url=os.getenv("OLLAMA_ENDPOINT"),
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
    MODEL_NAME = os.getenv("GITHUB_MODEL")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


def lookup_weather(city_name=None, zip_code=None):
    """Lookup the weather for a given city name or zip code."""
    print(f"Looking up weather for {city_name or zip_code}...")
    return "It's sunny!"


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

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "You are a weather chatbot."},
        {"role": "user", "content": "is it sunny in that small city near sydney where anthony lives?"},
    ],
    tools=tools,
    tool_choice="auto",
)

print("Response:")
print(response.choices[0].message.tool_calls[0].function.name)
print(response.choices[0].message.tool_calls[0].function.arguments)

# Now actually call the function as indicated
if response.choices[0].message.tool_calls:
    function_name = response.choices[0].message.tool_calls[0].function.name
    arguments = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    if function_name == "lookup_weather":
        lookup_weather(**arguments)
