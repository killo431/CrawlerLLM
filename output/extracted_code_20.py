import requests

def suggest_selector(html: str, field_name: str) -> str:
    prompt = f"Given this HTML, find the best CSS selector for '{field_name}':\n{html}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    selector = response.json()["response"].strip()
    return selector

🐳 Dockerfile.llm
Dockerfile
FROM ghcr.io/ollama/ollama:latest

# Pull and prepare model
RUN ollama pull mistral

🧾 docker-compose.yml
version: '3.8'

services:
  scraper:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - llm
    environment:
      - OPENAI_API_KEY=unused
    volumes:
      - .:/app

  llm:
    build:
      context: .
      dockerfile: Dockerfile.llm
    ports:
      - "11434:11434"
