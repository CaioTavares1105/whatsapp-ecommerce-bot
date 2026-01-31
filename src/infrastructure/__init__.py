# ===========================================================
# src/infrastructure/__init__.py
# ===========================================================
"""
Camada de INFRAESTRUTURA (Infrastructure Layer).

Esta é a camada mais externa da Clean Architecture.
Ela contém implementações CONCRETAS de interfaces definidas
nas camadas internas.

Subcamadas:
1. database/: Conexão e repositórios do banco de dados
2. cache/: Implementação Redis para sessões e cache
3. whatsapp/: Cliente e handlers do WhatsApp

REGRAS:
- Pode importar de: domain, application
- Implementa interfaces definidas em domain/repositories
- Detalhes técnicos ficam aqui (SQL, Redis, HTTP, etc.)
"""
