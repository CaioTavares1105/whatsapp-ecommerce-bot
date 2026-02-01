# ===========================================================
# src/application/usecases/__init__.py
# ===========================================================
"""
Casos de uso da aplicação.

Cada caso de uso representa uma ação do sistema.
"""

from src.application.usecases.handle_message import HandleMessageUseCase

__all__ = [
    "HandleMessageUseCase",
]
