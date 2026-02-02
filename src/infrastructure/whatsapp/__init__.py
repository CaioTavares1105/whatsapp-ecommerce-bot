# ===========================================================
# src/infrastructure/whatsapp/__init__.py
# ===========================================================
"""
Módulo de infraestrutura do WhatsApp.

Exporta:
- WhatsAppClient: Cliente HTTP para enviar mensagens
- WebhookHandler: Handler para processar webhooks
"""

from src.infrastructure.whatsapp.client import WhatsAppClient
from src.infrastructure.whatsapp.webhook import WebhookHandler

__all__ = [
    "WhatsAppClient",
    "WebhookHandler",
]
