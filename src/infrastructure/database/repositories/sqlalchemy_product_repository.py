# ===========================================================
# src/infrastructure/database/repositories/sqlalchemy_product_repository.py
# ===========================================================
# Implementação CONCRETA do IProductRepository usando SQLAlchemy.
# ===========================================================
"""
Implementação do repositório de produtos com SQLAlchemy.

Esta classe implementa IProductRepository usando
SQLAlchemy para persistência no PostgreSQL.
"""

from decimal import Decimal

from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.product import Product
from src.domain.repositories.product_repository import IProductRepository
from src.infrastructure.database.models import ProductModel


class SQLAlchemyProductRepository(IProductRepository):
    """
    Repositório de produtos usando SQLAlchemy.

    Implementa a interface IProductRepository com
    persistência real no PostgreSQL.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Inicializa o repositório com uma sessão do banco."""
        self._session = session

    # =========================================================
    # MÉTODOS DE BUSCA
    # =========================================================

    async def find_by_id(self, id: str) -> Product | None:
        """Busca produto por ID único."""
        query = select(ProductModel).where(ProductModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            return None

        return self._to_entity(model)

    async def find_by_category(self, category: str) -> list[Product]:
        """Busca produtos por categoria."""
        query = (
            select(ProductModel)
            .where(ProductModel.category == category)
            .where(ProductModel.active == True)
            .order_by(ProductModel.name)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def find_all_active(self) -> list[Product]:
        """Lista todos os produtos ativos (disponíveis para venda)."""
        query = (
            select(ProductModel)
            .where(ProductModel.active == True)
            .where(ProductModel.stock > 0)
            .order_by(ProductModel.category, ProductModel.name)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def search(self, query_text: str) -> list[Product]:
        """Busca produtos por nome ou descrição."""
        search_pattern = f"%{query_text}%"
        query = (
            select(ProductModel)
            .where(
                (ProductModel.name.ilike(search_pattern)) |
                (ProductModel.description.ilike(search_pattern))
            )
            .where(ProductModel.active == True)
            .order_by(ProductModel.name)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def list_categories(self) -> list[str]:
        """Lista todas as categorias disponíveis."""
        query = (
            select(distinct(ProductModel.category))
            .where(ProductModel.active == True)
            .order_by(ProductModel.category)
        )
        result = await self._session.execute(query)
        categories = result.scalars().all()

        return list(categories)

    # =========================================================
    # MÉTODOS DE PERSISTÊNCIA
    # =========================================================

    async def save(self, product: Product) -> None:
        """Salva um novo produto no banco."""
        model = self._to_model(product)
        self._session.add(model)
        await self._session.flush()

    async def update(self, product: Product) -> None:
        """Atualiza um produto existente."""
        query = select(ProductModel).where(ProductModel.id == product.id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise ValueError(f"Produto não encontrado: {product.id}")

        model.name = product.name
        model.description = product.description
        model.price = product.price
        model.image_url = product.image_url
        model.category = product.category
        model.stock = product.stock
        model.active = product.active
        model.updated_at = product.updated_at

        await self._session.flush()

    async def delete(self, id: str) -> None:
        """Remove um produto do banco."""
        query = select(ProductModel).where(ProductModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise ValueError(f"Produto não encontrado: {id}")

        await self._session.delete(model)
        await self._session.flush()

    # =========================================================
    # CONVERSORES (Model <-> Entity)
    # =========================================================

    def _to_entity(self, model: ProductModel) -> Product:
        """Converte ProductModel (banco) -> Product (entidade)."""
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            image_url=model.image_url,
            category=model.category,
            stock=model.stock,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Product) -> ProductModel:
        """Converte Product (entidade) -> ProductModel (banco)."""
        return ProductModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            image_url=entity.image_url,
            category=entity.category,
            stock=entity.stock,
            active=entity.active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
