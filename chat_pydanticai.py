import os

import azure.identity
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

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
    client = AsyncOpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="fake")
    model = OpenAIModel(os.environ["OLLAMA_MODEL"], provider=OpenAIProvider(openai_client=client))
elif API_HOST == "github":
    client = AsyncOpenAI(api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.github.ai/inference")
    model = OpenAIModel(os.getenv("GITHUB_MODEL", "openai/gpt-4o"), provider=OpenAIProvider(openai_client=client))
else:
    client = AsyncOpenAI(api_key=os.environ["OPENAI_KEY"])
    model = OpenAIModel(os.environ["OPENAI_MODEL"], provider=OpenAIProvider(openai_client=client))


agent = Agent(model, system_prompt="You are a helpful assistant that makes lots of cat references and uses emojis.")

result = agent.run_sync("Write a haiku about a hungry cat who wants tuna")

print(f"Response from {API_HOST}: \n")
print(result.data)
