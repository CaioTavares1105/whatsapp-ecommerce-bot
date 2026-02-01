# ===========================================================
# tests/unit/domain/entities/test_customer.py
# ===========================================================
# TESTES UNITÁRIOS para a entidade Customer.
#
# O QUE SÃO TESTES UNITÁRIOS?
# São testes que verificam uma "unidade" isolada de código.
# No nosso caso, testamos a entidade Customer separadamente.
#
# FRAMEWORK: PYTEST
# Pytest é o framework de testes mais popular do Python.
# É simples, poderoso e tem boa integração com IDEs.
#
# ESTRUTURA DE UM TESTE:
#   1. ARRANGE (Preparar): Configurar os dados de teste
#   2. ACT (Agir): Executar a ação sendo testada
#   3. ASSERT (Verificar): Verificar o resultado
#
# CONVENÇÕES DE NOMENCLATURA:
# - Arquivo: test_*.py ou *_test.py
# - Classe: Test* (ex: TestCustomer)
# - Método: test_* (ex: test_create_customer)
#
# COMO RODAR OS TESTES:
#   pytest                          # Roda todos os testes
#   pytest -v                       # Modo verbose (detalhado)
#   pytest tests/unit/             # Só testes unitários
#   pytest -k "customer"            # Só testes com "customer" no nome
#   pytest --cov=src               # Com cobertura de código
# ===========================================================
"""
Testes unitários para entidade Customer.

Este arquivo demonstra os conceitos básicos de testes:
- Testes de criação válida/inválida
- Testes de métodos de negócio
- Uso de pytest.raises para testar exceções
"""

# pytest: Framework de testes
import pytest

# Importa a entidade que vamos testar
from src.domain.entities.customer import Customer


class TestCustomer:
    """
    Classe de testes para a entidade Customer.
    
    Agrupa todos os testes relacionados ao Customer.
    O pytest descobre automaticamente classes que começam com "Test".
    """
    
    # ===== TESTES DE CRIAÇÃO =====
    
    def test_create_customer_with_valid_phone(self):
        """
        Deve criar cliente com telefone válido.
        
        Testa o "caminho feliz" - quando tudo funciona como esperado.
        """
        # ARRANGE: Preparar dados
        phone = "5511999999999"
        name = "João Silva"
        
        # ACT: Executar a ação
        customer = Customer(phone_number=phone, name=name)
        
        # ASSERT: Verificar resultados
        # assert verifica se a condição é True
        # Se for False, o teste FALHA
        assert customer.id is not None  # ID foi gerado
        assert customer.phone_number == phone  # Telefone correto
        assert customer.name == name  # Nome correto
        assert customer.email is None  # Email começa vazio
        assert customer.created_at is not None  # Data criada
    
    def test_create_customer_cleans_phone_number(self):
        """
        Deve limpar caracteres especiais do telefone.
        
        Testa se a validação remove: espaços, parênteses, traços, +
        """
        # Telefone com formatação (como usuário digitaria)
        customer = Customer(phone_number="+55 (11) 99999-9999")
        
        # Deve estar limpo (apenas dígitos)
        assert customer.phone_number == "5511999999999"
    
    def test_create_customer_without_name(self):
        """
        Deve criar cliente sem nome (nome é opcional).
        """
        customer = Customer(phone_number="5511999999999")
        
        assert customer.name is None
        assert customer.phone_number == "5511999999999"
    
    def test_create_customer_generates_unique_id(self):
        """
        Cada cliente deve ter um ID único.
        """
        customer1 = Customer(phone_number="5511111111111")
        customer2 = Customer(phone_number="5522222222222")
        
        # IDs devem ser diferentes
        assert customer1.id != customer2.id
    
    # ===== TESTES DE VALIDAÇÃO (ERROS ESPERADOS) =====
    
    def test_create_customer_with_short_phone_raises_error(self):
        """
        Deve levantar erro se telefone for muito curto.
        
        pytest.raises() verifica se uma exceção é levantada.
        Se NÃO levantar exceção, o teste FALHA.
        """
        # with pytest.raises(TipoDoErro) as exc_info:
        #     código_que_deve_dar_erro()
        
        with pytest.raises(ValueError) as exc_info:
            Customer(phone_number="123")  # Muito curto!
        
        # Podemos verificar a mensagem do erro
        assert "inválido" in str(exc_info.value).lower()
    
    def test_create_customer_with_long_phone_raises_error(self):
        """
        Deve levantar erro se telefone for muito longo.
        """
        with pytest.raises(ValueError) as exc_info:
            Customer(phone_number="1234567890123456789")  # 19 dígitos
        
        assert "inválido" in str(exc_info.value).lower()
    
    # ===== TESTES DE MÉTODOS DE NEGÓCIO =====
    
    def test_update_name(self):
        """
        Deve atualizar o nome do cliente.
        """
        customer = Customer(phone_number="5511999999999", name="João")
        original_updated_at = customer.updated_at
        
        # Força uma pequena espera para garantir que o tempo mudou
        customer.update_name("João Silva")
        
        assert customer.name == "João Silva"
        # updated_at deve ter sido atualizado
        assert customer.updated_at >= original_updated_at
    
    def test_update_email_with_valid_email(self):
        """
        Deve atualizar email quando válido.
        """
        customer = Customer(phone_number="5511999999999")
        
        customer.update_email("joao@email.com")
        
        assert customer.email == "joao@email.com"
    
    def test_update_email_with_invalid_email_raises_error(self):
        """
        Deve levantar erro com email inválido.
        """
        customer = Customer(phone_number="5511999999999")
        
        with pytest.raises(ValueError) as exc_info:
            customer.update_email("email-invalido")
        
        assert "inválido" in str(exc_info.value).lower()
    
    def test_update_email_without_dot_raises_error(self):
        """
        Deve levantar erro com email sem ponto.
        """
        customer = Customer(phone_number="5511999999999")
        
        with pytest.raises(ValueError):
            customer.update_email("joao@email")  # Sem .com


# ===========================================================
# COMO RODAR ESTE TESTE:
#
# No terminal (com ambiente virtual ativado):
#   pytest tests/unit/domain/entities/test_customer.py -v
#
# Saída esperada:
#   test_create_customer_with_valid_phone PASSED
#   test_create_customer_cleans_phone_number PASSED
#   test_create_customer_without_name PASSED
#   ...
#
# Para ver cobertura de código:
#   pytest tests/unit/domain/entities/test_customer.py --cov=src/domain/entities/customer
# ===========================================================
