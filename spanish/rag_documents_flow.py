import json
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

# Indexar los datos del JSON - cada objeto tiene id, texto y embedding
with open("rag_ingested_chunks.json") as file:
    documents = json.load(file)
    documents_by_id = {doc["id"]: doc for doc in documents}
index = lunr(ref="id", fields=["text"], documents=documents)

# Obtener la pregunta del usuario
user_question = "¿dónde vive la abeja solitaria?"

# Buscar la pregunta del usuario en el índice
results = index.search(user_question)
retrieved_documents = [documents_by_id[result["ref"]] for result in results]
print(f"Recuperados {len(retrieved_documents)} documentos coincidentes, enviando sólo los primeros 5.")
context = "\n".join([f"{doc['id']}: {doc['text']}" for doc in retrieved_documents[0:5]])

# Ahora podemos usar las coincidencias para generar una respuesta
SYSTEM_MESSAGE = """
Eres un asistente útil que responde preguntas sobre insectos regionales.
Debes utilizar el conjunto de datos para responder las preguntas,
no debes proporcionar ninguna información que no esté en las fuentes proporcionadas.
Cita las fuentes que utilizaste para responder la pregunta entre corchetes.
Las fuentes están en el formato: <id>: <texto>.
"""

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": f"{user_question}\nFuentes: {context}"},
    ],
)

print(f"\nRespuesta de {MODEL_NAME} en {API_HOST}: \n")
print(response.choices[0].message.content)
