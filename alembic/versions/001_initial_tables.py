# ===========================================================
# alembic/versions/001_initial_tables.py
# ===========================================================
# Migration Inicial - Cria todas as tabelas do sistema.
#
# COMO FUNCIONA:
# - upgrade(): Cria as tabelas
# - downgrade(): Remove as tabelas
#
# ORDEM IMPORTANTE:
# 1. Tabelas sem FK primeiro (customers, products)
# 2. Tabelas com FK depois (orders, sessions)
#
# REVERSÃO:
# Ordem inversa para evitar erros de FK
# ===========================================================
"""
Migration inicial - Criar todas as tabelas.

Revision ID: 001
Revises: (nenhuma - é a primeira)
Create Date: 2026-02-01

Tabelas criadas:
- customers
- products
- orders
- sessions
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Identificadores da revisão
revision: str = "001"
down_revision: Union[str, None] = None  # Primeira migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Aplica as mudanças - CRIA todas as tabelas.
    
    Ordem: tabelas sem FK primeiro, tabelas com FK depois.
    """
    
    # =========================================================
    # 1. TABELA: customers (sem FK)
    # =========================================================
    op.create_table(
        "customers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("phone_number", sa.String(15), unique=True, index=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    
    # =========================================================
    # 2. TABELA: products (sem FK)
    # =========================================================
    op.create_table(
        "products",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("category", sa.String(100), index=True, nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    
    # =========================================================
    # 3. CRIAR ENUMS (PostgreSQL específico)
    # =========================================================
    # Cria tipos ENUM no PostgreSQL
    order_status_enum = postgresql.ENUM(
        "pending", "confirmed", "processing", "shipped", "delivered", "cancelled",
        name="order_status",
        create_type=True,
    )
    order_status_enum.create(op.get_bind(), checkfirst=True)
    
    session_state_enum = postgresql.ENUM(
        "initial", "menu", "products", "order_status", "faq", "human_transfer", "closed",
        name="session_state",
        create_type=True,
    )
    session_state_enum.create(op.get_bind(), checkfirst=True)
    
    # =========================================================
    # 4. TABELA: orders (com FK para customers)
    # =========================================================
    op.create_table(
        "orders",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "customer_id",
            sa.String(36),
            sa.ForeignKey("customers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "status",
            order_status_enum,
            nullable=False,
            server_default="pending",
        ),
        sa.Column("total", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    
    # Índice para buscar pedidos por cliente
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"])
    
    # =========================================================
    # 5. TABELA: sessions (com FK para customers)
    # =========================================================
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "customer_id",
            sa.String(36),
            sa.ForeignKey("customers.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "state",
            session_state_enum,
            nullable=False,
            server_default="initial",
        ),
        sa.Column("context", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
    )
    
    # Índice para buscar sessões por cliente
    op.create_index("ix_sessions_customer_id", "sessions", ["customer_id"])


def downgrade() -> None:
    """
    Reverte as mudanças - REMOVE todas as tabelas.
    
    Ordem inversa: tabelas com FK primeiro, tabelas sem FK depois.
    """
    
    # 1. Remover tabelas com FK primeiro
    op.drop_index("ix_sessions_customer_id", table_name="sessions")
    op.drop_table("sessions")
    
    op.drop_index("ix_orders_customer_id", table_name="orders")
    op.drop_table("orders")
    
    # 2. Remover enums
    op.execute("DROP TYPE IF EXISTS session_state")
    op.execute("DROP TYPE IF EXISTS order_status")
    
    # 3. Remover tabelas sem FK
    op.drop_table("products")
    op.drop_table("customers")
