# AI Content Generator — LangChain + Hugging Face

Production-minded layout for an AI content-generation service using LangChain and Hugging Face models.

Features
- FastAPI service with a /generate endpoint
- Reusable model client that supports Hugging Face Hub (via token) and local Transformers pipelines
- Prompt templates for tone / format / length control
- Dockerfile and GitHub Actions CI for basic checks

Quickstart (local)
1. Create a venv and install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Provide an HF hub token if you want hosted models:
   cp .env.example .env
   # edit .env and add HUGGINGFACEHUB_API_TOKEN

3. Run the server (ensure PYTHONPATH includes ./src):
   export PYTHONPATH=./src
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload

Docker (example)
  docker build -t ai-content-gen:latest .
  docker run -p 8000:8080 --env-file .env ai-content-gen:latest

License: MIT
