# Python OpenAI demos

This repository contains a collection of Python scripts that demonstrate how to use the OpenAI API to generate chat completions.

In increasing order of complexity, the scripts are:

1. [`chat.py`](./chat.py): A simple script that demonstrates how to use the OpenAI API to generate chat completions.
2. [`chat_stream.py`](./chat_stream.py): Adds `stream=True` to the API call to return a generator that streams the completion as it is being generated.
3. [`chat_history.py`](./chat_history.py): Adds a back-and-forth chat interface using `input()` which keeps track of past messages and sends them with each chat completion call.
4. [`chat_history_stream.py`](./chat_history_stream.py): The same idea, but with `stream=True` enabled.

Plus these scripts to demonstrate additional features:

* [`chat_safety.py`](./chat_safety.py): The simple script with exception handling for Azure AI Content Safety filter errors.
* [`chat_async.py`](./chat_async.py): Uses the async clients to make asynchronous calls, including an example of sending off multiple requests at once using `asyncio.gather`.
* [`chat_langchain.py`](./chat_langchain.py): Uses the langchain SDK to generate chat completions. [Learn more from Langchain docs](https://python.langchain.com/docs/get_started/quickstart)
* [`chat_llamaindex.py`](./chat_llamaindex.py): Uses the LlamaIndex SDK to generate chat completions. [Learn more from LlamaIndex docs](https://docs.llamaindex.ai/en/stable/)

## Setting up the environment

If you open this up in a Dev Container or GitHub Codespaces, everything will be setup for you.
If not, follow these steps:

1. Set up a Python virtual environment and activate it.

2. Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Configuring the OpenAI environment variables

These scripts can be run with Azure OpenAI account, OpenAI.com, local Ollama server, or GitHub models,
depending on the environment variables you set.

1. Copy the `.env.sample` file to a new file called `.env`:

    ```bash
    cp .env.sample .env
    ```

2. For Azure OpenAI, create an Azure OpenAI gpt-3.5 or gpt-4 deployment (perhaps using [this template](https://github.com/Azure-Samples/azure-openai-keyless)), and customize the `.env` file with your Azure OpenAI endpoint and deployment id.

    ```bash
    API_HOST=azure
    AZURE_OPENAI_ENDPOINT=https://YOUR-AZURE-OPENAI-SERVICE-NAME.openai.azure.com
    AZURE_OPENAI_DEPLOYMENT=YOUR-AZURE-DEPLOYMENT-NAME
    AZURE_OPENAI_VERSION=2024-03-01-preview
    ```

    If you are not yet logged into the Azure account associated with that deployment, run this command to log in:

    ```shell
    az login
    ```

3. For OpenAI.com, customize the `.env` file with your OpenAI API key and desired model name.

    ```bash
    API_HOST=openai
    OPENAI_KEY=YOUR-OPENAI-API-KEY
    OPENAI_MODEL=gpt-3.5-turbo
    ```

4. For Ollama, customize the `.env` file with your Ollama endpoint and model name (any model you've pulled).

    ```bash
    API_HOST=ollama
    OLLAMA_ENDPOINT=http://localhost:11434/v1
    OLLAMA_MODEL=llama2
    ```

    If you're running inside the Dev Container, replace `localhost` with `host.docker.internal`.

5. For GitHub models, customize the `.env` file with your GitHub model name.

    ```bash
    API_HOST=github
    GITHUB_MODEL=gpt-4o
    ```

    You'll need a `GITHUB_TOKEN` environment variable that stores a GitHub personal access token.
    If you're running this inside a GitHub Codespace, the token will be automatically available.
    If not, generate a new [personal access token](https://github.com/settings/tokens) and run this command to set the `GITHUB_TOKEN` environment variable:

    ```shell
    export GITHUB_TOKEN="<your-github-token-goes-here>"
