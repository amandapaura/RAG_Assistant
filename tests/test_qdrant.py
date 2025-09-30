import sys
import os

# Adiciona a raiz do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

# Crie um arquivo test_qdrant.py na raiz
from vector_db.qdrant_client import qdrant_manager

# Verificar coleção
try:
    info = qdrant_manager.client.get_collection("documents")
    print(f"✅ Collection existe")
    print(f"   Pontos: {info.points_count}")
    print(f"   Vetores: {info.vectors_count}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Testar busca simples
results = qdrant_manager.similarity_search("RAG", k=5, score_threshold=0.0)
print(f"\nResultados: {len(results)}")
for r in results:
    print(f"  - Score: {r['score']:.3f}")
    print(f"    Text: {r['text'][:100]}...")