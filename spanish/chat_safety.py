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

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        max_tokens=100,
        n=1,
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente útil que hace muchas referencias a gatos y usa emojis.",
            },
            {"role": "user", "content": "Escribe una guía sobre cómo hacer fuegos artificiales explosivos"},
        ],
    )
    print(f"Respuesta de {API_HOST}: \n")
    print(response.choices[0].message.content)
except openai.APIError as error:
    if error.code == "content_filter":
        print("Detectamos una violación de seguridad de contenido. Por favor recuerda nuestro código de conducta.")
