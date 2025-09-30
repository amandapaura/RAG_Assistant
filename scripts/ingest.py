#!/usr/bin/env python3
"""Script para ingestão de documentos na base vetorial"""

import os
import sys
import argparse
from pathlib import Path
from typing import List
import PyPDF2
import docx
from bs4 import BeautifulSoup

# Adiciona path do projeto
sys.path.append(str(Path(__file__).parent.parent))

from vector_db.qdrant_client import qdrant_manager
from app.core.embeddings import embedding_manager

class DocumentIngester:
    def __init__(self):
        self.supported_formats = {'.txt', '.pdf', '.docx', '.html', '.md'}
    
    def ingest_directory(self, directory_path: str):
        """Ingere todos os documentos de um diretório"""
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"Diretório não encontrado: {directory_path}")
            return
        
        documents = []
        metadatas = []
        
        for file_path in directory.rglob('*'):
            if file_path.suffix.lower() in self.supported_formats:
                try:
                    content = self._extract_text(file_path)
                    if content.strip():
                        # Divide em chunks
                        chunks = self._chunk_text(content, chunk_size=500, overlap=50)
                        
                        for i, chunk in enumerate(chunks):
                            documents.append(chunk)
                            metadatas.append({
                                'source': str(file_path),
                                'chunk_id': i,
                                'file_type': file_path.suffix,
                                'file_name': file_path.name
                            })
                        
                        print(f"Processado: {file_path.name} ({len(chunks)} chunks)")
                
                except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")
        
        if documents:
            print(f"\nIngerindo {len(documents)} chunks...")
            qdrant_manager.add_documents(documents, metadatas)
            print("Ingestão concluída!")
        else:
            print("Nenhum documento válido encontrado.")
    
    def _extract_text(self, file_path: Path) -> str:
        """Extrai texto de diferentes formatos de arquivo"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.txt' or suffix == '.md':
            return file_path.read_text(encoding='utf-8')
        
        elif suffix == '.pdf':
            return self._extract_pdf_text(file_path)
        
        elif suffix == '.docx':
            return self._extract_docx_text(file_path)
        
        elif suffix == '.html':
            return self._extract_html_text(file_path)
        
        return ""
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extrai texto de PDF"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except:
            return ""
    
    def _extract_docx_text(self, file_path: Path) -> str:
        """Extrai texto de DOCX"""
        try:
            doc = docx.Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except:
            return ""
    
    def _extract_html_text(self, file_path: Path) -> str:
        """Extrai texto de HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
                return soup.get_text()
        except:
            return ""
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Divide texto em chunks com overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks

def main():
    parser = argparse.ArgumentParser(description="Ingerir documentos na base vetorial")
    parser.add_argument("directory", help="Diretório contendo documentos para ingestão")
    parser.add_argument("--chunk-size", type=int, default=500, help="Tamanho dos chunks")
    parser.add_argument("--overlap", type=int, default=50, help="Overlap entre chunks")
    
    args = parser.parse_args()
    
    ingester = DocumentIngester()
    ingester.ingest_directory(args.directory)

if __name__ == "__main__":
    main()