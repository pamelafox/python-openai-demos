import csv
import os

import azure.identity
import openai
from dotenv import load_dotenv
from lunr import lunr

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

# Indexamos los datos del CSV
with open("hybridos.csv") as file:
    reader = csv.reader(file)
    rows = list(reader)
documents = [{"id": (i + 1), "body": " ".join(row)} for i, row in enumerate(rows[1:])]
index = lunr(ref="id", fields=["body"], documents=documents)


def search(query):
    # Buscamos en el índice la pregunta del usuario
    query = query.lower().replace("?", "")
    results = index.search(query)
    matching_rows = [rows[int(result["ref"])] for result in results]

    # Formateamos como tabla markdown, ya que los llms entienden markdown
    matches_table = " | ".join(rows[0]) + "\n" + " | ".join(" --- " for _ in range(len(rows[0]))) + "\n"
    matches_table += "\n".join(" | ".join(row) for row in matching_rows)
    return matches_table


SYSTEM_MESSAGE = """
Eres un asistente útil que responde preguntas sobre automóviles basándote en un conjunto de datos de autos híbridos.
Debes utilizar el conjunto de datos para responder las preguntas, no debes proporcionar ninguna información que no
esté en las fuentes proporcionadas.
"""
messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

while True:
    question = input("\nTu pregunta acerca de carros híbridos: ")

    # Buscar en el CSV la pregunta
    matches = search(question)
    print("Found matches:\n")
    print(matches)

    # Usar los resultados para generar una respuesta
    messages.append({"role": "user", "content": f"{question}\nSources: {matches}"})
    response = client.chat.completions.create(model=MODEL_NAME, temperature=0.3, messages=messages)

    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_response})

    print(f"\nResponse from {API_HOST} {MODEL_NAME}: \n")
    print(bot_response)
