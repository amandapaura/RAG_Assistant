# RAG Assistant - Comandos úteis

.PHONY: help setup build start stop logs clean test ingest

help:
	@echo "RAG Assistant - Comandos disponíveis:"
	@echo "  setup     - Setup completo do projeto"
	@echo "  build     - Build das imagens Docker"
	@echo "  start     - Inicia todos os serviços"
	@echo "  stop      - Para todos os serviços"
	@echo "  logs      - Mostra logs da aplicação"
	@echo "  clean     - Remove containers e volumes"
	@echo "  test      - Executa testes"
	@echo "  ingest    - Ingere documentos na base"

setup:
	python scripts/setup.py

build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f app

clean:
	docker-compose down -v
	docker system prune -f

test:
	python -m pytest tests/ -v

ingest:
	python scripts/ingest.py data/documents