# 🤖 RAG Assistant - Sistema Conversacional Open Source

Sistema avançado de assistente conversacional baseado em RAG (Retrieval-Augmented Generation) usando apenas tecnologias open source.

## ✨ Características

* **🧠 LLMs Open Source**: Utiliza modelos do Hugging Face
* **🔍 Busca Vetorial**: Qdrant para similarity search
* **🌐 Multi-Agent**: Agentes especializados (RAG, Web Search, Weather, SQL)
* **📊 Avaliação Automatizada**: Métricas de context relevance, groundedness, PII detection
* **🕸️ LangGraph**: Orquestração avançada de workflows
* **💬 Interface Moderna**: Streamlit com chat em tempo real
* **🐳 Docker First**: Deploy completo com docker-compose

## 📊 Fluxo Completo

1. Usuário pergunta: "O que é RAG?"
   ↓
2. `rag_agent.py` chama:

   ```python
   search_results = self.execute_tool("vector_search", query=query, k=3)
   ```

   ↓
3. `vector_search.py` busca no Qdrant e retorna resultados com score:

   * 0.8: RAG significa Retrieval-Augmented Generation...
   * 0.7: O RAG funciona em três etapas...
   * 0.6: Componentes do Sistema RAG...
     ↓
4. `rag_agent.py` passa para o LLM:

   ```python
   llm_response = llm_manager.generate_response(query, search_results)
   ```

   ↓
5. LLM monta o prompt:

   ```text
   Context: [documentos do Qdrant]
   Question: o que é RAG?
   Answer:
   ```

   ↓
6. LLM gera resposta **baseada no contexto**
   ↓
7. Retorna resposta natural ao usuário

## 🐳 Docker - Configuração e Execução

### Build e Start dos containers

```bash
# Build das imagens
docker-compose build

# Start dos serviços em background
docker-compose up -d

# Verificar status dos containers
docker-compose ps
```

### Logs

```bash
# Logs do Streamlit
docker-compose logs -f app

# Logs do LLM service
docker-compose logs -f llm-service
```

### Parar ou reiniciar containers

```bash
# Parar todos os containers
docker-compose down

# Reiniciar containers
docker-compose restart
```

## 🚀 Quick Start - Desenvolvimento Local

```bash
# 1. Clone o repositório
git clone https://github.com/amandapaura/RAG_Assistant.git
cd RAG_Assistant

# 2. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 3. Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# 4. Instale dependências Python
pip install -r requirements.txt

# 5. Suba os serviços Docker
docker-compose up -d
# OU se usar a versão simples (Recomendado)
docker-compose -f docker-compose-simple.yml up -d

# 6. Aguarde serviços ficarem prontos (~30 segundos)

# 7. Ingira documentos no Qdrant
python scripts/ingest.py data/documents

# 8. Rode a aplicação
streamlit run app/main.py

# 9. Testar no navegador
# A aplicação deve abrir em http://localhost:8501
```

### Perguntas para testar:

* "O que é RAG?"
* "Me fale sobre LLM?"
* "Como está o tempo em São Paulo?" (dados simulados)
* "Buscar notícias sobre inteligência artificial"

