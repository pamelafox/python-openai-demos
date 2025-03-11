import os

import azure.identity
from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    llm = AzureOpenAI(
        model=os.environ["OPENAI_MODEL"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        use_azure_ad=True,
        azure_ad_token_provider=token_provider,
    )
elif API_HOST == "ollama":
    llm = OpenAILike(
        model=os.environ["OLLAMA_MODEL"], api_base=os.environ["OLLAMA_ENDPOINT"], api_key="fake", is_chat_model=True
    )
elif API_HOST == "github":
    llm = OpenAILike(
        model=os.environ["GITHUB_MODEL"],
        api_base="https://models.inference.ai.azure.com",
        api_key=os.environ["GITHUB_TOKEN"],
        is_chat_model=True,
    )
else:
    llm = OpenAI(model=os.environ["OPENAI_MODEL"], api_key=os.environ["OPENAI_KEY"])

chat_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=("You are a helpful assistant that makes lots of cat references and uses emojis."),
    ),
    ChatMessage(role=MessageRole.USER, content="Write a haiku about a hungry cat who wants tuna"),
]
response = llm.chat(chat_msgs)
print(f"Response from {API_HOST}: \n")
print(str(response))
