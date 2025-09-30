from langgraph.graph import Graph, END
from graph.nodes import WorkflowNodes, WorkflowState
from typing import Dict, Any

class RAGWorkflow:
    def __init__(self):
        self.nodes = WorkflowNodes()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> Graph:
        """Constrói o grafo do workflow"""
        workflow = Graph()
        
        # Adiciona nós
        workflow.add_node("classifier", self.nodes.classifier_node)
        workflow.add_node("rag", self.nodes.rag_node)
        workflow.add_node("search", self.nodes.search_node)
        workflow.add_node("weather", self.nodes.weather_node)
        workflow.add_node("fallback", self.nodes.fallback_node)
        
        # Define entrada
        workflow.set_entry_point("classifier")
        
        # Define edges condicionais do classifier
        def route_after_classifier(state: WorkflowState) -> str:
            agent = state.context.get("selected_agent", "rag")
            return agent
        
        workflow.add_conditional_edges(
            "classifier",
            route_after_classifier,
            {
                "rag": "rag",
                "search": "search",
                "weather": "weather"
            }
        )
        
        # Define edges condicionais para fallback
        def should_fallback(state: WorkflowState) -> str:
            if state.confidence < 0.5:
                return "fallback"
            return END
        
        # Conecta todos os agents ao sistema de fallback
        for node_name in ["rag", "search", "weather"]:
            workflow.add_conditional_edges(
                node_name,
                should_fallback,
                {
                    "fallback": "fallback",
                    END: END
                }
            )
        
        # Fallback sempre termina
        workflow.add_edge("fallback", END)
        
        return workflow.compile()
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa uma consulta através do workflow"""
        initial_state = WorkflowState(
            query=query,
            context=context or {}
        )
        
        # Executa o workflow
        result = self.graph.invoke(initial_state)
        
        return {
            "response": result.response,
            "agent_used": result.agent_used,
            "confidence": result.confidence,
            "tool_calls": result.tool_calls,
            "query": result.query
        }

# Instância global do workflow
rag_workflow = RAGWorkflow()