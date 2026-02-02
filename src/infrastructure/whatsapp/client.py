# ===========================================================
# src/infrastructure/whatsapp/client.py
# ===========================================================
# Cliente HTTP assíncrono para WhatsApp Cloud API.
#
# O QUE É WHATSAPP CLOUD API?
# API oficial do Meta para enviar/receber mensagens WhatsApp.
# Requer: App no Meta Developers, token de acesso, número verificado.
#
# ENDPOINTS PRINCIPAIS:
# - POST /messages -> Enviar mensagem
# - GET /webhook -> Verificar webhook
# - POST /webhook -> Receber mensagens
#
# HTTPX:
# Cliente HTTP moderno para Python, suporta async.
# Similar ao requests, mas com async/await.
# ===========================================================
"""
Cliente HTTP para WhatsApp Cloud API.

Este cliente abstrai todas as chamadas à API do WhatsApp,
fornecendo métodos simples para enviar mensagens.
"""

from typing import Any
import httpx

from src.config.settings import get_settings


class WhatsAppClient:
    """
    Cliente assíncrono para WhatsApp Cloud API.
    
    Responsabilidades:
    - Enviar mensagens de texto
    - Enviar mensagens com botões
    - Enviar templates
    - Marcar mensagens como lidas
    
    Attributes:
        _settings: Configurações do app (tokens, IDs)
        _base_url: URL base da API do WhatsApp
        _client: Cliente HTTP async
        
    Example:
        >>> async with WhatsAppClient() as client:
        ...     await client.send_text_message("5511999999999", "Olá!")
    """
    
    # URL base da API do WhatsApp (versão 18.0)
    BASE_URL = "https://graph.facebook.com/v18.0"
    
    def __init__(self) -> None:
        """Inicializa o cliente com configurações do ambiente."""
        self._settings = get_settings()
        self._client: httpx.AsyncClient | None = None
    
    async def __aenter__(self) -> "WhatsAppClient":
        """
        Context manager async - entrada.
        
        Cria o cliente HTTP ao entrar no contexto.
        
        Usage:
            async with WhatsAppClient() as client:
                await client.send_text_message(...)
        """
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=self._get_headers(),
            timeout=30.0,  # Timeout de 30 segundos
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager async - saída.
        
        Fecha o cliente HTTP ao sair do contexto.
        """
        if self._client:
            await self._client.aclose()
    
    def _get_headers(self) -> dict[str, str]:
        """
        Retorna headers para autenticação.
        
        Authorization: Bearer token de acesso do WhatsApp Business.
        """
        return {
            "Authorization": f"Bearer {self._settings.whatsapp_token}",
            "Content-Type": "application/json",
        }
    
    def _get_phone_number_id(self) -> str:
        """Retorna ID do número de telefone cadastrado."""
        return self._settings.whatsapp_phone_number_id
    
    # =========================================================
    # MÉTODOS PÚBLICOS - Envio de Mensagens
    # =========================================================
    
    async def send_text_message(
        self, 
        to: str, 
        text: str,
    ) -> dict[str, Any]:
        """
        Envia mensagem de texto simples.
        
        Args:
            to: Número do destinatário (ex: "5511999999999")
            text: Texto da mensagem
            
        Returns:
            Resposta da API do WhatsApp
            
        Example:
            >>> await client.send_text_message(
            ...     to="5511999999999",
            ...     text="Olá! Como posso ajudar?"
            ... )
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }
        
        return await self._send_message(payload)
    
    async def send_reply_button_message(
        self,
        to: str,
        body_text: str,
        buttons: list[dict[str, str]],
    ) -> dict[str, Any]:
        """
        Envia mensagem com botões de resposta.
        
        Args:
            to: Número do destinatário
            body_text: Texto principal da mensagem
            buttons: Lista de botões (máximo 3)
                     [{"id": "btn_1", "title": "Opção 1"}, ...]
            
        Returns:
            Resposta da API
            
        Example:
            >>> await client.send_reply_button_message(
            ...     to="5511999999999",
            ...     body_text="Escolha uma opção:",
            ...     buttons=[
            ...         {"id": "opt_1", "title": "Ver produtos"},
            ...         {"id": "opt_2", "title": "Rastrear pedido"},
            ...     ]
            ... )
        """
        # Formata botões para o formato da API
        formatted_buttons = [
            {
                "type": "reply",
                "reply": {"id": btn["id"], "title": btn["title"][:20]},  # Max 20 chars
            }
            for btn in buttons[:3]  # Máximo 3 botões
        ]
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": formatted_buttons},
            },
        }
        
        return await self._send_message(payload)
    
    async def send_list_message(
        self,
        to: str,
        header: str,
        body_text: str,
        button_text: str,
        sections: list[dict],
    ) -> dict[str, Any]:
        """
        Envia mensagem com lista de opções.
        
        Útil para mostrar menus, categorias, produtos.
        
        Args:
            to: Número do destinatário
            header: Título da mensagem
            body_text: Texto do corpo
            button_text: Texto do botão que abre a lista
            sections: Seções da lista
            
        Returns:
            Resposta da API
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {"type": "text", "text": header},
                "body": {"text": body_text},
                "action": {
                    "button": button_text,
                    "sections": sections,
                },
            },
        }
        
        return await self._send_message(payload)
    
    async def mark_as_read(self, message_id: str) -> dict[str, Any]:
        """
        Marca uma mensagem como lida.
        
        Mostra os "ticks azuis" para o usuário.
        
        Args:
            message_id: ID da mensagem recebida
        """
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        
        return await self._send_message(payload)
    
    # =========================================================
    # MÉTODOS PRIVADOS
    # =========================================================
    
    async def _send_message(self, payload: dict) -> dict[str, Any]:
        """
        Envia payload para a API do WhatsApp.
        
        Args:
            payload: Dados da mensagem
            
        Returns:
            Resposta da API
            
        Raises:
            httpx.HTTPStatusError: Se a API retornar erro
        """
        if not self._client:
            raise RuntimeError("Cliente não inicializado. Use 'async with'.")
        
        phone_id = self._get_phone_number_id()
        url = f"/{phone_id}/messages"
        
        response = await self._client.post(url, json=payload)
        response.raise_for_status()  # Levanta exceção se erro
        
        return response.json()
