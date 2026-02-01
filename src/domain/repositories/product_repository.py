# ===========================================================
# src/domain/repositories/product_repository.py
# ===========================================================
# Interface para o repositório de produtos.
#
# MÉTODOS COMUNS EM REPOSITÓRIOS:
# - find_by_id: Buscar por ID único
# - find_all: Listar todos
# - save: Criar novo
# - update: Atualizar existente
# - delete: Remover
#
# MÉTODOS ESPECÍFICOS:
# - find_by_category: Filtrar por categoria
# - search: Busca textual
# - find_all_active: Só produtos à venda
# ===========================================================
"""
Interface (ABC) para repositório de Product.

Define operações de busca e persistência de produtos.
"""

from abc import ABC, abstractmethod

from src.domain.entities.product import Product


class IProductRepository(ABC):
    """
    Interface para repositório de produtos.
    
    Produtos são consultados frequentemente pelos clientes,
    então incluímos métodos específicos de busca.
    """
    
    # ===== MÉTODOS DE BUSCA (Query) =====
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Product | None:
        """
        Busca produto por ID único.
        
        Args:
            id: UUID do produto
            
        Returns:
            Product se encontrado, None se não existir
        """
        ...
    
    @abstractmethod
    async def find_by_category(self, category: str) -> list[Product]:
        """
        Busca produtos por categoria.
        
        Usado quando cliente diz: "Quero ver roupas" ou
        "Me mostra os acessórios".
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de produtos da categoria
            
        Example:
            produtos = await repo.find_by_category("Camisetas")
        """
        ...
    
    @abstractmethod
    async def find_all_active(self) -> list[Product]:
        """
        Lista todos os produtos ativos (disponíveis para venda).
        
        Um produto está ativo se:
        - active = True
        - stock > 0
        
        Returns:
            Lista de produtos disponíveis
        """
        ...
    
    @abstractmethod
    async def search(self, query: str) -> list[Product]:
        """
        Busca produtos por nome ou descrição.
        
        Permite busca textual quando cliente diz:
        "Procura camiseta azul" ou "Tem algo de algodão?"
        
        Args:
            query: Termo de busca
            
        Returns:
            Lista de produtos que correspondem à busca
            
        Example:
            produtos = await repo.search("camiseta azul")
        """
        ...
    
    @abstractmethod
    async def list_categories(self) -> list[str]:
        """
        Lista todas as categorias disponíveis.
        
        Usado para mostrar menu de categorias ao cliente.
        
        Returns:
            Lista de nomes de categorias únicas
        """
        ...
    
    # ===== MÉTODOS DE PERSISTÊNCIA (Command) =====
    
    @abstractmethod
    async def save(self, product: Product) -> None:
        """
        Salva um novo produto.
        
        Args:
            product: Entidade Product a ser salva
        """
        ...
    
    @abstractmethod
    async def update(self, product: Product) -> None:
        """
        Atualiza um produto existente.
        
        Usado para atualizar estoque, preço, status ativo, etc.
        
        Args:
            product: Entidade Product com dados atualizados
        """
        ...
    
    @abstractmethod
    async def delete(self, id: str) -> None:
        """
        Remove um produto.
        
        Args:
            id: UUID do produto
        """
        ...
