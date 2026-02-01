# ===========================================================
# src/domain/entities/session.py - Entidade Sessão de Chat
# ===========================================================
# Representa uma sessão de conversa entre o cliente e o bot.
#
# CONCEITOS:
#
# 1. Sessão
#    - Uma "conversa" entre cliente e bot
#    - Tem um ESTADO atual (menu, produtos, etc.)
#    - Tem um CONTEXTO (dados temporários da conversa)
#    - EXPIRA após 24 horas de inatividade
#
# 2. timedelta
#    - Representa uma duração de tempo
#    - timedelta(hours=24) = 24 horas
#    - datetime.now() + timedelta(hours=24) = daqui 24 horas
#
# 3. typing.Any
#    - Tipo que aceita qualquer valor
#    - Usado no contexto que pode ter valores variados
# ===========================================================
"""
Entidade Session (Sessão de Chat).

Representa uma sessão de conversa no chatbot.
A sessão mantém o estado da conversa e um contexto
com dados temporários (como carrinho, pesquisa atual, etc.).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
# Any: Tipo que aceita qualquer valor (para o contexto flexível)
from typing import Any
import uuid

from src.shared.types.enums import SessionState


@dataclass
class Session:
    """
    Entidade de domínio que representa uma sessão de chat.
    
    A sessão mantém:
    - O estado atual da conversa (menu, produtos, etc.)
    - Um contexto com dados temporários (carrinho, busca)
    - Expiração automática após 24 horas de inatividade
    
    Example:
        >>> session = Session(customer_id="uuid-cliente")
        >>> print(session.state)
        SessionState.INITIAL
        
        >>> session.update_state(SessionState.PRODUCTS)
        >>> session.set_context("search_query", "camiseta")
        >>> print(session.get_context("search_query"))
        camiseta
    """
    
    # ===== ATRIBUTOS OBRIGATÓRIOS =====
    
    # ID do cliente dono da sessão
    customer_id: str
    
    # ===== ATRIBUTOS COM VALOR PADRÃO =====
    
    # Estado atual do chat (começa em INITIAL)
    state: SessionState = SessionState.INITIAL
    
    # Contexto da sessão (dados temporários)
    # dict[str, Any] = dicionário com chaves string e valores de qualquer tipo
    # default_factory=dict cria um dicionário vazio para cada instância
    context: dict[str, Any] = field(default_factory=dict)
    
    # ===== ATRIBUTOS GERADOS =====
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Sessão expira em 24 horas por padrão
    # timedelta(hours=24) cria uma duração de 24 horas
    expires_at: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(hours=24)
    )
    
    # ===== PROPRIEDADES =====
    
    @property
    def is_expired(self) -> bool:
        """
        Verifica se a sessão expirou.
        
        Uma sessão expira após 24 horas de inatividade.
        A cada interação, a expiração é renovada.
        
        Returns:
            True se a sessão expirou
            
        Example:
            >>> session.is_expired
            False  # Sessão recém-criada
        """
        return datetime.now() > self.expires_at
    
    @property
    def time_until_expiration(self) -> timedelta:
        """
        Retorna tempo restante até expiração.
        
        Returns:
            timedelta com o tempo restante
            
        Example:
            >>> session.time_until_expiration
            datetime.timedelta(hours=23, minutes=59)
        """
        remaining = self.expires_at - datetime.now()
        # Se já expirou, retorna zero
        return max(remaining, timedelta(0))
    
    # ===== MÉTODOS DE ESTADO =====
    
    def update_state(self, new_state: SessionState) -> None:
        """
        Atualiza o estado da sessão.
        
        A cada atualização de estado:
        - O estado muda para o novo valor
        - A data de atualização é renovada
        - A expiração é renovada (+24 horas)
        
        Args:
            new_state: Novo estado da sessão
            
        Example:
            >>> session.update_state(SessionState.MENU)
            >>> session.state == SessionState.MENU
            True
        """
        self.state = new_state
        self.updated_at = datetime.now()
        # Renova expiração a cada interação
        self.expires_at = datetime.now() + timedelta(hours=24)
    
    # ===== MÉTODOS DE CONTEXTO =====
    
    def set_context(self, key: str, value: Any) -> None:
        """
        Define um valor no contexto da sessão.
        
        O contexto armazena dados temporários da conversa,
        como carrinho de compras, busca atual, etc.
        
        Args:
            key: Chave do contexto
            value: Valor a armazenar
            
        Example:
            >>> session.set_context("cart", [{"product_id": "123", "qty": 2}])
            >>> session.set_context("last_search", "camiseta azul")
        """
        self.context[key] = value
        self.updated_at = datetime.now()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor do contexto da sessão.
        
        Args:
            key: Chave do contexto
            default: Valor padrão se chave não existir
            
        Returns:
            O valor armazenado ou o default
            
        Example:
            >>> session.get_context("cart", [])
            [{"product_id": "123", "qty": 2}]
            
            >>> session.get_context("nonexistent", "default")
            "default"
        """
        return self.context.get(key, default)
    
    def has_context(self, key: str) -> bool:
        """
        Verifica se uma chave existe no contexto.
        
        Args:
            key: Chave a verificar
            
        Returns:
            True se a chave existir
        """
        return key in self.context
    
    def remove_context(self, key: str) -> None:
        """
        Remove uma chave do contexto.
        
        Args:
            key: Chave a remover
            
        Note:
            Não levanta erro se a chave não existir.
        """
        self.context.pop(key, None)
        self.updated_at = datetime.now()
    
    def clear_context(self) -> None:
        """
        Limpa todo o contexto da sessão.
        
        Útil ao reiniciar uma conversa ou limpar dados temporários.
        
        Example:
            >>> session.clear_context()
            >>> session.context
            {}
        """
        self.context = {}
        self.updated_at = datetime.now()
    
    def renew(self) -> None:
        """
        Renova a sessão (atualiza expiração).
        
        Chamado implicitamente em update_state e set_context.
        Pode ser chamado explicitamente para manter sessão ativa.
        """
        self.updated_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(hours=24)
