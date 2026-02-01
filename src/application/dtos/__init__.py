# ===========================================================
# src/application/dtos/__init__.py
# ===========================================================
"""
DTOs (Data Transfer Objects) da camada de aplicação.

DTOs são objetos simples que transportam dados entre camadas.
"""

from src.application.dtos.message_dto import (
    IncomingMessageDTO,
    MessageResponseDTO,
    OutgoingMessageDTO,
)

__all__ = [
    "IncomingMessageDTO",
    "MessageResponseDTO",
    "OutgoingMessageDTO",
]
