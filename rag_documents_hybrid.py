import json
import os

import azure.identity
import openai
from dotenv import load_dotenv
from lunr import lunr
from sentence_transformers import CrossEncoder

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

# Index the data from the JSON - each object has id, text, and embedding
with open("rag_ingested_chunks.json") as file:
    documents = json.load(file)
    documents_by_id = {doc["id"]: doc for doc in documents}
index = lunr(ref="id", fields=["text"], documents=documents)


def full_text_search(query, limit):
    """
    Perform a full-text search on the indexed documents.
    """
    results = index.search(query)
    retrieved_documents = [documents_by_id[result["ref"]] for result in results[:limit]]
    return retrieved_documents


def vector_search(query, limit):
    """
    Perform a vector search on the indexed documents
    using a simple cosine similarity function.
    """

    def cosine_similarity(a, b):
        return sum(x * y for x, y in zip(a, b)) / ((sum(x * x for x in a) ** 0.5) * (sum(y * y for y in b) ** 0.5))

    query_embedding = client.embeddings.create(model="text-embedding-3-small", input=query).data[0].embedding
    similarities = []
    for doc in documents:
        doc_embedding = doc["embedding"]
        similarity = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((doc, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)

    retrieved_documents = [doc for doc, _ in similarities[:limit]]
    return retrieved_documents


def reciprocal_rank_fusion(text_results, vector_results, k=60):
    """
    Perform Reciprocal Rank Fusion (RRF) on the results from text and vector searches,
    based on algorithm described here:
    https://learn.microsoft.com/azure/search/hybrid-search-ranking#how-rrf-ranking-works
    """
    scores = {}

    for i, doc in enumerate(text_results):
        if doc["id"] not in scores:
            scores[doc["id"]] = 0
        scores[doc["id"]] += 1 / (i + k)
    for i, doc in enumerate(vector_results):
        if doc["id"] not in scores:
            scores[doc["id"]] = 0
        scores[doc["id"]] += 1 / (i + k)
    scored_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    retrieved_documents = [documents_by_id[doc_id] for doc_id, _ in scored_documents]
    return retrieved_documents


def rerank(query, retrieved_documents):
    """
    Rerank the results using a cross-encoder model.
    """
    encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    scores = encoder.predict([(query, doc["text"]) for doc in retrieved_documents])
    scored_documents = [v for _, v in sorted(zip(scores, retrieved_documents), reverse=True)]
    return scored_documents


def hybrid_search(query, limit):
    """
    Perform a hybrid search using both full-text and vector search.
    """
    text_results = full_text_search(query, limit * 2)
    vector_results = vector_search(query, limit * 2)
    fused_results = reciprocal_rank_fusion(text_results, vector_results)
    reranked_results = rerank(query, fused_results)
    return reranked_results[:limit]


# Get the user question
user_question = "cute gray fuzzy bee"

# Search the index for the user question
retrieved_documents = hybrid_search(user_question, limit=5)
print(f"Retrieved {len(retrieved_documents)} matching documents.")
context = "\n".join([f"{doc['id']}: {doc['text']}" for doc in retrieved_documents[0:5]])

# Now we can use the matches to generate a response
SYSTEM_MESSAGE = """
You are a helpful assistant that answers questions about insects.
You must use the data set to answer the questions,
you should not provide any info that is not in the provided sources.
Cite the sources you used to answer the question inside square brackets.
The sources are in the format: <id>: <text>.
"""

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.3,
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": f"{user_question}\nSources: {context}"},
    ],
)

print(f"\nResponse from {MODEL_NAME} on {API_HOST}: \n")
print(response.choices[0].message.content)
