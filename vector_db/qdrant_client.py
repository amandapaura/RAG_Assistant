from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any, Optional
from app.config import settings
from app.core.embeddings import embedding_manager
import uuid
from ui.sidebar import render_sidebar

class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = "documents"
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Cria collection se não existir"""
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=embedding_manager.dimension,
                    distance=Distance.COSINE,
                ),
            )
    
    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """Adiciona documentos à collection"""
        if metadatas is None:
            metadatas = [{"text": text} for text in texts]
        
        embeddings = embedding_manager.embed_texts(texts)
        
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": text, **metadata}
            )
            for text, embedding, metadata in zip(texts, embeddings, metadatas)
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 5,
        score_threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Busca por similaridade"""
        query_embedding = embedding_manager.embed_query(query)
        
        print(f"   🔎 Buscando: k={k}, threshold={score_threshold}")
        
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
            score_threshold=score_threshold
        )
        
        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            }
            for hit in search_result
        ]

qdrant_manager = QdrantManager()