# 🏗️ Arquitetura - RAG Assistant

## 📌 Visão Geral
O **RAG Assistant** é um sistema de assistente conversacional baseado em **RAG (Retrieval-Augmented Generation)**, construído apenas com tecnologias **open source**.  
A aplicação integra **busca vetorial**, **busca na web**, **consulta de previsão do tempo** e **LLMs open source**, oferecendo uma interface interativa via **Streamlit**.

---

## 🔹 Componentes Principais

- **Frontend**
  - Streamlit (interface de chat em tempo real)
  - Configurações de parâmetros (alguns ainda em default, ex: `confidence=0.3`)

- **Orquestração**
  - LangGraph (implementação atual com router simples)

- **Agentes**
  - **RAG Agent** → Busca em documentos com Qdrant
  - **Web Agent** → Busca de informações na web
  - **Weather Agent** → Consulta API de clima
  - **SQL Agent** → (planejado/expandível)

- **Modelos de Linguagem (LLMs)**
  - Hugging Face (modelos open source)
  - LLaMA Tiny (teste de geração contextual baseada nos documentos recuperados)

- **Vector Database**
  - Qdrant (armazenamento de embeddings e similarity search)

- **Embeddings**
  - Sentence Transformers

---

## 🔹 Fluxo de Funcionamento

1. Usuário envia uma pergunta pela interface Streamlit  
   ↓  
2. **Router (LangGraph)** direciona para o agente adequado (RAG, Web, Weather, SQL)  
   ↓  
3. Agente selecionado executa a ferramenta:  
   - RAG → consulta no Qdrant  
   - Web → busca externa  
   - Weather → chamada à API de clima  
   ↓  
4. Resultados retornam para o **LLM Manager**  
   - (Se RAG) LLaMA Tiny gera resposta baseada no contexto recuperado  
   ↓  
5. Resposta é formatada e exibida ao usuário na interface  

---

## 🔹 Infraestrutura

- **Docker-Compose** para orquestração dos serviços
  - `app` → aplicação principal (Streamlit + agentes)
  - `qdrant` → banco vetorial
  - `llm-service` → endpoint de modelos open source
  - `postgres` → suporte a dados tabulares (futuro uso em SQL Agent)

- **Ambiente de Desenvolvimento**
  - Python + Virtualenv (`.venv`)
  - Execução local com `streamlit run app/main.py`

---

## 🔹 Limitações Atuais

- Agentes ainda funcionam de forma **isolada** (não integrados entre si).
- Alguns parâmetros configuráveis estão fixados em **valores default**.
- LangGraph implementado apenas com **router simples**.
- LLaMA Tiny em fase de **testes** para geração contextual.

---

## 🔹 Futuras Melhorias

- Integração entre agentes para fluxos mais complexos.
- Parametrização dinâmica de configurações via interface.
- Implementação de métricas mais robustas (groundedness, relevance, PII detection).
- Substituição do router simples por workflows mais sofisticados no LangGraph.
