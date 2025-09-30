"""API FastAPI para servir o LLM"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms.ctransformers import CTransformers
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Service")

# Variável global para o modelo
llm = None

class GenerateRequest(BaseModel):
    query: str
    context: str
    max_tokens: int = 256
    temperature: float = 0.7

class GenerateResponse(BaseModel):
    response: str
    model_loaded: bool

@app.on_event("startup")
async def load_model():
    """Carrega o modelo na inicialização do serviço"""
    global llm
    try:
        logger.info("🤖 Carregando LLM... (isso pode demorar alguns minutos)")
        llm = CTransformers(
                model='TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF',  # Só 600MB!
                model_type='llama',
                model_file='tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf',
                config={
                    'max_new_tokens': 256,
                    'temperature': 0.7,
                    'context_length': 2048
                }
            )
        logger.info("✅ LLM carregado com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar LLM: {e}")
        llm = None

@app.get("/health")
async def health_check():
    """Verifica se o serviço está pronto"""
    return {
        "status": "healthy",
        "model_loaded": llm is not None
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """Gera resposta usando o LLM"""
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM not loaded yet")
    
    try:
        # Monta o prompt
        prompt = f"""Context: {request.context}

Question: {request.query}

Answer (based on the context above):"""
        
        logger.info(f"Gerando resposta para: {request.query[:50]}...")
        
        # Gera resposta
        response = llm(prompt)
        
        return GenerateResponse(
            response=response.strip(),
            model_loaded=True
        )
    
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        raise HTTPException(status_code=500, detail=str(e))