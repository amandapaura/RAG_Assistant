"""
Test modules
"""

# Configuração básica para testes
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configurações de teste
TEST_DATA_DIR = project_root / "tests" / "data"
TEST_CONFIG = {
    "embedding_model": "all-MiniLM-L6-v2",
    "qdrant_url": "http://localhost:6333",
    "test_mode": True
}

__all__ = [
    "TEST_DATA_DIR",
    "TEST_CONFIG"
]