# ===========================================================
# src/application/dtos/__init__.py
# ===========================================================
"""
DTOs - Data Transfer Objects.

DTOs são objetos simples para transferir dados entre camadas.
Usamos Pydantic BaseModel para validação automática.

Por que usar DTOs?
1. Validação de entrada (o que vem do usuário)
2. Formato de saída (o que retornamos)
3. Desacoplamento (entidades internas != API externa)

Exemplo:
    class MessageInputDTO(BaseModel):
        phone_number: str
        text: str
"""
