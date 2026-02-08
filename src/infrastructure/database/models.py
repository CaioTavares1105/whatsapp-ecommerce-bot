# ===========================================================
# src/infrastructure/database/models.py
# ===========================================================
# Modelos SQLAlchemy para o banco de dados PostgreSQL.
#
# O QUE SÃO MODELOS SQLAlchemy?
# Modelos são classes Python que representam tabelas no banco.
# Cada atributo da classe vira uma coluna da tabela.
#
# MAPEAMENTO OBJETO-RELACIONAL (ORM):
# - Classe Python ↔ Tabela SQL
# - Atributo Python ↔ Coluna SQL
# - Instância Python ↔ Linha SQL
#
# SQLAlchemy 2.0 (Novo estilo):
# - Usa type hints com `Mapped[tipo]`
# - Usa `mapped_column()` para configurar colunas
# - Usa `DeclarativeBase` como classe base
#
# IMPORTANTE:
# - Modelos NÃO são entidades! São representação do banco.
# - Precisamos converter Model ↔ Entity ao usar.
# ===========================================================
"""
Modelos SQLAlchemy para o banco de dados.

Estes modelos definem a estrutura das tabelas no PostgreSQL.
Cada modelo corresponde a uma tabela no banco.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.shared.types.enums import OrderStatus, SessionState


# ===========================================================
# CLASSE BASE - Todas as outras herdam dela
# ===========================================================

class Base(DeclarativeBase):
    """
    Classe base para todos os modelos SQLAlchemy.
    
    DeclarativeBase é a forma moderna (SQLAlchemy 2.0) de
    criar a classe base para modelos.
    
    Todos os modelos herdam dela para:
    - Registro automático no metadata
    - Suporte a type hints
    - Configuração centralizada
    """
    pass


# ===========================================================
# CustomerModel - Tabela 'customers'
# ===========================================================

class CustomerModel(Base):
    """
    Modelo de cliente no banco de dados.
    
    Corresponde à tabela 'customers' no PostgreSQL.
    
    Attributes:
        id: Identificador único (UUID como string)
        phone_number: Número do WhatsApp (único, indexado)
        name: Nome do cliente (opcional)
        email: Email do cliente (opcional)
        created_at: Data de criação
        updated_at: Data de última atualização
        orders: Relacionamento com pedidos
        sessions: Relacionamento com sessões
    """
    
    # Nome da tabela no banco de dados
    __tablename__ = "customers"
    
    # Colunas da tabela
    # Mapped[tipo]: Define o tipo Python
    # mapped_column(...): Configura a coluna SQL
    
    id: Mapped[str] = mapped_column(
        String(36),  # UUID tem 36 caracteres
        primary_key=True,
    )
    
    phone_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,  # Telefone é único
        index=True,   # Indexado para busca rápida
    )
    
    name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,  # Pode ser NULL
    )
    
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,  # Valor padrão: agora
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,  # Atualiza automaticamente ao modificar
    )
    
    # Relacionamentos (ORM)
    # relationship() define relações entre tabelas
    # back_populates: nome do atributo na outra classe
    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",  # Deleta orders quando customer é deletado
    )
    
    sessions: Mapped[list["SessionModel"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )


# ===========================================================
# ProductModel - Tabela 'products'
# ===========================================================

class ProductModel(Base):
    """
    Modelo de produto no banco de dados.
    
    Attributes:
        id: Identificador único
        name: Nome do produto
        description: Descrição detalhada
        price: Preço (Decimal para precisão)
        image_url: URL da imagem
        category: Categoria do produto (indexado)
        stock: Quantidade em estoque
        active: Se está ativo para venda
    """
    
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,  # Obrigatório
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,  # Texto longo
        nullable=True,
    )
    
    # Numeric(10, 2): 10 dígitos total, 2 decimais
    # Ex: 99999999.99
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    category: Mapped[str] = mapped_column(
        String(100),
        index=True,  # Indexado para busca por categoria
        nullable=False,
    )
    
    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )


# ===========================================================
# OrderModel - Tabela 'orders'
# ===========================================================

class OrderModel(Base):
    """
    Modelo de pedido no banco de dados.
    
    Attributes:
        id: Identificador único do pedido
        customer_id: FK para cliente
        status: Status atual do pedido (enum)
        total: Valor total do pedido
        customer: Relacionamento com cliente
    """
    
    __tablename__ = "orders"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    
    # ForeignKey: Chave estrangeira para customers.id
    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )
    
    # SQLEnum: Armazena enum como tipo nativo do PostgreSQL
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(
            OrderStatus,
            name="order_status",
            values_callable=lambda x: [e.value for e in x],
        ),
        default=OrderStatus.PENDING,
    )
    
    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
    
    # Relacionamento N:1 com Customer
    customer: Mapped["CustomerModel"] = relationship(
        back_populates="orders",
    )


# ===========================================================
# SessionModel - Tabela 'sessions'
# ===========================================================

class SessionModel(Base):
    """
    Modelo de sessão de chat no banco de dados.
    
    Sessões armazenam o estado atual da conversa com o cliente.
    
    Attributes:
        id: Identificador único
        customer_id: FK para cliente
        state: Estado atual da conversa (enum)
        context: Dados de contexto (JSON)
        expires_at: Quando a sessão expira
    """
    
    __tablename__ = "sessions"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    
    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )
    
    state: Mapped[SessionState] = mapped_column(
        SQLEnum(
            SessionState,
            name="session_state",
            values_callable=lambda x: [e.value for e in x],
        ),
        default=SessionState.INITIAL,
    )
    
    # JSON: Armazena dicionário Python como JSON no banco
    context: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    
    # Relacionamento N:1 com Customer
    customer: Mapped["CustomerModel"] = relationship(
        back_populates="sessions",
    )
