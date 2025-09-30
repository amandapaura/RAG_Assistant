from langchain.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
from app.config import settings

try:
    from langchain_community.utilities import SQLDatabase
except ImportError:
    from langchain.sql_database import SQLDatabase

class SQLQueryInput(BaseModel):
    question: str = Field(description="Pergunta em linguagem natural para consultar o banco")

class SQLQueryTool(BaseTool):
    name = "sql_query"
    description = "Executa consultas SQL baseadas em perguntas em linguagem natural. Retorna informações sobre produtos, vendas e dados estruturados."
    args_schema: Type[BaseModel] = SQLQueryInput
    
    def __init__(self):
        super().__init__()
        self.db = None
        try:
            self.db = SQLDatabase.from_uri(settings.postgres_url)
        except Exception as e:
            print(f"⚠️  PostgreSQL não disponível: {e}")
            print("   Tool SQL funcionará em modo informativo")
    
    def _run(self, question: str) -> str:
        """Executa consulta SQL ou retorna informações"""
        
        if not self.db:
            return self._mock_response(question)
        
        try:
            # Obtém informações das tabelas
            tables_info = self.db.get_table_info()
            
            # Lista de tabelas disponíveis
            table_names = self.db.get_usable_table_names()
            
            response = f"""**Informações do Banco de Dados:**

Tabelas disponíveis: {', '.join(table_names)}

Sua pergunta: "{question}"

📊 Esquema das tabelas:
{tables_info}

💡 Para consultas reais, conecte o PostgreSQL seguindo as instruções no README.
"""
            return response
        
        except Exception as e:
            return f"Erro ao consultar banco de dados: {str(e)}"
    
    def _mock_response(self, question: str) -> str:
        """Resposta simulada quando banco não está disponível"""
        
        mock_data = {
            "produtos": [
                {"id": 1, "nome": "Notebook", "preco": 2500.00, "estoque": 15},
                {"id": 2, "nome": "Mouse", "preco": 89.90, "estoque": 50},
                {"id": 3, "nome": "Teclado", "preco": 299.99, "estoque": 25}
            ]
        }
        
        question_lower = question.lower()
        
        if "produto" in question_lower or "item" in question_lower:
            return f"""**Dados simulados - Produtos:**

Com base na pergunta: "{question}"

Produtos disponíveis:
- Notebook: R$ 2.500,00 (15 em estoque)
- Mouse: R$ 89,90 (50 em estoque)  
- Teclado: R$ 299,99 (25 em estoque)

⚠️  **Nota:** PostgreSQL não conectado. Dados simulados para demonstração.
Para consultas reais, configure PostgreSQL com `docker-compose up -d postgres`
"""
        
        elif "preço" in question_lower or "preco" in question_lower or "valor" in question_lower:
            return """**Preços dos produtos:**
- Notebook: R$ 2.500,00
- Mouse: R$ 89,90
- Teclado: R$ 299,99

⚠️  Dados simulados. Configure PostgreSQL para dados reais."""
        
        elif "estoque" in question_lower:
            return """**Estoque disponível:**
- Notebook: 15 unidades
- Mouse: 50 unidades
- Teclado: 25 unidades

⚠️  Dados simulados. Configure PostgreSQL para dados reais."""
        
        else:
            return f"""**Consulta SQL:** "{question}"

⚠️  PostgreSQL não está conectado.

**Para ativar consultas SQL reais:**
1. Inicie PostgreSQL: `docker-compose up -d postgres`
2. Configure .env com as credenciais corretas
3. Reinicie a aplicação

**Dados simulados disponíveis:**
- Tabela 'produtos': 3 produtos cadastrados
- Consultas sobre preços, estoque e produtos
"""