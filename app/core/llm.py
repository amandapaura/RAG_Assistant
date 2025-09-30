"""Cliente para o serviço LLM via API"""

import requests
from typing import Optional
from app.config import settings

class LLMManager:
    def __init__(self):
        self.llm_url = "http://llm-service:8000"  # URL do serviço no Docker
        # Para desenvolvimento local: self.llm_url = "http://localhost:8000"
        self._initialized = False
    
    def initialize(self):
        """Verifica se o serviço LLM está disponível"""
        if self._initialized:
            return
        
        try:
            print("🔍 Verificando serviço LLM...")
            response = requests.get(f"{self.llm_url}/health", timeout=5)
            data = response.json()
            
            if data.get("model_loaded"):
                print("✅ Serviço LLM disponível!")
                self._initialized = True
            else:
                print("⏳ Serviço LLM ainda carregando o modelo...")
                self._initialized = False
        except Exception as e:
            print(f"⚠️ Serviço LLM não disponível: {e}")
            self._initialized = False
    
    def generate_response(self, query: str, context: str) -> str:
        """Gera resposta usando o serviço LLM"""
        if not self._initialized:
            self.initialize()
        
        if not self._initialized:
            # Fallback sem LLM
            return f"**Informações encontradas:**\n\n{context}\n\n_Nota: Serviço LLM não disponível. Mostrando documentos recuperados._"
        
        try:
            response = requests.post(
                f"{self.llm_url}/generate",
                json={
                    "query": query,
                    "context": context,
                    "max_tokens": 256,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["response"]
            else:
                print(f"❌ Erro na API LLM: {response.status_code}")
                return f"Contexto recuperado:\n\n{context}"
        
        except Exception as e:
            print(f"❌ Erro ao chamar serviço LLM: {e}")
            return f"**Documentos encontrados:**\n\n{context}"

# Instância global
llm_manager = LLMManager()