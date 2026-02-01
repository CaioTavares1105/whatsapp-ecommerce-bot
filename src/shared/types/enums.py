# ===========================================================
# src/shared/types/enums.py - Enumerações do Sistema
# ===========================================================
# Este arquivo contém os ENUMS (enumerações) usados em todo o
# sistema. Enums são conjuntos fixos de valores possíveis.
#
# POR QUE USAR ENUMS?
# 1. Evita "magic strings" (strings soltas no código)
# 2. Autocompletar no IDE
# 3. Validação em tempo de compilação (mypy)
# 4. Documentação automática dos valores possíveis
#
# SINTAXE:
#   class MeuEnum(str, Enum):
#       VALOR1 = "valor1"
#       VALOR2 = "valor2"
#
# Herdar de `str` permite comparar diretamente com strings:
#   OrderStatus.PENDING == "pending"  # True
# ===========================================================
"""
Enums compartilhados do sistema.

Enums (Enumerações) são conjuntos de valores constantes.
Usar enums em vez de strings soltas traz benefícios:
- Autocompletar no IDE
- Validação de tipos
- Documentação automática

Uso:
    from src.shared.types.enums import OrderStatus
    
    status = OrderStatus.PENDING
    print(status.value)  # "pending"
"""

from enum import Enum


# ===========================================================
# OrderStatus - Status de um Pedido
# ===========================================================
# Representa o ciclo de vida de um pedido no e-commerce.
# O pedido segue este fluxo:
#
#   PENDING --> CONFIRMED --> PROCESSING --> SHIPPED --> DELIVERED
#       |          |              |
#       +----------+--------------+-----> CANCELLED
#
# Regras de transição:
# - PENDING: Pedido criado, aguardando confirmação
# - CONFIRMED: Cliente confirmou, aguardando processamento
# - PROCESSING: Em preparação/separação
# - SHIPPED: Enviado para entrega
# - DELIVERED: Entregue ao cliente
# - CANCELLED: Cancelado (só antes de SHIPPED)
# ===========================================================

class OrderStatus(str, Enum):
    """
    Status possíveis de um pedido.
    
    Herda de `str` para permitir comparação direta:
        OrderStatus.PENDING == "pending"  # True
    
    Attributes:
        PENDING: Aguardando confirmação
        CONFIRMED: Confirmado pelo cliente
        PROCESSING: Em processamento/preparação
        SHIPPED: Enviado para entrega
        DELIVERED: Entregue ao cliente
        CANCELLED: Pedido cancelado
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ===========================================================
# SessionState - Estado da Sessão de Chat
# ===========================================================
# O chatbot é uma máquina de estados. Cada mensagem do usuário
# é processada de acordo com o estado atual da sessão.
#
# Diagrama de Estados:
#
#                    +------------+
#                    |  INITIAL   | (primeira mensagem)
#                    +-----+------+
#                          |
#                          v
#                    +-----+------+
#              +---->|    MENU    |<----+
#              |     +-----+------+     |
#              |           |            |
#              |     +-----+-----+      |
#              |     |           |      |
#              v     v           v      |
#         +--------+ +--------+ +-------+-+
#         |PRODUCTS| |ORDER   | |FAQ      |
#         +--------+ |STATUS  | +---------+
#                    +--------+
#                          |
#                          v
#                    +------------+
#                    |HUMAN       | (transferência)
#                    |TRANSFER    |
#                    +------------+
#
# ===========================================================

class SessionState(str, Enum):
    """
    Estados possíveis de uma sessão de chat.
    
    O chatbot funciona como uma máquina de estados:
    - Cada estado define quais respostas são possíveis
    - A transição entre estados depende da entrada do usuário
    
    Attributes:
        INITIAL: Estado inicial (primeira mensagem)
        MENU: Menu principal de opções
        PRODUCTS: Navegando/buscando produtos
        ORDER_STATUS: Consultando status de pedidos
        FAQ: Perguntas frequentes
        HUMAN_TRANSFER: Transferência para atendimento humano
    """
    INITIAL = "initial"           # Primeira interação
    MENU = "menu"                 # Menu principal
    PRODUCTS = "products"         # Navegando produtos
    ORDER_STATUS = "order_status" # Consultando pedidos
    FAQ = "faq"                   # Perguntas frequentes
    HUMAN_TRANSFER = "human_transfer"  # Atendente humano


# ===========================================================
# MessageDirection - Direção da Mensagem
# ===========================================================
# Indica se a mensagem foi ENVIADA pelo usuário ou RECEBIDA
# pelo usuário (enviada pelo bot).
#
# INCOMING: Usuário --> Bot (mensagem recebida)
# OUTGOING: Bot --> Usuário (mensagem enviada)
# ===========================================================

class MessageDirection(str, Enum):
    """
    Direção da mensagem no chat.
    
    Usado para identificar se a mensagem foi enviada
    pelo usuário ou pelo bot.
    
    Attributes:
        INCOMING: Mensagem do usuário para o bot
        OUTGOING: Mensagem do bot para o usuário
    """
    INCOMING = "incoming"  # Usuário --> Bot
    OUTGOING = "outgoing"  # Bot --> Usuário
