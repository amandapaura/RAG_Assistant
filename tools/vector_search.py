from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from vector_db.qdrant_client import qdrant_manager

class VectorSearchInput(BaseModel):
    query: str = Field(description="Consulta para busca vetorial")
    k: int = Field(default=5, description="Número de resultados")
    threshold: float = Field(default=0.3, description="Score mínimo")

class VectorSearchTool(BaseTool):
    name = "vector_search"
    description = "Busca documentos relevantes na base de conhecimento usando similaridade vetorial"
    args_schema: Type[BaseModel] = VectorSearchInput
    
    def _run(self, query: str, k: int = 5,threshold: float = 0.3) -> str:
        print(f"\n🔍 VECTOR SEARCH TOOL")
        print(f"   Query: {query}")
        print(f"   K: {k}")
        try:
            results = qdrant_manager.similarity_search(query, 
                                                       k=k, 
                                                       score_threshold=threshold)
            print(f"   Resultados encontrados: {len(results)}")
            
            if not results:
                return "Nenhum documento relevante encontrado na base de conhecimento."
            
            # Debug: mostrar scores
            for i, result in enumerate(results):
                print(f"   [{i}] Score: {result['score']:.3f} - Text preview: {result['text'][:50]}...")
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. (Score: {result['score']:.3f}) {result['text']}"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return f"Erro na busca vetorial: {str(e)}"