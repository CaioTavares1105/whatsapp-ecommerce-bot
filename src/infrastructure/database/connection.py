# ===========================================================
# src/infrastructure/database/connection.py
# ===========================================================
# Configuração da conexão assíncrona com PostgreSQL.
#
# POR QUE CONEXÃO ASSÍNCRONA?
# - Não bloqueia a thread enquanto espera o banco
# - Permite processar múltiplas requests simultaneamente
# - Essencial para aplicações de alta performance
#
# CONCEITOS IMPORTANTES:
#
# 1. ENGINE:
#    - Ponto de conexão com o banco
#    - Gerencia o pool de conexões
#    - Criada UMA vez na aplicação
#
# 2. SESSION:
#    - Representa uma "conversa" com o banco
#    - Guarda mudanças a serem commitadas
#    - Criada por REQUEST (uma por operação)
#
# 3. POOL:
#    - Conjunto de conexões reutilizáveis
#    - pool_size: conexões mantidas abertas
#    - max_overflow: conexões extras temporárias
# ===========================================================
"""
Configuração da conexão com o banco de dados PostgreSQL.

Este módulo cria:
- Engine assíncrona para conectar ao banco
- Factory de sessões para criar sessões sob demanda
- Dependency injection para FastAPI
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src.config.settings import get_settings


# Carrega configurações do ambiente
settings = get_settings()


# ===========================================================
# ENGINE - Ponto de conexão com o banco
# ===========================================================

# create_async_engine: Cria engine ASSÍNCRONA
# - url: string de conexão (postgresql+asyncpg://...)
# - echo: se True, loga todas as queries SQL (útil em dev)
# - pool_size: conexões mantidas no pool
# - max_overflow: conexões extras permitidas

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL apenas em desenvolvimento
    pool_size=5,          # 5 conexões permanentes
    max_overflow=10,      # Até 10 extras temporárias
)


# ===========================================================
# SESSION FACTORY - Fábrica de sessões
# ===========================================================

# async_sessionmaker: Cria "fábrica" de sessões
# - bind: engine a usar
# - class_: tipo de sessão (AsyncSession)
# - expire_on_commit: se objetos "expiram" após commit
#   - False: mantém dados em memória após commit
#   - True: recarrega do banco após commit

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Não recarregar objetos após commit
)


# ===========================================================
# DEPENDENCY INJECTION - Para uso com FastAPI
# ===========================================================

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Cria sessão do banco para injection em endpoints FastAPI.
    
    Uso com FastAPI:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            result = await db.execute(select(UserModel))
            return result.scalars().all()
    
    Yields:
        AsyncSession: Sessão do banco de dados
        
    Note:
        - Sessão é commitada automaticamente se não houver erro
        - Rollback automático em caso de exceção
        - Sessão é fechada ao final (finally)
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()  # Commit se tudo OK
        except Exception:
            await session.rollback()  # Rollback se erro
            raise
        finally:
            await session.close()  # Sempre fecha a sessão


# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================

async def create_all_tables() -> None:
    """
    Cria todas as tabelas no banco de dados.
    
    Útil para desenvolvimento/testes. Em produção, use migrations.
    
    Example:
        import asyncio
        asyncio.run(create_all_tables())
    """
    from src.infrastructure.database.models import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:
    """
    Remove todas as tabelas do banco de dados.
    
    CUIDADO: Isso deleta TODOS os dados! Usar apenas em testes.
    """
    from src.infrastructure.database.models import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
