"""
RAG Assistant - Sistema Conversacional Open Source
"""

__version__ = "1.0.0"
__author__ = "RAG Assistant Team"

from .config import settings
from .core.embeddings import embedding_manager
from .core.evaluation import rag_evaluator

__all__ = [
    "settings",
    "embedding_manager", 
    "rag_evaluator"
]