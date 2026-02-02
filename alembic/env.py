# ===========================================================
# alembic/env.py - Ambiente de Migrations
# ===========================================================
# Este script é executado pelo Alembic para:
# - Configurar a conexão com o banco
# - Carregar os modelos SQLAlchemy
# - Executar migrations
#
# IMPORTANTE:
# - Importa os models para registrar no metadata
# - Usa a URL do banco das configurações
# - Suporta modo offline (gera SQL) e online (executa)
# ===========================================================
"""
Configuração do ambiente Alembic.

Este arquivo é executado automaticamente pelo Alembic
quando rodamos comandos de migration.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importa configurações
from src.config.settings import get_settings

# IMPORTANTE: Importa os models para registrar no metadata
# Sem isso, o Alembic não sabe quais tabelas criar
from src.infrastructure.database.models import Base

# Objeto de configuração do Alembic
# Dá acesso ao arquivo alembic.ini
config = context.config

# Configura logging do Python usando alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dos models - usado pelo autogenerate
# target_metadata contém a definição de todas as tabelas
target_metadata = Base.metadata

# Carrega URL do banco das configurações
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)


def run_migrations_offline() -> None:
    """
    Executa migrations em modo 'offline'.
    
    Modo offline:
    - Não conecta ao banco
    - Gera script SQL para executar manualmente
    - Útil para review antes de aplicar
    
    Uso:
        alembic upgrade head --sql > migration.sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Executa migrations com conexão ativa."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Cria engine e executa migrations assíncronas.
    
    Engine configurada com:
    - poolclass=NullPool: Não mantém conexões abertas
    - Adequado para migrations que rodam e terminam
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Executa migrations em modo 'online'.
    
    Modo online:
    - Conecta ao banco diretamente
    - Aplica migrations imediatamente
    - Usado no dia a dia
    
    Uso:
        alembic upgrade head
    """
    asyncio.run(run_async_migrations())


# ===========================================================
# PONTO DE ENTRADA
# ===========================================================
# Determina qual modo usar baseado no contexto

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
