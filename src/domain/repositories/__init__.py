# ===========================================================
# src/domain/repositories/__init__.py
# ===========================================================
"""
Interfaces dos repositórios (Abstract Base Classes).

Um repositório é um CONTRATO que define como acessar dados.
Aqui definimos apenas as INTERFACES (ABCs), não as implementações.

Por que usar interfaces?
1. Desacoplamento: O domínio não sabe se usa PostgreSQL, MongoDB, etc.
2. Testabilidade: Podemos criar mocks fácilmente
3. Flexibilidade: Trocar banco de dados sem mudar regras de negócio

A implementação real fica em: infrastructure/database/repositories/
"""
