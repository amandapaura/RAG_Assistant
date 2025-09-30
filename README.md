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

## 📊 Fluxo Completo:

1. Usuário pergunta: "o que é RAG?"
                ↓
2. rag_agent.py chama:
   search_results = self.execute_tool("vector_search", query=query, k=3)
                ↓
3. vector_search.py busca no Qdrant e retorna:
   "1. (Score: 0.8) RAG significa Retrieval-Augmented Generation...
    2. (Score: 0.7) O RAG funciona em três etapas...
    3. (Score: 0.6) Componentes do Sistema RAG..."
                ↓

## Passos da V2
4. rag_agent.py passa para o LLM:
   llm_response = llm_manager.generate_response(query, search_results)
                ↓
5. llm.py monta o prompt:
   "Context: [documentos do Qdrant]
    Question: o que é RAG?
    Answer:"
                ↓
6. LLM gera resposta BASEADA no contexto
                ↓
7. Retorna resposta natural ao usuário

## 🚀 Quick Start
```bash
# 1. Clone o repositório
git clone https://github.com/amandapaura/RAG_Assistant.git
cd RAG_Assistant

# 2. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 3. Inicie com Docker
docker-compose up --build

# 4. Acesse a aplicação
streamlit run app/main.py
```

