# ===========================================================
# src/infrastructure/database/repositories/sqlalchemy_customer_repository.py
# ===========================================================
# Implementação CONCRETA do ICustomerRepository usando SQLAlchemy.
#
# O QUE É UM REPOSITÓRIO CONCRETO?
# É a implementação real da interface abstrata.
# Aqui conectamos ao banco de dados de verdade.
#
# PADRÃO DE IMPLEMENTAÇÃO:
# 1. Recebe AsyncSession no __init__
# 2. Implementa TODOS os métodos abstratos
# 3. Converte entre Model e Entity
#
# OPERAÇÕES COMUNS:
# - session.execute(select(...)) -> buscar dados
# - session.add(model) -> inserir/atualizar
# - session.delete(model) -> remover
# - session.commit() -> confirmar (feito na dependency)
# ===========================================================
"""
Implementação do repositório de clientes com SQLAlchemy.

Esta classe implementa ICustomerRepository usando
SQLAlchemy para persistência no PostgreSQL.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.customer import Customer
from src.domain.repositories.customer_repository import ICustomerRepository
from src.infrastructure.database.models import CustomerModel


class SQLAlchemyCustomerRepository(ICustomerRepository):
    """
    Repositório de clientes usando SQLAlchemy.
    
    Implementa a interface ICustomerRepository com
    persistência real no PostgreSQL.
    
    Attributes:
        _session: Sessão async do SQLAlchemy
        
    Example:
        >>> async with AsyncSessionFactory() as session:
        ...     repo = SQLAlchemyCustomerRepository(session)
        ...     customer = await repo.find_by_phone("5511999999999")
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa o repositório com uma sessão do banco.
        
        Args:
            session: Sessão async do SQLAlchemy
        """
        self._session = session
    
    # =========================================================
    # MÉTODOS DE BUSCA
    # =========================================================
    
    async def find_by_phone(self, phone: str) -> Customer | None:
        """
        Busca cliente pelo número de telefone.
        
        Args:
            phone: Número de telefone (ex: "5511999999999")
            
        Returns:
            Customer se encontrado, None caso contrário
            
        Example:
            >>> customer = await repo.find_by_phone("5511999999999")
            >>> if customer:
            ...     print(f"Encontrado: {customer.name}")
        """
        # select(Model): Cria query SELECT
        # where(...): Adiciona condição WHERE
        query = select(CustomerModel).where(CustomerModel.phone_number == phone)
        
        # execute(): Executa a query
        # scalars(): Extrai objetos do resultado
        # first(): Pega primeiro ou None
        result = await self._session.execute(query)
        model = result.scalars().first()
        
        if model is None:
            return None
        
        # Converte Model -> Entity
        return self._to_entity(model)
    
    async def find_by_id(self, id: str) -> Customer | None:
        """
        Busca cliente pelo ID único.
        
        Args:
            id: UUID do cliente
            
        Returns:
            Customer se encontrado, None caso contrário
        """
        query = select(CustomerModel).where(CustomerModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()
        
        if model is None:
            return None
        
        return self._to_entity(model)
    
    async def find_all(self) -> list[Customer]:
        """
        Retorna todos os clientes.
        
        Returns:
            Lista de todos os clientes cadastrados
        """
        query = select(CustomerModel)
        result = await self._session.execute(query)
        models = result.scalars().all()
        
        return [self._to_entity(model) for model in models]
    
    # =========================================================
    # MÉTODOS DE PERSISTÊNCIA
    # =========================================================
    
    async def save(self, customer: Customer) -> None:
        """
        Salva um novo cliente no banco.
        
        Args:
            customer: Entidade Customer a ser salva
            
        Note:
            O commit é feito automaticamente pela dependency
            get_db_session() ao final da request.
        """
        model = self._to_model(customer)
        self._session.add(model)
        
        # Flush: Envia para o banco mas não comita
        # Útil para obter IDs gerados, etc.
        await self._session.flush()
    
    async def update(self, customer: Customer) -> None:
        """
        Atualiza um cliente existente.
        
        Args:
            customer: Entidade Customer com dados atualizados
            
        Raises:
            ValueError: Se cliente não existe no banco
        """
        # Busca o modelo existente
        query = select(CustomerModel).where(CustomerModel.id == customer.id)
        result = await self._session.execute(query)
        model = result.scalars().first()
        
        if model is None:
            raise ValueError(f"Cliente não encontrado: {customer.id}")
        
        # Atualiza os campos
        model.phone_number = customer.phone_number
        model.name = customer.name
        model.email = customer.email
        model.updated_at = customer.updated_at
        
        await self._session.flush()
    
    async def delete(self, id: str) -> None:
        """
        Remove um cliente do banco.
        
        Args:
            id: UUID do cliente a remover
            
        Raises:
            ValueError: Se cliente não existe
        """
        query = select(CustomerModel).where(CustomerModel.id == id)
        result = await self._session.execute(query)
        model = result.scalars().first()
        
        if model is None:
            raise ValueError(f"Cliente não encontrado: {id}")
        
        await self._session.delete(model)
        await self._session.flush()
    
    # =========================================================
    # CONVERSORES (Model <-> Entity)
    # =========================================================
    
    def _to_entity(self, model: CustomerModel) -> Customer:
        """
        Converte CustomerModel (banco) -> Customer (entidade).
        
        Args:
            model: Modelo do SQLAlchemy
            
        Returns:
            Entidade de domínio Customer
        """
        return Customer(
            id=model.id,
            phone_number=model.phone_number,
            name=model.name,
            email=model.email,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, entity: Customer) -> CustomerModel:
        """
        Converte Customer (entidade) -> CustomerModel (banco).
        
        Args:
            entity: Entidade de domínio
            
        Returns:
            Modelo para persistência
        """
        return CustomerModel(
            id=entity.id,
            phone_number=entity.phone_number,
            name=entity.name,
            email=entity.email,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
