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
from src.infrastructure.database.repositories.sqlalchemy_product_repository import (
    SQLAlchemyProductRepository,
)
from src.infrastructure.database.repositories.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.infrastructure.database.repositories.sqlalchemy_session_repository import (
    SQLAlchemySessionRepository,
)

__all__ = [
    "SQLAlchemyCustomerRepository",
    "SQLAlchemyProductRepository",
    "SQLAlchemyOrderRepository",
    "SQLAlchemySessionRepository",
]
