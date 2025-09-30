from .base import BaseAgent, AgentResponse
from tools.weather_api import WeatherTool
from typing import Dict, Any
import re

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__([WeatherTool()])
        self.name = "weather_agent"
    
    def process(self, query: str, context: Dict[str, Any] = None) -> AgentResponse:
        # Extrai cidade da consulta (implementação simples)
        city = self._extract_city(query)
        
        if not city:
            return AgentResponse(
                content="Por favor, especifique uma cidade para consultar o tempo. Exemplo: 'Como está o tempo em São Paulo?'",
                confidence=0.2
            )
        
        weather_info = self.execute_tool("weather_query", city=city)
        
        return AgentResponse(
            content=weather_info,
            tool_calls=[{"tool": "weather_query", "city": city}],
            confidence=0.9
        )
    
    def _extract_city(self, query: str) -> str:
         # Padrões de extração
        patterns = [
            r"tempo (?:em|de|do|da|no|na) ([\w\s]+)",
            r"clima (?:em|de|do|da|no|na) ([\w\s]+)",
            r"temperatura (?:em|de|do|da|no|na) ([\w\s]+)",
            r"weather in ([\w\s]+)",
            r"(?:em|de|do|da|no|na) ([\w\s]+)",
        ]
        
        query_lower = query.lower()
        for pattern in patterns:
            match = re.search(pattern, query_lower)
            if match:
                city = match.group(1).capitalize()
                # Remove palavras comuns que não são cidades
                stop_words = ["tempo", "clima", "como", "está", "é", "tá"]
                city_words = [w for w in city.split() if w not in stop_words]
                if city_words:
                    return " ".join(city_words).title()
        
        return ""