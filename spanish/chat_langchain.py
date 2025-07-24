import os

import azure.identity
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    llm = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_ad_token_provider=token_provider,
    )
elif API_HOST == "ollama":
    llm = ChatOpenAI(
        model_name=os.environ["OLLAMA_MODEL"],
        openai_api_base=os.environ["OLLAMA_ENDPOINT"],
        openai_api_key=os.environ["OPENAI_KEY"],
    )
elif API_HOST == "github":
    llm = ChatOpenAI(
        model_name=os.getenv("GITHUB_MODEL", "openai/gpt-4o"),
        openai_api_base="https://models.github.ai/inference",
        openai_api_key=os.environ["GITHUB_TOKEN"],
    )
else:
    llm = ChatOpenAI(model_name=os.environ["OPENAI_MODEL"], openai_api_key=os.environ["OPENAI_KEY"])


prompt = ChatPromptTemplate.from_messages(
    [("system", "Eres un asistente útil que hace muchas referencias a gatos y usa emojis."), ("user", "{input}")]
)
chain = prompt | llm
response = chain.invoke({"input": "escribe un haiku sobre un gato hambriento que quiere atún"})

print(f"Respuesta de {API_HOST}: \n")
print(response.content)
