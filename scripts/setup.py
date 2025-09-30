#!/usr/bin/env python3
"""
Script de setup completo para o RAG Assistant
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import requests
from dotenv import load_dotenv

def check_docker():
    """Verifica se Docker está disponível"""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        print("✅ Docker e Docker Compose encontrados")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker ou Docker Compose não encontrados")
        return False

def setup_environment():
    """Configura arquivo .env se não existir"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✅ Arquivo .env criado a partir de .env.example")
    else:
        print("✅ Arquivo .env já existe")

def wait_for_services():
    """Aguarda serviços ficarem prontos"""
    services = {
        "Qdrant": "http://localhost:6333/health",
        "PostgreSQL": None  # Verificado via docker logs
    }
    
    print("⏳ Aguardando serviços ficarem prontos...")
    
    # Verifica Qdrant
    for i in range(30):
        try:
            response = requests.get(services["Qdrant"], timeout=2)
            if response.status_code == 200:
                print("✅ Qdrant está pronto")
                break
        except:
            pass
        
        if i == 29:
            print("❌ Timeout aguardando Qdrant")
            return False
        
        time.sleep(2)
    
    # Verifica PostgreSQL via logs
    result = subprocess.run(
        ["docker-compose", "logs", "postgres"], 
        capture_output=True, 
        text=True
    )
    
    if "database system is ready to accept connections" in result.stdout:
        print("✅ PostgreSQL está pronto")
    else:
        print("⚠️  PostgreSQL pode não estar completamente pronto")
    
    return True

def setup_sample_data():
    """Configura dados de exemplo"""
    sample_data_dir = Path("data/documents")
    sample_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Cria documento de exemplo
    sample_doc = sample_data_dir / "sample_knowledge.md"
    if not sample_doc.exists():
        sample_content = """# Base de Conhecimento - RAG Assistant

## O que é RAG?
RAG (Retrieval-Augmented Generation) é uma técnica que combina busca de informações com geração de texto usando LLMs.

## Componentes do Sistema
- **Vector Database**: Qdrant para armazenamento de embeddings
- **LLM**: Modelos open source via Hugging Face
- **Agents**: Agentes especializados para diferentes tarefas
- **Workflow**: LangGraph para orquestração

## Funcionalidades
- Busca vetorial em documentos
- Busca na web em tempo real  
- Consultas meteorológicas
- Consultas SQL automatizadas
- Avaliação de qualidade das respostas

## Métricas de Avaliação
- Context Relevance: Relevância do contexto recuperado
- Answer Relevance: Relevância da resposta à pergunta
- Groundedness: Fundamentação da resposta no contexto
- PII Detection: Detecção de informações pessoais
- Jailbreak Detection: Detecção de tentativas de bypass
"""
        sample_doc.write_text(sample_content)
        print("✅ Documento de exemplo criado")

def run_ingestion():
    """Executa ingestão de documentos"""
    try:
        subprocess.run([
            "python", "scripts/ingest.py", "data/documents"
        ], check=True)
        print("✅ Ingestão de documentos concluída")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro na ingestão de documentos")
        return False

def main():
    """Função principal de setup"""
    print("🚀 Iniciando setup do RAG Assistant...\n")
    
    # Verificações preliminares
    if not check_docker():
        sys.exit(1)
    
    # Setup do ambiente
    setup_environment()
    load_dotenv()
    
    # Cria dados de exemplo
    setup_sample_data()
    
    # Inicia serviços
    print("📦 Iniciando serviços com Docker Compose...")
    try:
        subprocess.run([
            "docker-compose", "up", "-d", "--build"
        ], check=True)
        print("✅ Serviços iniciados")
    except subprocess.CalledProcessError:
        print("❌ Erro ao iniciar serviços")
        sys.exit(1)
    
    # Aguarda serviços
    if not wait_for_services():
        sys.exit(1)
    
    # Executa ingestão
    time.sleep(5)  # Aguarda um pouco mais
    run_ingestion()
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("   1. Acesse: http://localhost:8501")
    print("   2. Teste algumas perguntas:")
    print("      - 'O que é RAG?'")
    print("      - 'Como está o tempo em São Paulo?'")
    print("      - 'Buscar notícias sobre IA'")
    print("\n🔧 Para desenvolvimento:")
    print("   - Logs: docker-compose logs -f app")
    print("   - Restart: docker-compose restart app")
    print("   - Stop: docker-compose down")

if __name__ == "__main__":
    main()