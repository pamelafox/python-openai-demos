import asyncio
import os

import azure.identity.aio
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

azure_credential = None  # Referencia para poder cerrar la credencial y su sesión HTTP.
if API_HOST == "azure":
    azure_credential = azure.identity.aio.DefaultAzureCredential()
    token_provider = azure.identity.aio.get_bearer_token_provider(
        azure_credential, "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AsyncOpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
elif API_HOST == "ollama":
    client = openai.AsyncOpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]
elif API_HOST == "github":
    client = openai.AsyncOpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")
else:
    client = openai.AsyncOpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


async def generate_response(location):
    print("Generando respuesta para", location)
    response = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {
                "role": "user",
                "content": (
                    f"Nombra un solo lugar que debería visitar en mi viaje a {location} y descríbelo en una oración"
                ),
            },
        ],
        temperature=1,
        max_tokens=400,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    print("Obtuve respuesta para ", location)
    return response.choices[0].message.content


async def single() -> None:
    """Ejecuta un único ejemplo."""
    print(await generate_response("Tokio"))


async def multiple() -> None:
    """Ejecuta varias solicitudes concurrentes."""
    answers = await asyncio.gather(
        generate_response("Tokio"),
        generate_response("Berkeley"),
        generate_response("Singapur"),
    )
    for answer in answers:
        print(answer, "\n")


async def close_clients() -> None:
    """Cierra el cliente OpenAI y la credencial de Azure (si existe)."""
    await client.close()
    if azure_credential is not None:
        await azure_credential.close()


async def main():
    """Punto de entrada que garantiza la liberación de recursos."""
    try:
        await single()  # Cambiar a multiple() para el ejemplo concurrente.
    finally:
        await close_clients()


if __name__ == "__main__":
    asyncio.run(main())
