import os

import azure.identity
import openai
import rich
from dotenv import load_dotenv
from pydantic import BaseModel, Field

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


class CalendarEvent(BaseModel):
    name: str
    date: str = Field(..., description="A date in the format YYYY-MM-DD")
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model=MODEL_NAME,
    messages=[
        {
            "role": "system",
            "content": "Extract the event information. If no year is specified, assume the current year (2025).",
        },
        {"role": "user", "content": "Alice and Bob are going to a science fair on the 1st of april."},
    ],
    response_format=CalendarEvent,
)
CalendarEvent(name="Science Fair", date="2025-04-01", participants=["Alice", "Bob"])

message = completion.choices[0].message
if message.refusal:
    rich.print(message.refusal)
else:
    event = message.parsed
    rich.print(event)
