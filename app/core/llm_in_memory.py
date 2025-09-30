"""Gerenciador de LLM local usando CTransformers"""

from langchain_community.llms.ctransformers import CTransformers
from typing import Optional

class LLMManager:
    def __init__(self):
        self.llm = None
        self._initialized = False
    
    def initialize(self):
        """Inicializa o LLM (carrega apenas uma vez)"""
        if self._initialized:
            return
        
        try:
            print("🤖 Carregando LLM local (isso pode demorar na primeira vez)...")
            self.llm = CTransformers(
                model='TheBloke/Llama-2-7B-Chat-GGML',  # Versão Chat é melhor para conversação
                model_type='llama',
                config={
                    'max_new_tokens': 256,
                    'temperature': 0.7,
                    'context_length': 2048
                }
            )
            self._initialized = True
            print("✅ LLM carregado com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar LLM: {e}")
            print("   Respostas serão baseadas apenas nos documentos recuperados")
            self.llm = None
    
    def generate_response(self, query: str, context: str) -> str:
        """Gera resposta usando LLM com contexto"""
        if not self._initialized:
            self.initialize()
        
        if self.llm is None:
            return f"Com base nos documentos:\n\n{context}\n\nEssa informação responde sua pergunta sobre: {query}"
        
        try:
            # DEBUG: Mostrar o que está sendo enviado ao LLM
            prompt = f"""Context: {context}

            Question: {query}

            Answer (based on the context above):"""
            
            print(f"\n🤖 PROMPT ENVIADO AO LLM:")
            print("="*60)
            print(prompt)
            print("="*60)
            
            response = self.llm(prompt)
            
            print(f"\n✅ RESPOSTA DO LLM:")
            print(response.strip())
            print("="*60)
            
            return response.strip()
        
        except Exception as e:
            print(f"❌ Erro ao gerar resposta com LLM: {e}")
            return f"Contexto recuperado:\n\n{context}"

# Instância global (singleton)
llm_manager = LLMManager()