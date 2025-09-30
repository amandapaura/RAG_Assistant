"""Router simples sem LangGraph - mais confiável"""

from typing import Dict, Any
from agents.rag_agent import RAGAgent
from agents.search_agent import SearchAgent
from agents.weather_agent import WeatherAgent

class SimpleRouter:
    def __init__(self):
        self.rag_agent = RAGAgent()
        self.search_agent = SearchAgent()
        self.weather_agent = WeatherAgent()
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa query escolhendo o agent correto"""
        
        query_lower = query.lower()
        
        print(f"\n🔍 ROUTER: Processando query: {query}")
        
        # 1. Weather Agent
        weather_keywords = [ "tempo", "clima", "weather", "temperatura", "chuva", 
                            "previsão", "graus", "celsius", "calor", "frio", "sol"]
        
        if any(kw in query_lower for kw in weather_keywords):
            print(f"   → Escolhido: WEATHER AGENT")
            response = self.weather_agent.process(query, context)
            agent_name = "weather"
        
        # 2. Search Agent
        elif any(kw in query_lower for kw in ["notícia", "noticia", "news", "buscar na web", "pesquisar", "google", "atual"]):
            print(f"   → Escolhido: SEARCH AGENT")
            response = self.search_agent.process(query, context)
            agent_name = "search"
        
        # 3. RAG Agent (padrão)
        else:
            print(f"   → Escolhido: RAG AGENT")
            response = self.rag_agent.process(query, context)
            agent_name = "rag"
        
        print(f"   ✅ Response: {response.content[:100]}...")
        
        return {
            "response": response.content,
            "agent_used": agent_name,
            "confidence": response.confidence,
            "tool_calls": response.tool_calls,
            "query": query
        }

# Instância global
simple_router = SimpleRouter()