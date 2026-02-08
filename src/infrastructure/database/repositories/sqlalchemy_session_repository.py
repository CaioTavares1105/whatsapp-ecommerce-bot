# ===========================================================
# src/infrastructure/database/repositories/sqlalchemy_session_repository.py
# ===========================================================
# Implementação CONCRETA do ISessionRepository usando SQLAlchemy.
# ===========================================================
"""
Implementação do repositório de sessões com SQLAlchemy.

Esta classe implementa ISessionRepository usando
SQLAlchemy para persistência no PostgreSQL.

NOTA: Em produção, sessões geralmente ficam no Redis
para melhor performance. Esta implementação SQL é
para desenvolvimento e casos onde Redis não está disponível.
"""

from datetime import datetime

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.session import Session
from src.domain.repositories.session_repository import ISessionRepository
from src.infrastructure.database.models import SessionModel, CustomerModel


class SQLAlchemySessionRepository(ISessionRepository):
    """
    Repositório de sessões usando SQLAlchemy.

    Implementa a interface ISessionRepository com
    persistência real no PostgreSQL.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Inicializa o repositório com uma sessão do banco."""
        self._session = session

    # =========================================================
    # MÉTODOS DE BUSCA
    # =========================================================

    async def find_by_id(self, id: str) -> Session | None:
        """Busca sessão por ID único."""
        query = select(SessionModel).where(SessionModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            return None

        entity = self._to_entity(model)

        # Retorna None se expirada
        if entity.is_expired:
            return None

        return entity

    async def find_by_customer(self, customer_id: str) -> Session | None:
        """Busca sessão ativa de um cliente."""
        now = datetime.now()
        query = (
            select(SessionModel)
            .where(SessionModel.customer_id == customer_id)
            .where(SessionModel.expires_at > now)
            .order_by(SessionModel.created_at.desc())
        )
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            return None

        return self._to_entity(model)

    async def find_active_by_phone(self, phone: str) -> Session | None:
        """Busca sessão ativa pelo telefone do cliente."""
        now = datetime.now()

        # Join com customers para buscar por telefone
        query = (
            select(SessionModel)
            .join(CustomerModel)
            .where(CustomerModel.phone_number == phone)
            .where(SessionModel.expires_at > now)
            .order_by(SessionModel.created_at.desc())
        )
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            return None

        return self._to_entity(model)

    # =========================================================
    # MÉTODOS DE PERSISTÊNCIA
    # =========================================================

    async def save(self, session_entity: Session) -> None:
        """Salva uma nova sessão no banco."""
        model = self._to_model(session_entity)
        self._session.add(model)
        await self._session.flush()

    async def update(self, session_entity: Session) -> None:
        """Atualiza uma sessão existente."""
        query = select(SessionModel).where(SessionModel.id == session_entity.id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise ValueError(f"Sessão não encontrada: {session_entity.id}")

        model.state = session_entity.state
        model.context = session_entity.context
        model.expires_at = session_entity.expires_at
        model.updated_at = session_entity.updated_at

        await self._session.flush()

    async def delete(self, id: str) -> None:
        """Remove uma sessão específica."""
        query = select(SessionModel).where(SessionModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise ValueError(f"Sessão não encontrada: {id}")

        await self._session.delete(model)
        await self._session.flush()

    async def delete_expired(self) -> int:
        """Remove todas as sessões expiradas."""
        now = datetime.now()

        # Conta antes de deletar
        count_query = (
            select(func.count())
            .select_from(SessionModel)
            .where(SessionModel.expires_at <= now)
        )
        result = await self._session.execute(count_query)
        count = result.scalar() or 0

        # Deleta expiradas
        delete_query = delete(SessionModel).where(SessionModel.expires_at <= now)
        await self._session.execute(delete_query)
        await self._session.flush()

        return count

    async def count_active(self) -> int:
        """Conta sessões ativas (não expiradas)."""
        now = datetime.now()
        query = (
            select(func.count())
            .select_from(SessionModel)
            .where(SessionModel.expires_at > now)
        )
        result = await self._session.execute(query)
        count = result.scalar()

        return count or 0

    # =========================================================
    # CONVERSORES (Model <-> Entity)
    # =========================================================

    def _to_entity(self, model: SessionModel) -> Session:
        """Converte SessionModel (banco) -> Session (entidade)."""
        return Session(
            id=model.id,
            customer_id=model.customer_id,
            state=model.state,
            context=model.context or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
            expires_at=model.expires_at,
        )

    def _to_model(self, entity: Session) -> SessionModel:
        """Converte Session (entidade) -> SessionModel (banco)."""
        return SessionModel(
            id=entity.id,
            customer_id=entity.customer_id,
            state=entity.state,
            context=entity.context,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            expires_at=entity.expires_at,
        )
