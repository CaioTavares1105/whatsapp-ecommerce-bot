# ===========================================================
# src/presentation/__init__.py
# ===========================================================
"""
Camada de APRESENTAÇÃO (Presentation Layer).

Esta camada é a interface com o mundo externo.
Ela recebe requisições e retorna respostas.

Subcamadas:
1. api/: API REST com FastAPI
   - routes/: Rotas da API
   - dependencies.py: Injeção de dependência
   - main.py: Aplicação FastAPI

2. whatsapp/: Controllers para mensagens WhatsApp

REGRAS:
- Pode importar de: domain, application, infrastructure
- Não contém lógica de negócio (só orquestra)
- Valida entrada e formata saída
"""
