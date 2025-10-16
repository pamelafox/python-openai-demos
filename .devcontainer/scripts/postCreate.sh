#!/bin/sh
set -e

echo "Installing large ML packages..."

# Install torch CPU-only (much smaller than CUDA versions)
pip3 install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch

# Install transformer/ML packages that depend on torch
pip3 install --no-cache-dir \
    sentence-transformers \
    pymupdf4llm \
    lunr

echo "Post-create setup complete!"
