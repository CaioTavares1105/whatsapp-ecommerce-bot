# ===========================================================
# src/presentation/whatsapp/handler.py
# ===========================================================
# Handler que conecta o Webhook com o UseCase.
#
# RESPONSABILIDADES:
# - Orquestrar o fluxo completo de mensagem
# - Injetar dependências no UseCase
# - Enviar resposta via WhatsAppClient
# - Gerenciar erros e logging
#
# FLUXO:
# 1. Recebe dados do webhook
# 2. Cria DTO de entrada
# 3. Executa UseCase
# 4. Envia resposta ao usuário
# ===========================================================
"""
Handler de mensagens WhatsApp.

Conecta o webhook com o caso de uso principal.
"""

import logging
from typing import Any

from src.application.dtos import IncomingMessageDTO
from src.application.usecases import HandleMessageUseCase
from src.domain.repositories import (
    ICustomerRepository,
    ISessionRepository,
    IProductRepository,
    IOrderRepository,
)
from src.infrastructure.whatsapp.client import WhatsAppClient


logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Orquestra o processamento de mensagens WhatsApp.
    
    Conecta:
    - Webhook → UseCase → WhatsAppClient
    
    Attributes:
        _use_case: Caso de uso principal
        
    Example:
        >>> handler = MessageHandler(
        ...     customer_repo=repo1,
        ...     session_repo=repo2,
        ...     product_repo=repo3,
        ...     order_repo=repo4,
        ... )
        >>> await handler.handle(message_data)
    """
    
    def __init__(
        self,
        customer_repo: ICustomerRepository,
        session_repo: ISessionRepository,
        product_repo: IProductRepository,
        order_repo: IOrderRepository,
    ) -> None:
        """
        Inicializa handler com repositórios.
        
        Args:
            customer_repo: Repositório de clientes
            session_repo: Repositório de sessões
            product_repo: Repositório de produtos
            order_repo: Repositório de pedidos
        """
        self._use_case = HandleMessageUseCase(
            customer_repo=customer_repo,
            session_repo=session_repo,
            product_repo=product_repo,
            order_repo=order_repo,
        )
    
    async def handle(self, message_data: dict[str, Any]) -> None:
        """
        Processa uma mensagem do WhatsApp.
        
        Fluxo completo:
        1. Extrai dados da mensagem
        2. Cria DTO de entrada
        3. Executa caso de uso
        4. Envia resposta via API
        
        Args:
            message_data: Dados extraídos do webhook
        """
        phone = message_data.get("from", "")
        text = message_data.get("text", "")
        message_id = message_data.get("message_id")
        
        logger.info(f"📩 Mensagem de {phone}: {text[:50]}...")
        
        # Ignora mensagens sem texto
        if not text:
            logger.info("Mensagem sem texto, ignorando")
            return
        
        try:
            # Cria DTO de entrada
            input_dto = IncomingMessageDTO(
                phone_number=phone,
                text=text,
                message_id=message_id,
            )
            
            # Executa caso de uso
            response = await self._use_case.execute(input_dto)
            
            logger.info(f"📤 Resposta: {response.text[:50]}...")
            
            # Envia resposta via WhatsApp
            async with WhatsAppClient() as client:
                # Marca mensagem original como lida
                if message_id:
                    await client.mark_as_read(message_id)
                
                # Envia resposta
                if response.should_transfer_to_human:
                    # Mensagem especial para transferência
                    await client.send_text_message(
                        to=phone,
                        text="🧑‍💼 Você será transferido para um atendente. Aguarde um momento...",
                    )
                else:
                    await client.send_text_message(
                        to=phone,
                        text=response.text,
                    )
            
            logger.info(f"✅ Mensagem enviada para {phone}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar mensagem: {e}", exc_info=True)
            
            # Tenta enviar mensagem de erro
            try:
                async with WhatsAppClient() as client:
                    await client.send_text_message(
                        to=phone,
                        text="Desculpe, ocorreu um erro. Por favor, tente novamente.",
                    )
            except Exception:
                logger.error("Não foi possível enviar mensagem de erro")
    
    async def handle_button_reply(
        self,
        phone: str,
        button_id: str,
        message_id: str | None = None,
    ) -> None:
        """
        Processa resposta de botão.
        
        Quando usuário clica em um botão, recebemos o ID.
        Convertemos para texto e processamos normalmente.
        
        Args:
            phone: Número do telefone
            button_id: ID do botão clicado
            message_id: ID da mensagem (para marcar como lida)
        """
        # Mapeamento de botões para texto
        button_to_text = {
            "btn_products": "ver produtos",
            "btn_orders": "meus pedidos",
            "btn_faq": "dúvidas",
            "btn_human": "falar com atendente",
            "btn_menu": "menu",
        }
        
        text = button_to_text.get(button_id, button_id)
        
        await self.handle({
            "from": phone,
            "text": text,
            "message_id": message_id,
        })
