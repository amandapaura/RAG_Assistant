import pytest
from unittest.mock import Mock, patch
from agents.rag_agent import RAGAgent
from agents.search_agent import SearchAgent
from agents.weather_agent import WeatherAgent

class TestRAGAgent:
    def setup_method(self):
        self.agent = RAGAgent()
    
    def test_process_with_valid_query(self):
        with patch.object(self.agent, 'execute_tool', return_value="Mocked search results"):
            response = self.agent.process("What is machine learning?")
            
            assert response.content is not None
            assert response.confidence > 0
            assert len(response.tool_calls) > 0
    
    def test_process_with_no_results(self):
        with patch.object(self.agent, 'execute_tool', return_value="Nenhum documento relevante encontrado"):
            response = self.agent.process("Unknown topic")
            
            assert "Não encontrei informações relevantes" in response.content
            assert response.confidence == 0.3

class TestSearchAgent:
    def setup_method(self):
        self.agent = SearchAgent()
    
    def test_process_web_search(self):
        with patch.object(self.agent, 'execute_tool', return_value="Web search results"):
            response = self.agent.process("latest news about AI")
            
            assert response.content is not None
            assert response.confidence == 0.7
            assert response.agent_used == "search_agent"

class TestWeatherAgent:
    def setup_method(self):
        self.agent = WeatherAgent()
    
    def test_process_with_city(self):
        with patch.object(self.agent, 'execute_tool', return_value="Weather info"):
            response = self.agent.process("How is the weather in São Paulo?")
            
            assert response.content == "Weather info"
            assert response.confidence == 0.9
    
    def test_process_without_city(self):
        response = self.agent.process("What's the weather?")
        
        assert "especifique uma cidade" in response.content
        assert response.confidence == 0.2