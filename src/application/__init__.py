# ===========================================================
# src/application/__init__.py
# ===========================================================
"""
Camada de Aplicação - Application Layer.

Esta camada contém:
- Casos de Uso (Use Cases): Ações do sistema
- DTOs: Objetos de transferência de dados

A camada de aplicação:
- Orquestra a lógica de negócio
- Não conhece detalhes de infraestrutura
- Depende apenas de INTERFACES
"""

from src.application.dtos import (
    IncomingMessageDTO,
    MessageResponseDTO,
    OutgoingMessageDTO,
)
from src.application.usecases import HandleMessageUseCase

__all__ = [
    # DTOs
    "IncomingMessageDTO",
    "MessageResponseDTO",
    "OutgoingMessageDTO",
    # Use Cases
    "HandleMessageUseCase",
]
