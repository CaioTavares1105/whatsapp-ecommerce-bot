# ===========================================================
# src/application/dtos/message_dto.py
# ===========================================================
# DTOs (Data Transfer Objects) para mensagens.
#
# O QUE É UM DTO?
# DTO é um objeto que transporta dados entre camadas.
# Diferente de entidades, DTOs:
# - Não têm lógica de negócio
# - São simples containers de dados
# - São validados com Pydantic (validação automática)
#
# POR QUE USAR DTOs?
# 1. Validação automática (Pydantic valida tipos)
# 2. Documentação clara (type hints)
# 3. Separação de camadas (API não conhece entidades)
#
# PYDANTIC BaseModel:
# - Valida dados automaticamente
# - Converte tipos (str "123" -> int 123)
# - Gera schemas JSON automaticamente
# ===========================================================
"""
DTOs (Data Transfer Objects) para mensagens.

DTOs transportam dados entre camadas da aplicação.
Usamos Pydantic para validação automática.

Tipos de DTOs:
- IncomingMessageDTO: Mensagem recebida do usuário
- OutgoingMessageDTO: Mensagem enviada ao usuário
- MessageResponseDTO: Resposta do processamento
"""

from pydantic import BaseModel, Field

from src.shared.types.enums import MessageDirection


class IncomingMessageDTO(BaseModel):
    """
    DTO para mensagem recebida do usuário (WhatsApp -> Bot).
    
    Attributes:
        phone_number: Número do WhatsApp (10-15 dígitos)
        text: Texto da mensagem (não pode ser vazio)
        message_id: ID único da mensagem (opcional, do WhatsApp)
        
    Example:
        >>> dto = IncomingMessageDTO(
        ...     phone_number="5511999999999",
        ...     text="Olá, quero ver produtos"
        ... )
    """
    
    # Field(...) significa que o campo é OBRIGATÓRIO
    # min_length e max_length validam automaticamente
    phone_number: str = Field(
        ...,  # ... = obrigatório
        min_length=10,
        max_length=15,
        description="Número de telefone do cliente"
    )
    
    text: str = Field(
        ...,
        min_length=1,
        description="Texto da mensagem recebida"
    )
    
    # Campo opcional (tem valor padrão None)
    message_id: str | None = Field(
        default=None,
        description="ID da mensagem no WhatsApp"
    )


class OutgoingMessageDTO(BaseModel):
    """
    DTO para mensagem enviada ao usuário (Bot -> WhatsApp).
    
    Usado quando queremos enviar uma mensagem proativamente.
    
    Attributes:
        phone_number: Número do destinatário
        text: Texto a ser enviado
        direction: Sempre OUTGOING
    """
    
    phone_number: str = Field(..., description="Número do destinatário")
    text: str = Field(..., description="Texto da mensagem")
    direction: MessageDirection = MessageDirection.OUTGOING


class MessageResponseDTO(BaseModel):
    """
    DTO para resposta do processamento de mensagem.
    
    Retornado pelo HandleMessageUseCase com:
    - O texto de resposta
    - Flag se deve transferir para humano
    - Metadados extras (opcional)
    
    Attributes:
        text: Texto da resposta
        should_transfer_to_human: Se deve transferir para atendente
        metadata: Dados extras (ex: ID do pedido consultado)
        
    Example:
        >>> response = MessageResponseDTO(
        ...     text="Olá! Como posso ajudar?",
        ...     should_transfer_to_human=False
        ... )
    """
    
    text: str = Field(..., description="Texto da resposta")
    
    should_transfer_to_human: bool = Field(
        default=False,
        description="Se deve transferir para atendimento humano"
    )
    
    metadata: dict | None = Field(
        default=None,
        description="Dados extras sobre o processamento"
    )
