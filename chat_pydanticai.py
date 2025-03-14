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
elif API_HOST == "openai":
    model = OpenAIModel(os.environ["OPENAI_MODEL"], api_key=os.environ["OPENAI_KEY"])
else:
    model = OpenAIModel(
        os.getenv("GITHUB_MODEL", "gpt-4o"), api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com"
    )

agent = Agent(model, system_prompt="You are a helpful assistant that makes lots of cat references and uses emojis.")

result = agent.run_sync("Write a haiku about a hungry cat who wants tuna")

print(f"Response from {API_HOST}: \n")
print(result.data)
