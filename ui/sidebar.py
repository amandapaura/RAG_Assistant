import streamlit as st
from typing import Dict, Any
import os

def render_sidebar() -> Dict[str, Any]:
    """Renderiza sidebar com configurações"""
    with st.sidebar:
        st.title("🤖 RAG Assistant")
        st.markdown("---")
        
        # Configurações do sistema
        st.subheader("⚙️ Configurações")
        
        # Seleção de modelo de embedding
        embedding_model = st.selectbox(
            "Modelo de Embedding",
            ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "paraphrase-multilingual-MiniLM-L12-v2"],
            index=0
        )
        
        # Configurações de busca
        max_results = st.slider("Máximo de resultados", 1, 10, 5)
        confidence_threshold = st.slider("Limiar de confiança", 0.0, 1.0, 0.7)
        
        # Configurações de debug
        st.subheader("🔧 Debug")
        show_debug = st.checkbox("Mostrar informações de debug")
        show_metrics = st.checkbox("Mostrar métricas de avaliação", value=True)
        
        # Status do sistema
        st.subheader("📈 Status")
        
        # Verificar conexões
        qdrant_status = "🟢 Conectado" if check_qdrant_connection() else "🔴 Desconectado"
        st.text(f"Qdrant: {qdrant_status}")
        
        postgres_status = "🟢 Conectado" if check_postgres_connection() else "🔴 Desconectado"
        st.text(f"PostgreSQL: {postgres_status}")
        
        # Estatísticas
        st.subheader("📊 Estatísticas")
        if 'message_count' not in st.session_state:
            st.session_state.message_count = 0
        
        st.metric("Mensagens processadas", st.session_state.message_count)
        
        # Botão para limpar histórico
        if st.button("🗑️ Limpar Histórico"):
            if 'messages' in st.session_state:
                st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()
    
    return {
        "embedding_model": embedding_model,
        "max_results": max_results,
        "confidence_threshold": confidence_threshold,
        "show_debug": show_debug,
        "show_metrics": show_metrics
    }

def check_qdrant_connection() -> bool:
    """Verifica conexão com Qdrant"""
    try:
        from vector_db.qdrant_client import qdrant_manager
        # Teste simples de conexão
        qdrant_manager.client.get_collections()
        return True
    except:
        return False

def check_postgres_connection() -> bool:
    """Verifica conexão com PostgreSQL"""
    try:
        from app.config import settings
        import psycopg2
        conn = psycopg2.connect(settings.postgres_url)
        conn.close()
        return True
    except:
        return False