#!/bin/bash

# Clear the contents of the .env file
> .env

# Append new values to the .env file
echo "API_HOST=azure" >> .env
echo "AZURE_TENANT_ID=$(azd env get-value AZURE_TENANT_ID)" >> .env
echo "AZURE_OPENAI_SERVICE=$(azd env get-value AZURE_OPENAI_SERVICE)" >> .env
echo "AZURE_OPENAI_ENDPOINT=$(azd env get-value AZURE_OPENAI_ENDPOINT)/openai/v1" >> .env
echo "AZURE_OPENAI_VERSION=2024-10-21" >> .env
echo "AZURE_OPENAI_CHAT_DEPLOYMENT=$(azd env get-value AZURE_OPENAI_CHAT_DEPLOYMENT)" >> .env
echo "AZURE_OPENAI_CHAT_MODEL=$(azd env get-value AZURE_OPENAI_CHAT_MODEL)" >> .env
echo "AZURE_OPENAI_EMBEDDING_DEPLOYMENT=$(azd env get-value AZURE_OPENAI_EMBEDDING_DEPLOYMENT)" >> .env
echo "AZURE_OPENAI_EMBEDDING_MODEL=$(azd env get-value AZURE_OPENAI_EMBEDDING_MODEL)" >> .env
