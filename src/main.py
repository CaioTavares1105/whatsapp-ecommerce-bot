# ===========================================================
# src/main.py - Aplicação FastAPI Principal
# ===========================================================
# Ponto de entrada da aplicação.
#
# RESPONSABILIDADES:
# - Criar instância do FastAPI
# - Registrar rotas (routers)
# - Configurar middlewares
# - Configurar eventos de startup/shutdown
# - Configurar CORS, logging, etc
#
# COMO RODAR:
# uvicorn src.main:app --reload
# ===========================================================
"""
Aplicação FastAPI principal.

Este é o ponto de entrada da API do chatbot WhatsApp.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import get_settings
from src.presentation.api.routes import webhook_router


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ===========================================================
# LIFESPAN - Eventos de Startup e Shutdown
# ===========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    
    Startup:
    - Log de inicialização
    - Verificar conexões (banco, redis, etc)
    
    Shutdown:
    - Fechar conexões
    - Cleanup de recursos
    """
    # === STARTUP ===
    settings = get_settings()
    logger.info(f"🚀 Iniciando {settings.app_name}...")
    logger.info(f"📍 Ambiente: {settings.app_env}")
    logger.info(f"🔧 Debug: {settings.debug}")
    
    # TODO: Verificar conexões com banco/redis
    
    yield  # Aplicação rodando
    
    # === SHUTDOWN ===
    logger.info("👋 Encerrando aplicação...")


# ===========================================================
# CRIAÇÃO DA APLICAÇÃO
# ===========================================================

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Chatbot WhatsApp para E-commerce",
    version="0.1.0",
    lifespan=lifespan,
    # Desabilita docs em produção
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)


# ===========================================================
# MIDDLEWARES
# ===========================================================

# CORS - Permite requisições de outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================================
# ROTAS
# ===========================================================

# Rota de health check
@app.get("/health")
async def health_check():
    """
    Verifica se a aplicação está funcionando.
    
    Usado por load balancers e kubernetes.
    """
    return {"status": "healthy", "app": settings.app_name}


# Rota raiz
@app.get("/")
async def root():
    """Rota raiz com informações da API."""
    return {
        "app": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs" if settings.is_development else None,
    }


# Registrar routers
app.include_router(webhook_router)


# ===========================================================
# PARA RODAR DIRETAMENTE
# ===========================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.is_development,
    )
