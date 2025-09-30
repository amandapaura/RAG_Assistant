-- Inicialização do banco PostgreSQL
CREATE DATABASE IF NOT EXISTS rag_assistant;

\c rag_assistant;

-- Tabela para logs de conversas
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_query TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    agent_used VARCHAR(100),
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Tabela para métricas de avaliação
CREATE TABLE IF NOT EXISTS evaluation_metrics (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    context_relevance FLOAT,
    answer_relevance FLOAT,
    groundedness FLOAT,
    pii_detected BOOLEAN DEFAULT FALSE,
    jailbreak_detected BOOLEAN DEFAULT FALSE,
    overall_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de exemplo para demonstrar consultas SQL
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    description TEXT,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados de exemplo
INSERT INTO products (name, category, price, description, stock_quantity) VALUES
('Notebook Gamer', 'Eletrônicos', 2499.99, 'Notebook para games com placa de vídeo dedicada', 15),
('Mouse Wireless', 'Eletrônicos', 89.90, 'Mouse sem fio com sensor óptico', 50),
('Teclado Mecânico', 'Eletrônicos', 299.99, 'Teclado mecânico com switches blue', 25),
('Monitor 24"', 'Eletrônicos', 899.99, 'Monitor LED 24 polegadas Full HD', 8),
('Cadeira Gamer', 'Móveis', 799.99, 'Cadeira ergonômica para games', 12);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);