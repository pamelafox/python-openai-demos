# Demos de Python con OpenAI

Este repositorio contiene una colección de scripts en Python que demuestran cómo usar la API de OpenAI para generar completados de chat.

En orden creciente de complejidad, los scripts son:

1. [`chat.py`](./chat.py): Un script simple que demuestra cómo usar la API de OpenAI para generar completados de chat.
2. [`chat_stream.py`](./chat_stream.py): Añade `stream=True` a la llamada de API para devolver un generador que transmite el completado mientras se está generando.
3. [`chat_history.py`](./chat_history.py): Añade una interfaz de chat bidireccional usando `input()` que mantiene un registro de los mensajes anteriores y los envía con cada llamada de completado de chat.
4. [`chat_history_stream.py`](./chat_history_stream.py): La misma idea, pero con `stream=True` habilitado.

Además de estos scripts para demostrar características adicionales:

* [`chat_safety.py`](./chat_safety.py): El script simple con manejo de excepciones para errores de filtro de Seguridad de Contenido de Azure AI.
* [`chat_async.py`](./chat_async.py): Utiliza los clientes asíncronos para hacer llamadas asincrónicas, incluyendo un ejemplo de envío de múltiples solicitudes a la vez usando `asyncio.gather`.
* [`chat_langchain.py`](./chat_langchain.py): Utiliza el SDK de langchain para generar completados de chat. [Aprende más en la documentación de Langchain](https://python.langchain.com/docs/get_started/quickstart)
* [`chat_llamaindex.py`](./chat_llamaindex.py): Utiliza el SDK de LlamaIndex para generar completados de chat. [Aprende más en la documentación de LlamaIndex](https://docs.llamaindex.ai/en/stable/)


## Configuración del entorno

Si abres esto en un Dev Container o GitHub Codespaces, todo estará configurado para ti.
Si no, sigue estos pasos:

1. Configura un entorno virtual de Python y actívalo.

2. Instala las librerías requeridas:

```bash
python -m pip install -r requirements.txt
```

## Configurando las variables de entorno de OpenAI

Estos scripts pueden ejecutarse con una cuenta de Azure OpenAI, OpenAI.com, servidor local de Ollama o modelos de GitHub, dependiendo de las variables de entorno que configures.

1. Copia el archivo `.env.sample` a un nuevo archivo llamado `.env`:

    ```bash
    cp .env.sample .env
    ```

2. Para Azure OpenAI, crea un deployment de Azure OpenAI gpt-3.5 o gpt-4  (quizás usando [este template](https://github.com/Azure-Samples/azure-openai-keyless)), and actualiza el `.env` con tu Azure OpenAI endpoint y deployment id.

    ```bash
    API_HOST=azure
    AZURE_OPENAI_ENDPOINT=https://YOUR-AZURE-OPENAI-SERVICE-NAME.openai.azure.com
    AZURE_OPENAI_DEPLOYMENT=YOUR-AZURE-DEPLOYMENT-NAME
    AZURE_OPENAI_VERSION=2024-03-01-preview
    ```

    Si aún no has iniciado sesión en la cuenta de Azure asociada con ese deployment, ejecuta este comando para iniciar sesión:

    ```shell
    az login
    ```
3. Para OpenAI.com, actualiza el archivo `.env` con tu clave API de OpenAI y el nombre del modelo deseado.

    ```bash
    API_HOST=openai
    OPENAI_KEY=TU-CLAVE-API-OPENAI
    OPENAI_MODEL=gpt-3.5-turbo
    ```

4. Para Ollama, actualiza el archivo [.env](http://_vscodecontentref_/0) con tu endpoint de Ollama y nombre del modelo (cualquier modelo que hayas descargado).

    ```bash
    API_HOST=ollama
    OLLAMA_ENDPOINT=http://localhost:11434/v1
    OLLAMA_MODEL=llama2
    ```

    Si estás ejecutando dentro del Dev Container, reemplaza `localhost` con `host.docker.internal`.

5. Para GitHub Models, actualiza el archivo [.env](http://_vscodecontentref_/1) con el nombre de tu GitHub Model.

    ```bash
    API_HOST=github
    GITHUB_MODEL=gpt-4o
    ```

    Necesitarás una variable de entorno `GITHUB_TOKEN` que almacene un token de acceso personal de GitHub.
    Si estás ejecutando esto dentro de un GitHub Codespace, el token estará disponible automáticamente.
    Si no, genera un nuevo [token de acceso personal](https://github.com/settings/tokens) y ejecuta este comando para establecer la variable de entorno `GITHUB_TOKEN`:

    ```shell
    export GITHUB_TOKEN="<aquí-va-tu-token-de-github>"
