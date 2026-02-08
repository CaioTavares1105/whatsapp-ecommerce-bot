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

# ===========================================================
# SEGURANCA: CORS Restritivo
# ===========================================================
# Em producao, NUNCA usar allow_origins=["*"]!
# Especificar apenas dominios confiaveis.

# Lista de origens permitidas (configurar conforme ambiente)
ALLOWED_ORIGINS = [
    "https://graph.facebook.com",      # Meta/WhatsApp API
    "https://developers.facebook.com",  # Meta Developers
]

# Em desenvolvimento, permite localhost
if settings.is_development:
    ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,  # Desabilitar credenciais por padrao
    allow_methods=["GET", "POST"],  # Apenas metodos necessarios
    allow_headers=["Content-Type", "X-Hub-Signature-256"],  # Headers especificos
)


# ===========================================================
# ROTAS
# ===========================================================

# Rota de health check (minima informacao)
@app.get("/health")
async def health_check():
    """
    Verifica se a aplicacao esta funcionando.

    Usado por load balancers e kubernetes.
    Retorna informacao MINIMA para nao expor detalhes.
    """
    return {"status": "healthy"}


# Rota raiz (minima informacao em producao)
@app.get("/")
async def root():
    """Rota raiz."""
    if settings.is_development:
        return {
            "app": settings.app_name,
            "version": "0.1.0",
            "docs": "/docs",
        }
    # Em producao, nao expor detalhes
    return {"status": "ok"}


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
