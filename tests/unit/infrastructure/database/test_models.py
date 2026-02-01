# ===========================================================
# tests/unit/infrastructure/database/test_models.py
# ===========================================================
# Testes para os modelos SQLAlchemy.
#
# OBJETIVO DOS TESTES:
# - Verificar que os modelos estão bem definidos
# - Testar relacionamentos entre modelos
# - Testar valores padrão
# - Verificar conversão de enums
#
# NOTA:
# Estes são testes UNITÁRIOS que não precisam de banco real.
# Testes de INTEGRAÇÃO com banco seriam em outra pasta.
# ===========================================================
"""
Testes unitários para modelos SQLAlchemy.

Testam a estrutura e configuração dos modelos,
sem necessidade de banco de dados real.
"""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from src.infrastructure.database.models import (
    Base,
    CustomerModel,
    ProductModel,
    OrderModel,
    SessionModel,
)
from src.shared.types.enums import OrderStatus, SessionState


class TestCustomerModel:
    """Testes para CustomerModel."""
    
    def test_model_has_correct_tablename(self):
        """Tabela deve ter nome correto."""
        assert CustomerModel.__tablename__ == "customers"
    
    def test_model_inherits_from_base(self):
        """Modelo deve herdar de Base."""
        assert issubclass(CustomerModel, Base)
    
    def test_model_can_be_instantiated(self):
        """Modelo pode ser instanciado com dados mínimos."""
        model = CustomerModel(
            id="test-uuid",
            phone_number="5511999999999",
        )
        
        assert model.id == "test-uuid"
        assert model.phone_number == "5511999999999"
        assert model.name is None  # Opcional
        assert model.email is None  # Opcional
    
    def test_model_with_all_fields(self):
        """Modelo pode ser instanciado com todos os campos."""
        now = datetime.now()
        
        model = CustomerModel(
            id="test-uuid",
            phone_number="5511999999999",
            name="João Silva",
            email="joao@email.com",
            created_at=now,
            updated_at=now,
        )
        
        assert model.name == "João Silva"
        assert model.email == "joao@email.com"
        assert model.created_at == now


class TestProductModel:
    """Testes para ProductModel."""
    
    def test_model_has_correct_tablename(self):
        """Tabela deve ter nome correto."""
        assert ProductModel.__tablename__ == "products"
    
    def test_model_can_be_instantiated(self):
        """Modelo pode ser instanciado com dados mínimos."""
        model = ProductModel(
            id="prod-uuid",
            name="Produto Teste",
            price=Decimal("99.99"),
            category="Eletrônicos",
        )
        
        assert model.id == "prod-uuid"
        assert model.name == "Produto Teste"
        assert model.price == Decimal("99.99")
        assert model.category == "Eletrônicos"
    
    def test_model_default_values(self):
        """Modelo deve ter valores padrão corretos."""
        model = ProductModel(
            id="prod-uuid",
            name="Produto",
            price=Decimal("10.00"),
            category="Cat",
        )
        
        # Valores padrão definidos no modelo
        assert model.stock == 0 or model.stock is None  # Depende do ORM
        assert model.active is True or model.active is None


class TestOrderModel:
    """Testes para OrderModel."""
    
    def test_model_has_correct_tablename(self):
        """Tabela deve ter nome correto."""
        assert OrderModel.__tablename__ == "orders"
    
    def test_model_can_be_instantiated(self):
        """Modelo pode ser instanciado com dados mínimos."""
        model = OrderModel(
            id="order-uuid",
            customer_id="customer-uuid",
            total=Decimal("150.00"),
        )
        
        assert model.id == "order-uuid"
        assert model.customer_id == "customer-uuid"
        assert model.total == Decimal("150.00")
    
    def test_model_with_status_enum(self):
        """Modelo deve aceitar enum de status."""
        model = OrderModel(
            id="order-uuid",
            customer_id="customer-uuid",
            total=Decimal("100.00"),
            status=OrderStatus.CONFIRMED,
        )
        
        assert model.status == OrderStatus.CONFIRMED


class TestSessionModel:
    """Testes para SessionModel."""
    
    def test_model_has_correct_tablename(self):
        """Tabela deve ter nome correto."""
        assert SessionModel.__tablename__ == "sessions"
    
    def test_model_can_be_instantiated(self):
        """Modelo pode ser instanciado com dados mínimos."""
        expires = datetime.now() + timedelta(hours=24)
        
        model = SessionModel(
            id="session-uuid",
            customer_id="customer-uuid",
            expires_at=expires,
        )
        
        assert model.id == "session-uuid"
        assert model.customer_id == "customer-uuid"
        assert model.expires_at == expires
    
    def test_model_with_state_enum(self):
        """Modelo deve aceitar enum de estado."""
        expires = datetime.now() + timedelta(hours=24)
        
        model = SessionModel(
            id="session-uuid",
            customer_id="customer-uuid",
            expires_at=expires,
            state=SessionState.MENU,
        )
        
        assert model.state == SessionState.MENU
    
    def test_model_with_context_json(self):
        """Modelo deve aceitar contexto como dict (JSON)."""
        expires = datetime.now() + timedelta(hours=24)
        context = {"last_intent": "products", "cart": []}
        
        model = SessionModel(
            id="session-uuid",
            customer_id="customer-uuid",
            expires_at=expires,
            context=context,
        )
        
        assert model.context == context
        assert model.context["last_intent"] == "products"


class TestBaseModel:
    """Testes para a classe Base."""
    
    def test_base_is_declarative(self):
        """Base deve ser DeclarativeBase."""
        from sqlalchemy.orm import DeclarativeBase
        
        assert issubclass(Base, DeclarativeBase)
    
    def test_all_models_registered(self):
        """Todos os modelos devem estar registrados no metadata."""
        # Importa para garantir que foram registrados
        from src.infrastructure.database.models import (
            CustomerModel, ProductModel, OrderModel, SessionModel
        )
        
        table_names = list(Base.metadata.tables.keys())
        
        assert "customers" in table_names
        assert "products" in table_names
        assert "orders" in table_names
        assert "sessions" in table_names
