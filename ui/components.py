import streamlit as st
from typing import Dict, Any, List
import json
from datetime import datetime

def display_chat_message(message: Dict[str, Any], is_user: bool = True):
    """Exibe uma mensagem do chat"""
    with st.chat_message("user" if is_user else "assistant"):
        st.write(message["content"])
        
        if not is_user and "metadata" in message:
            with st.expander("Detalhes da resposta"):
                metadata = message["metadata"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Confiança", f"{metadata.get('confidence', 0):.2f}")
                with col2:
                    st.metric("Agent", metadata.get('agent_used', 'N/A'))
                with col3:
                    st.metric("Score", f"{metadata.get('eval_score', 0):.2f}")
                
                if metadata.get('tool_calls'):
                    st.json(metadata['tool_calls'])

def display_evaluation_metrics(metrics: Dict[str, float]):
    """Exibe métricas de avaliação"""
    st.subheader("📊 Métricas de Avaliação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Context Relevance", f"{metrics.get('context_relevance', 0):.3f}")
        st.metric("Answer Relevance", f"{metrics.get('answer_relevance', 0):.3f}")
        st.metric("Groundedness", f"{metrics.get('groundedness', 0):.3f}")
    
    with col2:
        pii_status = "❌" if metrics.get('pii_detected', False) else "✅"
        st.metric("PII Detection", pii_status)
        
        jailbreak_status = "❌" if metrics.get('jailbreak_detected', False) else "✅"
        st.metric("Jailbreak Detection", jailbreak_status)
        
        st.metric("Overall Score", f"{metrics.get('overall_score', 0):.3f}")

def display_debug_info(debug_data: Dict[str, Any]):
    """Exibe informações de debug"""
    with st.expander("🔍 Debug Info"):
        st.json(debug_data)