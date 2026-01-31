# ===========================================================
# src/__init__.py
# ===========================================================
# Este arquivo transforma a pasta 'src' em um PACOTE Python.
#
# O QUE É UM PACOTE?
# Em Python, uma pasta com __init__.py é tratada como um
# "pacote" - um módulo que pode conter outros módulos.
#
# SEM este arquivo: Python NÃO reconhece a pasta como módulo
# COM este arquivo: Você pode fazer: from src import algo
#
# NOTA: A partir do Python 3.3, existem "namespace packages"
# que não precisam de __init__.py, mas é boa prática ter.
# ===========================================================
"""
Pacote raiz da aplicação WhatsApp E-commerce Bot.

Este pacote contém toda a lógica da aplicação, organizada
seguindo os princípios da Clean Architecture:

- domain/: Entidades e regras de negócio (núcleo)
- application/: Casos de uso (orquestração)
- infrastructure/: Implementações externas (DB, APIs)
- presentation/: Interfaces (API REST, handlers)
- config/: Configurações da aplicação
- shared/: Código compartilhado entre camadas
"""
