#!/usr/bin/env python3
"""
Script de monitoramento do sistema RAG Assistant
"""

import time
import requests
import psycopg2
from pathlib import Path
import json
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent))
from app.config import settings

class SystemMonitor:
    def __init__(self):
        self.services = {
            "streamlit": "http://localhost:8501/_stcore/health",
            "qdrant": "http://localhost:6333/health",
            "postgres": None  # Checado via conexão direta
        }
    
    def check_all_services(self):
        """Verifica status de todos os serviços"""
        status = {}
        
        # Check HTTP services
        for service, url in self.services.items():
            if url:
                status[service] = self._check_http_service(url)
            else:
                status[service] = self._check_postgres()
        
        return status
    
    def _check_http_service(self, url):
        """Verifica serviço HTTP"""
        try:
            response = requests.get(url, timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _check_postgres(self):
        """Verifica PostgreSQL"""
        try:
            conn = psycopg2.connect(settings.postgres_url)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_report(self):
        """Gera relatório de status"""
        status = self.check_all_services()
        
        print("🔍 RAG Assistant - Status dos Serviços")
        print("=" * 40)
        
        for service, info in status.items():
            emoji = "✅" if info["status"] == "healthy" else "❌"
            print(f"{emoji} {service.capitalize()}: {info['status']}")
            
            if "response_time" in info:
                print(f"   Response time: {info['response_time']:.3f}s")
            
            if "error" in info:
                print(f"   Error: {info['error']}")
        
        print(f"\n⏰ Última verificação: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return status

def main():
    monitor = SystemMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        print("📊 Monitoramento contínuo iniciado (Ctrl+C para parar)")
        try:
            while True:
                monitor.generate_report()
                time.sleep(30)
                print("\n" + "="*50 + "\n")
        except KeyboardInterrupt:
            print("\n👋 Monitoramento interrompido")
    else:
        monitor.generate_report()

if __name__ == "__main__":
    main()