import streamlit as st
from typing import List, Dict, Any
from graph.workflow import rag_workflow
from app.core.evaluation import rag_evaluator
from ui.components import display_chat_message, display_evaluation_metrics, display_debug_info
import time
import uuid

class ChatInterface:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializa estado da sessão"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'message_count' not in st.session_state:
            st.session_state.message_count = 0
    
    def render_chat(self, config: Dict[str, Any]):
        """Renderiza interface de chat"""
        st.title("💬 RAG Assistant Chat")
        
        # Exibe mensagens do histórico
        for message in st.session_state.messages:
            display_chat_message(message, message["role"] == "user")
        
        # Input do usuário
        if prompt := st.chat_input("Digite sua pergunta..."):
            self.process_user_message(prompt, config)
    
    def process_user_message(self, prompt: str, config: Dict[str, Any]):
        """Processa mensagem do usuário"""
        # Adiciona mensagem do usuário
        user_message = {"role": "user", "content": prompt, "timestamp": time.time()}
        st.session_state.messages.append(user_message)
        
        # Exibe mensagem do usuário imediatamente
        display_chat_message(user_message, is_user=True)
        
        # Processa a consulta
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                response_data = self.get_assistant_response(prompt, config)
            
            # Exibe resposta
            st.write(response_data["response"])
            
            # Exibe métricas se habilitado
            if config.get("show_metrics") and "evaluation" in response_data:
                display_evaluation_metrics(response_data["evaluation"])
            
            # Exibe debug se habilitado
            if config.get("show_debug"):
                display_debug_info({
                    "agent_used": response_data.get("agent_used"),
                    "confidence": response_data.get("confidence"),
                    "tool_calls": response_data.get("tool_calls", [])
                })
        
        # Adiciona resposta do assistente ao histórico
        assistant_message = {
            "role": "assistant",
            "content": response_data["response"],
            "timestamp": time.time(),
            "metadata": {
                "agent_used": response_data.get("agent_used"),
                "confidence": response_data.get("confidence"),
                "tool_calls": response_data.get("tool_calls", []),
                "eval_score": response_data.get("evaluation", {}).get("overall_score", 0)
            }
        }
        st.session_state.messages.append(assistant_message)
        st.session_state.message_count += 1
        
        # Força atualização da interface
        st.rerun()
    
    # def get_assistant_response(self, query: str, config: Dict[str, Any]) -> Dict[str, Any]:
    #     """Obtém resposta do assistente via workflow"""
    #     try:
    #         # Processa via LangGraph workflow
    #         result = rag_workflow.process_query(query, config)
            
    #         # Avalia a resposta
    #         evaluation = rag_evaluator.evaluate_response(
    #             query=query,
    #             response=result["response"],
    #             context_docs=self._extract_context_docs(result)
    #         )
            
    #         return {
    #             **result,
    #             "evaluation": {
    #                 "context_relevance": evaluation.context_relevance,
    #                 "answer_relevance": evaluation.answer_relevance,
    #                 "groundedness": evaluation.groundedness,
    #                 "pii_detected": evaluation.pii_detected,
    #                 "jailbreak_detected": evaluation.jailbreak_detected,
    #                 "overall_score": evaluation.overall_score
    #             }
    #         }
            
    #     except Exception as e:
    #         return {
    #             "response": f"Erro ao processar consulta: {str(e)}",
    #             "agent_used": "error",
    #             "confidence": 0.0,
    #             "tool_calls": [],
    #             "evaluation": {
    #                 "context_relevance": 0.0,
    #                 "answer_relevance": 0.0,
    #                 "groundedness": 0.0,
    #                 "pii_detected": False,
    #                 "jailbreak_detected": False,
    #                 "overall_score": 0.0
    #             }
    #         }
    
    def get_assistant_response(self, query: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Obtém resposta do assistente"""
        try:
            # USAR ROUTER SIMPLES ao invés do workflow
            from graph.simple_router import simple_router
            result = simple_router.process_query(query, config)
            
            # Avalia a resposta
            from app.core.evaluation import rag_evaluator
            evaluation = rag_evaluator.evaluate_response(
                query=query,
                response=result["response"],
                context_docs=[]
            )
            
            return {
                **result,
                "evaluation": {
                    "context_relevance": evaluation.context_relevance,
                    "answer_relevance": evaluation.answer_relevance,
                    "groundedness": evaluation.groundedness,
                    "pii_detected": evaluation.pii_detected,
                    "jailbreak_detected": evaluation.jailbreak_detected,
                    "overall_score": evaluation.overall_score
                }
            }
            
        except Exception as e:
            print(f"❌ ERRO: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "response": f"Erro ao processar: {str(e)}",
                "agent_used": "error",
                "confidence": 0.0,
                "tool_calls": [],
                "evaluation": {
                    "context_relevance": 0.0,
                    "answer_relevance": 0.0,
                    "groundedness": 0.0,
                    "pii_detected": False,
                    "jailbreak_detected": False,
                    "overall_score": 0.0
                }
            }
    
    def _extract_context_docs(self, result: Dict[str, Any]) -> List[str]:
        """Extrai documentos de contexto dos tool calls"""
        context_docs = []
        
        for tool_call in result.get("tool_calls", []):
            if tool_call.get("tool") == "vector_search":
                # Em uma implementação real, você guardaria os documentos recuperados
                # Por enquanto, retornamos lista vazia
                pass
        
        return context_docs

chat_interface = ChatInterface()