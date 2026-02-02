# ===========================================================
# src/presentation/api/routes/webhook.py
# ===========================================================
# Endpoint FastAPI para receber webhooks do WhatsApp.
#
# DOIS ENDPOINTS:
# 1. GET /webhook -> Verificação inicial do webhook
# 2. POST /webhook -> Receber mensagens
#
# FLUXO:
# 1. WhatsApp envia POST com mensagem
# 2. Validamos assinatura HMAC
# 3. Extraímos dados da mensagem
# 4. Processamos com HandleMessageUseCase
# 5. Enviamos resposta via WhatsAppClient
# ===========================================================
"""
Endpoints do Webhook do WhatsApp.

Recebe e processa mensagens do WhatsApp Cloud API.
"""

from typing import Any
import logging

from fastapi import APIRouter, Request, Query, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse

from src.infrastructure.whatsapp.webhook import WebhookHandler
from src.infrastructure.whatsapp.client import WhatsAppClient
from src.application.dtos import IncomingMessageDTO


# Logger para debug
logger = logging.getLogger(__name__)

# Router do FastAPI
router = APIRouter(prefix="/webhook", tags=["WhatsApp"])

# Handler do webhook (sem estado, pode ser instância global)
webhook_handler = WebhookHandler()


@router.get("")
async def verify_webhook(
    mode: str | None = Query(None, alias="hub.mode"),
    token: str | None = Query(None, alias="hub.verify_token"),
    challenge: str | None = Query(None, alias="hub.challenge"),
) -> PlainTextResponse:
    """
    Verifica o webhook (chamado pelo Meta ao configurar).
    
    O WhatsApp faz GET com parâmetros:
    - hub.mode: "subscribe"
    - hub.verify_token: Token que configuramos
    - hub.challenge: String para retornar
    
    Args:
        mode: Tipo de requisição (deve ser "subscribe")
        token: Token de verificação
        challenge: String de desafio
        
    Returns:
        PlainTextResponse com o challenge
        
    Raises:
        HTTPException 403: Se verificação falhar
    """
    logger.info(f"Webhook verification: mode={mode}")
    
    success, response = webhook_handler.verify_webhook(mode, token, challenge)
    
    if not success:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")
    
    logger.info("Webhook verified successfully")
    return PlainTextResponse(content=response or "")


@router.post("")
async def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    """
    Recebe mensagens do WhatsApp.
    
    O WhatsApp envia POST com:
    - Header X-Hub-Signature-256 (HMAC)
    - Body JSON com dados da mensagem
    
    Processamento:
    1. Valida assinatura HMAC
    2. Extrai dados da mensagem
    3. Agenda processamento em background
    4. Retorna 200 OK imediatamente
    
    Args:
        request: Requisição FastAPI
        background_tasks: Para processar em background
        
    Returns:
        Dict com status "received"
        
    Note:
        O WhatsApp espera resposta em até 5 segundos.
        Por isso processamos em background.
    """
    # Lê body da requisição
    body = await request.body()
    payload = await request.json()
    
    # Log para debug
    logger.debug(f"Webhook received: {payload}")
    
    # Valida assinatura (opcional em dev)
    signature = request.headers.get("X-Hub-Signature-256")
    if signature:
        is_valid = webhook_handler.validate_signature(body, signature)
        if not is_valid:
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Extrai dados da mensagem
    message_data = webhook_handler.extract_message_data(payload)
    
    if message_data:
        # Agenda processamento em background
        background_tasks.add_task(
            process_message,
            message_data,
        )
    
    # Retorna imediatamente (WhatsApp espera resposta rápida)
    return {"status": "received"}


async def process_message(message_data: dict[str, Any]) -> None:
    """
    Processa uma mensagem em background.
    
    Chamado via BackgroundTasks para não bloquear
    a resposta ao WhatsApp.
    
    Args:
        message_data: Dados extraídos da mensagem
    """
    logger.info(f"Processing message from {message_data.get('from')}")
    
    try:
        # Monta DTO de entrada
        phone = message_data.get("from", "")
        text = message_data.get("text", "")
        
        if not text:
            logger.info("Message without text, skipping")
            return
        
        # Cria DTO
        input_dto = IncomingMessageDTO(
            phone_number=phone,
            text=text,
            message_id=message_data.get("message_id"),
        )
        
        # TODO: Injetar UseCase via dependency injection
        # Por enquanto, apenas loga
        logger.info(f"Would process: {input_dto}")
        
        # Marca como lida
        async with WhatsAppClient() as client:
            if message_data.get("message_id"):
                await client.mark_as_read(message_data["message_id"])
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
