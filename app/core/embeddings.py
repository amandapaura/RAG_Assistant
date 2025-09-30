from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
from app.config import settings

class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model_name)
        
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings para lista de textos"""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()
    
    def embed_query(self, query: str) -> List[float]:
        """Gera embedding para consulta única"""
        embedding = self.model.encode([query], convert_to_tensor=False)
        return embedding[0].tolist()
    
    @property
    def dimension(self) -> int:
        """Retorna dimensão dos embeddings"""
        return self.model.get_sentence_embedding_dimension()

embedding_manager = EmbeddingManager()