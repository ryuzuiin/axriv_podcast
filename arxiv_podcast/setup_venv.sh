#！/bin/bash

echo "🚀 Creating virtual environment (.venv)..."
python3 -m venv .venv

echo "✅ Virtual environment created."

echo "🐍 Activating environment and installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install openai arxiv pyyaml pytest

echo "📦 Freezing dependencies..."
pip freeze > requirements.txt

echo "🎉 Setup complete. To activate your environment:"
echo "  source .venv/bin/activate"