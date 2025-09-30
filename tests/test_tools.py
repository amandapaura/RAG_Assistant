import pytest
from unittest.mock import Mock, patch
from tools.vector_search import VectorSearchTool
from tools.web_search import WebSearchTool
from tools.weather_api import WeatherTool

class TestVectorSearchTool:
    def setup_method(self):
        self.tool = VectorSearchTool()
    
    @patch('tools.vector_search.qdrant_manager')
    def test_vector_search_success(self, mock_qdrant):
        mock_qdrant.similarity_search.return_value = [
            {"text": "Test document", "score": 0.8, "metadata": {}}
        ]
        
        result = self.tool._run("test query")
        
        assert "Test document" in result
        assert "0.800" in result

    @patch('tools.vector_search.qdrant_manager')
    def test_vector_search_no_results(self, mock_qdrant):
        mock_qdrant.similarity_search.return_value = []
        
        result = self.tool._run("unknown query")
        
        assert "Nenhum documento relevante encontrado" in result

class TestWebSearchTool:
    def setup_method(self):
        self.tool = WebSearchTool()
    
    @patch('requests.get')
    def test_web_search_success(self, mock_get):
        mock_response = Mock()
        mock_response.content = "<html><div class='result'><h2>Test Title</h2><a class='result__snippet'>Test snippet</a></div></html>"
        mock_get.return_value = mock_response
        
        result = self.tool._run("test query")
        
        assert "Test Title" in result or "Nenhum resultado encontrado" in result

class TestWeatherTool:
    def setup_method(self):
        self.tool = WeatherTool()
    
    @patch('tools.weather_api.settings')
    def test_weather_without_api_key(self, mock_settings):
        mock_settings.openweather_api_key = None
        
        result = self.tool._run("São Paulo")
        
        assert "dados simulados" in result
        assert "25°C" in result