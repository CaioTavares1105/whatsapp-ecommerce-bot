# ===========================================================
# src/application/__init__.py
# ===========================================================
"""
Camada de APLICAÇÃO (Application Layer).

Esta camada orquestra o fluxo da aplicação. Ela contém:

1. USE CASES (Casos de Uso):
   - Implementam as ações que o sistema pode fazer
   - Coordenam entidades e repositórios
   - Exemplo: HandleMessageUseCase, GetProductsUseCase

2. DTOs (Data Transfer Objects):
   - Objetos para transferir dados entre camadas
   - Validação de entrada/saída
   - Exemplo: MessageDTO, ProductDTO

REGRAS:
- Pode importar de: domain
- NÃO importar de: infrastructure, presentation
- Use cases recebem repositórios por INJEÇÃO DE DEPENDÊNCIA
"""
