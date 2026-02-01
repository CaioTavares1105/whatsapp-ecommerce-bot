# ===========================================================
# src/domain/repositories/__init__.py
# ===========================================================
# Este arquivo exporta todas as interfaces de repositório.
#
# POR QUE CENTRALIZAR OS EXPORTS?
# Permite importar de forma simples:
#   from src.domain.repositories import ICustomerRepository
#
# Em vez de:
#   from src.domain.repositories.customer_repository import ICustomerRepository
#
# __all__ define o que é exportado quando alguém faz:
#   from src.domain.repositories import *
# ===========================================================
"""
Interfaces (contratos) dos repositórios.

Este pacote contém as Abstract Base Classes (ABCs) que definem
os contratos para acesso a dados. A camada de domínio depende
apenas destas interfaces, nunca das implementações concretas.

Uso:
    from src.domain.repositories import (
        ICustomerRepository,
        IProductRepository,
        IOrderRepository,
        ISessionRepository,
    )
    
    class MyUseCase:
        def __init__(self, customer_repo: ICustomerRepository):
            self.customer_repo = customer_repo
            # Funciona com qualquer implementação!

Vantagens deste padrão:
    1. Desacoplamento: Domínio não conhece SQLAlchemy/Redis
    2. Testabilidade: Fácil criar mocks para testes
    3. Flexibilidade: Trocar banco sem mudar lógica
"""

from src.domain.repositories.customer_repository import ICustomerRepository
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.repositories.product_repository import IProductRepository
from src.domain.repositories.session_repository import ISessionRepository

# __all__ = lista de nomes públicos do módulo
# Usado por: from src.domain.repositories import *
__all__ = [
    "ICustomerRepository",
    "IOrderRepository",
    "IProductRepository",
    "ISessionRepository",
]
