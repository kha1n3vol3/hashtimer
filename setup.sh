#!/bin/bash
# Install Python 3.11
uv python install 3.11

# Create venv with Python 3.11
uv venv --python 3.11

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip first as recommended
uv pip install --upgrade pip

# Install dependencies
uv pip install tdigest asyncio uvloop
uv pip install matplotlib

# Deactivate the virtual environment
deactivate

echo "Setup complete. "
echo "Use:"
echo "source .venv/bin/activate"
echo "to activate the environment"
