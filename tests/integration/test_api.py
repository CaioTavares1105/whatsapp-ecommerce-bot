# ===========================================================
# tests/integration/test_api.py
# ===========================================================
# Testes de Integração para a API FastAPI.
#
# O QUE SÃO TESTES DE INTEGRAÇÃO?
# Testam componentes combinados (não isolados).
# Ex: API + Rotas + Handlers juntos.
#
# FASTAPI TESTCLIENT:
# Cliente de teste que simula requisições HTTP.
# Não precisa subir o servidor, executa em memória.
# ===========================================================
"""
Testes de integração para a API FastAPI.

Testa os endpoints reais com TestClient.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)


class TestHealthCheck:
    """Testes para o endpoint /health."""
    
    def test_health_returns_200(self, client):
        """Deve retornar status 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy_status(self, client):
        """Deve retornar status healthy."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_includes_app_name(self, client):
        """Deve incluir nome da aplicação."""
        response = client.get("/health")
        data = response.json()
        assert "app" in data


class TestRootEndpoint:
    """Testes para o endpoint /."""
    
    def test_root_returns_200(self, client):
        """Deve retornar status 200."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_app_info(self, client):
        """Deve retornar informações da app."""
        response = client.get("/")
        data = response.json()
        assert "app" in data
        assert "version" in data


class TestWebhookVerification:
    """Testes para GET /webhook (verificação)."""
    
    def test_webhook_valid_verification(self, client):
        """Deve retornar challenge quando válido."""
        from src.config.settings import get_settings
        settings = get_settings()
        
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": settings.whatsapp_verify_token or "test",
                "hub.challenge": "test_challenge_123",
            },
        )
        
        # Se token não configurado, espera 403
        if settings.whatsapp_verify_token:
            assert response.status_code == 200
            assert response.text == "test_challenge_123"
        else:
            assert response.status_code == 403
    
    def test_webhook_invalid_mode_returns_403(self, client):
        """Deve retornar 403 para mode inválido."""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "invalid",
                "hub.verify_token": "any_token",
                "hub.challenge": "test_challenge",
            },
        )
        assert response.status_code == 403
    
    def test_webhook_missing_params_returns_403(self, client):
        """Deve retornar 403 sem parâmetros."""
        response = client.get("/webhook")
        assert response.status_code == 403


class TestWebhookPost:
    """Testes para POST /webhook (receber mensagens)."""
    
    def test_webhook_post_returns_received(self, client):
        """Deve retornar status received."""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "messages": [],
                    },
                }],
            }],
        }
        
        response = client.post("/webhook", json=payload)
        
        assert response.status_code == 200
        assert response.json()["status"] == "received"
    
    def test_webhook_post_with_message(self, client):
        """Deve processar mensagem e retornar received."""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "contacts": [{
                            "wa_id": "5511999999999",
                            "profile": {"name": "Test User"},
                        }],
                        "messages": [{
                            "from": "5511999999999",
                            "id": "wamid.test123",
                            "timestamp": "1234567890",
                            "type": "text",
                            "text": {"body": "Olá!"},
                        }],
                    },
                }],
            }],
        }
        
        response = client.post("/webhook", json=payload)
        
        assert response.status_code == 200
        assert response.json()["status"] == "received"
    
    def test_webhook_post_empty_body_returns_received(self, client):
        """Deve aceitar payload vazio."""
        response = client.post("/webhook", json={})
        
        assert response.status_code == 200
