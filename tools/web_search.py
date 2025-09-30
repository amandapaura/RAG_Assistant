from langchain.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from app.config import settings

class WebSearchInput(BaseModel):
    query: str = Field(description="Consulta para busca na web")
    num_results: int = Field(default=3, description="Número de resultados")

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Busca informações atualizadas na web usando DuckDuckGo"
    args_schema: Type[BaseModel] = WebSearchInput
    
    def _run(self, query: str, num_results: int = 3) -> str:
        try:
            # Usando DuckDuckGo API gratuita (sem necessidade de API key)
            search_url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(search_url, params=params, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            result_elements = soup.find_all('div', class_='result')[:num_results]
            
            for element in result_elements:
                title_elem = element.find('h2')
                snippet_elem = element.find('a', class_='result__snippet')
                link_elem = element.find('a', class_='result__url')
                
                if title_elem and snippet_elem:
                    title = title_elem.get_text().strip()
                    snippet = snippet_elem.get_text().strip()
                    link = link_elem['href'] if link_elem else "N/A"
                    
                    results.append(f"**{title}**\n{snippet}\nFonte: {link}\n")
            
            return "\n".join(results) if results else "Nenhum resultado encontrado."
        
        except Exception as e:
            return f"Erro na busca web: {str(e)}"