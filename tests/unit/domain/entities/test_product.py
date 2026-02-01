# ===========================================================
# tests/unit/domain/entities/test_product.py
# ===========================================================
"""
Testes unitários para entidade Product.
"""

import pytest
from decimal import Decimal

from src.domain.entities.product import Product


class TestProduct:
    """Testes para a entidade Product."""
    
    # ===== TESTES DE CRIAÇÃO =====
    
    def test_create_product_with_valid_data(self):
        """Deve criar produto com dados válidos."""
        product = Product(
            name="Camiseta Azul",
            price=Decimal("49.90"),
            category="Vestuário",
            stock=10
        )
        
        assert product.id is not None
        assert product.name == "Camiseta Azul"
        assert product.price == Decimal("49.90")
        assert product.category == "Vestuário"
        assert product.stock == 10
        assert product.active is True
    
    def test_create_product_with_negative_price_raises_error(self):
        """Deve levantar erro se preço for negativo."""
        with pytest.raises(ValueError) as exc_info:
            Product(
                name="Produto",
                price=Decimal("-10.00"),
                category="Teste"
            )
        
        assert "negativo" in str(exc_info.value).lower()
    
    def test_create_product_with_negative_stock_raises_error(self):
        """Deve levantar erro se estoque for negativo."""
        with pytest.raises(ValueError):
            Product(
                name="Produto",
                price=Decimal("10.00"),
                category="Teste",
                stock=-5
            )
    
    # ===== TESTES DE DISPONIBILIDADE =====
    
    def test_product_is_available_when_active_and_has_stock(self):
        """Produto disponível se ativo E com estoque."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=5,
            active=True
        )
        
        assert product.is_available is True
    
    def test_product_not_available_when_inactive(self):
        """Produto indisponível se inativo."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=5,
            active=False
        )
        
        assert product.is_available is False
    
    def test_product_not_available_when_no_stock(self):
        """Produto indisponível se sem estoque."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=0,
            active=True
        )
        
        assert product.is_available is False
    
    # ===== TESTES DE ESTOQUE =====
    
    def test_decrease_stock(self):
        """Deve diminuir estoque corretamente."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=10
        )
        
        product.decrease_stock(3)
        
        assert product.stock == 7
    
    def test_decrease_stock_with_insufficient_stock_raises_error(self):
        """Deve levantar erro se não tiver estoque suficiente."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=5
        )
        
        with pytest.raises(ValueError) as exc_info:
            product.decrease_stock(10)
        
        assert "insuficiente" in str(exc_info.value).lower()
    
    def test_increase_stock(self):
        """Deve aumentar estoque corretamente."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=5
        )
        
        product.increase_stock(3)
        
        assert product.stock == 8
    
    # ===== TESTES DE ATIVAÇÃO =====
    
    def test_deactivate_product(self):
        """Deve desativar produto."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            active=True
        )
        
        product.deactivate()
        
        assert product.active is False
    
    def test_activate_product(self):
        """Deve ativar produto."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            active=False
        )
        
        product.activate()
        
        assert product.active is True
