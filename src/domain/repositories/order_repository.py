# ===========================================================
# src/domain/repositories/order_repository.py
# ===========================================================
# Interface para o repositório de pedidos.
#
# PEDIDOS SÃO CRÍTICOS:
# - Contêm informações financeiras
# - Precisam de rastreabilidade (histórico)
# - Status muda ao longo do tempo
# ===========================================================
"""
Interface (ABC) para repositório de Order.

Pedidos são a entidade central do e-commerce.
Esta interface permite buscar e atualizar pedidos.
"""

from abc import ABC, abstractmethod

from src.domain.entities.order import Order
from src.shared.types.enums import OrderStatus


class IOrderRepository(ABC):
    """
    Interface para repositório de pedidos.
    
    Inclui métodos específicos para consulta por cliente
    e por status (ex: todos os pedidos pendentes).
    """
    
    # ===== MÉTODOS DE BUSCA (Query) =====
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Order | None:
        """
        Busca pedido por ID único.
        
        Args:
            id: UUID do pedido
            
        Returns:
            Order se encontrado, None se não existir
        """
        ...
    
    @abstractmethod
    async def find_by_customer(self, customer_id: str) -> list[Order]:
        """
        Busca todos os pedidos de um cliente.
        
        Usado quando cliente pergunta: "Quero ver meus pedidos"
        ou "Qual o status do meu pedido?"
        
        Args:
            customer_id: UUID do cliente
            
        Returns:
            Lista de pedidos do cliente (ordenados por data)
        """
        ...
    
    @abstractmethod
    async def find_by_status(self, status: OrderStatus) -> list[Order]:
        """
        Busca pedidos por status.
        
        Útil para:
        - Dashboard administrativo
        - Processar pedidos pendentes
        - Verificar entregas atrasadas
        
        Args:
            status: Status a filtrar (PENDING, CONFIRMED, etc.)
            
        Returns:
            Lista de pedidos com o status especificado
            
        Example:
            pendentes = await repo.find_by_status(OrderStatus.PENDING)
        """
        ...
    
    @abstractmethod
    async def find_recent_by_customer(
        self, 
        customer_id: str, 
        limit: int = 5
    ) -> list[Order]:
        """
        Busca os pedidos mais recentes de um cliente.
        
        Usado para mostrar histórico resumido ao cliente.
        
        Args:
            customer_id: UUID do cliente
            limit: Quantidade máxima de pedidos
            
        Returns:
            Lista dos pedidos mais recentes
        """
        ...
    
    # ===== MÉTODOS DE PERSISTÊNCIA (Command) =====
    
    @abstractmethod
    async def save(self, order: Order) -> None:
        """
        Salva um novo pedido.
        
        Args:
            order: Entidade Order a ser salva
        """
        ...
    
    @abstractmethod
    async def update(self, order: Order) -> None:
        """
        Atualiza um pedido existente.
        
        Usado principalmente para atualizar status.
        
        Args:
            order: Entidade Order com dados atualizados
        """
        ...
    
    # ===== MÉTODOS DE RELATÓRIO =====
    
    @abstractmethod
    async def count_by_status(self, status: OrderStatus) -> int:
        """
        Conta pedidos por status.
        
        Útil para dashboards e métricas.
        
        Args:
            status: Status a contar
            
        Returns:
            Quantidade de pedidos com esse status
        """
        ...
