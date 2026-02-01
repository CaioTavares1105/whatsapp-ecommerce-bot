# ===========================================================
# src/domain/entities/product.py - Entidade Produto
# ===========================================================
# Representa um produto à venda no e-commerce.
#
# CONCEITOS IMPORTANTES:
#
# 1. Decimal vs float
#    - float: 0.1 + 0.2 = 0.30000000000000004 (erro!)
#    - Decimal: Decimal("0.1") + Decimal("0.2") = Decimal("0.3")
#    - Para valores monetários, SEMPRE use Decimal!
#
# 2. @property
#    - Transforma um método em atributo (sem parênteses)
#    - Permite lógica computada que parece atributo
#    - produto.is_available (não produto.is_available())
# ===========================================================
"""
Entidade Product (Produto).

Representa um produto disponível para venda no e-commerce.
Contém informações como nome, preço, estoque e categoria.

Importante: O preço usa Decimal para evitar erros de ponto flutuante.
"""

from dataclasses import dataclass, field
from datetime import datetime
# Decimal: Tipo para valores monetários (precisão exata)
from decimal import Decimal
import uuid


@dataclass
class Product:
    """
    Entidade de domínio que representa um produto.
    
    Produtos têm controle de estoque e podem estar ativos ou inativos.
    Um produto está disponível para venda se estiver ativo E tiver estoque.
    
    Example:
        >>> from decimal import Decimal
        >>> product = Product(
        ...     name="Camiseta Azul",
        ...     price=Decimal("49.90"),
        ...     category="Vestuário",
        ...     stock=10
        ... )
        >>> print(product.is_available)
        True
        
        >>> product.decrease_stock(5)
        >>> print(product.stock)
        5
    """
    
    # ===== ATRIBUTOS OBRIGATÓRIOS =====
    
    # Nome do produto
    name: str
    
    # Preço (usar Decimal para precisão monetária)
    # Exemplo: Decimal("49.90") em vez de 49.90
    price: Decimal
    
    # Categoria do produto (ex: "Vestuário", "Eletrônicos")
    category: str
    
    # ===== ATRIBUTOS OPCIONAIS =====
    
    # Descrição detalhada
    description: str | None = None
    
    # URL da imagem do produto
    image_url: str | None = None
    
    # Quantidade em estoque
    stock: int = 0
    
    # Se o produto está ativo (disponível para venda)
    active: bool = True
    
    # ===== ATRIBUTOS GERADOS =====
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """
        Validações após inicialização.
        
        Garante que preço e estoque não são negativos.
        
        Raises:
            ValueError: Se preço ou estoque forem negativos
        """
        if self.price < 0:
            raise ValueError("Preço não pode ser negativo")
        if self.stock < 0:
            raise ValueError("Estoque não pode ser negativo")
    
    # ===== PROPRIEDADES COMPUTADAS =====
    
    @property
    def is_available(self) -> bool:
        """
        Verifica se produto está disponível para venda.
        
        Um produto está disponível se:
        - Estiver ativo (active=True)
        - Tiver estoque > 0
        
        Returns:
            True se disponível, False caso contrário
            
        Example:
            >>> product.is_available
            True  # Se ativo e com estoque
        """
        return self.active and self.stock > 0
    
    # ===== MÉTODOS DE NEGÓCIO =====
    
    def decrease_stock(self, quantity: int) -> None:
        """
        Diminui o estoque do produto.
        
        Usado quando um pedido é realizado.
        
        Args:
            quantity: Quantidade a diminuir
            
        Raises:
            ValueError: Se quantidade > estoque disponível
            
        Example:
            >>> product.stock = 10
            >>> product.decrease_stock(3)
            >>> print(product.stock)
            7
        """
        if quantity > self.stock:
            raise ValueError(
                f"Estoque insuficiente. "
                f"Disponível: {self.stock}, Solicitado: {quantity}"
            )
        
        self.stock -= quantity
        self.updated_at = datetime.now()
    
    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta o estoque do produto.
        
        Usado quando chegam novas unidades.
        
        Args:
            quantity: Quantidade a adicionar
            
        Raises:
            ValueError: Se quantidade for negativa
        """
        if quantity < 0:
            raise ValueError("Quantidade não pode ser negativa")
        
        self.stock += quantity
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """
        Desativa o produto (remove da venda).
        
        O produto ainda existe, mas não aparece para clientes.
        """
        self.active = False
        self.updated_at = datetime.now()
    
    def activate(self) -> None:
        """
        Ativa o produto (disponibiliza para venda).
        """
        self.active = True
        self.updated_at = datetime.now()
