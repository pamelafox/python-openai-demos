# Python OpenAI demos

This repository contains a collection of Python scripts that demonstrate how to use the OpenAI API to generate chat completions.

## OpenAI package

These scripts use the OpenAI package to demonstrate how to use the OpenAI API.
In increasing order of complexity, the scripts are:

1. [`chat.py`](./chat.py): A simple script that demonstrates how to use the OpenAI API to generate chat completions.
2. [`chat_stream.py`](./chat_stream.py): Adds `stream=True` to the API call to return a generator that streams the completion as it is being generated.
3. [`chat_history.py`](./chat_history.py): Adds a back-and-forth chat interface using `input()` which keeps track of past messages and sends them with each chat completion call.
4. [`chat_history_stream.py`](./chat_history_stream.py): The same idea, but with `stream=True` enabled.

Plus these scripts to demonstrate additional features:

* [`chat_safety.py`](./chat_safety.py): The simple script with exception handling for Azure AI Content Safety filter errors.
* [`chat_async.py`](./chat_async.py): Uses the async clients to make asynchronous calls, including an example of sending off multiple requests at once using `asyncio.gather`.

## Popular LLM libraries

These scripts use popular LLM libraries to demonstrate how to use the OpenAI API with them:

* [`chat_langchain.py`](./chat_langchain.py): Uses the Langchain package to generate chat completions. [Learn more from Langchain docs](https://python.langchain.com/docs/get_started/quickstart)
* [`chat_llamaindex.py`](./chat_llamaindex.py): Uses the LlamaIndex package to generate chat completions. [Learn more from LlamaIndex docs](https://docs.llamaindex.ai/en/stable/)
* [`chat_pydanticai.py`](./chat_pydanticai.py): Uses the PydanticAI package to generate chat completions. [Learn more from PydanticAI docs](https://ai.pydantic.dev/)

## Retrieval-Augmented Generation (RAG)

These scripts demonstrate how to use the OpenAI API for Retrieval-Augmented Generation (RAG) tasks, where the model retrieves relevant information from a source and uses it to generate a response.

First install the RAG dependencies:

```bash
python -m pip install -r requirements-rag.txt
```

Then run the scripts (in order of increasing complexity):

* [`rag_csv.py`](./rag.py): Retrieves matching results from a CSV file and uses them to answer user's question.
* [`rag_multiturn.py`](./rag_multiturn.py): The same idea, but with a back-and-forth chat interface using `input()` which keeps track of past messages and sends them with each chat completion call.
* [`rag_queryrewrite.py`](./rag_queryrewrite.py): Adds a query rewriting step to the RAG process, where the user's question is rewritten to improve the retrieval results.
* [`rag_documents_ingestion.py`](./rag_ingestion.py): Ingests PDFs by using pymupdf to convert to markdown, then using Langchain to split into chunks, then using OpenAI to embed the chunks, and finally storing in a local JSON file.
* [`rag_documents_flow.py`](./rag_pdfs.py): A RAG flow that retrieves matching results from the local JSON file created by `rag_documents_ingestion.py`.
* [`rag_documents_hybrid.py`](./rag_documents_hybrid.py): A RAG flow that implements a hybrid retrieval with both vector and keyword search, merging with Reciprocal Rank Fusion (RRF), and semantic re-ranking with a cross-encoder model.

## Structured outputs with OpenAI

These scripts demonstrate how to use the OpenAI API to generate structured responses using Pydantic data models:

* [`structured_outputs_basic.py`](./structured_outputs_basic.py): Basic example extracting simple event information using a Pydantic model.
* [`structured_outputs_description.py`](./structured_outputs_description.py): Uses additional descriptions in Pydantic model fields to clarify to the model how to format the response.
* [`structured_outputs_enum.py`](./structured_outputs_enum.py): Uses enumerations (Enums) to restrict possible values in structured responses.
* [`structured_outputs_function_calling.py`](./structured_outputs_function_calling.py): Demonstrates how to use functions defined with Pydantic for automatic function calling based on user queries.
* [`structured_outputs_nested.py`](./structured_outputs_nested.py): Uses nested Pydantic models to handle more complex structured responses, such as events with participants having multiple attributes.

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
