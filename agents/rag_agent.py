from .base import BaseAgent, AgentResponse
from tools.vector_search import VectorSearchTool
from typing import Dict, Any
from app.core.llm import llm_manager

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__([VectorSearchTool()])
        self.name = "rag_agent"
        # Inicializa LLM na primeira execução
        llm_manager.initialize()
    
    def process(self, query: str, context: Dict[str, Any] = None) -> AgentResponse:
        query_lower = query.lower()
        
        # Saudações simples
        if any(word in query_lower for word in ["oi", "olá", "ola", "hey", "hi", "hello"]):
            return AgentResponse(
                content="Olá! 👋 Como posso te ajudar hoje?\n\nPosso buscar informações na base de conhecimento, consultar o tempo ou buscar notícias na web.",
                confidence=1.0
            )
        
        # Agradecimentos
        if any(word in query_lower for word in ["obrigado", "obrigada", "valeu", "thanks"]):
            return AgentResponse(
                content="De nada! 😊 Posso ajudar com mais alguma coisa?",
                confidence=1.0
            )
        
        # Despedidas
        if any(word in query_lower for word in ["tchau", "adeus", "até logo", "bye"]):
            return AgentResponse(
                content="Até logo! 👋 Volte sempre!",
                confidence=1.0
            )
        
        # Busca na base de conhecimento
        try:
            search_results = self.execute_tool("vector_search", query=query, k=3)
            
            # Se não encontrou nada relevante
            if "Nenhum documento relevante encontrado" in search_results:
                return AgentResponse(
                    content=f"""Desculpe, não encontrei informações sobre "{query}" na base de conhecimento.

                            💡 **Sugestões:**
                            - Tente reformular sua pergunta
                            - Use "buscar notícias sobre..." para buscar na web
                            - Pergunte sobre RAG, embeddings, ou os componentes do sistema

                            O que você gostaria de saber?""",
                                                confidence=0.3
                                            )
            
            llm_response = llm_manager.generate_response(query, search_results)
            
            return AgentResponse(
                content=llm_response,
                tool_calls=[{"tool": "vector_search", "query": query}, {"tool": "llm_generation", "used": True}],
                confidence=0.8
            )
            
            # # Formata resposta com os resultados encontrados
            # return AgentResponse(
            #     content=f"""Encontrei estas informações sobre "{query}":\n\n{search_results}\n\nPosso esclarecer algum ponto específico?""",
            #     tool_calls=[{"tool": "vector_search", "query": query}],
            #     confidence=0.8
            # )
            
        except Exception as e:
            return AgentResponse(
                content=f"Erro ao buscar informações: {str(e)}",
                confidence=0.0
            )