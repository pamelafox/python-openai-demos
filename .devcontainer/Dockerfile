FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

COPY requirements-dev.txt /tmp/pip-tmp/
COPY requirements.txt /tmp/pip-tmp/
COPY requirements-rag.txt /tmp/pip-tmp/

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt \
    && rm -rf /tmp/pip-tmp
