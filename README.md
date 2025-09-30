# 🤖 RAG Assistant - Sistema Conversacional Open Source

Sistema avançado de assistente conversacional baseado em RAG (Retrieval-Augmented Generation) usando apenas tecnologias open source.

## ✨ Características

- **🧠 LLMs Open Source**: Utiliza modelos do Hugging Face
- **🔍 Busca Vetorial**: Qdrant para similarity search
- **🌐 Multi-Agent**: Agentes especializados (RAG, Web Search, Weather, SQL)
- **📊 Avaliação Automatizada**: Métricas de context relevance, groundedness, PII detection
- **🕸️ LangGraph**: Orquestração avançada de workflows
- **💬 Interface Moderna**: Streamlit com chat em tempo real
- **🐳 Docker First**: Deploy completo com docker-compose

## 🚀 Quick Start
```bash
# 1. Clone o repositório
git clone <repo-url>
cd rag-assistant

# 2. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 3. Inicie com Docker
docker-compose up --build

# 4. Acesse a aplicação
open http://localhost:8501