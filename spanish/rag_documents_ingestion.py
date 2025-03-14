import json
import os
import pathlib

import azure.identity
import openai
import pymupdf4llm
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
    client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]

data_dir = pathlib.Path(os.path.dirname(__file__)) / "data"
filenames = ["Xylocopa_californica.pdf", "Centris_pallida.pdf", "Apis_mellifera.pdf", "Syrphidae.pdf"]
all_chunks = []
for filename in filenames:
    # Extraemos texto del archivo PDF
    md_text = pymupdf4llm.to_markdown(data_dir / filename)

    # Dividimos el texto en fragmentos más pequeños
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o", chunk_size=500, chunk_overlap=0
    )
    texts = text_splitter.create_documents([md_text])
    file_chunks = [{"id": f"{filename}-{(i + 1)}", "text": text.page_content} for i, text in enumerate(texts)]

    # Generamos embeddings utilizando el SDK de openAI para cada texto
    for file_chunk in file_chunks:
        file_chunk["embedding"] = (
            client.embeddings.create(model="text-embedding-3-small", input=file_chunk["text"]).data[0].embedding
        )
    all_chunks.extend(file_chunks)

# Guardamos los documentos con embeddings en un archivo JSON
with open("rag_ingested_chunks.json", "w") as f:
    json.dump(all_chunks, f, indent=4)
