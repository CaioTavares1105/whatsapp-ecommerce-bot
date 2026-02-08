# ===========================================================
# src/presentation/api/dependencies.py
# ===========================================================
# Sistema de Dependency Injection para FastAPI.
#
# O QUE É DEPENDENCY INJECTION?
# Padrão onde dependências são "injetadas" de fora,
# em vez de serem criadas dentro da classe.
#
# BENEFÍCIOS:
# - Desacoplamento
# - Facilita testes (injetar mocks)
# - Configuração centralizada
#
# COMO FUNCIONA NO FASTAPI:
# Use Depends() nos parâmetros do endpoint.
# FastAPI chama a função e injeta o retorno.
# ===========================================================
"""
Dependências para injeção no FastAPI.

Centraliza a criação de repositórios e handlers.
Usa implementações SQLAlchemy reais para produção.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import AsyncSessionFactory
from src.infrastructure.database.repositories import (
    SQLAlchemyCustomerRepository,
    SQLAlchemyProductRepository,
    SQLAlchemyOrderRepository,
    SQLAlchemySessionRepository,
)
from src.domain.repositories import (
    ICustomerRepository,
    ISessionRepository,
    IProductRepository,
    IOrderRepository,
)
from src.application.usecases.handle_message import HandleMessageUseCase
from src.presentation.whatsapp.handler import MessageHandler


# ===========================================================
# SESSÃO DO BANCO DE DADOS
# ===========================================================

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Cria sessão do banco para cada request.

    Uso:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ===========================================================
# REPOSITÓRIOS (Implementações reais SQLAlchemy)
# ===========================================================

async def get_customer_repository(
    session: AsyncSession,
) -> ICustomerRepository:
    """Cria repositório de clientes."""
    return SQLAlchemyCustomerRepository(session)


async def get_product_repository(
    session: AsyncSession,
) -> IProductRepository:
    """Cria repositório de produtos."""
    return SQLAlchemyProductRepository(session)


async def get_order_repository(
    session: AsyncSession,
) -> IOrderRepository:
    """Cria repositório de pedidos."""
    return SQLAlchemyOrderRepository(session)


async def get_session_repository(
    session: AsyncSession,
) -> ISessionRepository:
    """Cria repositório de sessões de chat."""
    return SQLAlchemySessionRepository(session)


# ===========================================================
# USE CASE
# ===========================================================

async def get_handle_message_use_case(
    session: AsyncSession,
) -> HandleMessageUseCase:
    """
    Cria o caso de uso de processamento de mensagens
    com todas as dependências reais.
    """
    return HandleMessageUseCase(
        customer_repo=SQLAlchemyCustomerRepository(session),
        session_repo=SQLAlchemySessionRepository(session),
        product_repo=SQLAlchemyProductRepository(session),
        order_repo=SQLAlchemyOrderRepository(session),
    )


# ===========================================================
# HANDLER DE MENSAGENS
# ===========================================================

async def get_message_handler(
    session: AsyncSession,
) -> MessageHandler:
    """
    Cria handler de mensagens com dependências reais.

    Esta função é chamada a cada request, criando
    um handler com repositórios conectados ao banco.
    """
    use_case = await get_handle_message_use_case(session)

    return MessageHandler(
        use_case=use_case,
    )
