"""
Vector database components
"""

from .qdrant_client import qdrant_manager, QdrantManager

__all__ = [
    "qdrant_manager",
    "QdrantManager"
]