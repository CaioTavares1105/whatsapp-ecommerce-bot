# ===========================================================
# src/application/usecases/handle_message.py
# ===========================================================
# CASO DE USO PRINCIPAL: Processar mensagem do WhatsApp.
#
# O QUE É UM CASO DE USO?
# Caso de uso (Use Case) é uma classe que:
# - Orquestra a lógica de negócio
# - Coordena entidades e repositórios
# - Representa uma ação do sistema
#
# PADRÃO DE IMPLEMENTAÇÃO:
# 1. __init__ recebe INTERFACES (não implementações)
# 2. execute() é o método principal
# 3. Métodos privados (_nome) auxiliam o fluxo
#
# FLUXO DESTE CASO DE USO:
# 1. Mensagem chega do WhatsApp
# 2. Identifica/cria cliente pelo telefone
# 3. Identifica/cria sessão do cliente
# 4. Identifica intenção da mensagem
# 5. Processa baseado no estado atual + intenção
# 6. Retorna resposta apropriada
# ===========================================================
"""
Caso de uso: Processar mensagem recebida do WhatsApp.

Este é o caso de uso PRINCIPAL do chatbot. Toda mensagem
recebida passa por aqui para ser processada.

Responsabilidades:
- Identificar cliente pelo telefone
- Gerenciar sessão de conversa
- Identificar intenção da mensagem
- Gerar resposta apropriada
"""

from src.application.dtos.message_dto import IncomingMessageDTO, MessageResponseDTO
from src.domain.entities.customer import Customer
from src.domain.entities.session import Session
from src.domain.repositories import (
    ICustomerRepository,
    ISessionRepository,
    IProductRepository,
    IOrderRepository,
)
from src.shared.types.enums import SessionState


class HandleMessageUseCase:
    """
    Processa uma mensagem recebida do WhatsApp.
    
    Este caso de uso coordena o fluxo completo de processamento:
    1. Identifica ou cria cliente
    2. Identifica ou cria sessão
    3. Identifica intenção da mensagem
    4. Processa baseado no estado atual
    5. Retorna resposta apropriada
    
    Attributes:
        _customer_repo: Repositório de clientes
        _session_repo: Repositório de sessões
        _product_repo: Repositório de produtos
        _order_repo: Repositório de pedidos
        
    Example:
        >>> use_case = HandleMessageUseCase(
        ...     customer_repo=customer_repo,
        ...     session_repo=session_repo,
        ...     product_repo=product_repo,
        ...     order_repo=order_repo,
        ... )
        >>> response = await use_case.execute(incoming_message)
    """
    
    def __init__(
        self,
        customer_repo: ICustomerRepository,
        session_repo: ISessionRepository,
        product_repo: IProductRepository,
        order_repo: IOrderRepository,
    ) -> None:
        """
        Inicializa o caso de uso com os repositórios necessários.
        
        NOTA: Recebemos INTERFACES, não implementações concretas!
        Isso permite trocar PostgreSQL por MongoDB, por exemplo,
        sem mudar nada neste código.
        """
        self._customer_repo = customer_repo
        self._session_repo = session_repo
        self._product_repo = product_repo
        self._order_repo = order_repo
        
        # Dicionário de palavras-chave para identificar intenções
        # Cada chave é uma intenção, o valor é lista de keywords
        self._intent_keywords: dict[str, list[str]] = {
            "greeting": [
                "oi", "olá", "ola", "bom dia", "boa tarde", 
                "boa noite", "hey", "hi", "hello", "e aí", "eai"
            ],
            "products": [
                "produto", "produtos", "catalogo", "catálogo", 
                "comprar", "preço", "preco", "ver", "mostrar"
            ],
            "order_status": [
                "pedido", "rastreio", "rastrear", "onde está", 
                "onde esta", "entrega", "status", "acompanhar"
            ],
            "faq": [
                "dúvida", "duvida", "ajuda", "como funciona", 
                "informação", "informacao", "pergunta"
            ],
            "human": [
                "atendente", "humano", "pessoa", "falar com alguém", 
                "falar com alguem", "suporte", "reclamação"
            ],
            "menu": [
                "menu", "voltar", "início", "inicio", 
                "opcoes", "opções", "começar", "comecar"
            ],
        }
    
    async def execute(self, input_dto: IncomingMessageDTO) -> MessageResponseDTO:
        """
        Executa o processamento da mensagem.
        
        Este é o método principal, chamado para cada mensagem recebida.
        
        Args:
            input_dto: Dados da mensagem recebida
            
        Returns:
            MessageResponseDTO com a resposta a ser enviada
        """
        # 1. Buscar ou criar cliente pelo telefone
        customer = await self._get_or_create_customer(input_dto.phone_number)
        
        # 2. Buscar ou criar sessão para o cliente
        session = await self._get_or_create_session(customer.id)
        
        # 3. Identificar a intenção da mensagem
        intent = self._identify_intent(input_dto.text)
        
        # 4. Processar mensagem baseado no estado + intenção
        response = await self._process_message(session, intent, input_dto.text)
        
        # 5. Atualizar sessão (salva mudanças de estado/contexto)
        await self._session_repo.update(session)
        
        return response
    
    # ===== MÉTODOS AUXILIARES (PRIVADOS) =====
    
    async def _get_or_create_customer(self, phone_number: str) -> Customer:
        """
        Busca cliente existente ou cria um novo.
        
        O cliente é identificado pelo número de telefone.
        Se não existir, cria automaticamente.
        """
        customer = await self._customer_repo.find_by_phone(phone_number)
        
        if customer is None:
            # Cliente novo! Criar registro
            customer = Customer(phone_number=phone_number)
            await self._customer_repo.save(customer)
        
        return customer
    
    async def _get_or_create_session(self, customer_id: str) -> Session:
        """
        Busca sessão ativa ou cria uma nova.
        
        Uma sessão expira após 24 horas de inatividade.
        Se expirada, cria uma nova.
        """
        session = await self._session_repo.find_by_customer(customer_id)
        
        if session is None or session.is_expired:
            # Criar nova sessão
            session = Session(customer_id=customer_id)
            await self._session_repo.save(session)
        
        return session
    
    def _identify_intent(self, text: str) -> str:
        """
        Identifica a intenção da mensagem do usuário.
        
        Procura palavras-chave no texto para determinar
        o que o usuário deseja fazer.
        
        Args:
            text: Texto da mensagem
            
        Returns:
            String representando a intenção detectada
        """
        # Normaliza texto (minúsculo, sem espaços extras)
        text_lower = text.lower().strip()
        
        # Procura palavras-chave de cada intenção
        for intent, keywords in self._intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        # Não identificou nenhuma intenção conhecida
        return "unknown"
    
    async def _process_message(
        self, 
        session: Session, 
        intent: str, 
        text: str
    ) -> MessageResponseDTO:
        """
        Processa mensagem baseado no estado atual e intenção.
        
        A resposta depende de:
        - Estado atual da sessão (MENU, PRODUCTS, etc.)
        - Intenção identificada na mensagem
        """
        # Se é saudação ou pede menu, mostra menu principal
        if intent in ["greeting", "menu"] or session.state == SessionState.INITIAL:
            return await self._handle_greeting(session)
        
        # Se quer ver produtos
        if intent == "products":
            return await self._handle_products(session)
        
        # Se quer status do pedido
        if intent == "order_status":
            return await self._handle_order_status(session)
        
        # Se quer FAQ
        if intent == "faq":
            return await self._handle_faq(session)
        
        # Se quer falar com humano
        if intent == "human":
            return await self._handle_human_transfer(session)
        
        # Processar baseado no estado atual
        if session.state == SessionState.ORDER_STATUS:
            return await self._process_order_number(session, text)
        
        # Não entendeu
        return await self._handle_unknown(session)
    
    # ===== HANDLERS PARA CADA INTENÇÃO =====
    
    async def _handle_greeting(self, session: Session) -> MessageResponseDTO:
        """Retorna saudação e menu principal."""
        session.update_state(SessionState.MENU)
        
        return MessageResponseDTO(
            text=(
                "Olá! 👋 Bem-vindo à nossa loja!\n\n"
                "Como posso ajudar você hoje?\n\n"
                "1️⃣ Ver produtos\n"
                "2️⃣ Rastrear pedido\n"
                "3️⃣ Dúvidas frequentes\n"
                "4️⃣ Falar com atendente\n\n"
                "Digite o número da opção desejada ou escreva sua dúvida."
            )
        )
    
    async def _handle_products(self, session: Session) -> MessageResponseDTO:
        """Retorna lista de produtos/categorias."""
        session.update_state(SessionState.PRODUCTS)
        
        # Busca produtos ativos no repositório
        products = await self._product_repo.find_all_active()
        
        if not products:
            return MessageResponseDTO(
                text="No momento não temos produtos disponíveis. Tente novamente mais tarde!"
            )
        
        # Agrupa produtos por categoria
        categories: dict[str, list] = {}
        for product in products:
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append(product)
        
        # Monta texto de resposta
        text = "📦 *Nossos Produtos*\n\n"
        for category, items in categories.items():
            text += f"*{category}:*\n"
            for item in items[:5]:  # Limita 5 por categoria
                text += f"  • {item.name} - R$ {item.price:.2f}\n"
            text += "\n"
        
        text += "Digite o nome do produto para mais detalhes ou 'menu' para voltar."
        
        return MessageResponseDTO(text=text)
    
    async def _handle_order_status(self, session: Session) -> MessageResponseDTO:
        """Inicia fluxo de rastreamento de pedido."""
        session.update_state(SessionState.ORDER_STATUS)
        
        return MessageResponseDTO(
            text=(
                "📦 *Rastrear Pedido*\n\n"
                "Por favor, digite o número do seu pedido.\n\n"
                "Exemplo: `PED-123456`"
            )
        )
    
    async def _process_order_number(
        self, 
        session: Session, 
        text: str
    ) -> MessageResponseDTO:
        """Processa número do pedido informado."""
        # Limpa e normaliza o número do pedido
        order_id = text.strip().upper()
        
        # Busca pedido no repositório
        order = await self._order_repo.find_by_id(order_id)
        
        if order is None:
            return MessageResponseDTO(
                text=(
                    f"❌ Pedido *{order_id}* não encontrado.\n\n"
                    "Verifique o número e tente novamente, ou digite 'menu' para voltar."
                )
            )
        
        # Mapeia status para mensagens amigáveis
        status_messages = {
            "pending": "⏳ Aguardando confirmação",
            "confirmed": "✅ Pedido confirmado",
            "processing": "📦 Em preparação",
            "shipped": "🚚 Enviado - A caminho",
            "delivered": "✅ Entregue",
            "cancelled": "❌ Cancelado",
        }
        
        status_text = status_messages.get(order.status.value, order.status.value)
        
        return MessageResponseDTO(
            text=(
                f"📦 *Pedido {order_id}*\n\n"
                f"Status: {status_text}\n"
                f"Valor: R$ {order.total:.2f}\n"
                f"Data: {order.created_at.strftime('%d/%m/%Y')}\n\n"
                "Digite 'menu' para voltar."
            )
        )
    
    async def _handle_faq(self, session: Session) -> MessageResponseDTO:
        """Retorna menu de perguntas frequentes."""
        session.update_state(SessionState.FAQ)
        
        return MessageResponseDTO(
            text=(
                "❓ *Perguntas Frequentes*\n\n"
                "1️⃣ Qual o prazo de entrega?\n"
                "2️⃣ Como faço para trocar?\n"
                "3️⃣ Quais formas de pagamento?\n"
                "4️⃣ Como cancelar um pedido?\n\n"
                "Digite o número da pergunta ou 'menu' para voltar."
            )
        )
    
    async def _handle_human_transfer(self, session: Session) -> MessageResponseDTO:
        """Transfere para atendimento humano."""
        session.update_state(SessionState.HUMAN_TRANSFER)
        
        return MessageResponseDTO(
            text=(
                "👤 *Atendimento Humano*\n\n"
                "Vou transferir você para um de nossos atendentes.\n"
                "Aguarde um momento, por favor.\n\n"
                "Horário de atendimento:\n"
                "Segunda a Sexta: 9h às 18h\n"
                "Sábado: 9h às 13h"
            ),
            should_transfer_to_human=True
        )
    
    async def _handle_unknown(self, session: Session) -> MessageResponseDTO:
        """Mensagem quando não entende a intenção."""
        return MessageResponseDTO(
            text=(
                "🤔 Desculpe, não entendi sua mensagem.\n\n"
                "Você pode:\n"
                "• Digitar 'menu' para ver as opções\n"
                "• Digitar 'atendente' para falar com uma pessoa\n"
            )
        )
