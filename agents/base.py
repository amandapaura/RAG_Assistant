from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel

class AgentResponse(BaseModel):
    content: str
    tool_calls: List[Dict[str, Any]] = []
    confidence: float = 1.0

class BaseAgent(ABC):
    def __init__(self, tools: List[BaseTool] = None):
        self.tools = tools or []
        self.tool_map = {tool.name: tool for tool in self.tools}
    
    @abstractmethod
    def process(self, query: str, context: Dict[str, Any] = None) -> AgentResponse:
        pass
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Executa uma ferramenta com os parâmetros fornecidos"""
        if tool_name not in self.tool_map:
            return f"Ferramenta '{tool_name}' não encontrada."
        
        try:
            tool = self.tool_map[tool_name]
            # Chama o método _run diretamente com os kwargs
            return tool._run(**kwargs)
        except Exception as e:
            return f"Erro ao executar {tool_name}: {str(e)}"