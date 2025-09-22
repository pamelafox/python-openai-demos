# Demos de Python con OpenAI

Este repositorio contiene una colección de scripts en Python que demuestran cómo usar la API de OpenAI (y modelos compatibles) para generar completados de chat.

* [Ejemplos](#ejemplos)
  * [Completados de chat de OpenAI](#completados-de-chat-de-openai)
  * [Llamadas a funciones (Function calling)](#llamadas-a-funciones-function-calling)
  * [Generación aumentada con recuperación (RAG)](#generación-aumentada-con-recuperación-rag)
  * [Salidas estructuradas](#salidas-estructuradas)
* [Configuración del entorno de Python](#configuración-del-entorno-de-python)
* [Configurando las variables de entorno de OpenAI](#configurando-las-variables-de-entorno-de-openai)
  * [Usando modelos de GitHub](#usando-modelos-de-github)
  * [Usando Azure OpenAI](#usando-azure-openai)
  * [Usando OpenAI.com](#usando-openaicom)
  * [Usando modelos de Ollama](#usando-modelos-de-ollama)
* [Recursos](#recursos)

## Ejemplos

### Completados de chat de OpenAI

Estos scripts usan el paquete `openai` de Python para demostrar cómo utilizar la API de Chat Completions. En orden creciente de complejidad:

1. [`chat.py`](../chat.py): Script simple que muestra cómo generar un completado de chat.
2. [`chat_stream.py`](../chat_stream.py): Añade `stream=True` para recibir el completado progresivamente.
3. [`chat_history.py`](../chat_history.py): Añade un chat bidireccional que conserva el historial y lo reenvía en cada llamada.
4. [`chat_history_stream.py`](../chat_history_stream.py): Igual que el anterior pero además con `stream=True`.

Scripts adicionales de características:

* [`chat_safety.py`](../chat_safety.py): Manejo de excepciones para filtros de seguridad de contenido (Azure AI Content Safety).
* [`chat_async.py`](../chat_async.py): Uso de clientes asíncronos y envío concurrente de múltiples solicitudes con `asyncio.gather`.

### Llamadas a funciones (Function calling)

Estos scripts muestran cómo usar la característica "tools" (function calling) de la API de Chat Completions. Permite que el modelo decida si invoca funciones definidas por el desarrollador y devolver argumentos estructurados en lugar (o antes) de una respuesta en lenguaje natural.

En todos los ejemplos se declara una lista de funciones en el parámetro `tools`. El modelo puede responder con `message.tool_calls` que contiene una o más llamadas. Cada llamada incluye el `name` de la función y una cadena JSON con `arguments` que respetan el esquema declarado. Tu aplicación debe: (1) detectar las llamadas, (2) ejecutar la lógica local/externa correspondiente y (3) (opcionalmente) enviar el resultado de la herramienta de vuelta al modelo para una respuesta final.

Scripts (en orden de capacidad):

1. [`function_calling_basic.py`](../function_calling_basic.py): Declara una sola función `lookup_weather` y muestra la llamada (si existe) o el contenido normal.
2. [`function_calling_call.py`](../function_calling_call.py): Ejecuta `lookup_weather` si el modelo la solicita, parseando los argumentos JSON.
3. [`function_calling_extended.py`](../function_calling_extended.py): Hace el ciclo completo: tras ejecutar la función, añade un mensaje de rol `tool` con el resultado y vuelve a consultar al modelo para incorporar los datos reales.
4. [`function_calling_multiple.py`](../function_calling_multiple.py): Expone múltiples funciones (`lookup_weather`, `lookup_movies`) para observar cómo el modelo elige y cómo podrían devolverse múltiples llamadas.

Debe usarse un modelo que soporte function calling (por ejemplo, `gpt-4o`, `gpt-4o-mini`, etc.). Algunos modelos locales o antiguos no soportan `tools`.

### Generación aumentada con recuperación (RAG)

Scripts que muestran cómo realizar tareas de RAG, donde el modelo recupera información relevante y la utiliza para generar la respuesta.

Primero instala las dependencias específicas:

```bash
python -m pip install -r requirements-rag.txt
```

Luego ejecuta (en orden de complejidad):

* [`rag_csv.py`](../rag_csv.py): Recupera filas coincidentes de un CSV y las usa para responder.
* [`rag_multiturn.py`](../rag_multiturn.py): Igual, pero con chat multi‑turno y preservación de historial.
* [`rag_queryrewrite.py`](../rag_queryrewrite.py): Añade reescritura de la consulta del usuario para mejorar la recuperación.
* [`rag_documents_ingestion.py`](../rag_documents_ingestion.py): Ingeste de PDFs: convierte a Markdown (pymupdf), divide en fragmentos (LangChain), genera embeddings (OpenAI) y guarda en un JSON local.
* [`rag_documents_flow.py`](../rag_documents_flow.py): Flujo RAG que consulta el JSON creado anteriormente.
* [`rag_documents_hybrid.py`](../rag_documents_hybrid.py): Recuperación híbrida (vector + keywords), fusión con RRF y re‑ranking semántico con un modelo cross‑encoder.

### Salidas estructuradas

Estos scripts muestran cómo generar respuestas estructuradas usando modelos Pydantic:

* [`structured_outputs_basic.py`](../structured_outputs_basic.py): Extrae información simple de un evento.
* [`structured_outputs_description.py`](../structured_outputs_description.py): Añade descripciones en campos para guiar el formato.
* [`structured_outputs_enum.py`](../structured_outputs_enum.py): Usa enumeraciones para restringir valores.
* [`structured_outputs_function_calling.py`](../structured_outputs_function_calling.py): Usa funciones definidas con Pydantic para llamadas automáticas.
* [`structured_outputs_nested.py`](../structured_outputs_nested.py): Modelos anidados para estructuras más complejas (por ejemplo, eventos con participantes detallados).

## Configuración del entorno de Python

Si abres el repositorio en un Dev Container o GitHub Codespaces, todo estará ya listo. Si no, sigue:

1. Crea y activa un entorno virtual de Python.
2. Instala dependencias base:

```bash
python -m pip install -r requirements.txt
```

## Configurando las variables de entorno de OpenAI

Los scripts pueden ejecutarse con Azure OpenAI, OpenAI.com, Ollama (local) o GitHub Models, según lo que configures en el archivo `.env`. Existe un `.env.sample` como plantilla.

1. Copia la plantilla:

```bash
cp .env.sample .env
```

Luego ajusta según el proveedor elegido.

### Usando modelos de GitHub

En GitHub Codespaces el `GITHUB_TOKEN` ya está disponible y puedes usar gratis GitHub Models.

Para uso local crea un [PAT de GitHub](https://github.com/settings/tokens) (sin scopes especiales) y expórtalo:

```bash
export GITHUB_TOKEN=TU_TOKEN
```

Opcional: cambia de modelo (por defecto `gpt-4o`) definiendo `GITHUB_MODEL` (por ejemplo `gpt-4o-mini`):

```bash
API_HOST=github
GITHUB_MODEL=gpt-4o
```

### Usando Azure OpenAI

Provisiona los recursos y despliegues (por ejemplo con Azure Developer CLI) de modelos como `gpt-4o` y un modelo de embeddings.

```bash
API_HOST=azure
AZURE_OPENAI_ENDPOINT=https://TU-SERVICIO.openai.azure.com/openai/v1
AZURE_OPENAI_CHAT_DEPLOYMENT=TU-DEPLOYMENT-CHAT
AZURE_OPENAI_VERSION=2024-03-01-preview
```

Inicia sesión si no lo has hecho:

```bash
az login
```

### Usando OpenAI.com

Configura tu clave y modelo:

```bash
API_HOST=openai
OPENAI_API_KEY=TU-CLAVE-OPENAI
OPENAI_MODEL=gpt-4o-mini
```

### Usando modelos de Ollama

Instala [Ollama](https://ollama.com/) y descarga un modelo:

```bash
ollama pull llama3.1
```

Configura tu `.env`:

```bash
API_HOST=ollama
OLLAMA_ENDPOINT=http://localhost:11434/v1
OLLAMA_MODEL=llama3.1
```

Si ejecutas dentro de un Dev Container, reemplaza `localhost` por `host.docker.internal`.

## Recursos

* [Próxima serie octubre 2025: Python + IA](https://aka.ms/PythonIA/serie)
* [Serie de videos: Aprende Python + IA](https://techcommunity.microsoft.com/blog/EducatorDeveloperBlog/learn-python--ai-from-our-video-series/4400393)
