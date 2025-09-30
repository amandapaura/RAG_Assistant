from typing import List, Dict, Any, Optional
import re
from dataclasses import dataclass
from sentence_transformers import util
from app.core.embeddings import embedding_manager

@dataclass
class EvaluationMetrics:
    context_relevance: float
    answer_relevance: float
    groundedness: float
    pii_detected: bool
    jailbreak_detected: bool
    overall_score: float

class RAGEvaluator:
    def __init__(self):
        self.pii_patterns = [
            r'\d{3}-\d{2}-\d{4}',  # SSN
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\(\d{3}\)\s*\d{3}-\d{4}',  # Phone number
        ]
        
        self.jailbreak_patterns = [
            "ignore previous instructions",
            "act as if",
            "pretend you are",
            "roleplay as",
            "forget everything",
            "disregard the above"
        ]
    
    def evaluate_response(
        self, 
        query: str,
        response: str,
        context_docs: List[str] = None
    ) -> EvaluationMetrics:
        """Avalia uma resposta RAG com múltiplas métricas"""
        
        context_relevance = self._calculate_context_relevance(query, context_docs or [])
        answer_relevance = self._calculate_answer_relevance(query, response)
        groundedness = self._calculate_groundedness(response, context_docs or [])
        pii_detected = self._detect_pii(response)
        jailbreak_detected = self._detect_jailbreak(query)
        
        # Score geral (média ponderada)
        overall_score = (
            context_relevance * 0.3 +
            answer_relevance * 0.3 +
            groundedness * 0.3 +
            (0 if pii_detected else 0.05) +
            (0 if jailbreak_detected else 0.05)
        )
        
        return EvaluationMetrics(
            context_relevance=context_relevance,
            answer_relevance=answer_relevance,
            groundedness=groundedness,
            pii_detected=pii_detected,
            jailbreak_detected=jailbreak_detected,
            overall_score=overall_score
        )
    
    def _calculate_context_relevance(self, query: str, context_docs: List[str]) -> float:
        """Calcula relevância do contexto recuperado"""
        if not context_docs:
            return 0.0
        
        query_embedding = embedding_manager.embed_query(query)
        context_embeddings = embedding_manager.embed_texts(context_docs)
        
        similarities = [
            util.cos_sim([query_embedding], [doc_emb]).item()
            for doc_emb in context_embeddings
        ]
        
        return max(similarities) if similarities else 0.0
    
    def _calculate_answer_relevance(self, query: str, response: str) -> float:
        """Calcula relevância da resposta à pergunta"""
        if not response.strip():
            return 0.0
        
        query_embedding = embedding_manager.embed_query(query)
        response_embedding = embedding_manager.embed_query(response)
        
        similarity = util.cos_sim([query_embedding], [response_embedding]).item()
        return max(0.0, similarity)
    
    def _calculate_groundedness(self, response: str, context_docs: List[str]) -> float:
        """Calcula quão fundamentada a resposta está no contexto"""
        if not context_docs or not response.strip():
            return 0.0
        
        response_embedding = embedding_manager.embed_query(response)
        context_embeddings = embedding_manager.embed_texts(context_docs)
        
        similarities = [
            util.cos_sim([response_embedding], [doc_emb]).item()
            for doc_emb in context_embeddings
        ]
        
        return max(similarities) if similarities else 0.0
    
    def _detect_pii(self, text: str) -> bool:
        """Detecta informações pessoais identificáveis"""
        for pattern in self.pii_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _detect_jailbreak(self, query: str) -> bool:
        """Detecta tentativas de jailbreak"""
        query_lower = query.lower()
        for pattern in self.jailbreak_patterns:
            if pattern in query_lower:
                return True
        return False

# Instância global do avaliador
rag_evaluator = RAGEvaluator()