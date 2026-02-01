# ===========================================================
# src/infrastructure/database/repositories/__init__.py
# ===========================================================
"""
Repositórios concretos com SQLAlchemy.

Implementam as interfaces definidas na camada de domínio.
"""

from src.infrastructure.database.repositories.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)

__all__ = [
    "SQLAlchemyCustomerRepository",
]
