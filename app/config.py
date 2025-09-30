try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings 
from typing import Optional
import os

class Settings(BaseSettings):
    # LLM Settings
    huggingface_model_name: str = "microsoft/DialoGPT-large"
    embedding_model_name: str = "all-MiniLM-L6-v2"
    
    # LLM Service 
    use_local_llm: bool = True
    llm_model_path: str = "TheBloke/Llama-2-7B-Chat-GGML"
    llm_max_tokens: int = 256
    llm_temperature: float = 0.7
    llm_service_url: str = "http://llm-service:8000"
    use_llm_service: bool = True

    # Vector DB
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    
    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "rag_assistant"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    
    # APIs
    openweather_api_key: str = "ValeTest"
    serpapi_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def postgres_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = "ignore" 
        
settings = Settings()