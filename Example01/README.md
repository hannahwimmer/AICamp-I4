# AICamp Coding Examples Setup

1. Eine virtuelle `uv`-Umgebung für das Projekt herstellen (aus dem zur Verfügung
   gestellten `.toml`-file):
   `uv sync`
2. Ein Llama-Modell (LLM) laden:
   - `curl -fsSL https://ollama.ai/install.sh | sh`
   - `ollama --version`
   - `ollama pull llama3.2:1b`
