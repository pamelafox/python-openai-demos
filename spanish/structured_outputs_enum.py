import os
from enum import Enum

import azure.identity
import openai
import rich
from dotenv import load_dotenv
from pydantic import BaseModel

# Configura el cliente de OpenAI para usar la API de Azure, OpenAI.com u Ollama
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

elif API_HOST == "github":
    client = openai.OpenAI(base_url="https://models.github.ai/inference", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


class DayOfWeek(str, Enum):
    DOMINGO = "Domingo"
    LUNES = "Lunes"
    MARTES = "Martes"
    MIÉRCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SÁBADO = "Sábado"


class CalendarEvent(BaseModel):
    name: str
    date: DayOfWeek
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "Extrae la info del evento."},
        {"role": "user", "content": "Alice y Bob van a ir a una feria de ciencias el viernes."},
    ],
    response_format=CalendarEvent,
)


message = completion.choices[0].message
if message.refusal:
    rich.print(message.refusal)
else:
    event = message.parsed
    rich.print(event)
