from typing import Dict, Any, List
from dataclasses import dataclass
from agents.rag_agent import RAGAgent
from agents.search_agent import SearchAgent
from agents.weather_agent import WeatherAgent
from agents.base import AgentResponse
import re

@dataclass
class WorkflowState:
    query: str
    response: str = ""
    agent_used: str = ""
    confidence: float = 0.0
    tool_calls: List[Dict[str, Any]] = None
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tool_calls is None:
            self.tool_calls = []
        if self.context is None:
            self.context = {}

class WorkflowNodes:
    def __init__(self):
        self.rag_agent = RAGAgent()
        self.search_agent = SearchAgent()
        self.weather_agent = WeatherAgent()
    
    def classifier_node(self, state: WorkflowState) -> WorkflowState:
        """Classifica a consulta e determina qual agent usar"""
        query_lower = state.query.lower()
        
        # Padrões para classificação
        weather_patterns = ["tempo", "clima", "weather", "temperatura", "chuva", "sol"]
        web_search_patterns = ["notícias", "atual", "hoje", "recente", "último", "buscar"]
        
        if any(pattern in query_lower for pattern in weather_patterns):
            state.context["selected_agent"] = "weather"
        elif any(pattern in query_lower for pattern in web_search_patterns):
            state.context["selected_agent"] = "search"
        else:
            state.context["selected_agent"] = "rag"
        
        return state
    
    def rag_node(self, state: WorkflowState) -> WorkflowState:
        """Processa consulta com RAG agent"""
        response = self.rag_agent.process(state.query, state.context)
        return self._update_state_with_response(state, response, "rag")
    
    def search_node(self, state: WorkflowState) -> WorkflowState:
        """Processa consulta com Search agent"""
        response = self.search_agent.process(state.query, state.context)
        return self._update_state_with_response(state, response, "search")
    
    def weather_node(self, state: WorkflowState) -> WorkflowState:
        """Processa consulta com Weather agent"""
        response = self.weather_agent.process(state.query, state.context)
        return self._update_state_with_response(state, response, "weather")
    
    def fallback_node(self, state: WorkflowState) -> WorkflowState:
        """Node de fallback quando outros falham"""
        if state.confidence < 0.5:
            # Tenta busca na web como fallback
            response = self.search_agent.process(state.query, state.context)
            return self._update_state_with_response(state, response, "search_fallback")
        
        return state
    
    def _update_state_with_response(
        self, 
        state: WorkflowState, 
        response: AgentResponse, 
        agent_name: str
    ) -> WorkflowState:
        """Atualiza o state com a resposta do agent"""
        state.response = response.content
        state.agent_used = agent_name
        state.confidence = response.confidence
        state.tool_calls.extend(response.tool_calls)
        return state