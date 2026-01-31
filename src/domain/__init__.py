# ===========================================================
# src/domain/__init__.py
# ===========================================================
"""
Camada de DOMÍNIO (Domain Layer).

Esta é a camada mais interna da Clean Architecture.
Ela contém:

1. ENTITIES (Entidades):
   - Objetos de negócio com identidade própria
   - Exemplo: Customer, Product, Order

2. REPOSITORIES (Interfaces):
   - Contratos (ABCs) para acesso a dados
   - Apenas INTERFACES, não implementações
   - Exemplo: ICustomerRepository

3. SERVICES (Serviços de Domínio):
   - Lógica de negócio que não pertence a uma entidade
   - Orquestração entre entidades

REGRAS IMPORTANTES:
- Esta camada NÃO depende de nenhuma outra
- NÃO importar nada de infrastructure ou presentation
- Apenas Python puro + bibliotecas do domínio (dataclasses)
"""
