# ===========================================================
# src/presentation/api/routes/__init__.py
# ===========================================================
"""
Rotas da API FastAPI.

Exporta:
- webhook_router: Endpoints do webhook do WhatsApp
"""

from src.presentation.api.routes.webhook import router as webhook_router

__all__ = [
    "webhook_router",
]
