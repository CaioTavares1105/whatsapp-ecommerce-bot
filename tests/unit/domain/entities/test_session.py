# ===========================================================
# tests/unit/domain/entities/test_session.py
# ===========================================================
"""
Testes unitários para entidade Session.

Testa gerenciamento de estado, contexto e expiração.
"""

import pytest
from datetime import datetime, timedelta

from src.domain.entities.session import Session
from src.shared.types.enums import SessionState


class TestSession:
    """Testes para a entidade Session."""
    
    # ===== TESTES DE CRIAÇÃO =====
    
    def test_create_session_with_initial_state(self):
        """Deve criar sessão com estado INITIAL."""
        session = Session(customer_id="customer-123")
        
        assert session.id is not None
        assert session.customer_id == "customer-123"
        assert session.state == SessionState.INITIAL
        assert session.context == {}
    
    def test_create_session_with_expiration(self):
        """Deve criar sessão com expiração de 24 horas."""
        session = Session(customer_id="123")
        
        # expires_at deve ser aproximadamente 24h no futuro
        expected_expiration = datetime.now() + timedelta(hours=24)
        diff = abs((session.expires_at - expected_expiration).total_seconds())
        
        # Tolerância de 1 segundo
        assert diff < 1
    
    # ===== TESTES DE ESTADO =====
    
    def test_update_state(self):
        """Deve atualizar o estado da sessão."""
        session = Session(customer_id="123")
        
        session.update_state(SessionState.MENU)
        
        assert session.state == SessionState.MENU
    
    def test_update_state_renews_expiration(self):
        """Deve renovar expiração ao atualizar estado."""
        session = Session(customer_id="123")
        
        # Força expiração antiga
        session.expires_at = datetime.now() - timedelta(hours=1)
        
        # Atualiza estado
        session.update_state(SessionState.MENU)
        
        # Expiração deveria ser renovada para 24h no futuro
        assert session.expires_at > datetime.now()
    
    # ===== TESTES DE CONTEXTO =====
    
    def test_set_and_get_context(self):
        """Deve salvar e recuperar valor do contexto."""
        session = Session(customer_id="123")
        
        session.set_context("cart", [{"product_id": "123", "qty": 2}])
        
        result = session.get_context("cart")
        
        assert result == [{"product_id": "123", "qty": 2}]
    
    def test_get_context_with_default(self):
        """Deve retornar default se chave não existir."""
        session = Session(customer_id="123")
        
        result = session.get_context("nonexistent", "default_value")
        
        assert result == "default_value"
    
    def test_get_context_returns_none_without_default(self):
        """Deve retornar None se chave não existir e sem default."""
        session = Session(customer_id="123")
        
        result = session.get_context("nonexistent")
        
        assert result is None
    
    def test_has_context(self):
        """Deve verificar se chave existe no contexto."""
        session = Session(customer_id="123")
        session.set_context("key1", "value1")
        
        assert session.has_context("key1") is True
        assert session.has_context("key2") is False
    
    def test_remove_context(self):
        """Deve remover chave do contexto."""
        session = Session(customer_id="123")
        session.set_context("key", "value")
        
        session.remove_context("key")
        
        assert session.has_context("key") is False
    
    def test_remove_nonexistent_context_does_not_raise(self):
        """Deve ignorar remoção de chave inexistente."""
        session = Session(customer_id="123")
        
        # Não deve levantar erro
        session.remove_context("nonexistent")
    
    def test_clear_context(self):
        """Deve limpar todo o contexto."""
        session = Session(customer_id="123")
        session.set_context("key1", "value1")
        session.set_context("key2", "value2")
        
        session.clear_context()
        
        assert session.context == {}
    
    # ===== TESTES DE EXPIRAÇÃO =====
    
    def test_is_not_expired_when_new(self):
        """Sessão recém-criada não está expirada."""
        session = Session(customer_id="123")
        
        assert session.is_expired is False
    
    def test_is_expired_when_past_expiration(self):
        """Sessão está expirada quando passou do tempo."""
        session = Session(customer_id="123")
        
        # Força expiração no passado
        session.expires_at = datetime.now() - timedelta(hours=1)
        
        assert session.is_expired is True
    
    def test_time_until_expiration(self):
        """Deve retornar tempo restante até expiração."""
        session = Session(customer_id="123")
        
        remaining = session.time_until_expiration
        
        # Deve ser aproximadamente 24 horas
        assert remaining.total_seconds() > 23 * 3600  # > 23 horas
        assert remaining.total_seconds() < 25 * 3600  # < 25 horas
    
    def test_renew_session(self):
        """Deve renovar expiração da sessão."""
        session = Session(customer_id="123")
        
        # Força expiração antiga
        session.expires_at = datetime.now() - timedelta(hours=1)
        assert session.is_expired is True
        
        # Renova
        session.renew()
        
        assert session.is_expired is False
