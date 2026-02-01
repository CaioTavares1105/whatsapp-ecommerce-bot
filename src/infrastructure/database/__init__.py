# ===========================================================
# src/infrastructure/database/__init__.py
# ===========================================================
"""
Módulo de infraestrutura de banco de dados.

Exporta:
- Modelos SQLAlchemy
- Conexão e factory de sessões
- Repositórios concretos
"""

from src.infrastructure.database.models import (
    Base,
    CustomerModel,
    ProductModel,
    OrderModel,
    SessionModel,
)
from src.infrastructure.database.connection import (
    engine,
    AsyncSessionFactory,
    get_db_session,
    create_all_tables,
    drop_all_tables,
)
from src.infrastructure.database.repositories import (
    SQLAlchemyCustomerRepository,
)

__all__ = [
    # Models
    "Base",
    "CustomerModel",
    "ProductModel",
    "OrderModel",
    "SessionModel",
    # Connection
    "engine",
    "AsyncSessionFactory",
    "get_db_session",
    "create_all_tables",
    "drop_all_tables",
    # Repositories
    "SQLAlchemyCustomerRepository",
]
