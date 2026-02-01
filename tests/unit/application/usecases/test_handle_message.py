# ===========================================================
# tests/unit/application/usecases/test_handle_message.py
# ===========================================================
# Testes unitários para o HandleMessageUseCase.
#
# O QUE SÃO MOCKS?
# Mocks são objetos "falsos" que simulam comportamento.
# Usamos mocks para:
# - Testar sem banco de dados real
# - Controlar o que os repositórios retornam
# - Verificar se métodos foram chamados
#
# AsyncMock vs MagicMock:
# - MagicMock: Para funções síncronas
# - AsyncMock: Para funções assíncronas (async def)
#
# @pytest.fixture:
# Fixtures são funções que preparam dados para os testes.
# São chamadas automaticamente quando declaradas como parâmetro.
#
# @pytest.mark.asyncio:
# Marca o teste como assíncrono. Permite usar await no teste.
# ===========================================================
"""
Testes unitários para HandleMessageUseCase.

Usamos mocks para simular os repositórios e testar
o caso de uso de forma isolada.
"""

import pytest
from unittest.mock import AsyncMock

from src.application.dtos.message_dto import IncomingMessageDTO
from src.application.usecases.handle_message import HandleMessageUseCase
from src.domain.entities.customer import Customer
from src.domain.entities.session import Session
from src.shared.types.enums import SessionState


# ===========================================================
# FIXTURES - Preparam dados para os testes
# ===========================================================

@pytest.fixture
def mock_repositories() -> dict:
    """
    Fixture que cria mocks de todos os repositórios.
    
    Returns:
        Dicionário com mocks dos repositórios
        
    Uso nos testes:
        def test_algo(mock_repositories):
            # mock_repositories já está criado!
    """
    return {
        "customer_repo": AsyncMock(),
        "session_repo": AsyncMock(),
        "product_repo": AsyncMock(),
        "order_repo": AsyncMock(),
    }


@pytest.fixture
def use_case(mock_repositories) -> HandleMessageUseCase:
    """
    Fixture que cria o caso de uso com mocks injetados.
    
    Note que recebe mock_repositories como parâmetro!
    O pytest injeta automaticamente.
    """
    return HandleMessageUseCase(**mock_repositories)


@pytest.fixture
def sample_customer() -> Customer:
    """Fixture com cliente de exemplo."""
    return Customer(
        phone_number="5511999999999",
        name="João Silva"
    )


@pytest.fixture
def sample_session(sample_customer) -> Session:
    """Fixture com sessão de exemplo já no estado MENU."""
    session = Session(customer_id=sample_customer.id)
    session.update_state(SessionState.MENU)  # Importante: não estar em INITIAL
    return session


# ===========================================================
# TESTES - Verificam comportamentos do caso de uso
# ===========================================================

class TestHandleMessageUseCase:
    """
    Testes para HandleMessageUseCase.
    
    Cada método testa um cenário específico.
    """
    
    # ===== TESTES DE SAUDAÇÃO =====
    
    @pytest.mark.asyncio
    async def test_greeting_returns_menu(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Saudação deve retornar menu principal.
        
        Cenário: Cliente envia "Olá"
        Esperado: Recebe menu com opções
        """
        # ARRANGE - Preparar
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Olá"
        )
        
        # ACT - Agir
        result = await use_case.execute(input_dto)
        
        # ASSERT - Verificar
        assert "Bem-vindo" in result.text
        assert "1️⃣" in result.text  # Menu tem opções numeradas
        assert result.should_transfer_to_human is False
    
    @pytest.mark.asyncio
    async def test_greeting_variations(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Diferentes saudações devem retornar menu.
        
        Testa: "oi", "bom dia", "hey"
        """
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        greetings = ["oi", "bom dia", "boa tarde", "hey", "e aí"]
        
        for greeting in greetings:
            input_dto = IncomingMessageDTO(
                phone_number="5511999999999",
                text=greeting
            )
            
            result = await use_case.execute(input_dto)
            
            assert "Bem-vindo" in result.text or "menu" in result.text.lower(), \
                f"Falhou para saudação: {greeting}"
    
    # ===== TESTES DE CRIAÇÃO DE CLIENTE =====
    
    @pytest.mark.asyncio
    async def test_new_customer_is_created(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
    ):
        """
        Novo cliente deve ser criado se não existir.
        
        Cenário: Telefone não cadastrado
        Esperado: customer_repo.save é chamado
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = None
        mock_repositories["session_repo"].find_by_customer.return_value = None
        
        input_dto = IncomingMessageDTO(
            phone_number="5511888888888",
            text="Oi"
        )
        
        # ACT
        await use_case.execute(input_dto)
        
        # ASSERT - Verifica que save foi chamado
        mock_repositories["customer_repo"].save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_existing_customer_not_recreated(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Cliente existente NÃO deve ser recriado.
        
        Cenário: Cliente já cadastrado
        Esperado: customer_repo.save NÃO é chamado
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Oi"
        )
        
        # ACT
        await use_case.execute(input_dto)
        
        # ASSERT - Verifica que save NÃO foi chamado
        mock_repositories["customer_repo"].save.assert_not_called()
    
    # ===== TESTES DE TRANSFERÊNCIA PARA HUMANO =====
    
    @pytest.mark.asyncio
    async def test_human_transfer_sets_flag(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Pedido de atendente deve setar flag de transferência.
        
        Cenário: Cliente pede para falar com pessoa
        Esperado: should_transfer_to_human = True
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Quero falar com um atendente"
        )
        
        # ACT
        result = await use_case.execute(input_dto)
        
        # ASSERT
        assert result.should_transfer_to_human is True
        assert "Atendimento Humano" in result.text
    
    @pytest.mark.asyncio
    async def test_human_transfer_keywords(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Várias palavras-chave devem acionar transferência.
        """
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        keywords = ["atendente", "humano", "pessoa", "suporte", "reclamação"]
        
        for keyword in keywords:
            input_dto = IncomingMessageDTO(
                phone_number="5511999999999",
                text=f"Quero {keyword}"
            )
            
            result = await use_case.execute(input_dto)
            
            assert result.should_transfer_to_human is True, \
                f"Falhou para keyword: {keyword}"
    
    # ===== TESTES DE PRODUTOS =====
    
    @pytest.mark.asyncio
    async def test_products_request_changes_state(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Pedido de produtos deve mudar estado da sessão.
        
        Cenário: Cliente quer ver produtos
        Esperado: Sessão muda para PRODUCTS
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        mock_repositories["product_repo"].find_all_active.return_value = []
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Quero ver produtos"
        )
        
        # ACT
        await use_case.execute(input_dto)
        
        # ASSERT
        assert sample_session.state == SessionState.PRODUCTS
    
    @pytest.mark.asyncio
    async def test_no_products_available_message(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Se não há produtos, deve informar cliente.
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        mock_repositories["product_repo"].find_all_active.return_value = []
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Ver catálogo"
        )
        
        # ACT
        result = await use_case.execute(input_dto)
        
        # ASSERT
        assert "não temos produtos" in result.text.lower()
    
    # ===== TESTES DE FAQ =====
    
    @pytest.mark.asyncio
    async def test_faq_request_returns_questions(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Pedido de FAQ deve retornar perguntas frequentes.
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Tenho uma dúvida"
        )
        
        # ACT
        result = await use_case.execute(input_dto)
        
        # ASSERT
        assert "Perguntas Frequentes" in result.text
        assert sample_session.state == SessionState.FAQ
    
    # ===== TESTES DE INTENÇÃO DESCONHECIDA =====
    
    @pytest.mark.asyncio
    async def test_unknown_intent_returns_help(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Mensagem não reconhecida deve oferecer ajuda.
        """
        # ARRANGE
        sample_session.update_state(SessionState.MENU)  # Força estado MENU
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="asdfghjkl qwerty"  # Texto sem sentido
        )
        
        # ACT
        result = await use_case.execute(input_dto)
        
        # ASSERT
        assert "não entendi" in result.text.lower()
    
    # ===== TESTES DE SESSÃO =====
    
    @pytest.mark.asyncio
    async def test_session_is_updated_after_processing(
        self, 
        use_case: HandleMessageUseCase, 
        mock_repositories: dict,
        sample_customer: Customer,
        sample_session: Session,
    ):
        """
        Sessão deve ser atualizada após processamento.
        
        Cenário: Qualquer mensagem processada
        Esperado: session_repo.update é chamado
        """
        # ARRANGE
        mock_repositories["customer_repo"].find_by_phone.return_value = sample_customer
        mock_repositories["session_repo"].find_by_customer.return_value = sample_session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Oi"
        )
        
        # ACT
        await use_case.execute(input_dto)
        
        # ASSERT
        mock_repositories["session_repo"].update.assert_called_once()


# ===========================================================
# TESTES DOS DTOs
# ===========================================================

class TestIncomingMessageDTO:
    """Testes para validação do IncomingMessageDTO."""
    
    def test_valid_dto_creation(self):
        """DTO válido deve ser criado sem erros."""
        dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Olá, mundo!"
        )
        
        assert dto.phone_number == "5511999999999"
        assert dto.text == "Olá, mundo!"
        assert dto.message_id is None  # Valor padrão
    
    def test_phone_too_short_raises_error(self):
        """Telefone muito curto deve levantar erro."""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            IncomingMessageDTO(
                phone_number="123",  # Muito curto
                text="Oi"
            )
    
    def test_empty_text_raises_error(self):
        """Texto vazio deve levantar erro."""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            IncomingMessageDTO(
                phone_number="5511999999999",
                text=""  # Vazio
            )
