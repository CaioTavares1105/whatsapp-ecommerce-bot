# ===========================================================
# src/domain/repositories/session_repository.py
# ===========================================================
# Interface para o repositório de sessões de chat.
#
# SESSÕES SÃO TEMPORÁRIAS:
# - Armazenadas em Redis (cache) para performance
# - Expiram após 24 horas de inatividade
# - Contêm estado atual da conversa
# ===========================================================
"""
Interface (ABC) para repositório de Session.

Sessões são armazenadas em cache (Redis) para
performance, já que são acessadas a cada mensagem.
"""

from abc import ABC, abstractmethod

from src.domain.entities.session import Session


class ISessionRepository(ABC):
    """
    Interface para repositório de sessões.
    
    Diferente dos outros repositórios, sessões geralmente
    são armazenadas em cache (Redis) em vez de banco SQL
    para melhor performance.
    """
    
    # ===== MÉTODOS DE BUSCA (Query) =====
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Session | None:
        """
        Busca sessão por ID único.
        
        Args:
            id: UUID da sessão
            
        Returns:
            Session se encontrada (e não expirada), None caso contrário
        """
        ...
    
    @abstractmethod
    async def find_by_customer(self, customer_id: str) -> Session | None:
        """
        Busca sessão ativa de um cliente.
        
        Um cliente só pode ter UMA sessão ativa por vez.
        
        Args:
            customer_id: UUID do cliente
            
        Returns:
            Session ativa do cliente, ou None se não houver
        """
        ...
    
    @abstractmethod
    async def find_active_by_phone(self, phone: str) -> Session | None:
        """
        Busca sessão ativa pelo telefone do cliente.
        
        Este é o método principal usado pelo chatbot:
        1. Mensagem chega com número de telefone
        2. Busca sessão ativa para esse número
        3. Se não existir, cria nova sessão
        
        Args:
            phone: Número de telefone do cliente
            
        Returns:
            Session ativa, ou None se não houver
            
        Example:
            session = await repo.find_active_by_phone("5511999999999")
            if not session:
                session = Session(customer_id=customer.id)
                await repo.save(session)
        """
        ...
    
    # ===== MÉTODOS DE PERSISTÊNCIA (Command) =====
    
    @abstractmethod
    async def save(self, session: Session) -> None:
        """
        Salva uma nova sessão.
        
        Args:
            session: Entidade Session a ser salva
        """
        ...
    
    @abstractmethod
    async def update(self, session: Session) -> None:
        """
        Atualiza uma sessão existente.
        
        Chamado a cada interação para:
        - Atualizar estado (MENU, PRODUCTS, etc.)
        - Salvar contexto (carrinho, busca atual)
        - Renovar expiração
        
        Args:
            session: Entidade Session com dados atualizados
        """
        ...
    
    @abstractmethod
    async def delete(self, id: str) -> None:
        """
        Remove uma sessão específica.
        
        Usado quando cliente encerra conversa explicitamente.
        
        Args:
            id: UUID da sessão
        """
        ...
    
    @abstractmethod
    async def delete_expired(self) -> int:
        """
        Remove todas as sessões expiradas.
        
        Deve ser chamado periodicamente (cron job, background task)
        para limpar sessões antigas e liberar memória.
        
        Returns:
            Quantidade de sessões removidas
            
        Example:
            # Rodar a cada hora
            removed = await repo.delete_expired()
            logger.info(f"Limpas {removed} sessões expiradas")
        """
        ...
    
    @abstractmethod
    async def count_active(self) -> int:
        """
        Conta sessões ativas (não expiradas).
        
        Útil para métricas e monitoramento.
        
        Returns:
            Quantidade de sessões ativas
        """
        ...
