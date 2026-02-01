# ===========================================================
# tests/unit/domain/entities/test_order.py
# ===========================================================
"""
Testes unitários para entidade Order.

Foca nos testes de transição de estados do pedido.
"""

import pytest
from decimal import Decimal

from src.domain.entities.order import Order
from src.shared.types.enums import OrderStatus


class TestOrder:
    """Testes para a entidade Order."""
    
    # ===== TESTES DE CRIAÇÃO =====
    
    def test_create_order_with_valid_data(self):
        """Deve criar pedido com dados válidos."""
        order = Order(
            customer_id="customer-123",
            total=Decimal("149.90")
        )
        
        assert order.id is not None
        assert order.customer_id == "customer-123"
        assert order.total == Decimal("149.90")
        assert order.status == OrderStatus.PENDING
    
    def test_create_order_with_negative_total_raises_error(self):
        """Deve levantar erro se total for negativo."""
        with pytest.raises(ValueError):
            Order(customer_id="123", total=Decimal("-10.00"))
    
    # ===== TESTES DE TRANSIÇÃO DE ESTADO =====
    
    def test_confirm_order(self):
        """Deve confirmar pedido PENDING."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        
        order.confirm()
        
        assert order.status == OrderStatus.CONFIRMED
    
    def test_confirm_order_not_pending_raises_error(self):
        """Não deve confirmar pedido que não está PENDING."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.CONFIRMED  # Força estado
        
        with pytest.raises(ValueError):
            order.confirm()
    
    def test_process_order(self):
        """Deve processar pedido CONFIRMED."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.CONFIRMED
        
        order.process()
        
        assert order.status == OrderStatus.PROCESSING
    
    def test_ship_order(self):
        """Deve enviar pedido PROCESSING."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.PROCESSING
        
        order.ship()
        
        assert order.status == OrderStatus.SHIPPED
    
    def test_deliver_order(self):
        """Deve entregar pedido SHIPPED."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.SHIPPED
        
        order.deliver()
        
        assert order.status == OrderStatus.DELIVERED
    
    # ===== TESTES DE CANCELAMENTO =====
    
    def test_cancel_pending_order(self):
        """Deve cancelar pedido PENDING."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        
        order.cancel()
        
        assert order.status == OrderStatus.CANCELLED
    
    def test_cancel_confirmed_order(self):
        """Deve cancelar pedido CONFIRMED."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.CONFIRMED
        
        order.cancel()
        
        assert order.status == OrderStatus.CANCELLED
    
    def test_cancel_shipped_order_raises_error(self):
        """Não deve cancelar pedido já enviado."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.SHIPPED
        
        with pytest.raises(ValueError):
            order.cancel()
    
    def test_cancel_delivered_order_raises_error(self):
        """Não deve cancelar pedido já entregue."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.DELIVERED
        
        with pytest.raises(ValueError):
            order.cancel()
    
    # ===== TESTES DE PROPRIEDADES =====
    
    def test_is_active_when_pending(self):
        """Pedido PENDING está ativo."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        
        assert order.is_active is True
    
    def test_is_not_active_when_cancelled(self):
        """Pedido CANCELLED não está ativo."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.CANCELLED
        
        assert order.is_active is False
    
    def test_is_not_active_when_delivered(self):
        """Pedido DELIVERED não está ativo."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.DELIVERED
        
        assert order.is_active is False
    
    def test_can_be_cancelled_when_pending(self):
        """Pedido PENDING pode ser cancelado."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        
        assert order.can_be_cancelled is True
    
    def test_cannot_be_cancelled_when_shipped(self):
        """Pedido SHIPPED não pode ser cancelado."""
        order = Order(customer_id="123", total=Decimal("100.00"))
        order.status = OrderStatus.SHIPPED
        
        assert order.can_be_cancelled is False
