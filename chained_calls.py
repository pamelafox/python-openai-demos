import os

import azure.identity
import openai
from dotenv import load_dotenv

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


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[{"role": "user", "content": "Explain how LLMs work in a single paragraph."}],
)

explanation = response.choices[0].message.content
print("Explanation: ", explanation)
response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[
        {
            "role": "user",
            "content": "You're an editor. Review the explanation and provide feedback (but don't edit yourself):\n\n"
            + explanation,
        }
    ],
)

feedback = response.choices[0].message.content
print("\n\nFeedback: ", feedback)

response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    messages=[
        {
            "role": "user",
            "content": (
                "Revise the article using the following feedback, but keep it to a single paragraph."
                f"\nExplanation:\n{explanation}\n\nFeedback:\n{feedback}"
            ),
        }
    ],
)

final_article = response.choices[0].message.content
print("\n\nFinal Article: ", final_article)
