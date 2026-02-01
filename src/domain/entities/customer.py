# ===========================================================
# src/domain/entities/customer.py - Entidade Cliente
# ===========================================================
# Esta é uma ENTIDADE DE DOMÍNIO. Entidades são objetos com
# IDENTIDADE própria que persistem ao longo do tempo.
#
# O QUE É UMA DATACLASS?
# Dataclass é um decorator do Python que gera automaticamente:
# - __init__() (construtor)
# - __repr__() (representação em string)
# - __eq__() (comparação de igualdade)
#
# Sem dataclass:
#   class Customer:
#       def __init__(self, phone, name):
#           self.phone = phone
#           self.name = name
#
# Com dataclass:
#   @dataclass
#   class Customer:
#       phone: str
#       name: str
#   # __init__, __repr__, __eq__ são gerados automaticamente!
#
# O QUE É field(default_factory=...)?
# Usado para valores padrão que precisam ser calculados:
#   id: str = field(default_factory=lambda: str(uuid.uuid4()))
# Cada instância recebe um UUID diferente.
#
# O QUE É __post_init__?
# Método chamado APÓS o __init__ gerado pelo @dataclass.
# Usado para validações e processamentos adicionais.
# ===========================================================
"""
Entidade Customer (Cliente).

Representa um cliente do e-commerce que interage via WhatsApp.
Esta entidade é o "coração" do domínio - sem cliente, não há pedido.

Attributes:
    id: Identificador único (UUID)
    phone_number: Número do WhatsApp (apenas dígitos)
    name: Nome do cliente (opcional)
    email: Email do cliente (opcional)
    created_at: Data de criação
    updated_at: Data da última atualização
"""

# dataclass: Decorator que gera __init__, __repr__, __eq__
# field: Permite customizar atributos individuais
from dataclasses import dataclass, field

# datetime: Trabalhar com datas e horas
from datetime import datetime

# uuid: Gerar identificadores únicos universais
import uuid


@dataclass
class Customer:
    """
    Entidade de domínio que representa um cliente.
    
    Um cliente é identificado pelo seu número de telefone do WhatsApp.
    O número é validado e limpo (apenas dígitos) na criação.
    
    Example:
        >>> customer = Customer(
        ...     phone_number="+55 (11) 99999-9999",
        ...     name="João Silva"
        ... )
        >>> print(customer.phone_number)
        5511999999999
        
        >>> print(customer.id)
        'a1b2c3d4-e5f6-...'  # UUID gerado automaticamente
    """
    
    # ===== ATRIBUTOS OBRIGATÓRIOS =====
    # Atributos SEM valor padrão devem vir primeiro!
    
    # Número do WhatsApp (será limpo para apenas dígitos)
    phone_number: str
    
    # ===== ATRIBUTOS OPCIONAIS =====
    # Atributos COM valor padrão vêm depois
    
    # Nome do cliente (obtido via conversa)
    name: str | None = None
    
    # Email do cliente (opcional)
    email: str | None = None
    
    # ===== ATRIBUTOS GERADOS AUTOMATICAMENTE =====
    # field(default_factory=...) gera um valor diferente para cada instância
    
    # ID único (UUID v4)
    # lambda: str(uuid.uuid4()) é uma função que gera um novo UUID
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Data de criação (momento da instanciação)
    created_at: datetime = field(default_factory=datetime.now)
    
    # Data da última atualização
    updated_at: datetime = field(default_factory=datetime.now)
    
    # ===== MÉTODOS ESPECIAIS =====
    
    def __post_init__(self) -> None:
        """
        Método chamado APÓS o __init__ gerado pelo @dataclass.
        
        Aqui fazemos validações que dependem dos valores já atribuídos.
        Se algo estiver errado, levantamos uma exceção.
        """
        self._validate_phone_number()
    
    # ===== MÉTODOS PRIVADOS =====
    # Métodos que começam com _ são "privados" (convenção)
    
    def _validate_phone_number(self) -> None:
        """
        Valida e limpa o número de telefone.
        
        Remove caracteres não numéricos e valida o comprimento.
        Um telefone válido tem entre 10 e 15 dígitos.
        
        Raises:
            ValueError: Se o telefone for inválido
        """
        # filter(str.isdigit, "abc123") retorna "123"
        # Mantém apenas caracteres numéricos
        clean_phone = "".join(filter(str.isdigit, self.phone_number))
        
        # Valida comprimento (10-15 dígitos)
        # 10: telefone local sem código país
        # 15: telefone internacional máximo
        if len(clean_phone) < 10 or len(clean_phone) > 15:
            raise ValueError(
                f"Número de telefone inválido: {self.phone_number}. "
                "Deve ter entre 10 e 15 dígitos."
            )
        
        # Atualiza o atributo com o número limpo
        self.phone_number = clean_phone
    
    # ===== MÉTODOS DE NEGÓCIO =====
    # Métodos que representam ações do domínio
    
    def update_name(self, name: str) -> None:
        """
        Atualiza o nome do cliente.
        
        Args:
            name: Novo nome do cliente
            
        Example:
            >>> customer.update_name("Maria Santos")
            >>> print(customer.name)
            Maria Santos
        """
        self.name = name
        self.updated_at = datetime.now()
    
    def update_email(self, email: str) -> None:
        """
        Atualiza o email do cliente.
        
        Faz validação básica do formato de email.
        
        Args:
            email: Novo email do cliente
            
        Raises:
            ValueError: Se o email for inválido
            
        Example:
            >>> customer.update_email("joao@email.com")
            >>> print(customer.email)
            joao@email.com
        """
        # Validação básica: deve ter @ e .
        if "@" not in email or "." not in email:
            raise ValueError(f"Email inválido: {email}")
        
        self.email = email
        self.updated_at = datetime.now()
