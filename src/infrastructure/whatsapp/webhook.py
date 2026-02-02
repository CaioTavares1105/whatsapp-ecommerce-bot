# ===========================================================
# src/infrastructure/whatsapp/webhook.py
# ===========================================================
# Handler do Webhook do WhatsApp.
#
# O QUE É UM WEBHOOK?
# URL que o WhatsApp chama quando algo acontece:
# - Nova mensagem recebida
# - Status de mensagem atualizado
# - Erro de entrega
#
# FLUXO:
# 1. WhatsApp chama nosso webhook (POST)
# 2. Extraímos dados da mensagem
# 3. Processamos e respondemos
#
# VERIFICAÇÃO:
# WhatsApp faz GET com token para verificar webhook.
# Precisamos responder com o challenge.
# ===========================================================
"""
Handler do Webhook do WhatsApp Cloud API.

Responsável por:
- Verificar webhook (GET)
- Extrair dados de mensagens recebidas
- Validar assinaturas
"""

import hmac
import hashlib
from typing import Any

from src.config.settings import get_settings


class WebhookHandler:
    """
    Processa eventos do webhook do WhatsApp.
    
    Responsabilidades:
    - Verificar token de validação do webhook
    - Validar assinatura das requisições
    - Extrair dados de mensagens
    
    Attributes:
        _settings: Configurações da aplicação
    """
    
    def __init__(self) -> None:
        """Inicializa handler com configurações."""
        self._settings = get_settings()
    
    # =========================================================
    # VERIFICAÇÃO DO WEBHOOK (GET)
    # =========================================================
    
    def verify_webhook(
        self,
        mode: str | None,
        token: str | None,
        challenge: str | None,
    ) -> tuple[bool, str | None]:
        """
        Verifica requisição de validação do webhook.
        
        Quando configuramos o webhook no Meta Developers,
        o WhatsApp faz uma requisição GET para verificar.
        
        Args:
            mode: Deve ser "subscribe"
            token: Token que configuramos no Meta Developers
            challenge: String aleatória que devemos retornar
            
        Returns:
            Tupla (sucesso, challenge ou None)
            
        Example:
            >>> handler = WebhookHandler()
            >>> ok, response = handler.verify_webhook(
            ...     mode="subscribe",
            ...     token="meu_token_secreto",
            ...     challenge="abc123"
            ... )
            >>> if ok:
            ...     return PlainTextResponse(response)
        """
        # Valida se é uma requisição de subscribe
        if mode != "subscribe":
            return False, None
        
        # Compara token com o configurado
        if token != self._settings.whatsapp_verify_token:
            return False, None
        
        # Retorna o challenge para confirmar
        return True, challenge
    
    # =========================================================
    # VALIDAÇÃO DE ASSINATURA (Segurança)
    # =========================================================
    
    def validate_signature(
        self,
        payload: bytes,
        signature: str | None,
    ) -> bool:
        """
        Valida assinatura HMAC da requisição.
        
        O WhatsApp assina cada requisição com HMAC-SHA256.
        Validamos para garantir que veio do WhatsApp.
        
        Args:
            payload: Body da requisição em bytes
            signature: Header X-Hub-Signature-256
            
        Returns:
            True se assinatura válida
        """
        if not signature:
            return False
        
        # Assinatura vem como "sha256=xxxxx"
        if not signature.startswith("sha256="):
            return False
        
        expected_hash = signature.replace("sha256=", "")
        
        # Calcula HMAC com app secret
        app_secret = self._settings.whatsapp_app_secret
        computed_hash = hmac.new(
            app_secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()
        
        # Comparação segura contra timing attacks
        return hmac.compare_digest(computed_hash, expected_hash)
    
    # =========================================================
    # EXTRAÇÃO DE DADOS
    # =========================================================
    
    def extract_message_data(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Extrai dados da mensagem do payload do webhook.
        
        O payload do WhatsApp tem estrutura aninhada:
        entry[0].changes[0].value.messages[0]
        
        Args:
            payload: JSON do webhook
            
        Returns:
            Dict com dados da mensagem ou None se não for mensagem
            
        Structure retornada:
            {
                "from": "5511999999999",
                "message_id": "wamid.xxx",
                "timestamp": "1234567890",
                "type": "text",
                "text": "Olá!",
            }
        """
        try:
            # Navega estrutura do payload
            entry = payload.get("entry", [])
            if not entry:
                return None
            
            changes = entry[0].get("changes", [])
            if not changes:
                return None
            
            value = changes[0].get("value", {})
            
            # Verifica se tem mensagens
            messages = value.get("messages", [])
            if not messages:
                return None  # Pode ser status update
            
            message = messages[0]
            
            # Extrai dados básicos
            result = {
                "from": message.get("from"),
                "message_id": message.get("id"),
                "timestamp": message.get("timestamp"),
                "type": message.get("type"),
            }
            
            # Extrai conteúdo baseado no tipo
            msg_type = message.get("type")
            
            if msg_type == "text":
                result["text"] = message.get("text", {}).get("body", "")
            
            elif msg_type == "interactive":
                # Resposta de botão ou lista
                interactive = message.get("interactive", {})
                interactive_type = interactive.get("type")
                
                if interactive_type == "button_reply":
                    result["button_id"] = interactive.get("button_reply", {}).get("id")
                    result["button_text"] = interactive.get("button_reply", {}).get("title")
                elif interactive_type == "list_reply":
                    result["list_id"] = interactive.get("list_reply", {}).get("id")
                    result["list_text"] = interactive.get("list_reply", {}).get("title")
            
            elif msg_type == "image":
                result["image_id"] = message.get("image", {}).get("id")
            
            elif msg_type == "audio":
                result["audio_id"] = message.get("audio", {}).get("id")
            
            return result
            
        except (KeyError, IndexError, TypeError):
            return None
    
    def extract_contact_info(
        self,
        payload: dict[str, Any],
    ) -> dict[str, str] | None:
        """
        Extrai informações do contato do payload.
        
        Returns:
            Dict com nome e número do contato
        """
        try:
            entry = payload.get("entry", [])
            changes = entry[0].get("changes", [])
            value = changes[0].get("value", {})
            contacts = value.get("contacts", [])
            
            if not contacts:
                return None
            
            contact = contacts[0]
            return {
                "phone_number": contact.get("wa_id"),
                "name": contact.get("profile", {}).get("name"),
            }
            
        except (KeyError, IndexError, TypeError):
            return None
