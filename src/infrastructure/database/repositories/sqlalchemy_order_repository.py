# ===========================================================
# src/infrastructure/database/repositories/sqlalchemy_order_repository.py
# ===========================================================
# Implementação CONCRETA do IOrderRepository usando SQLAlchemy.
# ===========================================================
"""
Implementação do repositório de pedidos com SQLAlchemy.

Esta classe implementa IOrderRepository usando
SQLAlchemy para persistência no PostgreSQL.
"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.order import Order
from src.domain.repositories.order_repository import IOrderRepository
from src.infrastructure.database.models import OrderModel
from src.shared.types.enums import OrderStatus


class SQLAlchemyOrderRepository(IOrderRepository):
    """
    Repositório de pedidos usando SQLAlchemy.

    Implementa a interface IOrderRepository com
    persistência real no PostgreSQL.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Inicializa o repositório com uma sessão do banco."""
        self._session = session

    # =========================================================
    # MÉTODOS DE BUSCA
    # =========================================================

    async def find_by_id(self, id: str) -> Order | None:
        """Busca pedido por ID único."""
        query = select(OrderModel).where(OrderModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            return None

        return self._to_entity(model)

    async def find_by_customer(self, customer_id: str) -> list[Order]:
        """Busca todos os pedidos de um cliente."""
        query = (
            select(OrderModel)
            .where(OrderModel.customer_id == customer_id)
            .order_by(OrderModel.created_at.desc())
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def find_by_status(self, status: OrderStatus) -> list[Order]:
        """Busca pedidos por status."""
        query = (
            select(OrderModel)
            .where(OrderModel.status == status)
            .order_by(OrderModel.created_at.desc())
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def find_recent_by_customer(
        self,
        customer_id: str,
        limit: int = 5
    ) -> list[Order]:
        """Busca os pedidos mais recentes de um cliente."""
        query = (
            select(OrderModel)
            .where(OrderModel.customer_id == customer_id)
            .order_by(OrderModel.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    # =========================================================
    # MÉTODOS DE PERSISTÊNCIA
    # =========================================================

    async def save(self, order: Order) -> None:
        """Salva um novo pedido no banco."""
        model = self._to_model(order)
        self._session.add(model)
        await self._session.flush()

    async def update(self, order: Order) -> None:
        """Atualiza um pedido existente."""
        query = select(OrderModel).where(OrderModel.id == order.id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise ValueError(f"Pedido não encontrado: {order.id}")

        model.status = order.status
        model.total = order.total
        model.updated_at = order.updated_at

        await self._session.flush()

    # =========================================================
    # MÉTODOS DE RELATÓRIO
    # =========================================================

    async def count_by_status(self, status: OrderStatus) -> int:
        """Conta pedidos por status."""
        query = (
            select(func.count())
            .select_from(OrderModel)
            .where(OrderModel.status == status)
        )
        result = await self._session.execute(query)
        count = result.scalar()

        return count or 0

    # =========================================================
    # CONVERSORES (Model <-> Entity)
    # =========================================================

    def _to_entity(self, model: OrderModel) -> Order:
        """Converte OrderModel (banco) -> Order (entidade)."""
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=model.status,
            total=model.total,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Order) -> OrderModel:
        """Converte Order (entidade) -> OrderModel (banco)."""
        return OrderModel(
            id=entity.id,
            customer_id=entity.customer_id,
            status=entity.status,
            total=entity.total,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
