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

# Indexar los datos del CSV
with open("hybridos.csv") as file:
    reader = csv.reader(file)
    rows = list(reader)
documents = [{"id": (i + 1), "body": " ".join(row)} for i, row in enumerate(rows[1:])]
index = lunr(ref="id", fields=["body"], documents=documents)


def search(query):
    # Buscar en el índice la pregunta del usuario
    results = index.search(query)
    matching_rows = [rows[int(result["ref"])] for result in results]

    # Formatear como una tabla markdown, ya que los modelos de lenguaje entienden markdown
    matches_table = " | ".join(rows[0]) + "\n" + " | ".join(" --- " for _ in range(len(rows[0]))) + "\n"
    matches_table += "\n".join(" | ".join(row) for row in matching_rows)
    return matches_table


QUERY_REWRITE_SYSTEM_MESSAGE = """
Eres un asistente útil que reescribe preguntas de usuarios a consultas de alta calidad de tipo keyword
para un índice de filas CSV con estas columnas: vehicle, year, msrp, acceleration, mpg, class.
Consultas de alta calidad de keyword no tienen puntuación y están en minúsculas.
Se te proporcionará la nueva pregunta del usuario y el historial de conversación.
Responde SÓLO con la consulta de keyword sugerida, sin texto adicional.
"""

SYSTEM_MESSAGE = """
Eres un asistente útil que responde preguntas sobre automóviles basándose en un conjunto de datos de coches híbridos.
Debes utilizar el conjunto de datos para responder las preguntas, no debes proporcionar información que no
esté en las fuentes proporcionadas.
"""
messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

while True:
    question = input("\nTu pregunta sobre coches eléctricos: ")

    # Reescribir la consulta para corregir errores tipográficos e incorporar contexto pasado
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.05,
        messages=[
            {"role": "system", "content": QUERY_REWRITE_SYSTEM_MESSAGE},
            {
                "role": "user",
                "content": f"Nueva pregunta del usuario:{question}\n\nHistorial de conversación:{messages}",
            },
        ],
    )
    search_query = response.choices[0].message.content
    print(f"Consulta reescrita: {search_query}")

    # Buscar en el CSV la pregunta
    matches = search(search_query)
    print("Coincidencias encontradas:\n", matches)

    # Usar las coincidencias para generar una respuesta
    messages.append({"role": "user", "content": f"{question}\nFuentes: {matches}"})
    response = client.chat.completions.create(model=MODEL_NAME, temperature=0.3, messages=messages)

    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_response})

    print(f"\nRespuesta de {API_HOST} {MODEL_NAME}: \n")
    print(bot_response)
