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
"""

from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import AsyncSessionFactory
from src.infrastructure.database.repositories import SQLAlchemyCustomerRepository
from src.domain.repositories import (
    ICustomerRepository,
    ISessionRepository,
    IProductRepository,
    IOrderRepository,
)
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
# REPOSITÓRIOS
# ===========================================================

async def get_customer_repository(
    session: AsyncSession,
) -> ICustomerRepository:
    """Cria repositório de clientes."""
    return SQLAlchemyCustomerRepository(session)


# TODO: Implementar outros repositórios quando necessário
# Por enquanto, usamos implementações mock para desenvolvimento

class MockSessionRepository(ISessionRepository):
    """Implementação mock do repositório de sessões."""
    
    async def find_by_customer(self, customer_id: str):
        return None
    
    async def find_by_id(self, id: str):
        return None
    
    async def save(self, session):
        pass
    
    async def update(self, session):
        pass
    
    async def delete(self, id: str):
        pass
    
    async def delete_expired(self):
        pass


class MockProductRepository(IProductRepository):
    """Implementação mock do repositório de produtos."""
    
    async def find_all(self):
        return []
    
    async def find_by_category(self, category: str):
        return []
    
    async def find_by_id(self, id: str):
        return None
    
    async def search(self, query: str):
        return []
    
    async def save(self, product):
        pass
    
    async def update(self, product):
        pass
    
    async def delete(self, id: str):
        pass


class MockOrderRepository(IOrderRepository):
    """Implementação mock do repositório de pedidos."""
    
    async def find_by_customer(self, customer_id: str):
        return []
    
    async def find_by_id(self, id: str):
        return None
    
    async def save(self, order):
        pass
    
    async def update(self, order):
        pass
    
    async def delete(self, id: str):
        pass
    
    async def find_by_status(self, status):
        return []


# ===========================================================
# HANDLER DE MENSAGENS
# ===========================================================

@lru_cache
def get_message_handler() -> MessageHandler:
    """
    Retorna handler de mensagens singleton.
    
    Usa @lru_cache para criar apenas uma instância.
    Em produção, use dependency injection real com banco.
    """
    return MessageHandler(
        customer_repo=MockCustomerRepository(),
        session_repo=MockSessionRepository(),
        product_repo=MockProductRepository(),
        order_repo=MockOrderRepository(),
    )


class MockCustomerRepository(ICustomerRepository):
    """Implementação mock do repositório de clientes."""
    
    _customers: dict = {}
    
    async def find_by_phone(self, phone: str):
        return self._customers.get(phone)
    
    async def find_by_id(self, id: str):
        for customer in self._customers.values():
            if customer.id == id:
                return customer
        return None
    
    async def find_all(self):
        return list(self._customers.values())
    
    async def save(self, customer):
        self._customers[customer.phone_number] = customer
    
    async def update(self, customer):
        self._customers[customer.phone_number] = customer
    
    async def delete(self, id: str):
        for phone, customer in list(self._customers.items()):
            if customer.id == id:
                del self._customers[phone]
                break
