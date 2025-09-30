from .base import BaseAgent, AgentResponse
from tools.web_search import WebSearchTool
from typing import Dict, Any

class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__([WebSearchTool()])
        self.name = "search_agent"
    
    def process(self, query: str, context: Dict[str, Any] = None) -> AgentResponse:
        # Executa busca na web
        search_results = self.execute_tool("web_search", query=query, num_results=3)
        
        response_content = f"""Informações atualizadas da web sobre "{query}":

                            {search_results}

                            Estas informações foram obtidas de fontes online em tempo real."""
        
        return AgentResponse(
            content=response_content,
            tool_calls=[{"tool": "web_search", "query": query}],
            confidence=0.7
        )