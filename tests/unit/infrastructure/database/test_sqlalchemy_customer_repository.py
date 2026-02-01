# ===========================================================
# tests/unit/infrastructure/database/test_sqlalchemy_customer_repository.py
# ===========================================================
# Testes para SQLAlchemyCustomerRepository.
#
# DESAFIO EM TESTES DE REPOSITÓRIO:
# Repositórios interagem com banco real.
# Em testes unitários, queremos isolamento.
#
# SOLUÇÃO: MOCK da AsyncSession
# - Simulamos o comportamento da sessão
# - Controlamos o que cada query retorna
# - Verificamos que métodos foram chamados
#
# NOTA: Testes de INTEGRAÇÃO com banco real seriam separados.
# ===========================================================
"""
Testes unitários para SQLAlchemyCustomerRepository.

Usa mocks para simular a AsyncSession do SQLAlchemy.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.domain.entities.customer import Customer
from src.infrastructure.database.models import CustomerModel
from src.infrastructure.database.repositories.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)


@pytest.fixture
def mock_session() -> AsyncMock:
    """
    Cria mock da AsyncSession do SQLAlchemy.
    
    Configura comportamento padrão para execute(),
    scalars(), first(), etc.
    """
    session = AsyncMock()
    
    # Configura cadeia de chamadas:
    # session.execute(query) -> result
    # result.scalars() -> scalars_result
    # scalars_result.first() -> model ou None
    # scalars_result.all() -> [models]
    
    return session


@pytest.fixture
def repository(mock_session: AsyncMock) -> SQLAlchemyCustomerRepository:
    """Cria repositório com sessão mockada."""
    return SQLAlchemyCustomerRepository(mock_session)


@pytest.fixture
def sample_customer() -> Customer:
    """Entidade Customer de exemplo."""
    return Customer(
        phone_number="5511999999999",
        name="João Silva",
        email="joao@email.com",
    )


@pytest.fixture
def sample_model() -> CustomerModel:
    """Modelo CustomerModel de exemplo."""
    return CustomerModel(
        id="test-uuid-123",
        phone_number="5511999999999",
        name="João Silva",
        email="joao@email.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


class TestFindByPhone:
    """Testes para find_by_phone."""
    
    @pytest.mark.asyncio
    async def test_returns_customer_when_found(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_model: CustomerModel,
    ):
        """Deve retornar Customer quando encontrado."""
        # Configura mock para retornar o modelo
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = sample_model
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa
        result = await repository.find_by_phone("5511999999999")
        
        # Verifica
        assert result is not None
        assert isinstance(result, Customer)
        assert result.phone_number == "5511999999999"
        assert result.name == "João Silva"
    
    @pytest.mark.asyncio
    async def test_returns_none_when_not_found(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
    ):
        """Deve retornar None quando não encontrado."""
        # Configura mock para retornar None
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa
        result = await repository.find_by_phone("5511000000000")
        
        # Verifica
        assert result is None
    
    @pytest.mark.asyncio
    async def test_calls_execute_with_query(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
    ):
        """Deve chamar execute com query correta."""
        # Configura mock
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa
        await repository.find_by_phone("5511999999999")
        
        # Verifica que execute foi chamado
        mock_session.execute.assert_called_once()


class TestFindById:
    """Testes para find_by_id."""
    
    @pytest.mark.asyncio
    async def test_returns_customer_when_found(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_model: CustomerModel,
    ):
        """Deve retornar Customer quando encontrado por ID."""
        # Configura mock
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = sample_model
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa
        result = await repository.find_by_id("test-uuid-123")
        
        # Verifica
        assert result is not None
        assert result.id == "test-uuid-123"


class TestSave:
    """Testes para save."""
    
    @pytest.mark.asyncio
    async def test_adds_model_to_session(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_customer: Customer,
    ):
        """Deve adicionar modelo à sessão."""
        # Executa
        await repository.save(sample_customer)
        
        # Verifica que add foi chamado com CustomerModel
        mock_session.add.assert_called_once()
        added_model = mock_session.add.call_args[0][0]
        assert isinstance(added_model, CustomerModel)
        assert added_model.phone_number == sample_customer.phone_number
    
    @pytest.mark.asyncio
    async def test_calls_flush(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_customer: Customer,
    ):
        """Deve chamar flush após save."""
        # Executa
        await repository.save(sample_customer)
        
        # Verifica
        mock_session.flush.assert_called_once()


class TestUpdate:
    """Testes para update."""
    
    @pytest.mark.asyncio
    async def test_updates_existing_customer(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_customer: Customer,
        sample_model: CustomerModel,
    ):
        """Deve atualizar cliente existente."""
        # Configura para encontrar o modelo
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = sample_model
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Atualiza o customer
        sample_customer.name = "Nome Atualizado"
        
        # Executa (precisa que o ID seja o mesmo)
        # Como sample_customer tem ID diferente, criamos um novo
        customer_to_update = Customer(
            id=sample_model.id,  # Mesmo ID do modelo
            phone_number="5511999999999",
            name="Nome Atualizado",
        )
        
        await repository.update(customer_to_update)
        
        # Verifica que flush foi chamado
        mock_session.flush.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_raises_error_when_not_found(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_customer: Customer,
    ):
        """Deve levantar erro quando cliente não existe."""
        # Configura para retornar None
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa e espera erro
        with pytest.raises(ValueError, match="Cliente não encontrado"):
            await repository.update(sample_customer)


class TestDelete:
    """Testes para delete."""
    
    @pytest.mark.asyncio
    async def test_deletes_existing_customer(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
        sample_model: CustomerModel,
    ):
        """Deve deletar cliente existente."""
        # Configura para encontrar
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = sample_model
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa
        await repository.delete("test-uuid-123")
        
        # Verifica que delete foi chamado
        mock_session.delete.assert_called_once_with(sample_model)
        mock_session.flush.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_raises_error_when_not_found(
        self,
        repository: SQLAlchemyCustomerRepository,
        mock_session: AsyncMock,
    ):
        """Deve levantar erro quando cliente não existe."""
        # Configura para retornar None
        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result
        
        # Executa e espera erro
        with pytest.raises(ValueError, match="Cliente não encontrado"):
            await repository.delete("nao-existe")


class TestConversions:
    """Testes para conversores Model <-> Entity."""
    
    def test_to_entity_converts_correctly(
        self,
        repository: SQLAlchemyCustomerRepository,
        sample_model: CustomerModel,
    ):
        """Deve converter Model para Entity corretamente."""
        entity = repository._to_entity(sample_model)
        
        assert isinstance(entity, Customer)
        assert entity.id == sample_model.id
        assert entity.phone_number == sample_model.phone_number
        assert entity.name == sample_model.name
        assert entity.email == sample_model.email
    
    def test_to_model_converts_correctly(
        self,
        repository: SQLAlchemyCustomerRepository,
        sample_customer: Customer,
    ):
        """Deve converter Entity para Model corretamente."""
        model = repository._to_model(sample_customer)
        
        assert isinstance(model, CustomerModel)
        assert model.id == sample_customer.id
        assert model.phone_number == sample_customer.phone_number
        assert model.name == sample_customer.name
        assert model.email == sample_customer.email
