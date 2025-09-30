import streamlit as st
import sys
import os

# # FORÇAR RELOAD DOS MÓDULOS (adicione isso)
# modules_to_reload = [
#     'graph.workflow',
#     'graph.nodes', 
#     'agents.rag_agent',
#     'agents.search_agent',
#     'agents.weather_agent',
#     'agents.base'
# ]

# for module_name in modules_to_reload:
#     if module_name in sys.modules:
#         reload(sys.modules[module_name])
                       
# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.chat import chat_interface
from ui.sidebar import render_sidebar
from dotenv import load_dotenv

def main():
    """Função principal da aplicação Streamlit"""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Configuração da página
    st.set_page_config(
        page_title="RAG Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ff6b6b;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        margin-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Renderiza sidebar e obtém configurações
    config = render_sidebar()
    
    # Renderiza interface principal
    chat_interface.render_chat(config)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 RAG Assistant - Powered by Open Source LLMs & LangGraph</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()