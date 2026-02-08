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

from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse

from src.infrastructure.whatsapp.webhook import WebhookHandler


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
) -> dict[str, str]:
    """
    Recebe mensagens do WhatsApp.

    O WhatsApp envia POST com:
    - Header X-Hub-Signature-256 (HMAC)
    - Body JSON com dados da mensagem

    Processamento:
    1. Valida assinatura HMAC
    2. Extrai dados da mensagem
    3. Processa a mensagem diretamente
    4. Retorna 200 OK

    Args:
        request: Requisição FastAPI

    Returns:
        Dict com status "received"

    Note:
        O WhatsApp espera resposta em até 5 segundos.
        Processamento direto é mais confiável que BackgroundTasks.
    """
    # Lê body da requisição
    body = await request.body()
    payload = await request.json()

    # Log para debug
    logger.info(f"Webhook received: {payload}")

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
        # Processa diretamente (sem BackgroundTasks)
        # WhatsApp dá 5 segundos de timeout, suficiente para processar
        await process_message(message_data)

    # Retorna após processamento
    return {"status": "received"}


async def process_message(message_data: dict[str, Any]) -> None:
    """
    Processa uma mensagem em background.

    Chamado via BackgroundTasks para não bloquear
    a resposta ao WhatsApp.

    Args:
        message_data: Dados extraídos da mensagem
    """
    from src.infrastructure.database.connection import AsyncSessionFactory
    from src.presentation.api.dependencies import get_message_handler

    logger.info(f"🔄 Processing message from {message_data.get('from')}")
    logger.info(f"📝 Message data: {message_data}")

    try:
        # Cria sessão do banco para este processamento
        logger.info("📊 Creating database session...")
        async with AsyncSessionFactory() as session:
            try:
                # Usa o handler com a sessão real do banco
                logger.info("🔧 Getting message handler...")
                handler = await get_message_handler(session)
                logger.info("✅ Handler obtained successfully")

                # Verifica se é resposta de botão
                if message_data.get("button_id"):
                    logger.info("🔘 Processing button reply...")
                    await handler.handle_button_reply(
                        phone=message_data.get("from", ""),
                        button_id=message_data["button_id"],
                        message_id=message_data.get("message_id"),
                    )
                else:
                    logger.info("💬 Processing text message...")
                    await handler.handle(message_data)

                # Commit das alterações no banco
                logger.info("💾 Committing to database...")
                await session.commit()
                logger.info("✅ Message processed successfully!")

            except Exception as e:
                logger.error(f"❌ Error in handler: {e}", exc_info=True)
                await session.rollback()
                raise

    except Exception as e:
        logger.error(f"❌ Error processing message: {e}", exc_info=True)
