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


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[{"role": "user", "content": "Explica cómo funcionan los LLM en un solo párrafo."}],
)

explanation = response.choices[0].message.content
print("Explicación: ", explanation)
response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[
        {
            "role": "user",
            "content": (
                "Eres un editor. Revisa la explicación y proporciona comentarios detallados sobre claridad, coherencia "
                "y cautivación (pero no la edites tú mismo):\n\n"
            )
            + explanation,
        }
    ],
)

feedback = response.choices[0].message.content
print("\n\nRetroalimentación: ", feedback)

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[
        {
            "role": "user",
            "content": (
                "Revisa el artículo utilizando los siguientes comentarios, pero mantenlo a un solo párrafo."
                f"\nExplicación:\n{explanation}\n\nComentarios:\n{feedback}"
            ),
        }
    ],
)

final_article = response.choices[0].message.content
print("\n\nFinal Article: ", final_article)
