# ===========================================================
# src/domain/entities/order.py - Entidade Pedido
# ===========================================================
# Representa um pedido feito por um cliente.
#
# CONCEITO: MÁQUINA DE ESTADOS
# Um pedido segue um fluxo de estados:
#
#   PENDING --> CONFIRMED --> PROCESSING --> SHIPPED --> DELIVERED
#       |          |              |
#       +----------+--------------+-----> CANCELLED
#
# Cada método de transição (confirm, cancel, ship) valida
# se a transição é válida antes de mudar o estado.
# ===========================================================
"""
Entidade Order (Pedido).

Representa um pedido feito por um cliente no e-commerce.
Contém o ciclo de vida completo do pedido.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
import uuid

# Importa o enum de status do pedido
from src.shared.types.enums import OrderStatus


@dataclass
class Order:
    """
    Entidade de domínio que representa um pedido.
    
    Um pedido pertence a um cliente e tem um status que
    evolui ao longo do ciclo de vida do pedido.
    
    Example:
        >>> from decimal import Decimal
        >>> order = Order(
        ...     customer_id="uuid-do-cliente",
        ...     total=Decimal("149.90")
        ... )
        >>> print(order.status)
        OrderStatus.PENDING
        
        >>> order.confirm()
        >>> print(order.status)
        OrderStatus.CONFIRMED
    """
    
    # ===== ATRIBUTOS OBRIGATÓRIOS =====
    
    # ID do cliente que fez o pedido
    customer_id: str
    
    # Valor total do pedido
    total: Decimal
    
    # ===== ATRIBUTOS COM VALOR PADRÃO =====
    
    # Status atual do pedido (começa em PENDING)
    status: OrderStatus = OrderStatus.PENDING
    
    # ===== ATRIBUTOS GERADOS =====
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validações após inicialização."""
        if self.total < 0:
            raise ValueError("Total não pode ser negativo")
    
    # ===== MÉTODOS DE TRANSIÇÃO DE ESTADO =====
    # Cada método valida se a transição é válida antes de mudar o estado
    
    def confirm(self) -> None:
        """
        Confirma o pedido.
        
        Transição: PENDING --> CONFIRMED
        
        Raises:
            ValueError: Se pedido não estiver PENDING
            
        Example:
            >>> order.confirm()
            >>> order.status == OrderStatus.CONFIRMED
            True
        """
        if self.status != OrderStatus.PENDING:
            raise ValueError(
                f"Pedido não pode ser confirmado. "
                f"Status atual: {self.status.value}"
            )
        
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.now()
    
    def process(self) -> None:
        """
        Inicia processamento do pedido.
        
        Transição: CONFIRMED --> PROCESSING
        
        Raises:
            ValueError: Se pedido não estiver CONFIRMED
        """
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError(
                f"Pedido não pode entrar em processamento. "
                f"Status atual: {self.status.value}"
            )
        
        self.status = OrderStatus.PROCESSING
        self.updated_at = datetime.now()
    
    def ship(self) -> None:
        """
        Marca pedido como enviado.
        
        Transição: PROCESSING --> SHIPPED
        
        Raises:
            ValueError: Se pedido não estiver PROCESSING
        """
        if self.status != OrderStatus.PROCESSING:
            raise ValueError(
                f"Pedido não pode ser enviado. "
                f"Status atual: {self.status.value}"
            )
        
        self.status = OrderStatus.SHIPPED
        self.updated_at = datetime.now()
    
    def deliver(self) -> None:
        """
        Marca pedido como entregue.
        
        Transição: SHIPPED --> DELIVERED
        
        Raises:
            ValueError: Se pedido não estiver SHIPPED
        """
        if self.status != OrderStatus.SHIPPED:
            raise ValueError(
                f"Pedido não pode ser marcado como entregue. "
                f"Status atual: {self.status.value}"
            )
        
        self.status = OrderStatus.DELIVERED
        self.updated_at = datetime.now()
    
    def cancel(self) -> None:
        """
        Cancela o pedido.
        
        Um pedido só pode ser cancelado se NÃO estiver
        SHIPPED ou DELIVERED (já saiu para entrega).
        
        Raises:
            ValueError: Se pedido já foi enviado ou entregue
            
        Example:
            >>> order.cancel()
            >>> order.status == OrderStatus.CANCELLED
            True
        """
        # Lista de status que impedem cancelamento
        cannot_cancel = [OrderStatus.SHIPPED, OrderStatus.DELIVERED]
        
        if self.status in cannot_cancel:
            raise ValueError(
                f"Pedido não pode ser cancelado. "
                f"Status atual: {self.status.value}"
            )
        
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()
    
    # ===== PROPRIEDADES =====
    
    @property
    def is_active(self) -> bool:
        """
        Verifica se pedido está ativo (não cancelado/entregue).
        
        Returns:
            True se pedido ainda está em andamento
        """
        inactive_statuses = [OrderStatus.CANCELLED, OrderStatus.DELIVERED]
        return self.status not in inactive_statuses
    
    @property
    def can_be_cancelled(self) -> bool:
        """
        Verifica se pedido pode ser cancelado.
        
        Returns:
            True se ainda pode ser cancelado
        """
        return self.status not in [
            OrderStatus.SHIPPED,
            OrderStatus.DELIVERED,
            OrderStatus.CANCELLED
        ]
