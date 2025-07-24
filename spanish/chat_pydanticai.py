import os

import azure.identity
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = AsyncAzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_ad_token_provider=token_provider,
    )
    model = OpenAIModel(os.environ["AZURE_OPENAI_DEPLOYMENT"], openai_client=client)
elif API_HOST == "ollama":
    model = OpenAIModel(os.environ["OLLAMA_MODEL"], api_key="fake", base_url=os.environ["OLLAMA_ENDPOINT"])
elif API_HOST == "github":
    model = OpenAIModel(
        os.getenv("GITHUB_MODEL", "openai/gpt-4o"),
        api_key=os.environ["GITHUB_TOKEN"],
        base_url="https://models.github.ai/inference",
    )

else:
    model = OpenAIModel(os.environ["OPENAI_MODEL"], api_key=os.environ["OPENAI_KEY"])


agent = Agent(model, system_prompt="Eres un asistente útil que hace muchas referencias a gatos y usa emojis.")

result = agent.run_sync("Escribe un haiku sobre un gato hambriento que quiere atún")

print(f"Respuesta de {API_HOST}: \n")
print(result.data)
