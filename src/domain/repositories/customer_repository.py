# ===========================================================
# src/domain/repositories/customer_repository.py
# ===========================================================
# Interface (Contrato) para o repositório de clientes.
#
# O QUE É UMA INTERFACE?
# Interface é um "contrato" que define QUAIS MÉTODOS uma classe
# deve ter, mas NÃO COMO eles devem ser implementados.
#
# POR QUE USAR INTERFACES?
# 1. Desacoplamento: O domínio não depende do banco de dados
# 2. Testabilidade: Podemos criar "mocks" para testes
# 3. Flexibilidade: Podemos trocar PostgreSQL por MongoDB sem
#    mudar a lógica de negócio
#
# ANALOGIA:
# Pense numa tomada elétrica. A interface define:
# - "Deve ter 2 ou 3 pinos"
# - "Deve fornecer 110V ou 220V"
# Qualquer aparelho que siga esse "contrato" funciona!
#
# O QUE É ABC (Abstract Base Class)?
# ABC é a forma do Python de criar interfaces/classes abstratas.
# - `abc.ABC`: Classe base para classes abstratas
# - `@abstractmethod`: Marca método como obrigatório
#
# Se uma classe herda de ABC e não implementa todos os
# @abstractmethod, Python levanta erro na instanciação.
# ===========================================================
"""
Interface (ABC) para repositório de Customer.

Esta interface define o CONTRATO que qualquer implementação
de repositório de clientes deve seguir.

A camada de domínio depende APENAS desta interface,
nunca da implementação concreta (SQLAlchemy, MongoDB, etc.).

Example:
    # Na camada de infraestrutura:
    class PostgresCustomerRepository(ICustomerRepository):
        async def find_by_phone(self, phone: str) -> Customer | None:
            # Implementação com SQLAlchemy
            ...
    
    # No teste unitário:
    class MockCustomerRepository(ICustomerRepository):
        async def find_by_phone(self, phone: str) -> Customer | None:
            # Retorna dados fake para teste
            ...
"""

# abc: Módulo para criar Abstract Base Classes
from abc import ABC, abstractmethod

# Importa a entidade Customer do domínio
from src.domain.entities.customer import Customer


class ICustomerRepository(ABC):
    """
    Interface para repositório de clientes.
    
    O prefixo "I" indica que é uma Interface (convenção comum).
    
    Todas as operações são ASSÍNCRONAS (async/await) porque
    acessar banco de dados é uma operação I/O que pode demorar.
    Usar async evita travar a aplicação enquanto espera.
    
    Attributes:
        Nenhum - interfaces não têm atributos, só métodos.
    """
    
    # ===== MÉTODOS DE BUSCA (Query) =====
    
    @abstractmethod
    async def find_by_phone(self, phone: str) -> Customer | None:
        """
        Busca cliente por número de telefone.
        
        Este é o método mais importante para o chatbot, pois
        identificamos clientes pelo número do WhatsApp.
        
        Args:
            phone: Número de telefone (apenas dígitos)
            
        Returns:
            Customer se encontrado, None se não existir
            
        Example:
            customer = await repo.find_by_phone("5511999999999")
            if customer:
                print(f"Olá, {customer.name}!")
        """
        ...  # O "..." indica que o corpo será implementado na subclasse
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Customer | None:
        """
        Busca cliente por ID único.
        
        Args:
            id: UUID do cliente
            
        Returns:
            Customer se encontrado, None se não existir
        """
        ...
    
    @abstractmethod
    async def find_all(self) -> list[Customer]:
        """
        Lista todos os clientes.
        
        Returns:
            Lista de todos os clientes cadastrados
            
        Note:
            Em produção, considere paginação para grandes volumes.
        """
        ...
    
    # ===== MÉTODOS DE PERSISTÊNCIA (Command) =====
    
    @abstractmethod
    async def save(self, customer: Customer) -> None:
        """
        Salva um novo cliente no repositório.
        
        Args:
            customer: Entidade Customer a ser salva
            
        Raises:
            Pode levantar exceção se cliente já existir
        """
        ...
    
    @abstractmethod
    async def update(self, customer: Customer) -> None:
        """
        Atualiza um cliente existente.
        
        Args:
            customer: Entidade Customer com dados atualizados
            
        Raises:
            Pode levantar exceção se cliente não existir
        """
        ...
    
    @abstractmethod
    async def delete(self, id: str) -> None:
        """
        Remove um cliente do repositório.
        
        Args:
            id: UUID do cliente a ser removido
            
        Note:
            Em sistemas reais, considere "soft delete" (marcar como
            inativo) em vez de remover permanentemente.
        """
        ...
