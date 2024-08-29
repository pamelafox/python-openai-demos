from pathlib import Path

import azure.identity
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Get a token from Azure
token_provider = azure.identity.get_bearer_token_provider(
    azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
token = token_provider()

# Path to the .env file
env_path = Path(__file__).parent / ".env"

# Read the existing lines
with open(env_path) as f:
    lines = f.readlines()

# Write back non-AUTH_TOKEN lines and append the new token
with open(env_path, "w") as f:
    for line in lines:
        if not line.startswith("TOKEN"):
            f.write(line)
    f.write(f"TOKEN={token}\n")
