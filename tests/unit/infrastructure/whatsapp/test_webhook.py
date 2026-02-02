# ===========================================================
# tests/unit/infrastructure/whatsapp/test_webhook.py
# ===========================================================
# Testes para o WebhookHandler.
# ===========================================================
"""
Testes unitários para WebhookHandler.

Testa:
- Verificação de webhook
- Validação de assinatura HMAC
- Extração de dados de mensagens
"""

import hmac
import hashlib
from unittest.mock import patch, MagicMock

import pytest

from src.infrastructure.whatsapp.webhook import WebhookHandler


@pytest.fixture
def handler():
    """Handler com settings mockados."""
    with patch("src.infrastructure.whatsapp.webhook.get_settings") as mock:
        settings = MagicMock()
        settings.whatsapp_verify_token = "test_verify_token"
        settings.whatsapp_app_secret = "test_app_secret"
        mock.return_value = settings
        yield WebhookHandler()


class TestVerifyWebhook:
    """Testes para verify_webhook."""
    
    def test_valid_verification(self, handler):
        """Deve retornar True e challenge quando válido."""
        success, response = handler.verify_webhook(
            mode="subscribe",
            token="test_verify_token",
            challenge="challenge_123",
        )
        
        assert success is True
        assert response == "challenge_123"
    
    def test_invalid_mode(self, handler):
        """Deve falhar se mode não é subscribe."""
        success, response = handler.verify_webhook(
            mode="unsubscribe",
            token="test_verify_token",
            challenge="challenge_123",
        )
        
        assert success is False
        assert response is None
    
    def test_invalid_token(self, handler):
        """Deve falhar se token não confere."""
        success, response = handler.verify_webhook(
            mode="subscribe",
            token="wrong_token",
            challenge="challenge_123",
        )
        
        assert success is False
        assert response is None
    
    def test_missing_mode(self, handler):
        """Deve falhar se mode está faltando."""
        success, response = handler.verify_webhook(
            mode=None,
            token="test_verify_token",
            challenge="challenge_123",
        )
        
        assert success is False


class TestValidateSignature:
    """Testes para validate_signature."""
    
    def test_valid_signature(self, handler):
        """Deve retornar True para assinatura válida."""
        payload = b'{"test": "data"}'
        secret = "test_app_secret"
        
        # Calcula assinatura correta
        expected_sig = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()
        
        signature = f"sha256={expected_sig}"
        
        assert handler.validate_signature(payload, signature) is True
    
    def test_invalid_signature(self, handler):
        """Deve retornar False para assinatura inválida."""
        payload = b'{"test": "data"}'
        signature = "sha256=invalid_signature"
        
        assert handler.validate_signature(payload, signature) is False
    
    def test_missing_signature(self, handler):
        """Deve retornar False se assinatura ausente."""
        payload = b'{"test": "data"}'
        
        assert handler.validate_signature(payload, None) is False
    
    def test_wrong_format_signature(self, handler):
        """Deve retornar False se formato incorreto."""
        payload = b'{"test": "data"}'
        signature = "md5=some_hash"
        
        assert handler.validate_signature(payload, signature) is False


class TestExtractMessageData:
    """Testes para extract_message_data."""
    
    def test_extract_text_message(self, handler):
        """Deve extrair mensagem de texto corretamente."""
        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "5511999999999",
                            "id": "wamid.123",
                            "timestamp": "1234567890",
                            "type": "text",
                            "text": {"body": "Olá!"},
                        }],
                    },
                }],
            }],
        }
        
        result = handler.extract_message_data(payload)
        
        assert result is not None
        assert result["from"] == "5511999999999"
        assert result["message_id"] == "wamid.123"
        assert result["type"] == "text"
        assert result["text"] == "Olá!"
    
    def test_extract_button_reply(self, handler):
        """Deve extrair resposta de botão."""
        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "5511999999999",
                            "id": "wamid.456",
                            "timestamp": "1234567890",
                            "type": "interactive",
                            "interactive": {
                                "type": "button_reply",
                                "button_reply": {
                                    "id": "btn_products",
                                    "title": "Ver produtos",
                                },
                            },
                        }],
                    },
                }],
            }],
        }
        
        result = handler.extract_message_data(payload)
        
        assert result is not None
        assert result["type"] == "interactive"
        assert result["button_id"] == "btn_products"
        assert result["button_text"] == "Ver produtos"
    
    def test_empty_payload(self, handler):
        """Deve retornar None para payload vazio."""
        result = handler.extract_message_data({})
        assert result is None
    
    def test_no_messages(self, handler):
        """Deve retornar None se não houver mensagens."""
        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "statuses": [{}],  # Status update, não mensagem
                    },
                }],
            }],
        }
        
        result = handler.extract_message_data(payload)
        assert result is None


class TestExtractContactInfo:
    """Testes para extract_contact_info."""
    
    def test_extract_contact(self, handler):
        """Deve extrair informações do contato."""
        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "contacts": [{
                            "wa_id": "5511999999999",
                            "profile": {"name": "João Silva"},
                        }],
                    },
                }],
            }],
        }
        
        result = handler.extract_contact_info(payload)
        
        assert result is not None
        assert result["phone_number"] == "5511999999999"
        assert result["name"] == "João Silva"
    
    def test_no_contact(self, handler):
        """Deve retornar None se não houver contato."""
        result = handler.extract_contact_info({})
        assert result is None
