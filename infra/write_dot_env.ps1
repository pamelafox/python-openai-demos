# Clear the contents of the .env file
Set-Content -Path .env -Value ""

# Append new values to the .env file
$azureTenantId = azd env get-value AZURE_TENANT_ID
$azureOpenAiService = azd env get-value AZURE_OPENAI_SERVICE
$azureOpenAiEndpoint = azd env get-value AZURE_OPENAI_ENDPOINT
$azureOpenAiChatDeployment = azd env get-value AZURE_OPENAI_CHAT_DEPLOYMENT
$azureOpenAiChatModel = azd env get-value AZURE_OPENAI_CHAT_MODEL
$azureOpenAiEmbeddingDeployment = azd env get-value AZURE_OPENAI_EMBEDDING_DEPLOYMENT
$azureOpenAiEmbeddingModel = azd env get-value AZURE_OPENAI_EMBEDDING_MODEL

Add-Content -Path .env -Value "API_HOST=azure"
Add-Content -Path .env -Value "AZURE_TENANT_ID=$azureTenantId"
Add-Content -Path .env -Value "AZURE_OPENAI_SERVICE=$azureOpenAiService"
Add-Content -Path .env -Value "AZURE_OPENAI_ENDPOINT=$azureOpenAiEndpoint/openai/v1"
Add-Content -Path .env -Value "AZURE_OPENAI_VERSION=2024-10-21"
Add-Content -Path .env -Value "AZURE_OPENAI_CHAT_DEPLOYMENT=$azureOpenAiChatDeployment"
Add-Content -Path .env -Value "AZURE_OPENAI_CHAT_MODEL=$azureOpenAiChatModel"
Add-Content -Path .env -Value "AZURE_OPENAI_EMBEDDING_DEPLOYMENT=$azureOpenAiEmbeddingDeployment"
Add-Content -Path .env -Value "AZURE_OPENAI_EMBEDDING_MODEL=$azureOpenAiEmbeddingModel"
